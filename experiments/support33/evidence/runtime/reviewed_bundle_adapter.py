"""Pinned replay of a fully reviewed supplied program in a fresh attempt tree.

This is an execution adapter, not a hostile-code sandbox. Every executable
source and imported sibling must receive a full static review before a job
using this adapter is admitted. Inputs and expected results are runner-pinned.
"""
import base64
import contextlib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import runpy
import sys

def digest(data):
    return hashlib.sha256(data).hexdigest()

def relative(name):
    path = PurePosixPath(name)
    assert name and not path.is_absolute() and '..' not in path.parts
    assert '\\' not in name and path.as_posix() == name
    return path

payload = json.loads(Path(sys.argv[1]).read_bytes())
assert payload['review_status'] == 'full-static-review-complete'
stage = Path.cwd() / 'reviewed-bundle'
stage.mkdir()
pins = {}
for name, record in payload['files'].items():
    target = stage / relative(name)
    data = base64.b64decode(record['base64'], validate=True)
    assert digest(data) == record['sha256']
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as handle:
        handle.write(data)
    pins[name] = record['sha256']
    if target.suffix == '.py':
        target.chmod(0o444)
entry_name = payload['entrypoint']
entry = stage / relative(entry_name)
assert entry_name in pins and entry.suffix == '.py'
assert pins[entry_name] == payload['entrypoint_sha256']
original_directory = Path.cwd()
stdout_path = original_directory / 'reviewed-program.stdout.txt'
sys.argv = [str(entry), *payload.get('argv', [])]
sys.path.insert(0, str(entry.parent))
os.chdir(stage)
try:
    with stdout_path.open('x', encoding='utf-8') as stdout:
        with contextlib.redirect_stdout(stdout):
            try:
                runpy.run_path(str(entry), run_name='__main__')
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    raise RuntimeError('Reviewed program exited unsuccessfully') from exc
        stdout.flush()
        os.fsync(stdout.fileno())
finally:
    os.chdir(original_directory)

# A checker may update a result JSON, but no pinned executable may mutate.
for name, expected in pins.items():
    if name.endswith('.py'):
        assert digest((stage / name).read_bytes()) == expected
raw_stdout = stdout_path.read_bytes()
output = payload['output']
if output['kind'] == 'json_file':
    raw_result = (stage / relative(output['path'])).read_bytes()
    result = json.loads(raw_result)
elif output['kind'] == 'json_stdout':
    raw_result = raw_stdout
    result = json.loads(raw_result)
elif output['kind'] == 'text_stdout':
    raw_result = raw_stdout
    result = raw_result.decode('utf-8')
    assert output['required_fragments']
    for fragment in output['required_fragments']:
        assert fragment in result
else:
    raise ValueError('Unknown reviewed output contract')

comparison = 'assertions and required output fragments'
if 'expected_result' in payload:
    assert result == payload['expected_result'], 'Result differs from pinned producer result'
    comparison = 'exact parsed result equality with pinned producer result'
print(json.dumps({
    'adapter_version': 'reviewed-bundle-adapter-1.0',
    'status': 'passed',
    'entrypoint': entry_name,
    'entrypoint_sha256': pins[entry_name],
    'reviewer': payload['reviewer'],
    'comparison': comparison,
    'scope': payload['scope'],
    'execution_provenance': 'Supplied model-generated code executed after full static review. Embedded author provenance fields are historical, not provenance of this replay.',
    'result_sha256': digest(raw_result),
    'program_stdout_sha256': digest(raw_stdout),
    'program_stdout': raw_stdout.decode('utf-8'),
    'result': result,
}, sort_keys=True))
