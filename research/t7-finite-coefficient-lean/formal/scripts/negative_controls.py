#!/usr/bin/env python3
"""Local rejection checks. Mutants are temporary and never become proof inputs."""
import hashlib, json, os, pathlib, subprocess, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[1]
if not os.environ.get('T7_LEAN_BIN'):
    raise SystemExit('Set T7_LEAN_BIN to the existing pinned Lean 4.33.0 bin directory.')
LEAN = pathlib.Path(os.environ['T7_LEAN_BIN'])/'lean'
cases = [
    ('score-penalty', 'T7Weighted/Scores.lean',
     'def pointLoss (p q : Point) : Int := 37*((degree q : Int)-(degree p : Int))^2',
     'def pointLoss (p q : Point) : Int := 36*((degree q : Int)-(degree p : Int))^2',
     'Changed the actual degree mismatch penalty from 37 to 36; retained the claimed penalty gap and score proofs.'),
    ('actual-weight-scale', 'T7Weighted/ActualWeights.lean',
     'rawMapWeight g = averagedScale*relativeWeight g',
     'rawMapWeight g = 2*averagedScale*relativeWeight g',
     'Inserted a spurious factor of two in the exact actual-weight bridge; retained its proof.'),
    ('orbit-sign', 'T7/Coefficient.lean',
     'def sigma (c : Corner) : Int := if c == 0 then -1 else 1',
     'def sigma (c : Corner) : Int := if c == 0 then 1 else 1',
     'Changed distinguished sign; retained original coefficient claims and proofs.'),
    ('activation-mass', 'T7Gap/Activation.lean',
     '(1/2)*tiltedWeight (D c) (branchBias c o.1) o.2',
     '(1/3)*tiltedWeight (D c) (branchBias c o.1) o.2',
     'Changed each branch mass from one half to one third; retained expectation/normalization proofs.')]
receipts = []
for label, source_path, before, after, explanation in cases:
    source = (ROOT/source_path).read_text()
    assert source.count(before) == 1
    mutant = source.replace(before, after)
    with tempfile.TemporaryDirectory(prefix='t7-repair-negative-') as temp:
        path = pathlib.Path(temp)/'Mutant.lean'
        path.write_text(mutant)
        result = subprocess.run([str(LEAN),'-t','0',str(path)],cwd=ROOT,
            env=dict(os.environ,LEAN_PATH=str(ROOT/'build/lean')),text=True,capture_output=True)
    output = result.stdout+result.stderr
    (ROOT/f'logs/negative-{label}.log').write_text(output)
    assert result.returncode != 0 and 'error:' in output, f'Mutant {label} was accepted'
    assert 'unsolved goals' in output.lower() or 'tactic' in output.lower() or 'type mismatch' in output.lower() or 'decide' in output.lower() or '`grind` failed' in output.lower(), 'Unexpected infrastructure failure'
    assert 'object file' not in output and 'unknown module' not in output
    (ROOT/f'logs/negative-{label}.log').write_text(output)
    receipts.append({'name':label,'status':'EXPECTED_REJECTION','explanation':explanation,
       'source':source_path,'lean_exit_code':result.returncode,
       'original_sha256':hashlib.sha256(source.encode()).hexdigest(),
       'mutant_sha256':hashlib.sha256(mutant.encode()).hexdigest(),
       'project_modified':False,'failed_mutant_used_as_proof':False})
(ROOT/'logs/negative-controls.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps(receipts,indent=2))
