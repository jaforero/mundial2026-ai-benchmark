# -*- coding: utf-8 -*-
"""Ensamble v4 = Dixon-Coles data-driven (v3) + Gradient Boosting Poisson (ML).
Valida fuera de muestra (2018+2022) si el ENSAMBLE supera a cada modelo por separado."""
import math, numpy as np
import wc2026_fit_v3 as dc
import wc2026_ml_v4 as ml

def dc_lams(f,h,a,neu):
    la=math.exp(f["mu"]+f["att"][h]-f["def"][a]+(0 if neu else f["home"]))
    lb=math.exp(f["mu"]+f["att"][a]-f["def"][h]); return la,lb

def rps(p,o):
    oo=[0,0,0]; oo[o]=1; c=cp=co=0.0
    for k in range(3): cp+=p[k];co+=oo[k];c+=(cp-co)**2
    return 0.5*c

def run(year,cutoff,wlam=0.5,wp=0.5):
    f=dc.fit(cutoff); m,state=ml.train(cutoff)
    out={"dc":[0,0],"ml":[0,0],"ens_p":[0,0],"ens_l":[0,0],"unif":0.0,"n":0}
    for d,h,a,hs,as_,tn,neu in ml.wc_group(year):
        if h not in f["att"] or a not in f["att"]: continue
        oc=0 if hs>as_ else (2 if as_>hs else 1)
        # DC
        la1,lb1=dc_lams(f,h,a,neu); pdc=dc.outcome_probs(la1,lb1,f["rho"])
        # ML
        la2=float(m.predict([ml.featvec(state,h,a,not neu)])[0])
        lb2=float(m.predict([ml.featvec(state,a,h,False)])[0])
        pml=ml.probs(la2,lb2,f["rho"])
        # ensamble por PROBABILIDADES
        pe=tuple(wp*x+(1-wp)*y for x,y in zip(pdc,pml))
        # ensamble por LAMBDAS (lo que usaría el simulador)
        lae=wlam*la1+(1-wlam)*la2; lbe=wlam*lb1+(1-wlam)*lb2
        pel=dc.outcome_probs(lae,lbe,f["rho"])
        out["dc"][0]+=rps(pdc,oc); out["ml"][0]+=rps(pml,oc)
        out["ens_p"][0]+=rps(pe,oc); out["ens_l"][0]+=rps(pel,oc)
        out["unif"]+=rps((1/3,1/3,1/3),oc); out["n"]+=1
    return out

if __name__=="__main__":
    agg=defaultdict=lambda:0
    T={"dc":0.0,"ml":0.0,"ens_p":0.0,"ens_l":0.0,"unif":0.0,"n":0}
    for year,cut in [("2018","2018-06-10"),("2022","2022-11-19")]:
        o=run(year,cut)
        for k in ("dc","ml","ens_p","ens_l"): T[k]+=o[k][0]
        T["unif"]+=o["unif"]; T["n"]+=o["n"]
    n=T["n"]
    print("=== OOS 2018+2022 — RPS medio (menor es mejor) ===")
    print(f"  Dixon-Coles v3      : {T['dc']/n:.4f}  (mejora {100*(1-T['dc']/T['unif']):.1f}%)")
    print(f"  ML Gradient Boosting: {T['ml']/n:.4f}  (mejora {100*(1-T['ml']/T['unif']):.1f}%)")
    print(f"  ENSAMBLE (probs)    : {T['ens_p']/n:.4f}  (mejora {100*(1-T['ens_p']/T['unif']):.1f}%)")
    print(f"  ENSAMBLE (lambdas)  : {T['ens_l']/n:.4f}  (mejora {100*(1-T['ens_l']/T['unif']):.1f}%)")
    print(f"  Uniforme            : {T['unif']/n:.4f}")
