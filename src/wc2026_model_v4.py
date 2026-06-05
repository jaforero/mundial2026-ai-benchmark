# -*- coding: utf-8 -*-
"""
MOTOR v4 — ENSAMBLE (el que mejor valida fuera de muestra):
  λ_v4 = 0.5·λ_DixonColes_v3  +  0.5·λ_MachineLearning
  - Dixon-Coles v3: ataque/defensa por equipo estimados de datos reales.
  - ML (Gradient Boosting Poisson): integra Elo actual (jun-2026), forma reciente
    e histórico de Mundiales.
Reutiliza el andamiaje del torneo del v2 (llaves oficiales 2026, terceros, Monte Carlo).
OOS 2018+2022: RPS 0.2122 (mejora 13.3% sobre azar), mejor que cada modelo por separado.
"""
import json, math
import numpy as np
import wc2026_model_v2 as m2
import wc2026_ml_v4 as ml
from wc2026_model import GROUPS, HOSTS, ALL_TEAMS, ROUNDS

# --- componente Dixon-Coles v3 (ya ajustado a 2026-06-05) ---
S = json.load(open("/home/claude/wc2026/strengths_v3.json", encoding="utf-8"))
MU,HOME,RHO,ATT,DEF = S["mu"],S["home"],S["rho"],S["att"],S["def"]
ES2EN = ml.ES2EN

# --- componente ML (entrenado con datos hasta 2026-06-05) ---
print("Entrenando componente ML (gradient boosting Poisson)…")
MLM, MLSTATE = ml.train("2026-06-05")

W = 0.5  # peso del ensamble (validado)

# --- precálculo de λ del ML para todos los pares (rápido: una predicción por lotes) ---
print("Precalculando tabla de goles esperados ML (48×48×2)…")
_pairs=[]; _idx={}
for a in ALL_TEAMS:
    for b in ALL_TEAMS:
        for hflag in (False,True):
            _idx[(a,b,hflag)]=len(_pairs)
            _pairs.append(ml.featvec(MLSTATE, ES2EN[a], ES2EN[b], hflag))
_pred=MLM.predict(np.array(_pairs))
MLG={k:float(_pred[v]) for k,v in _idx.items()}

def dc_lam(a,b,ha,hb):
    la=math.exp(MU+ATT[a]-DEF[b]+(HOME if ha else 0.0))
    lb=math.exp(MU+ATT[b]-DEF[a]+(HOME if hb else 0.0))
    return la,lb
def ml_lam(a,b,ha,hb):
    return MLG[(a,b,ha)], MLG[(b,a,hb)]
def lambdas_v4(a,b,home_a=False,home_b=False):
    la1,lb1=dc_lam(a,b,home_a,home_b); la2,lb2=ml_lam(a,b,home_a,home_b)
    return W*la1+(1-W)*la2, W*lb1+(1-W)*lb2

m2.lambdas=lambdas_v4
m2.DC_RHO=RHO

if __name__=="__main__":
    tot=[];draws=0;ng=0
    for gl,teams in GROUPS.items():
        for i in range(4):
            for j in range(i+1,4):
                a,b=teams[i],teams[j]; d=m2.match_detail(a,b,a in HOSTS,b in HOSTS)
                tot.append(d["la"]+d["lb"]);draws+=d["pD"];ng+=1
    print(f"Partidos {ng} | goles esperados/juego {np.mean(tot):.3f} | empate medio {draws/ng:.1f}%")
    N=60000
    track,_=m2.run(N)
    champ=sorted(track["reach"]["CAMPEON"].items(),key=lambda x:-x[1])
    print(f"\n=== TÍTULO (v4 ensamble, N={N}) ===")
    for t,c in champ[:12]: print(f"  {t:16s}{100*c/N:6.2f}%")
    def pct(d,t): return round(100.0*d.get(t,0)/N,4)
    out={"N":N,"engine":"v4-Ensemble-DixonColes+ML",
         "params":{"weight_dc":W,"weight_ml":1-W,"mu":round(MU,4),"home":round(HOME,4),"rho":round(RHO,4),
                   "ml_features":["Elo actual (jun-2026)","forma reciente GF/GA","histórico Mundiales (part./%vict)","localía"],
                   "oos_rps":0.2122,"oos_rps_uniform":0.2448,"oos_gain_pct":13.3,
                   "oos_rps_dc_only":0.2127,"oos_rps_ml_only":0.2138},
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
    json.dump(out,open("/home/claude/wc2026/results_v4.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print("\nGuardado results_v4.json (ensamble Dixon-Coles + ML)")
