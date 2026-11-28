"""Bounded replication from public anonymous OSF data; print aggregates only."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, norm, chi2
from scipy.optimize import minimize
from scipy.special import expit

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--study1',required=True,type=Path)
parser.add_argument('--study2',required=True,type=Path)
parser.add_argument('--output',required=True,type=Path)
parser.add_argument('--verbose',action='store_true')
args=parser.parse_args()
first=args.study1
second=args.study2
expected_hashes=['0af5c74ac5594924a7f605ab1ff046a6b0a4f94d125b5954c888bf6fbe009808',
                 '72718f830d91d84fa94e4c0d69eecc9aefb13648be4eeb986c31a5d1f498f413']
for path,digest in zip([first,second],expected_hashes):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,'Use the documented public OSF data version'
s1=pd.read_csv(first)
s2=pd.read_csv(second)
pf=[f'J-PFIS_{i}' for i in range(1,10)]
f1=[f'TAI_f1_{i}' for i in range(1,6)]
f2=[f'TAI_f2_{i}' for i in range(6,11)]
s2['PFI']=s2[pf].mean(axis=1)
s2['TAI1']=s2[f1].mean(axis=1)
s2['TAI2']=s2[f2].mean(axis=1)
q1=[c for c in s2 if c.endswith('_q1')]
assert s2[q1].notna().sum(axis=1).eq(1).all()
assert all(set(s2[c].dropna()).issubset({0.,1.}) for c in q1)
conditions=[]
long=[]
for column in q1:
    q2=column[:-1]+'2'
    sub=s2.loc[s2[column].notna()].copy()
    assert sub[q2].notna().all()
    sub['response']=sub[column]
    sub['change']=(sub[column]!=sub[q2]).astype(int)
    sub['advisor']='AI' if '_AI_' in column else 'Expert'
    sub['condition']=column[:-3]
    long.append(sub[['age','sex_male1_female0','PFI','TAI1','TAI2','response','change','advisor','condition']])
    conditions.append({'condition':column[:-3],'n':len(sub),'response_1':int(sub[column].sum()),
       'proportion_1':float(sub[column].mean()),'q1_q2_discrepancies':int(sub['change'].sum())})
stack=pd.concat(long,ignore_index=True)
results={'scope':'Bounded replication of public OSF CSV counts,printed omnibus comparisons and pooled logistic models. No author code,no participant-level outputs,no source-model inference or independent replication dataset.',
    'hashes':{name:hashlib.sha256(p.read_bytes()).hexdigest()
              for name,p in [('study1.csv',first),('study2.csv',second)]},
    'sample_sizes':{'study1':len(s1),'study2':len(s2),'one_assigned_condition_per_person':True},
    'conditions':conditions,
    'scale_aggregates':{c:{'mean':float(s2[c].mean()),'sd':float(s2[c].std())} for c in ['PFI','TAI1','TAI2']},
    'omnibus':{},'logistic':{}}
mapping={'trolley(switch)':'Trolley_switch_','trolley(bridge)':'Trolley_bridge_',
         'delay':'Delay_2','gender':'Gender_3'}
for task,baseline in mapping.items():
    chosen=[c for c in conditions if c['condition'].startswith(task+'_')]
    cells=[{'condition':'historical_study1','n':len(s1),'response_1':int(s1[baseline].sum())},*chosen]
    observed=np.array([[c['response_1'] for c in cells],[c['n']-c['response_1'] for c in cells]])
    statistic,p,df,expected=chi2_contingency(observed,correction=False)
    total=observed.sum()
    rowp=observed.sum(axis=1)/total
    colp=observed.sum(axis=0)/total
    adjusted=(observed-expected)/np.sqrt(expected*(1-rowp[:,None])*(1-colp[None,:]))
    results['omnibus'][task]={'chi2':float(statistic),'df':int(df),'p':float(p),
      'cramers_v':float(np.sqrt(statistic/total)),
      'adjusted_residuals':[{'condition':c['condition'],'z_response1':float(adjusted[0,i]),
          'uncorrected_two_sided_p':float(2*norm.sf(abs(adjusted[0,i])))} for i,c in enumerate(cells)]}
for advisor in ['AI','Expert']:
    frame=stack[stack['advisor']==advisor]
    names=['const','age','sex_male1_female0','PFI','TAI1','TAI2']
    x=np.column_stack([np.ones(len(frame)),frame[names[1:]].to_numpy()])
    y=frame['change'].to_numpy(dtype=float)
    def objective(beta):
        eta=x@beta
        return np.logaddexp(0,eta).sum()-y@eta
    def gradient(beta):
        return x.T@(expit(x@beta)-y)
    def information(beta):
        p=expit(x@beta)
        return x.T@((p*(1-p))[:,None]*x)
    fit=minimize(objective,np.zeros(x.shape[1]),jac=gradient,hess=information,
        method='trust-exact',options={'gtol':1e-8,'maxiter':1000})
    max_gradient=float(np.abs(gradient(fit.x)).max())
    assert max_gradient<1e-5,(advisor,fit.message,max_gradient)
    covariance=np.linalg.inv(information(fit.x))
    se=np.sqrt(np.diag(covariance))
    p_wald=2*norm.sf(np.abs(fit.x/se))
    mean=y.mean()
    ll0=float((y*np.log(mean)+(1-y)*np.log1p(-mean)).sum())
    ll=-float(objective(fit.x))
    lr=2*(ll-ll0)
    results['logistic'][advisor]={'n':len(frame),'events':int(frame['change'].sum()),
        'llr':lr,'llr_p':float(chi2.sf(lr,5)),'mcfadden_r2':1-ll/ll0,
        'nagelkerke_r2':(1-np.exp(-lr/len(frame)))/(1-np.exp(2*ll0/len(frame))),
        'scale_aggregates':{c:{'mean':float(frame[c].mean()),'sd':float(frame[c].std())}
                            for c in ['PFI','TAI1','TAI2']},
        'max_abs_gradient':max_gradient,
        'coefficients':{c:{'B':float(fit.x[i]),'SE':float(se[i]),'p':float(p_wald[i])}
                        for i,c in enumerate(names)},
        'pfi_odds_ratio':float(math.exp(fit.x[names.index('PFI')]))}
results['limits']=[
    'Study1 is a different January sample and survey context,not a concurrent randomized no-advice arm of Study2.',
    'q2 is a hypothetical no-advice choice asked after the advised choice,not a pre-advice baseline or verified causal change.',
    'Scale aggregates use the nine deposited PFI columns and five items per TAI factor. Materials list eleven PFI items;mapping,omission and reverse scoring remain unresolved without a codebook.',
    'Adjusted residual tests compare each cell with the pooled omnibus expectation,not each advised group directly with the historical baseline. P-values here are uncorrected for multiplicity.',
    'Separate significant/non-significant results do not prove advisor equivalence,source-by-direction interactions,emotion mediation or absence of trust effects.'
]
out=args.output
out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
display=results if args.verbose else {
    'output':str(out),'sample_sizes':results['sample_sizes'],
    'omnibus':{task:{k:v for k,v in result.items() if k!='adjusted_residuals'}
               for task,result in results['omnibus'].items()},
    'logistic':results['logistic']}
print(json.dumps(display,ensure_ascii=False,indent=2))
