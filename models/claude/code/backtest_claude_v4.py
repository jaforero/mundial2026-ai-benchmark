# -*- coding: utf-8 -*-
"""
Backtest OOS COMPLETO del modelo Claude v4 (ensamble Dixon-Coles + ML).
Para cada Mundial (2010, 2014, 2018, 2022) el modelo se ajusta SOLO con datos
previos al torneo y predice sus 48 partidos de grupos reales. Métricas:
RPS, Brier multiclase (V/E/D), Log-loss, MAE de goles totales, acierto de marcador.
Compara DC solo, ML solo y el ENSAMBLE contra baseline uniforme.
"""
import math, numpy as np
import wc2026_fit_v3 as dc, wc2026_ml_v4 as ml

CUT = {"2010":"2010-06-10","2014":"2014-06-11","2018":"2018-06-13","2022":"2022-11-19"}

def dc_lams(f,h,a,neu):
    la=math.exp(f["mu"]+f["att"][h]-f["def"][a]+(0 if neu else f["home"]))
    lb=math.exp(f["mu"]+f["att"][a]-f["def"][h]); return la,lb

def score_grid(la,lb,rho,K=9):
    P=np.zeros((K,K))
    for x in range(K):
        for y in range(K):
            P[x,y]=math.exp(-la)*la**x/math.factorial(x)*math.exp(-lb)*lb**y/math.factorial(y)*dc.tau(x,y,la,lb,rho)
    P/=P.sum(); return P

def metrics_accum(p,oc,la,lb,rho,hs,as_,acc):
    # p = (pH,pD,pA) ; oc = 0/1/2
    oo=[0,0,0]; oo[oc]=1
    # RPS
    c=cp=co=0.0
    for k in range(3): cp+=p[k]; co+=oo[k]; c+=(cp-co)**2
    acc["rps"]+=0.5*c
    # Brier multiclase
    acc["brier"]+=sum((p[k]-oo[k])**2 for k in range(3))
    # Log-loss
    pa=min(max(p[oc],1e-12),1.0); acc["logloss"]+=-math.log(pa)
    # MAE goles totales
    acc["mae"]+=abs((la+lb)-(hs+as_))
    # acierto marcador modal
    G=score_grid(la,lb,rho); mx,my=np.unravel_index(G.argmax(),G.shape)
    if mx==hs and my==as_: acc["hit"]+=1
    acc["n"]+=1

def newacc(): return {"rps":0.,"brier":0.,"logloss":0.,"mae":0.,"hit":0,"n":0}

A={m:newacc() for m in ("dc","ml","ens")}
U=newacc()
per_year={}
for year,cut in CUT.items():
    f=dc.fit(cut); m,state=ml.train(cut)
    ay={m_:newacc() for m_ in ("dc","ml","ens")}
    for d,h,a,hs,as_,tn,neu in ml.wc_group(year):
        if h not in f["att"] or a not in f["att"]: continue
        oc=0 if hs>as_ else (2 if as_>hs else 1)
        la1,lb1=dc_lams(f,h,a,neu); pdc=dc.outcome_probs(la1,lb1,f["rho"])
        la2=float(m.predict([ml.featvec(state,h,a,not neu)])[0]); lb2=float(m.predict([ml.featvec(state,a,h,False)])[0])
        pml=ml.probs(la2,lb2,f["rho"])
        lae=0.5*la1+0.5*la2; lbe=0.5*lb1+0.5*lb2; pens=dc.outcome_probs(lae,lbe,f["rho"])
        metrics_accum(pdc,oc,la1,lb1,f["rho"],hs,as_,A["dc"]); metrics_accum(pdc,oc,la1,lb1,f["rho"],hs,as_,ay["dc"])
        metrics_accum(pml,oc,la2,lb2,f["rho"],hs,as_,A["ml"]); metrics_accum(pml,oc,la2,lb2,f["rho"],hs,as_,ay["ml"])
        metrics_accum(pens,oc,lae,lbe,f["rho"],hs,as_,A["ens"]); metrics_accum(pens,oc,lae,lbe,f["rho"],hs,as_,ay["ens"])
        # baseline uniforme
        oo=[0,0,0]; oo[oc]=1; c=cp=co=0.
        for k in range(3): cp+=1/3; co+=oo[k]; c+=(cp-co)**2
        U["rps"]+=0.5*c; U["brier"]+=sum((1/3-oo[k])**2 for k in range(3)); U["logloss"]+=-math.log(1/3); U["n"]+=1
    per_year[year]={k:ay[k]["rps"]/ay[k]["n"] for k in ay}

def rep(acc):
    n=acc["n"]; return dict(RPS=acc["rps"]/n,Brier=acc["brier"]/n,LogLoss=acc["logloss"]/n,
                            MAEgoles=acc["mae"]/n,HitMarcador=acc["hit"]/n)

print("=== BACKTEST OOS CLAUDE v4 — 4 Mundiales (2010-2022), 192 partidos ===\n")
print(f"{'Modelo':22s}{'RPS':>9s}{'Brier':>9s}{'LogLoss':>9s}{'MAEgoles':>10s}{'HitMarc':>9s}")
for k,lbl in [("dc","Dixon-Coles solo"),("ml","Machine Learning solo"),("ens","ENSAMBLE (modelo v4)")]:
    r=rep(A[k]); print(f"{lbl:22s}{r['RPS']:9.4f}{r['Brier']:9.4f}{r['LogLoss']:9.4f}{r['MAEgoles']:10.4f}{r['HitMarcador']*100:8.1f}%")
ru=rep(U); print(f"{'Baseline uniforme':22s}{ru['RPS']:9.4f}{ru['Brier']:9.4f}{ru['LogLoss']:9.4f}{'—':>10s}{'—':>9s}")
imp=100*(ru['RPS']-rep(A['ens'])['RPS'])/ru['RPS']
print(f"\nMejora del ensamble vs azar (RPS): {imp:.2f}%")
print("\nRPS por Mundial (ensamble):")
for y in CUT: print(f"  {y}: {per_year[y]['ens']:.4f}")
import json
json.dump({"overall":{k:rep(A[k]) for k in A},"uniform":rep(U),"improvement_pct":imp,
           "per_year_ens":{y:per_year[y]['ens'] for y in CUT},"n_matches":A['ens']['n']},
          open("backtest_claude_v4_results.json","w"),indent=2)
print("\nGuardado backtest_claude_v4_results.json")
