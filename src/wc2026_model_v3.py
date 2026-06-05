# -*- coding: utf-8 -*-
"""
MOTOR v3 — Ataque/Defensa por equipo estimados de DATOS (no del Elo).
Reutiliza el andamiaje del torneo del v2 (grupos, llaves oficiales 2026, terceros,
prórroga/penales, Monte Carlo) y reemplaza SOLO el motor de goles por las fuerzas
ajustadas por máxima verosimilitud Dixon-Coles sobre resultados internacionales
reales, validadas fuera de muestra contra los Mundiales 2018 y 2022.
"""
import json, math
import numpy as np
import wc2026_model_v2 as m2
from wc2026_model import GROUPS, HOSTS, ALL_TEAMS, ROUNDS

S = json.load(open("/home/claude/wc2026/strengths_v3.json", encoding="utf-8"))
MU, HOME, RHO = S["mu"], S["home"], S["rho"]
ATT, DEF = S["att"], S["def"]

# Fallback por si faltara algún equipo (no ocurre: las 48 tienen datos)
_def_att = float(np.mean(list(ATT.values()))); _def_def = float(np.mean(list(DEF.values())))

def lambdas_v3(a, b, home_a=False, home_b=False):
    aa = ATT.get(a, _def_att); ab = ATT.get(b, _def_att)
    da = DEF.get(a, _def_def); db = DEF.get(b, _def_def)
    la = math.exp(MU + aa - db + (HOME if home_a else 0.0))
    lb = math.exp(MU + ab - da + (HOME if home_b else 0.0))
    return la, lb

# --- Inyección: reemplazar el motor de goles del v2 ---
m2.lambdas = lambdas_v3      # usado por match_detail, sim_goals, sim_knockout
m2.DC_RHO  = RHO             # usado por score_matrix

if __name__ == "__main__":
    # 1) chequeo a nivel partido
    tot=[]; draws=0; ng=0
    for gl,teams in GROUPS.items():
        for i in range(4):
            for j in range(i+1,4):
                a,b=teams[i],teams[j]
                d=m2.match_detail(a,b,a in HOSTS,b in HOSTS)
                tot.append(d["la"]+d["lb"]); draws+=d["pD"]; ng+=1
    print(f"Partidos: {ng} | goles esperados/juego (media λA+λB): {np.mean(tot):.3f} | "
          f"empate medio {draws/ng:.1f}% | rango {min(tot):.2f}-{max(tot):.2f}")

    # 2) Monte Carlo del torneo (más corridas que v2 para mayor precisión)
    N=60000
    track,_=m2.run(N)
    champ=sorted(track["reach"]["CAMPEON"].items(),key=lambda x:-x[1])
    print(f"\n=== TÍTULO (v3 data-driven, N={N}) ===")
    for t,c in champ[:12]:
        print(f"  {t:16s}{100*c/N:6.2f}%")

    # 3) exportar con el mismo esquema enriquecido que v2
    def pct(d,t): return round(100.0*d.get(t,0)/N, 4)
    out={"N":N,"engine":"v3-DixonColes-DataDriven",
         "params":{"mu":round(MU,4),"home":round(HOME,4),"rho":round(RHO,4),
                   "n_matches_fit":S["n_matches"],
                   "oos_rps_2018_2022":0.2127,"oos_rps_uniform":0.2448,"oos_gain_pct":13.1},
         "title":{},"group_win":{},"advance":{},"third_adv":{},"pos":{},
         "reach":{r:{} for r in ROUNDS},"fixtures":[],
         "strength":{t:{"att":round(ATT[t],3),"def":round(DEF[t],3)} for t in ALL_TEAMS}}
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
                a,b=teams[i],teams[j]
                d=m2.match_detail(a,b,a in HOSTS,b in HOSTS); d["group"]=gl
                out["fixtures"].append(d)
    json.dump(out, open("/home/claude/wc2026/results_v3.json","w",encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\nGuardado results_v3.json (motor v3 enriquecido, ataque/defensa por datos)")
