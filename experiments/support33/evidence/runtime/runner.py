"""Auditable stdlib-only finite verification runner, version 1.0.

One durable checkpoint per completed work unit. Unfinished units restart from their
beginning. This is a local reviewed-code runner, not an adversarial-code sandbox.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import threading
import time
import traceback
import uuid

VERSION = '1.0'
HERE = Path(__file__).resolve().parent
STOP = threading.Event()

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode() + b'\n'

def digest(x):
    return hashlib.sha256(x).hexdigest()

def now():
    return datetime.now(timezone.utc).isoformat()

def sync_dir(p):
    fd = os.open(p, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def atomic(path, data, immutable=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name('.' + path.name + '.' + uuid.uuid4().hex + '.tmp')
    with open(tmp, 'xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if immutable:
        os.chmod(tmp, 0o444)
        try:
            os.link(tmp, path)
        except FileExistsError:
            if path.read_bytes() != data:
                raise ValueError('Attempt to overwrite immutable artifact: ' + str(path))
        finally:
            tmp.unlink()
    else:
        os.replace(tmp, path)
    sync_dir(path.parent)

def envelope(payload):
    return canonical({'sha256': digest(canonical(payload)), 'payload': payload})

def unwrap(path):
    doc = json.loads(path.read_bytes())
    if doc['sha256'] != digest(canonical(doc['payload'])):
        raise ValueError('Corrupt envelope: ' + str(path))
    return doc['payload']

def name(x):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,100}', x):
        raise ValueError('Invalid identifier')
    return x

def put(root, data):
    h = digest(data)
    atomic(root / 'objects' / h, data, immutable=True)
    return h

def get(root, h):
    if not re.fullmatch('[0-9a-f]{64}', h):
        raise ValueError('Invalid digest')
    p = root / 'objects' / h
    if p.is_symlink():
        raise ValueError('Symlink object rejected')
    data = p.read_bytes()
    if digest(data) != h:
        raise ValueError('Corrupt immutable object: ' + h)
    return data

def runtime():
    import decimal
    import fractions
    import _decimal
    p = Path(sys.executable).resolve()
    return {'python': sys.version, 'executable': str(p), 'executable_sha256': digest(p.read_bytes()),
            'stdlib_sha256': {m.__name__: digest(Path(m.__file__).read_bytes()) for m in (fractions, decimal, _decimal, json)},
            'runner_version': VERSION, 'runner_sha256': digest(Path(__file__).read_bytes()),
            'worker_sha256': digest((HERE / 'worker.py').read_bytes())}

@contextmanager
def locked(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

def event(jdir, kind, **data):
    atomic(jdir / 'events' / (str(time.time_ns()) + '-' + uuid.uuid4().hex + '.json'),
           envelope({'time': now(), 'kind': kind, **data}), immutable=True)

def register(root, spec_path):
    spec_path = spec_path.resolve()
    spec = json.loads(spec_path.read_bytes())
    jid = name(spec['job_id'])
    for key in ('claim_id', 'assumptions', 'scope', 'unproved_implications', 'source_pins', 'review', 'estimate', 'units'):
        if not spec.get(key):
            raise ValueError('Missing manifest field: ' + key)
    if spec['review']['status'] != 'reviewed-independent-small-checker':
        raise ValueError('Unreviewed source is not executable')
    if not 0 < spec['limits']['wall_seconds'] <= 3600 or not 0 < spec['limits']['cpu_seconds'] <= 3600:
        raise ValueError('Local work unit limits must be at most one hour')
    if not 0 < spec['limits']['output_bytes'] <= 16 * 1024**2:
        raise ValueError('Invalid output cap')
    units = []
    seen = set()
    for unit in spec['units']:
        u = dict(unit)
        uid = name(u['unit_id'])
        if uid in seen:
            raise ValueError('Duplicate unit identifier')
        seen.add(uid)
        for field in ('source', 'input'):
            path = (spec_path.parent / u.pop(field)).resolve()
            u[field + '_sha256'] = put(root, path.read_bytes())
        if u['expect']['kind'] not in ('json', 'assertion_rejected'):
            raise ValueError('Unknown expectation')
        units.append(u)
    spec['units'] = units
    spec['runtime'] = runtime()
    spec['worker_object'] = put(root, (HERE / 'worker.py').read_bytes())
    spec['runner_object'] = put(root, Path(__file__).read_bytes())
    spec['spec_sha256'] = put(root, spec_path.read_bytes())
    h = put(root, canonical(spec))
    jdir = root / 'jobs' / jid
    with locked(root / 'register.lock'):
        pin = jdir / 'registration.json'
        if pin.exists():
            if unwrap(pin)['manifest_sha256'] != h:
                raise ValueError('Job already registered differently; use a new job_id')
        else:
            atomic(pin, envelope({'job_id': jid, 'manifest_sha256': h}), immutable=True)
            event(jdir, 'registered', manifest_sha256=h)
    return {'job_id': jid, 'manifest_sha256': h}

def load(root, jid):
    jdir = root / 'jobs' / name(jid)
    registration = unwrap(jdir / 'registration.json')
    h = registration['manifest_sha256']
    spec = json.loads(get(root, h))
    if spec['job_id'] != jid:
        raise ValueError('Job identifier mismatch')
    if spec['runtime'] != runtime():
        raise ValueError('Runtime changed: review and register a new job version')
    get(root, spec['worker_object'])
    get(root, spec['runner_object'])
    get(root, spec['spec_sha256'])
    for u in spec['units']:
        get(root, u['source_sha256'])
        get(root, u['input_sha256'])
    return jdir, h, spec

def subset(actual, expected):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(k in actual and subset(actual[k], v) for k, v in expected.items())
    return type(actual) is type(expected) and actual == expected

def check(expect, rc, out, err):
    if expect['kind'] == 'assertion_rejected':
        if rc == 1 and b'AssertionError' in err and b'SyntaxError' not in err and b'Traceback' in err:
            return {'classification': 'expected_mutation_rejection'}
        raise ValueError('Mutation did not produce an assertion rejection')
    if rc != 0:
        raise ValueError('Checker exit code ' + str(rc))
    parsed = json.loads(out)
    if not subset(parsed, expect.get('subset', {})):
        raise ValueError('JSON output contract mismatch')
    return {'classification': 'finite_check_passed', 'output': parsed}

def validate_receipt(root, receipt_hash, mh, u):
    rec = json.loads(get(root, receipt_hash))
    if rec['manifest_sha256'] != mh or rec['unit_id'] != u['unit_id']:
        raise ValueError('Checkpoint receipt binding mismatch')
    if rec['source_sha256'] != u['source_sha256'] or rec['input_sha256'] != u['input_sha256']:
        raise ValueError('Receipt source/input mismatch')
    out = get(root, rec['stdout_sha256'])
    err = get(root, rec['stderr_sha256'])
    judged = check(u['expect'], rec['exit_code'], out, err)
    if judged != rec['checked']:
        raise ValueError('Receipt result does not match its output')
    return rec

def terminate(proc):
    if proc.poll() is None:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()

def execute_unit(root, jdir, mh, spec, u):
    attempt = jdir / 'attempts' / (u['unit_id'] + '-' + uuid.uuid4().hex)
    attempt.mkdir(parents=True)
    info = {'manifest_sha256': mh, 'unit_id': u['unit_id'], 'started_at': now(),
            'source_sha256': u['source_sha256'], 'input_sha256': u['input_sha256']}
    atomic(attempt / 'started.json', envelope(info), immutable=True)
    worker = root / 'objects' / spec['worker_object']
    source = root / 'objects' / u['source_sha256']
    payload = root / 'objects' / u['input_sha256']
    limits = spec['limits']
    cmd = [sys.executable, '-I', '-B', str(worker), str(source), u['source_sha256'], str(payload), u['input_sha256'],
           str(attempt / 'usage.json'), str(limits['cpu_seconds']), str(limits['output_bytes'])]
    began = time.monotonic()
    reason = None
    with open(attempt / 'stdout.partial', 'xb') as out, open(attempt / 'stderr.partial', 'xb') as err:
        proc = subprocess.Popen(cmd, cwd=attempt, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                env={'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8'}, start_new_session=True)
        event(jdir, 'unit_started', unit_id=u['unit_id'], pid=proc.pid, attempt=attempt.name)
        try:
            while proc.poll() is None:
                if STOP.is_set():
                    reason = 'interrupted'
                    break
                if time.monotonic() - began > limits['wall_seconds']:
                    reason = 'timeout'
                    break
                time.sleep(0.05)
        finally:
            terminate(proc)
            out.flush(); os.fsync(out.fileno())
            err.flush(); os.fsync(err.fileno())
    for stream in ('stdout', 'stderr'):
        os.replace(attempt / (stream + '.partial'), attempt / (stream + '.txt'))
    sync_dir(attempt)
    stdout = (attempt / 'stdout.txt').read_bytes()
    stderr = (attempt / 'stderr.txt').read_bytes()
    info.update({'exit_code': proc.returncode, 'finished_at': now(), 'wall_seconds': time.monotonic() - began,
                 'stdout_sha256': put(root, stdout), 'stderr_sha256': put(root, stderr), 'reason': reason})
    usage_path = attempt / 'usage.json'
    if usage_path.exists():
        info['usage'] = json.loads(usage_path.read_bytes())
    atomic(attempt / 'execution.json', envelope(info), immutable=True)
    if reason:
        raise RuntimeError(reason)
    info['checked'] = check(u['expect'], proc.returncode, stdout, stderr)
    # Recheck all pins after execution before accepting output.
    load(root, spec['job_id'])
    h = put(root, canonical(info))
    atomic(attempt / 'receipt.json', envelope({'receipt_sha256': h}), immutable=True)
    return h

def run_job(root, jid, max_new_units=None):
    jdir = root / 'jobs' / name(jid)
    with locked(jdir / 'run.lock'):
        try:
            jdir, mh, spec = load(root, jid)
            checkpoint = jdir / 'checkpoint.json'
            done = {}
            if checkpoint.exists():
                cp = unwrap(checkpoint)
                if cp['manifest_sha256'] != mh:
                    raise ValueError('Checkpoint manifest changed')
                done = cp['completed']
                if set(done) - {u['unit_id'] for u in spec['units']}:
                    raise ValueError('Unknown completed unit')
            for u in spec['units']:
                if u['unit_id'] in done:
                    validate_receipt(root, done[u['unit_id']], mh, u)
            reused = len(done)
            event(jdir, 'resume_validated', completed=reused)
            count = 0
            for u in spec['units']:
                if u['unit_id'] in done:
                    continue
                if STOP.is_set() or (max_new_units is not None and count >= max_new_units):
                    return {'job_id': jid, 'status': 'checkpointed', 'completed': len(done), 'reused': reused}
                done[u['unit_id']] = execute_unit(root, jdir, mh, spec, u)
                cp = {'manifest_sha256': mh, 'completed': done.copy(), 'updated_at': now()}
                # Keep immutable checkpoint generations, then update the durable pointer.
                cp_hash = put(root, canonical(cp))
                atomic(jdir / 'checkpoints' / (cp_hash + '.json'), envelope(cp), immutable=True)
                atomic(checkpoint, envelope(cp))
                event(jdir, 'checkpoint_committed', unit_id=u['unit_id'], checkpoint_sha256=cp_hash)
                count += 1
            result = {'job_id': jid, 'manifest_sha256': mh, 'claim_id': spec['claim_id'],
                      'status': 'verified_finite_arithmetic' if spec.get('role') == 'claim' else 'control_passed',
                      'scope': spec['scope'], 'unproved_implications': spec['unproved_implications'],
                      'receipts': done}
            atomic(jdir / 'result.json', envelope(result), immutable=True)
            event(jdir, 'completed', reused=reused)
            return {**result, 'reused': reused}
        except Exception as exc:
            event(jdir, 'failure', error=type(exc).__name__, message=str(exc), traceback=traceback.format_exc())
            return {'job_id': jid, 'status': 'failed', 'error': str(exc)}

def audit(root, jid):
    jdir, mh, spec = load(root, jid)
    result = unwrap(jdir / 'result.json')
    if result['manifest_sha256'] != mh or set(result['receipts']) != {u['unit_id'] for u in spec['units']}:
        raise ValueError('Incomplete or mismatched result')
    for u in spec['units']:
        validate_receipt(root, result['receipts'][u['unit_id']], mh, u)
    cp = unwrap(jdir / 'checkpoint.json')
    if cp['manifest_sha256'] != mh or cp['completed'] != result['receipts']:
        raise ValueError('Checkpoint/result mismatch')
    return result

def ledger(root, pending_path):
    rows = json.loads(pending_path.read_bytes()) if pending_path else []
    for reg in sorted((root / 'jobs').glob('*/registration.json')):
        jid = reg.parent.name
        try:
            result = audit(root, jid)
            if result['status'] == 'verified_finite_arithmetic':
                rows.append(result)
        except Exception as exc:
            rows.append({'job_id': jid, 'status': 'not_verified', 'reason': str(exc)})
    doc = {'generated_at': now(), 'runner_version': VERSION, 'claims': rows,
           'rule': 'Finite computations do not establish the surrounding all-size theorem.'}
    atomic(root / 'claim-ledger.json', envelope(doc))
    return doc

def main():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must remain enabled; do not use -O or PYTHONOPTIMIZE')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--state', type=Path, default=HERE / 'state')
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('register'); a.add_argument('specs', nargs='+', type=Path)
    a = sub.add_parser('run'); a.add_argument('jobs', nargs='+'); a.add_argument('--workers', type=int, default=2)
    a.add_argument('--max-new-units', type=int)
    a = sub.add_parser('audit'); a.add_argument('jobs', nargs='+')
    a = sub.add_parser('ledger'); a.add_argument('--pending', type=Path)
    args = p.parse_args()
    root = args.state.resolve(); root.mkdir(parents=True, exist_ok=True)
    signal.signal(signal.SIGTERM, lambda *_: STOP.set())
    signal.signal(signal.SIGINT, lambda *_: STOP.set())
    if args.command == 'register':
        result = [register(root, s) for s in args.specs]
    elif args.command == 'run':
        if not 1 <= args.workers <= 2:
            p.error('Tintagel concurrency is capped at 2')
        if len(set(args.jobs)) != len(args.jobs):
            p.error('Duplicate jobs')
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            result = list(pool.map(lambda j: run_job(root, j, args.max_new_units), args.jobs))
    elif args.command == 'audit':
        result = [audit(root, j) for j in args.jobs]
    else:
        result = ledger(root, args.pending)
    print(json.dumps(result, indent=2))
    if args.command == 'run' and any(r['status'] == 'failed' for r in result):
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
