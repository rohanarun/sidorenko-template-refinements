#!/usr/bin/env python3
"""Check required proof/data dependency paths; this supplements semantic review."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
d = json.loads((ROOT/'logs/rebuild/declaration-audit.json').read_text())
def closure(name):
    result=set(); todo=[name]
    while todo:
        x=todo.pop()
        if x in result: continue
        result.add(x)
        todo.extend(dep for dep in d.get(x,{}).get('direct_dependencies',[]) if dep not in result)
    return result
checks={
 'T7Weighted.source_weighted_negativity':['T7Weighted.averagedCoefficient_negative','T7Gap.averagedCoefficient','T7Weighted.sourceScore_eq_score','T7Weighted.actual_weight_relative','T7Weighted.finiteRemainder_bound','T7Gap.activation_moment_eq_formula','T7Gap.pointPrior','T7Gap.facePrior'],
 'T7Weighted.finiteRemainder_two_sided':['T7Weighted.generalCoefficient_bounds','T7Weighted.score_max_iff','T7.stable_endomorphisms_exact','T7Gap.generalCoefficient_non_incidence'],
 'T7Weighted.eta_source':['T7Weighted.pointNormalizer_source','T7Weighted.faceNormalizer_source'],
 'T7Gap.stochastic_signed_orbit':['T7Gap.activation_moment_eq_formula','T7Gap.activationMoment','T7Gap.activationWeight','T7Gap.FiniteLaw.mean','T7.signed_orbit_coefficient'],
 'T7Gap.general_signed_orbit':['T7Gap.stochastic_signed_orbit','T7Gap.pairMoment'],
 'T7Gap.averagedCoefficient_exact':['T7Gap.thinnedCoefficient_factor','T7Gap.thinnedMoment_factor','T7Gap.bernoulliLaw','T7Gap.pointPrior','T7Gap.facePrior'],
 'T7Gap.constructedKernel_mean_one':['T7Gap.activationKernel_mean_one','T7Gap.SignedBase.mean_one','T7Gap.FiniteLaw.mean'],
 'T7Gap.symmetricProduct_density':['T7Gap.independent_productLaw','T7Gap.RationalBipartiteKernel.density'],
 'T7Gap.boundedConstructed_mean_positive':['T7Gap.constructed_symmetric_mean_one','T7Gap.kernelBound_positive']}
results=[]
for name, required in checks.items():
    assert d[name]['direct_body_dependencies'], f'Proof body dependencies missing: {name}'
    c=closure(name); missing=set(required)-c
    assert not missing, (name, missing)
    results.append({'theorem':name,'required_dependencies_found':required,'dependency_closure_count':len(c),'status':'PASS'})
host=closure('T7.finite_host_conditional')
assert 'T7Gap.activation_moment_eq_formula' not in host
assert 'T7.signed_orbit_coefficient' not in host
result={'status':'PASS','method':'Executable constant-dependency closure checks supplement the semantic source correspondence review in COVERAGE.md. Type and proof-body dependencies are recorded separately.',
 'checks':results,'host_not_connected_to_new_kernel':True,'host_not_dependent_on_signed_coefficient':True,
 'reviewed_open_gaps':['RL-to-actual-density transfer','kernel deficit','sampling estimates'],
 'all_decl_count':len(d),'all_decl_axiom_union':sorted({a for v in d.values() for a in v['axioms']})}
(ROOT/'logs/correspondence-review.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'dependency_checks':len(results),'project_declarations_audited':len(d)}))
