# -*- coding: utf-8 -*-
"""
Backtest de las TRANSFORMACIONES de recalibración v7 contra datos reales.
=========================================================================
Cierra el círculo de auditoría con EVIDENCIA, no con criterio. Reutiliza el
backtest OOS del modelo de Claude (Mundiales 2010, 2014, 2018, 2022 = 192
partidos de grupos reales; el modelo se ajusta SOLO con datos previos a cada
torneo) y, sobre las probabilidades del ensamble, prueba dos preguntas:

  1) ¿La INFLACIÓN DE EMPATE acerca la tasa proyectada de empates a la real
     y mejora el RPS fuera de muestra?  -> barrido de beta.
  2) ¿El ENCOGIMIENTO (temperatura, anti-sobreconfianza) mejora el RPS/Log-loss
     fuera de muestra?                  -> barrido de temperatura T.

Métricas: RPS (ordinal H<D<A), Log-loss, Brier y la BRECHA de empate
(|tasa proyectada - tasa real|). Las transformaciones se evalúan exactamente
con las fórmulas de wc2026_recalibrate_v7.py.
"""
import math, json
import numpy as np
import wc2026_fit_v3 as dc, wc2026_ml_v4 as ml

CUT = {"2010":"2010-06-10","2014":"2014-06-11","2018":"2018-06-13","2022":"2022-11-19"}

def dc_lams(f,h,a,neu):
    la=math.exp(f["mu"]+f["att"][h]-f["def"][a]+(0 if neu else f["home"]))
    lb=math.exp(f["mu"]+f["att"][a]-f["def"][h]); return la,lb

# ---- recolectar probabilidades del ENSAMBLE + resultado real (OOS) ----
records=[]   # cada uno: (pH,pD,pA, oc)  con oc: 0=local,1=empate,2=visitante
for year,cut in CUT.items():
    f=dc.fit(cut); m,state=ml.train(cut)
    for d,h,a,hs,as_,tn,neu in ml.wc_group(year):
        if h not in f["att"] or a not in f["att"]: continue
        oc=0 if hs>as_ else (2 if as_>hs else 1)
        la1,lb1=dc_lams(f,h,a,neu)
        la2=float(m.predict([ml.featvec(state,h,a,not neu)])[0]); lb2=float(m.predict([ml.featvec(state,a,h,False)])[0])
        lae=0.5*la1+0.5*la2; lbe=0.5*lb1+0.5*lb2
        pH,pD,pA=dc.outcome_probs(lae,lbe,f["rho"])   # (local, empate, visitante)
        records.append((pH,pD,pA,oc))
N=len(records)

# ---- métricas ----
def rps3(p,oc):
    oo=[0,0,0]; oo[oc]=1; c=cp=co=0.0
    for k in range(3): cp+=p[k]; co+=oo[k]; c+=(cp-co)**2
    return 0.5*c
def logloss(p,oc): return -math.log(min(max(p[oc],1e-12),1.0))
def brier(p,oc):
    oo=[0,0,0]; oo[oc]=1; return sum((p[k]-oo[k])**2 for k in range(3))

def aggregate(recs):
    r=sum(rps3((pH,pD,pA),oc) for pH,pD,pA,oc in recs)/len(recs)
    ll=sum(logloss((pH,pD,pA),oc) for pH,pD,pA,oc in recs)/len(recs)
    br=sum(brier((pH,pD,pA),oc) for pH,pD,pA,oc in recs)/len(recs)
    proj_draw=sum(pD for pH,pD,pA,oc in recs)/len(recs)
    return r,ll,br,proj_draw

real_draw=sum(1 for *_,oc in records if oc==1)/N

# ---- transformaciones (idénticas a wc2026_recalibrate_v7.py) ----
def draw_inflate(rec, beta):
    pH,pD,pA,oc=rec
    parity=1-abs(pH-pA)            # probs en fracción (0..1)
    pD2=pD+beta*parity*(1-pD)*0.5
    rest=1-pD2; s=pH+pA
    pH2,pA2=(pH*rest/s,pA*rest/s) if s>0 else (rest/2,rest/2)
    return (pH2,pD2,pA2,oc)

def temper(rec, T):
    pH,pD,pA,oc=rec
    q=[pH**(1/T),pD**(1/T),pA**(1/T)]; s=sum(q)
    return (q[0]/s,q[1]/s,q[2]/s,oc)

# ===================== BARRIDO 1: inflación de empate =====================
print("=== BACKTEST DE TRANSFORMACIONES v7 — 192 partidos OOS (2010-2022) ===\n")
base_r,base_ll,base_br,base_draw=aggregate(records)
print("Base (ensamble sin transformar):")
print(f"  RPS {base_r:.4f} · LogLoss {base_ll:.4f} · Brier {base_br:.4f}")
print(f"  Tasa de empate REAL {real_draw*100:.2f}% · proyectada {base_draw*100:.2f}% · brecha {abs(base_draw-real_draw)*100:.2f} pp\n")

print("1) INFLACIÓN DE EMPATE (beta):")
print(f"  {'beta':>6s}{'RPS':>9s}{'LogLoss':>9s}{'tasaEmp.proj':>13s}{'brecha(pp)':>11s}")
betas=[round(b,2) for b in np.arange(0,0.55,0.05)]
draw_rows=[]
for b in betas:
    recs=[draw_inflate(r,b) for r in records]
    rr,ll,br,pdraw=aggregate(recs)
    gap=abs(pdraw-real_draw)*100
    draw_rows.append((b,rr,ll,pdraw,gap))
    print(f"  {b:6.2f}{rr:9.4f}{ll:9.4f}{pdraw*100:12.2f}%{gap:11.2f}")
best_rps_beta=min(draw_rows,key=lambda x:x[1])
best_gap_beta=min(draw_rows,key=lambda x:x[4])
print(f"  -> beta óptimo por RPS: {best_rps_beta[0]:.2f} (RPS {best_rps_beta[1]:.4f})")
print(f"  -> beta que mejor iguala la tasa real: {best_gap_beta[0]:.2f} (brecha {best_gap_beta[4]:.2f} pp)\n")

# ===================== BARRIDO 2: temperatura (encogimiento) =====================
print("2) ENCOGIMIENTO / TEMPERATURA (T>1 = menos confianza):")
print(f"  {'T':>6s}{'RPS':>9s}{'LogLoss':>9s}{'Brier':>9s}")
Ts=[round(t,2) for t in np.arange(0.90,1.45,0.05)]
temp_rows=[]
for T in Ts:
    recs=[temper(r,T) for r in records]
    rr,ll,br,_=aggregate(recs)
    temp_rows.append((T,rr,ll,br))
    print(f"  {T:6.2f}{rr:9.4f}{ll:9.4f}{br:9.4f}")
best_T_rps=min(temp_rows,key=lambda x:x[1])
best_T_ll=min(temp_rows,key=lambda x:x[2])
print(f"  -> T óptimo por RPS: {best_T_rps[0]:.2f} (RPS {best_T_rps[1]:.4f})")
print(f"  -> T óptimo por LogLoss: {best_T_ll[0]:.2f} (LogLoss {best_T_ll[2]:.4f})\n")

# ===================== combinación: empate óptimo + temperatura óptima =====================
b=best_rps_beta[0]; T=best_T_rps[0]
recs=[temper(draw_inflate(r,b),T) for r in records]
cr,cll,cbr,cdraw=aggregate(recs)
print(f"3) COMBINADO (beta={b:.2f} + T={T:.2f}):")
print(f"  RPS {cr:.4f} (base {base_r:.4f}, {100*(base_r-cr)/base_r:+.2f}%) · LogLoss {cll:.4f} · brecha empate {abs(cdraw-real_draw)*100:.2f} pp")

out={
 "n_matches":N,"real_draw_rate":real_draw,
 "base":{"RPS":base_r,"LogLoss":base_ll,"Brier":base_br,"proj_draw":base_draw},
 "draw_sweep":[{"beta":b,"RPS":r,"LogLoss":l,"proj_draw":pd,"gap_pp":g} for b,r,l,pd,g in draw_rows],
 "temp_sweep":[{"T":t,"RPS":r,"LogLoss":l,"Brier":br} for t,r,l,br in temp_rows],
 "best":{"beta_rps":best_rps_beta[0],"beta_gap":best_gap_beta[0],"T_rps":best_T_rps[0],"T_logloss":best_T_ll[0]},
 "combined":{"beta":b,"T":T,"RPS":cr,"LogLoss":cll,"gap_pp":abs(cdraw-real_draw)*100,"rps_gain_pct":100*(base_r-cr)/base_r},
}
json.dump(out,open("backtest_recalibration_v7_results.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("\nGuardado backtest_recalibration_v7_results.json")
