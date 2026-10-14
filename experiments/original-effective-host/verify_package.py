#!/usr/bin/env python3
"""Verify package hashes and replay only the three independent small checkers.

No network, installations, source-program execution, huge powers, theorem-sized
field/kernel/host, or Lean compilation. Outputs are made in a temporary copy.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def verify_manifest(root, manifest):
    seen=set()
    for line in manifest.read_text().splitlines():
        digest,name=line.split(None,1)
        name=name.strip().lstrip('*');relative=PurePosixPath(name)
        require(not relative.is_absolute() and '..' not in relative.parts,'unsafe manifest path')
        require(name not in seen,'duplicate manifest path');seen.add(name)
        path=root.joinpath(*relative.parts)
        require(path.is_file() and not path.is_symlink(),'missing/nonordinary manifest input: '+name)
        require(hashlib.sha256(path.read_bytes()).hexdigest()==digest,'hash mismatch: '+name)
    require(bool(seen),'empty manifest')
    return len(seen)

def main():
    require(sys.flags.optimize==0,'Assertions must be active; do not use -O or PYTHONOPTIMIZE.')
    verify_manifest(ROOT,ROOT/'verification/PACKAGE-SHA256SUMS')
    entries=verify_manifest(ROOT/'recovered',ROOT/'recovered/SHA256SUMS')
    require(entries==12,'unexpected recovered manifest count')
    proof=(ROOT/'recovered/PROOF.md').read_bytes()
    require(hashlib.sha256(proof).hexdigest()=='20c917f8fbab9cc51a92d0a4c853ca2080541a9a15c116bd3343150993aaf031','recovered proof changed')
    require(len(proof.splitlines())==1573,'unexpected proof length')
    source_pins=json.loads((ROOT/'recovered/source-pins.json').read_text())['sources']
    auth=json.loads((ROOT/'upstream-authentication.json').read_text())
    require(len(auth)==len(source_pins)==10,'incomplete source closure')
    authenticated=set()
    for source in auth:
        path=ROOT/source['path'];data=path.read_bytes()
        require(hashlib.sha256(data).hexdigest()==source['sha256'],'upstream SHA256 differs')
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==source['git_blob_sha1'],'upstream Git blob differs')
        authenticated.add((source['repository'],source['commit'],source['upstream_path'],blob))
    require(authenticated=={(s['repository'],s['commit'],s['path'],s['git_blob_sha1']) for s in source_pins},'source pins disagree')
    license=(ROOT/'upstream/OpenAI-LICENSE.txt').read_bytes()
    require(hashlib.sha1(b'blob '+str(len(license)).encode()+b'\0'+license).hexdigest()=='261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64','OpenAI license differs')
    ledger=json.loads((ROOT/'review/dependency-ledger-18.json').read_text())
    require([x['number'] for x in ledger['components']]==list(range(1,19)),'incomplete dependency audit')
    results={}
    with tempfile.TemporaryDirectory(prefix='sidorenko-small-checks-') as td:
        copy=Path(td)/'package'
        shutil.copytree(ROOT,copy)
        for name in ['geometry','data','algebra']:
            script=copy/'independent'/('own_'+name+'_audit.py')
            proc=subprocess.run([sys.executable,'-I','-B',str(script)],cwd=copy,
                                check=True,capture_output=True,text=True,timeout=60)
            actual=json.loads((copy/('own-'+name+'-results.json')).read_text())
            # The geometry console output is deliberately a condensed summary;
            # acceptance compares the complete saved result, including all orbits.
            json.loads(proc.stdout)
            expected=json.loads((ROOT/'evidence'/('expected-'+name+'-results.json')).read_text())
            require(actual==expected,'independent result differs: '+name)
            results[name]='PASS'
    print(json.dumps({'status':'PASS','package_hashes_verified':True,
      'recovered_manifest_entries':entries,'recovered_proof_lines':1573,
      'pinned_source_files_verified':10,'dependency_audit_components':18,
      'independent_checkers':results,'recovered_programs_executed':False,
      'huge_prime_field_kernel_or_host_materialized':False,'Lean_run':False},indent=2))

if __name__=='__main__':
    main()
