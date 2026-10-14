#!/usr/bin/env python3
"""Replay a delivered ZIP in a new directory and save evidence outside the archive."""
import argparse,hashlib,json,pathlib,subprocess,sys,tempfile,time,zipfile
ap=argparse.ArgumentParser()
ap.add_argument('--archive',required=True)
ap.add_argument('--lean-bin',required=True)
ap.add_argument('--receipt',required=True)
a=ap.parse_args();archive=pathlib.Path(a.archive).expanduser().resolve();receipt=pathlib.Path(a.receipt).expanduser().resolve()
start=time.monotonic();digest=hashlib.sha256(archive.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix='t7-finite-publication-replay-') as td:
    dest=pathlib.Path(td)
    with zipfile.ZipFile(archive) as z:
        for e in z.infolist():
            p=pathlib.PurePosixPath(e.filename)
            if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0]!='t7-finite-coefficient-publication':
                raise SystemExit('Unsafe or unexpected archive path')
            if ((e.external_attr>>16)&0o170000)==0o120000:raise SystemExit('Archive symlinks not accepted')
        z.extractall(dest)
    root=dest/'t7-finite-coefficient-publication'
    command=[sys.executable,str(root/'replay.py'),'--lean-bin',str(pathlib.Path(a.lean_bin).expanduser().resolve()),'--verify-evidence']
    r=subprocess.run(command,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if r.returncode:
        print(r.stdout[-12000:]);raise SystemExit('Fresh archive replay failed')
    result=json.loads((root/'evidence/replay-receipt.json').read_text())
    if result['status']!='PASS':raise SystemExit('Replay receipt did not confirm success')
    result={'status':'PASS','archive_sha256':digest,'fresh_directory':True,'archived_evidence_hashes_verified':True,
        'all_reviewed_proof_files_unchanged':result['reviewed_proof_files_unchanged'],'trust_level':result['trust_level'],
        'formal_modules':result['formal_modules'],'formal_theorems':result['formal_theorems'],'formal_declarations':result['formal_declarations'],
        'control_lemmas':len(result['new_beta_control_lemmas']),'control_declarations':result['new_control_declarations_audited'],
        'axiom_union':result['axiom_union'],'historical_beta_control':result['historical_InsufficientBeta_status'],
        'full_toolchain_hash_verified':result['full_toolchain_hash_verified'],
        'scope':result['scope'],'opus_reviewed_packaging':False,'newer_RL_or_host_results_included':False,
        'elapsed_seconds':round(time.monotonic()-start,3),'replay_stdout_tail':r.stdout[-6000:],'external_actions':[]}
receipt.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='replay_stdout_tail'},indent=2))
