#!/usr/bin/env python3
"""Create a deterministic local ZIP; no publication or network action."""
import hashlib,json,pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(ROOT)
    if any(x in {'build','.lake','__pycache__','development'} for x in rel.parts):continue
    if rel.as_posix() in {'MANIFEST.json','SHA256SUMS'}:continue
    files.append((rel,p))
manifest={'project':'t7-finite-coefficient-publication','hash_algorithm':'SHA-256','files':{}}
for rel,p in files:
    regenerated=rel.parts[0]=='evidence' or rel.parts[:2]==('formal','logs') or rel.as_posix() in {'formal/Audit.lean','formal/Statements.lean'}
    manifest['files'][rel.as_posix()]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size,
        'kind':'replay_output' if regenerated else 'immutable_input'}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
files.append((pathlib.Path('MANIFEST.json'),ROOT/'MANIFEST.json'))
(ROOT/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+rel.as_posix()+'\n' for rel,p in sorted(files)))
files.append((pathlib.Path('SHA256SUMS'),ROOT/'SHA256SUMS'))
archive=ROOT.parent/'t7-finite-coefficient-publication.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for rel,p in sorted(files):
        e=zipfile.ZipInfo(ROOT.name+'/'+rel.as_posix(),date_time=(2026,10,11,0,0,0));e.compress_type=zipfile.ZIP_DEFLATED;e.external_attr=0o100644<<16
        z.writestr(e,p.read_bytes(),compresslevel=9)
receipt={'status':'PACKAGED_LOCALLY','archive':str(archive),'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'bytes':archive.stat().st_size,
    'entries':len(files),'scope':'Finite coefficient formalization only','opus_reviewed_proof_bytes_preserved':True,'new_packaging_opus_reviewed':False,'external_actions':[]}
(ROOT.parent/'t7-finite-coefficient-publication-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
