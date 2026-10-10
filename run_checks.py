"""Rebuild the enumeration and independently verify the saved certificates."""
import json
import os
from pathlib import Path
import subprocess
import sys

if not __debug__:
    raise RuntimeError('Run without -O: the certificate scripts use assertions')
root=Path(__file__).resolve().parent
os.chdir(root)
Path('build').mkdir(exist_ok=True)

def run(*args):
    subprocess.run(args,check=True)

def python(*args):
    run(sys.executable,'-B',*args)

def identical(actual,expected):
    if json.loads(Path(actual).read_text())!=json.loads(Path(expected).read_text()):
        raise AssertionError(f'Reproduced result differs: {actual}')

run(os.environ.get('CC','cc'),'-O3','-o','build/plantri','vendor/plantri/plantri.c')
python('fetch_sources.py','--output','upstream')
python('enumerate_triangulations.py','--plantri','build/plantri','--min-n','4','--max-n','13','--output','build/enumeration')
identical('build/enumeration/candidates-13.json','experiments/sphere-enumeration/candidates-13.json')
python('verify_minimality.py','--plantri','build/plantri','--generator-source','vendor/plantri/plantri.c','--witnesses','experiments/cut-obstructions/summary.json','--min-n','4','--max-n','12','--output','build/minimality.json')
identical('build/minimality.json','experiments/minimality-independent.json')
python('verify_order13.py','--candidates','build/enumeration/candidates-13.json','--results','experiments/order-13-cuts/summary.json','--finite-checker','check_complex.py','--original','experiments/original-baseline.json','--output','build/order13.json')
identical('build/order13.json','experiments/order-13-classification-independent.json')
python('check_complex.py','experiments/original-baseline.json','--output','build/baseline.json')
manifest=json.loads(Path('source-manifest.json').read_text())
source=Path('upstream')/manifest['files'][0]['path']
python('audit_residual.py','--complex-source',str(source),'--output','build/residual.json')
identical('build/residual.json','experiments/residual-expected.json')
python('audit_support.py','--output','build/support.json')
identical('build/support.json','experiments/support-expected.json')
python('audit_sequential.py','--output','build/sequential.json')
identical('build/sequential.json','experiments/sequential-expected.json')
python('audit_overlap.py','--output','build/overlap.json')
identical('build/overlap.json','experiments/overlap-expected.json')
print('All enumeration, exact certificates, rejection controls, residual, active-support, sequential-count and overlap checks passed.')
