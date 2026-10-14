#!/usr/bin/env python3
"""Rebuild every local proof with the already-installed Lean binary. No network code."""
import argparse, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time
ROOT = pathlib.Path(__file__).resolve().parents[1]
if not os.environ.get('T7_LEAN_BIN'):
    raise SystemExit('Set T7_LEAN_BIN to the bin directory of the existing pinned Lean 4.33.0 toolchain; no automatic installation is attempted.')
BIN = pathlib.Path(os.environ['T7_LEAN_BIN']).resolve()
LEAN = BIN/'lean'
LOG = ROOT/'logs/rebuild'
BUILD = ROOT/'build/lean'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()

def verify_files(base, files):
    for name, record in files.items():
        path = base/name
        if not path.is_file() or digest(path) != record['sha256']:
            raise SystemExit(f'Pinned input mismatch: {path}')

def run(command, log_path, env):
    start = time.monotonic()
    with log_path.open('w') as log:
        result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        print(log_path.read_text()[:16000], file=sys.stderr)
        raise SystemExit(f'Build failed ({result.returncode}); see {log_path}')
    return {'command': command, 'log': str(log_path.relative_to(ROOT)), 'exit_code': result.returncode,
            'elapsed_seconds': round(time.monotonic()-start, 3)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip-full-toolchain-hash', action='store_true', help='Still checks lean executable hash; skips hashing every library/toolchain file.')
    args = parser.parse_args()
    LOG.mkdir(parents=True, exist_ok=True)
    toolchain = json.loads((ROOT/'inputs/toolchain-manifest.json').read_text())
    verify_files(BIN.parent, {'bin/lean': toolchain['files']['bin/lean']})
    if not args.skip_full_toolchain_hash:
        verify_files(BIN.parent, toolchain['files'])
    baseline = json.loads((ROOT/'BASELINE.json').read_text())
    for name, pinned in baseline['baseline_proofs'].items():
        if digest(ROOT/name) != pinned:
            raise SystemExit(f'Copied baseline proof changed: {name}')
    parent = json.loads((ROOT/'PARENT.json').read_text())
    for name, pinned in parent['copied_proofs'].items():
        if digest(ROOT/name) != pinned:
            raise SystemExit(f'Copied parent proof changed: {name}')
    source = json.loads((ROOT/'inputs/source-packet-manifest.json').read_text())
    verify_files(ROOT/'inputs/publication', source['files'])
    literals = json.loads((ROOT/'inputs/t7-literals.json').read_text())
    text = (ROOT/'T7/Finite.lean').read_text()
    body = text.split('def face :', 1)[1].split('def pointEdge :', 1)[0]
    transcription = [list(map(int, nums.split(','))) for nums in re.findall(r'=> \[([\d, ]+)\]', body)]
    if transcription != literals['faces']:
        raise SystemExit('Lean face transcription differs from pinned source literals')
    if digest(ROOT/'inputs/t7-literals.json') != source['files']['proposed/experiments/t7-orbit/inputs/t7-literals.json']['sha256']:
        raise SystemExit('Standalone literal file pin mismatch')
    sources = {'T7': ROOT/'T7.lean', 'T7Gap': ROOT/'T7Gap.lean', 'T7Weighted': ROOT/'T7Weighted.lean'}
    for prefix in ['T7', 'T7Gap', 'T7Weighted']:
        sources.update({prefix+'.'+p.stem: p for p in sorted((ROOT/prefix).glob('*.lean'))})
    for name, path in sources.items():
        content = path.read_text()
        if re.search(r'\b(sorry|admit|native_decide|unsafe)\b|^\s*axiom\b', content, re.MULTILINE):
            raise SystemExit(f'Forbidden proof escape in {name}')
    order, done = [], set()
    def visit(name):
        if name in done:
            return
        done.add(name)
        for dep in re.findall(r'^import\s+(T7(?:Gap|Weighted)?(?:\.\w+)*)\s*$', sources[name].read_text(), re.MULTILINE):
            visit(dep)
        order.append(name)
    for name in sources:
        visit(name)
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    env = dict(os.environ, LEAN_PATH=str(BUILD))
    results = []
    for name in order:
        output = BUILD/pathlib.Path(*name.split('.')).with_suffix('.olean')
        output.parent.mkdir(parents=True, exist_ok=True)
        cmd = [str(LEAN), '-t', '0', '-R', str(ROOT), '-o', str(output), str(sources[name])]
        results.append(run(cmd, LOG/(name+'.log'), env))
        print('CHECKED', name, flush=True)
    names = []
    for name in order:
        prefix = name.split('.')[0]
        names.extend(prefix+'.'+x for x in re.findall(r'^theorem\s+([A-Za-z_][A-Za-z_0-9.]*)', sources[name].read_text(), re.MULTILINE))
    audit_path = ROOT/'Audit.lean'
    audit_path.write_text('import T7Weighted\n'+''.join(f'#print axioms {x}\n' for x in names))
    results.append(run([str(LEAN), '-t', '0', str(audit_path)], LOG/'axioms.log', env))
    axiom_text = (LOG/'axioms.log').read_text()
    axioms = {}
    for line in axiom_text.splitlines():
        match = re.fullmatch(r"'([^']+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)", line)
        if match:
            axioms[match[1]] = [x.strip() for x in (match[2] or '').split(',') if x.strip()]
    if set(axioms) != set(names):
        raise SystemExit('Axiom audit did not produce exactly one result for every theorem')
    extra = set().union(*map(set, axioms.values()))-ALLOWED_AXIOMS
    if extra:
        raise SystemExit(f'Unapproved theorem axioms: {sorted(extra)}')
    (LOG/'axioms.json').write_text(json.dumps(axioms, indent=2)+'\n')
    statements_path = ROOT/'Statements.lean'
    statements_path.write_text('import T7Weighted\n'+''.join(f'#check {x}\n' for x in names))
    results.append(run([str(LEAN), '-t', '0', str(statements_path)], LOG/'theorem-statements.log', env))
    results.append(run([str(LEAN), '-t', '0', str(ROOT/'DeclarationAudit.lean')], LOG/'all-declarations.log', env))
    declarations = {}
    for line in (LOG/'all-declarations.log').read_text().splitlines():
        if line.startswith('DECL|'):
            _, name, kind, axs, deps, body = line.split('|')
            declarations[name] = {'kind': kind, 'axioms': [a for a in axs.split(',') if a],
                                  'direct_type_dependencies': [d for d in deps.split(',') if d],
                                  'direct_body_dependencies': [d for d in body.split(',') if d],
                                  'direct_dependencies': sorted(set(d for d in (deps+','+body).split(',') if d))}
    if not set(names).issubset(declarations):
        raise SystemExit('Declaration audit omitted an authored theorem')
    for name, info in declarations.items():
        if info['kind'] == 'axiom' or set(info['axioms'])-ALLOWED_AXIOMS:
            raise SystemExit(f'Forbidden declaration or transitive axioms: {name}: {info}')
    if not declarations:
        raise SystemExit('Empty declaration audit')
    (LOG/'declaration-audit.json').write_text(json.dumps(declarations, indent=2)+'\n')
    final = {'status': 'PASS', 'trust_level': 0, 'lean_version': subprocess.check_output([str(LEAN), '--version'], text=True).strip(),
             'full_toolchain_hash_verified': not args.skip_full_toolchain_hash, 'source_packet_files_verified': len(source['files']),
             'modules': order, 'theorem_count': len(names), 'new_authored_theorems': len([n for n in names if n.startswith('T7Weighted.')]), 'project_declarations_audited': len(declarations), 'axiom_union': sorted(set().union(*map(set, axioms.values()))),
             'source_hashes': {str(p.relative_to(ROOT)): digest(p) for p in sources.values()}, 'runs': results,
             'isolated_lean_path': str(BUILD), 'baseline_proofs_unchanged': True,
             'network_actions': [], 'actual_averaged_coefficient_negative_proved': True, 'kernel_deficit_proved': False, 'sampling_estimates_proved': False, 'analytic_rank_layer_law_proved': False, 'full_non_sidorenko_theorem_proved': False}
    (LOG/'build-receipt.json').write_text(json.dumps(final, indent=2)+'\n')
    print(json.dumps({k:v for k,v in final.items() if k in ['status','trust_level','theorem_count','axiom_union']}, indent=2))

if __name__ == '__main__':
    main()
