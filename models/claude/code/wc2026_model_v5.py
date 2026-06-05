# -*- coding: utf-8 -*-
"""
MOTOR v5 — ENSAMBLE afinado por el backtesting OOS de 4 Mundiales (2010-2022).
  λ_v5 = 0.4·λ_DixonColes_v3  +  0.6·λ_MachineLearning   (peso óptimo del backtest; curva plana 0.4-0.5)
Cambios v4 -> v5:
  1) CORRECCIÓN DE BRACKET: build_r32 reescrito para garantizar biyección exacta
     (32 clasificados -> 16 partidos, cada equipo UNA vez). En v4 algunos equipos
     se contaban dos veces en R32 (Inglaterra 120.9%, Croacia 130.9%). Ya no ocurre.
  2) Peso del ensamble afinado a 0.4/0.6 (DC/ML) según RPS mínimo en 192 partidos OOS.
  3) Siembra del bracket por Elo (ganadores fuertes vs terceros) con salvaguarda de mismo grupo.
Validación OOS 2010-2022: ensamble RPS 0.2002 (mejora 17.0% sobre azar), supera DC solo (0.2016) y ML solo (0.2012).
"""
import json, math
import numpy as np
import wc2026_model_v2 as m2
import wc2026_ml_v4 as ml
from wc2026_model import GROUPS, HOSTS, ALL_TEAMS, ROUNDS

S = json.load(open("/home/claude/wc2026/strengths_v3.json", encoding="utf-8"))
MU,HOME,RHO,ATT,DEF = S["mu"],S["home"],S["rho"],S["att"],S["def"]
ES2EN = ml.ES2EN
print("Entrenando componente ML (gradient boosting Poisson)…")
MLM, MLSTATE = ml.train("2026-06-05")

W = 0.4  # peso Dixon-Coles (0.6 ML) — óptimo del backtest 2010-2022

print("Precalculando tabla de goles esperados ML…")
_pairs=[]; _idx={}
for a in ALL_TEAMS:
    for b in ALL_TEAMS:
        for hflag in (False,True):
            _idx[(a,b,hflag)]=len(_pairs); _pairs.append(ml.featvec(MLSTATE, ES2EN[a], ES2EN[b], hflag))
_pred=MLM.predict(np.array(_pairs)); MLG={k:float(_pred[v]) for k,v in _idx.items()}

def dc_lam(a,b,ha,hb):
    return (math.exp(MU+ATT[a]-DEF[b]+(HOME if ha else 0.0)), math.exp(MU+ATT[b]-DEF[a]+(HOME if hb else 0.0)))
def ml_lam(a,b,ha,hb): return MLG[(a,b,ha)], MLG[(b,a,hb)]
def lambdas_v5(a,b,home_a=False,home_b=False):
    la1,lb1=dc_lam(a,b,home_a,home_b); la2,lb2=ml_lam(a,b,home_a,home_b)
    return W*la1+(1-W)*la2, W*lb1+(1-W)*lb2

m2.lambdas=lambdas_v5
m2.DC_RHO=RHO
# Sembrar el bracket por Elo actual (en nombres en español, como GROUPS)
m2.STRENGTH={t: float(MLSTATE["elo"].get(ES2EN[t],1500.0)) for t in ALL_TEAMS}

if __name__=="__main__":
    N=60000
    track,_=m2.run(N)
    def pct(d,t): return round(100.0*d.get(t,0)/N,4)
    out={"N":N,"engine":"v5-Ensemble-DixonColes+ML (bracket corregido + peso afinado)",
         "params":{"weight_dc":W,"weight_ml":round(1-W,4),"mu":round(MU,4),"home":round(HOME,4),"rho":round(RHO,4),
                   "ml_features":["Elo actual (jun-2026)","forma reciente GF/GA","histórico Mundiales (part./%vict)","localía"],
                   "oos_rps":0.2002,"oos_rps_uniform":0.2413,"oos_gain_pct":17.0,
                   "oos_rps_dc_only":0.2016,"oos_rps_ml_only":0.2012,"oos_n_matches":192,"oos_worldcups":"2010-2022"},
         "title":{},"group_win":{},"advance":{},"third_adv":{},"pos":{},
         "reach":{r:{} for r in ROUNDS},"fixtures":[],
         "elo_now":{t:round(MLSTATE["elo"].get(ES2EN[t],1500),0) for t in ALL_TEAMS}}
    for t in ALL_TEAMS:
        out["title"][t]=pct(track["reach"]["CAMPEON"],t)
        out["group_win"][t]=pct(track["group_win"],t)
        out["advance"][t]=pct(track["advance"],t)
        out["third_adv"][t]=pct(track["third_adv"],t)
        out["pos"][t]=[round(100*x/N,3) for x in track["pos"][t]]
        for r in ROUNDS: out["reach"][r][t]=pct(track["reach"][r],t)
    for gl,teams in GROUPS.items():
        for i in range(4):
            for j in range(i+1,4):
                a,b=teams[i],teams[j]; d=m2.match_detail(a,b,a in HOSTS,b in HOSTS); d["group"]=gl
                out["fixtures"].append(d)
    # ---- VALIDACIÓN DURA: ninguna probabilidad puede superar 100% ----
    bad=[(r,t,v) for r in ROUNDS for t,v in out["reach"][r].items() if v>100.0001]
    assert not bad, f"PROBABILIDAD >100% DETECTADA: {bad[:5]}"
    # R32 debe sumar ~32*100% (32 clasificados); cada ronda r suma ~ n_equipos(r)*100
    for r,n in [("R32",32),("R16",16),("QF",8),("SF",4),("FINAL",2),("CAMPEON",1)]:
        ssum=sum(out["reach"][r].values())
        assert abs(ssum-100*n)<1.0, f"Suma de {r}={ssum:.2f}, esperado ~{100*n}"
    print("✓ VALIDACIÓN OK: ninguna probabilidad >100%, y cada ronda suma lo correcto.")
    json.dump(out,open("/home/claude/wc2026/results_v5.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    champ=sorted(out["title"].items(),key=lambda x:-x[1])[:8]
    print("\n=== TÍTULO v5 (top 8) ===")
    for t,v in champ: print(f"  {t:16s}{v:6.2f}%")
    print("\nInglaterra R32 ahora:", out["reach"]["R32"]["Inglaterra"], "| Croacia R32:", out["reach"]["R32"]["Croacia"])
    print("Guardado results_v5.json")
