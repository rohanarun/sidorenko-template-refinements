#!/usr/bin/env python3
"""Path-independent offline replay. Requires an existing pinned Lean toolchain."""
import argparse, hashlib, json, os, pathlib, re, shutil, subprocess, sys, time
ROOT = pathlib.Path(__file__).resolve().parent
ALLOWED = {'propext','Classical.choice','Quot.sound'}
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--lean-bin',required=True,help='Existing pinned Lean 4.33.0 bin directory; no toolchain installation is attempted.')
    ap.add_argument('--verify-evidence',action='store_true',help='Also verify archived replay-output hashes before rebuilding.')
    args=ap.parse_args(); started=time.monotonic()
    binpath=pathlib.Path(args.lean_bin).expanduser().resolve(); lean=binpath/'lean'
    if not lean.is_file(): raise SystemExit('Missing existing Lean binary: '+str(lean))
    manifest=json.loads((ROOT/'MANIFEST.json').read_text()); count=0
    for name,e in manifest['files'].items():
        if e['kind']=='replay_output' and not args.verify_evidence: continue
        p=ROOT/name
        if not p.is_file() or sha(p)!=e['sha256']: raise SystemExit('Manifest mismatch: '+name)
        count+=1
    pins=json.loads((ROOT/'review/REVIEWED-PROOF-PINS.json').read_text())
    for name,h in pins['files'].items():
        if sha(ROOT/'formal'/name)!=h: raise SystemExit('Reviewed proof bytes changed: '+name)
    if any((ROOT/'formal'/name).exists() for name in ['T7RL','T7Host']):
        raise SystemExit('Newer, non-reviewed extension found in finite publication package')
    evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
    env=dict(os.environ,T7_LEAN_BIN=str(binpath))
    runs=[]
    def run(cmd,logname,cwd=ROOT,extra_env=None):
        log=evidence/logname;t=time.monotonic()
        with log.open('w') as f:
            result=subprocess.run(cmd,cwd=cwd,env=extra_env or env,stdout=f,stderr=subprocess.STDOUT)
        rec={'command':list(map(str,cmd)),'log':str(log.relative_to(ROOT)),'exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-t,3)}
        runs.append(rec)
        if result.returncode:
            print(log.read_text()[-8000:],file=sys.stderr)
            raise SystemExit('Replay failed: '+logname)
        print('PASS',logname,flush=True)
    formal=ROOT/'formal'
    run([sys.executable,'scripts/build_offline.py'],'formal-build.log',formal)
    run([sys.executable,'scripts/review_dependencies.py'],'dependency-checks.log',formal)
    run([sys.executable,'scripts/negative_controls.py'],'author-negative-controls.log',formal)
    controlbuild=ROOT/'build/controls'
    if controlbuild.exists(): shutil.rmtree(controlbuild)
    controlbuild.mkdir(parents=True)
    controlenv=dict(env,LEAN_PATH=os.pathsep.join([str(controlbuild),str(formal/'build/lean')]))
    run([str(lean),'-t','0',str(ROOT/'controls/PublicationClaim.lean')],'paired-publication-claim.log',extra_env=controlenv)
    run([str(lean),'-t','0','-R',str(ROOT/'controls'),'-o',str(controlbuild/'BetaMargin.olean'),str(ROOT/'controls/BetaMargin.lean')],
        'beta-margin.log',extra_env=controlenv)
    run([str(lean),'-t','0',str(ROOT/'controls/ControlAudit.lean')],'beta-all-declarations.log',extra_env=controlenv)
    decls={}
    for line in (evidence/'beta-all-declarations.log').read_text().splitlines():
        if not line.startswith('DECL|'): continue
        _,name,kind,axs,deps,body=line.split('|')
        axioms=[a for a in axs.split(',') if a]
        if kind=='axiom' or set(axioms)-ALLOWED: raise SystemExit('Forbidden control axiom: '+name)
        decls[name]={'kind':kind,'axioms':axioms,'direct_type_dependencies':deps.split(','),'direct_body_dependencies':body.split(',')}
    expected={f'T7Publication.{x}' for x in ['beta564_budget','beta563_budget','beta563_exceeds_threshold','beta563_not_same_budget']}
    if not expected.issubset(decls): raise SystemExit('Control declaration audit missing named lemmas')
    (evidence/'beta-declarations.json').write_text(json.dumps(decls,indent=2)+'\n')
    build=json.loads((formal/'logs/rebuild/build-receipt.json').read_text())
    assert build['status']=='PASS' and build['trust_level']==0
    assert build['theorem_count']==312 and build['project_declarations_audited']==1187
    assert build['axiom_union']==sorted(ALLOWED)
    receipt={'status':'PASS','scope':'Source section 6 finite coefficient bound with source-expanded eta; no density or counterexample claim',
        'reviewed_proof_files_unchanged':len(pins['files']),'manifest_files_verified':count,'trust_level':0,
        'formal_modules':len(build['modules']),'formal_theorems':build['theorem_count'],'formal_declarations':build['project_declarations_audited'],
        'full_toolchain_hash_verified':build['full_toolchain_hash_verified'],'source_packet_files_verified':build['source_packet_files_verified'],
        'axiom_union':build['axiom_union'],'paired_claims':['T7Weighted.source_weighted_negativity','T7Weighted.eta_source'],
        'new_beta_control_lemmas':sorted(expected),'new_control_declarations_audited':len(decls),
        'historical_InsufficientBeta_status':'INCONCLUSIVE_REDUCTION_NOT_A_SEMANTIC_REJECTION',
        'beta_correction_status':'FOUR_KERNEL_PROVED_BUDGET_STATEMENTS_INCLUDING_DISEQUALITY',
        'changed_beta_headline_disproved':False,'opus_review_scope':'Unchanged finite core; static review only; new packaging/controls not Opus-reviewed',
        'newer_RL_or_host_results_included':False,'elapsed_seconds':round(time.monotonic()-started,3),'runs':runs,'external_actions':[]}
    (evidence/'replay-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ['runs','new_beta_control_lemmas']},indent=2))
if __name__=='__main__':main()
