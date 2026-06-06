# -*- coding: utf-8 -*-
"""
Claude · FASE de Recalibración v7  (auditoría + calibración sobre v5/v6)
=========================================================================
NO reentrena el modelo: toma las salidas del motor v5 (selecciones y partidos)
y del modelo de goleadores v6, y aplica una CAPA DE CALIBRACIÓN documentada para
corregir exceso de confianza, tratar partidos de alta incertidumbre y exponer
los riesgos por goleador. No inventa datos ausentes.

Cuatro bloques (coherentes con los demás modelos del proyecto):
  1) Selecciones  : encogimiento hacia la tasa base por ronda (anti-sobreconfianza).
  2) Partidos     : inflación de empate en partidos parejos + marcador e índice de
                    incertidumbre; ajuste de marcador solo cuando el riesgo lo justifica.
  3) Goleadores   : recalibración por temperatura + desglose de riesgos
                    (minutos, rol, dificultad de grupo, dependencia, titularidad).
  4) Incertidumbre: diagnósticos de calibración y señales contradictorias.
"""
import json, math, statistics
import numpy as np

HERE = "/home/claude/wc2026"
V5 = json.load(open(f"{HERE}/results_v5.json", encoding="utf-8"))
GROUPS = json.load(open(f"{HERE}/consolidated.json", encoding="utf-8"))["groups"]
ELO = V5["elo_now"]; FIX = V5["fixtures"]; REACH5 = V5["reach"]

ROUND_TEAMS = {"R32":32,"R16":16,"QF":8,"SF":4,"FINAL":2,"CAMPEON":1}
ROUND_ORDER = ["R32","R16","QF","SF","FINAL","CAMPEON"]
TEAMS = list(V5["title"].keys())

# =====================================================================
# BLOQUE 1 — SELECCIONES: encogimiento hacia la tasa base por ronda
#   p' = base + (p - base)·s   (s<1 reduce el exceso de confianza)
#   luego se renormaliza cada ronda a su total (nº de equipos) y se
#   impone monotonía p(R32) >= p(R16) >= ... >= p(CAMPEON) por equipo.
# =====================================================================
SHRINK = {"R32":0.97,"R16":0.95,"QF":0.92,"SF":0.90,"FINAL":0.88,"CAMPEON":0.86}

def recalibrate_reach(reach5):
    out = {r: {} for r in ROUND_ORDER}
    for r in ROUND_ORDER:
        base = ROUND_TEAMS[r] / 48.0 * 100.0           # tasa base de la ronda (%)
        s = SHRINK[r]
        shr = {t: base + (reach5[r].get(t, 0.0) - base) * s for t in TEAMS}
        shr = {t: max(0.0, min(100.0, v)) for t, v in shr.items()}
        total = sum(shr.values()); target = ROUND_TEAMS[r] * 100.0
        out[r] = {t: v * target / total for t, v in shr.items()} if total > 0 else shr
    # monotonía por equipo
    for t in TEAMS:
        for i in range(1, len(ROUND_ORDER)):
            a, b = ROUND_ORDER[i-1], ROUND_ORDER[i]
            if out[b][t] > out[a][t]:
                out[b][t] = out[a][t]
    return {r: {t: round(out[r][t], 2) for t in TEAMS} for r in ROUND_ORDER}

reach7 = recalibrate_reach(REACH5)
title7 = dict(reach7["CAMPEON"])
# renormalizar campeón a 100 tras la monotonía
s = sum(title7.values()); title7 = {t: round(v*100.0/s, 4) for t, v in title7.items()}

# =====================================================================
# BLOQUE 2 — PARTIDOS: inflación de empate en partidos parejos +
#   índice de incertidumbre (entropía normalizada) + ajuste de marcador.
# =====================================================================
BETA_DRAW = 0.22   # cuánto se infla el empate en función de la paridad

def shannon(ps):
    return -sum(p*math.log(p) for p in ps if p > 0) / math.log(3)  # 0..1

def modal_draw(la, lb):
    m = (la + lb) / 2.0
    g = 0 if m < 0.75 else (1 if m < 1.6 else 2)
    return f"{g}-{g}"

def recalibrate_match(f):
    pA, pD, pB = f["pA"], f["pD"], f["pB"]
    closeness = 1 - abs(pA - pB) / 100.0                      # 0..1 (1 = parejo)
    pD2 = pD + BETA_DRAW * closeness * (100 - pD) * 0.5        # inflar empate
    rest = 100 - pD2
    s = pA + pB
    pA2, pB2 = (pA*rest/s, pB*rest/s) if s > 0 else (rest/2, rest/2)
    ps = [pA2/100, pD2/100, pB2/100]
    unc = shannon(ps)                                          # índice de incertidumbre
    high = (max(ps) < 0.45) or (unc > 0.93)
    # ajuste de marcador: solo si alta incertidumbre
    score = f["score"]
    la, lb = f.get("la", 1.2), f.get("lb", 1.0)
    adj = False
    if high:
        if pD2 >= max(pA2, pB2) - 3:                          # empate manda o casi
            score = modal_draw(la, lb); adj = True
        else:                                                  # acotar margen a 1
            try:
                ga, gb = map(int, f["score"].split("-"))
                if abs(ga-gb) >= 2:
                    if ga > gb: score = f"{gb+1}-{gb}"
                    else:       score = f"{ga}-{ga+1}"
                    adj = True
            except: pass
    return {"a":f["a"],"b":f["b"],"pA":round(pA2,1),"pD":round(pD2,1),"pB":round(pB2,1),
            "score":score,"unc":round(unc,3),"high_unc":high,"adj":adj,
            "pA5":pA,"pD5":pD,"pB5":pB,"score5":f["score"]}

matches7 = [recalibrate_match(f) for f in FIX]

# =====================================================================
# BLOQUE 3 — GOLEADORES: recalibración por temperatura + desglose de riesgos.
#   Reutiliza la descomposición v6 (goles de equipo × cuota × penales ×
#   titularidad × disponibilidad × forma) con la reach RECALIBRADA (v7),
#   aplica temperatura para reducir sobreconfianza y clasifica riesgos.
# =====================================================================
# candidatos (mismos del v6) con rol explícito para el desglose de riesgo
# player, team, role, role_share, pen, starter, avail, form
CAND = [
 ("Harry Kane","Inglaterra","Delantero central",0.30,1.12,0.96,0.95,1.06),
 ("Kylian Mbappé","Francia","Delantero central",0.32,1.12,0.96,0.85,1.08),
 ("Erling Haaland","Noruega","Delantero central",0.34,1.05,0.98,0.95,1.12),
 ("Cody Gakpo","Países Bajos","Extremo finalizador",0.26,1.0,0.90,0.90,1.05),
 ("Vinícius Júnior","Brasil","Extremo finalizador",0.24,1.0,0.92,0.85,1.02),
 ("Luis Díaz","Colombia","Extremo finalizador",0.27,1.0,0.94,0.92,1.05),
 ("Jamal Musiala","Alemania","Creador-finalizador",0.22,1.0,0.88,0.88,1.00),
 ("Bukayo Saka","Inglaterra","Extremo finalizador",0.19,1.0,0.82,0.75,0.95),
 ("Lionel Messi","Argentina","Creador-finalizador",0.24,1.12,0.85,0.85,1.00),
 ("Julián Álvarez","Argentina","Delantero móvil",0.22,1.0,0.72,0.65,0.95),
 ("Lamine Yamal","España","Extremo finalizador",0.20,1.0,0.85,0.70,0.95),
 ("Mikel Oyarzabal","España","Falso 9 / delantero",0.23,1.05,0.75,0.85,0.95),
 ("Cristiano Ronaldo","Portugal","Delantero central",0.26,1.12,0.70,0.80,0.90),
 ("Darwin Núñez","Uruguay","Delantero central",0.24,1.0,0.68,0.70,0.85),
]
ROUND_PLAY = ["R32","R16","QF","SF","FINAL"]
def exp_matches(team): return 3.0 + sum(reach7[r].get(team,0.0)/100.0 for r in ROUND_PLAY)
def xg_match(team):
    v=[f["la"] for f in FIX if f["a"]==team]+[f["lb"] for f in FIX if f["b"]==team]
    return statistics.mean(v) if v else 1.0
def team_goals(team): return exp_matches(team)*xg_match(team)

# dificultad de grupo: Elo medio de los rivales de grupo
def group_difficulty(team):
    for g, ts in GROUPS.items():
        if team in ts:
            opps=[ELO.get(o,1500) for o in ts if o!=team]
            return statistics.mean(opps) if opps else 1500
    return 1500
gd_all=[group_difficulty(c[1]) for c in CAND]
gd_lo,gd_hi=min(gd_all),max(gd_all)
def lvl(x,a,b): return "Baja" if x<a else ("Media" if x<b else "Alta")
def lvl_inv(x,a,b): return "Bajo" if x>b else ("Medio" if x>a else "Alto")

cands=[]
for player,team,role,share,pen,starter,avail,form in CAND:
    G=team_goals(team); eg=G*share*pen*starter*avail*form
    cands.append(dict(player=player,team=team,role=role,share=share,pen=pen,
                      starter=starter,avail=avail,form=form,eg=eg,G=G,gd=group_difficulty(team)))

# --- recalibración por temperatura sobre P(Bota) simulada (anti-sobreconfianza) ---
rng=np.random.default_rng(2026); N=300_000; R_DISP=2.8
def nb(mu,size):
    mu=np.asarray(mu,float); lam=rng.gamma(R_DISP,mu/R_DISP,size); return rng.poisson(lam).astype(float)
egs=np.array([c["eg"] for c in cands])
goals=nb(np.broadcast_to(egs,(N,len(cands))),(N,len(cands)))
field=nb(1.85,(N,12)).max(axis=1)
goals+=rng.uniform(0,.01,goals.shape); field+=rng.uniform(0,.01,field.shape)
best=goals.max(axis=1); win=(goals==best[:,None])&(best>=field)[:,None]
ties=win.sum(axis=1); m=ties>=1; raw=np.array([ (win[m,j]/ties[m]).sum() for j in range(len(cands))])/N*100
# temperatura T>1 aplana la parte alta (reduce sobreconfianza del favorito)
T=1.12
tempd=raw**(1/T); tempd=tempd/ tempd.sum()*raw.sum()   # conserva masa de candidatos
for c,p0,p1 in zip(cands,raw,tempd):
    c["prob5"]=round(float(p0),2); c["prob"]=round(float(p1),2)
    c["xg"]=round(c["eg"]*0.97,2)   # leve encogimiento de xG (sobreconfianza)

# riesgos
for c in cands:
    mins=c["starter"]*c["avail"]
    c["r_min"]=lvl_inv(mins,0.72,0.88)
    c["r_dep"]=lvl(c["share"],0.22,0.28)
    c["r_grp"]=lvl(c["gd"],gd_lo+(gd_hi-gd_lo)*0.33,gd_lo+(gd_hi-gd_lo)*0.66)
    c["r_tit"]=lvl(1-c["starter"],0.08,0.18)
    c["min_pct"]=round(mins*100)

cands.sort(key=lambda x:-x["prob"]); top=cands[:10]
for i,c in enumerate(top,1): c["rank"]=i
scorers7=[{ "rank":c["rank"],"player":c["player"],"team":c["team"],"prob":c["prob"],"xg":c["xg"],
           "starter":round(c["starter"]*100),"avail":round(c["avail"]*100),"role":c["role"],
           "r_min":c["r_min"],"r_dep":c["r_dep"],"r_grp":c["r_grp"],"r_tit":c["r_tit"],
           "note":f"Rol {c['role'].lower()}; minutos {c['r_min'].lower()}, dependencia {c['r_dep'].lower()}, "
                  f"dificultad de grupo {c['r_grp'].lower()}, incertidumbre de titularidad {c['r_tit'].lower()}."}
          for c in top]

# =====================================================================
# BLOQUE 4 — INCERTIDUMBRE Y CALIBRACIÓN: diagnósticos
# =====================================================================
def topn(d,n=5): return sorted(d.items(),key=lambda x:-x[1])[:n]
champ5=topn(V5["title"]); champ7=topn(title7)
deltas={t: round(title7[t]-V5["title"][t],2) for t in TEAMS}
high_unc_matches=[m for m in matches7 if m["high_unc"]]
adj_matches=[m for m in matches7 if m["adj"]]

diag={
 "champ_v5_top": champ5, "champ_v7_top": champ7,
 "fav_drop": round(V5["title"][champ5[0][0]]-title7[champ5[0][0]],2),
 "tail_lift": round(sum(title7[t] for t in TEAMS if title7[t]<1)-sum(V5["title"][t] for t in TEAMS if V5["title"][t]<1),2),
 "n_high_unc": len(high_unc_matches), "n_adj": len(adj_matches),
 "scorer_fav_drop": round(max(c["prob5"] for c in cands)-max(c["prob"] for c in cands),2),
 "field_pct": round(100-sum(c["prob"] for c in cands),1),
 "biggest_deltas": sorted(deltas.items(),key=lambda x:-abs(x[1]))[:8],
}

out={"engine":"v7-Recalibracion (capa de calibracion sobre v5/v6)","reach":reach7,"title":title7,
     "matches":matches7,"scorers":scorers7,"diag":diag,
     "params":{"shrink":SHRINK,"beta_draw":BETA_DRAW,"temp_scorers":T,"R_DISP":R_DISP}}
json.dump(out, open(f"{HERE}/results_v7.json","w",encoding="utf-8"), ensure_ascii=False)
json.dump(scorers7, open(f"{HERE}/claude_scorers_v7.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- resumen ----
print("== SELECCIONES (campeón) v5 -> v7 ==")
for (t,_),  in [(x,) for x in champ7[:6]]:
    print(f"  {t:12s} v5 {V5['title'][t]:5.2f}%  ->  v7 {title7[t]:5.2f}%  (Δ {deltas[t]:+.2f})")
print(f"  favorito baja {diag['fav_drop']:+.2f} pp · cola (<1%) sube {diag['tail_lift']:+.2f} pp")
print(f"== PARTIDOS == alta incertidumbre: {diag['n_high_unc']}/72 · marcadores ajustados: {diag['n_adj']}")
print("== GOLEADORES v7 ==")
for c in top:
    print(f"  {c['rank']:2d} {c['player']:18s} {c['prob']:5.2f}% (v6 {c['prob5']:5.2f}) xG {c['xg']:.2f} "
          f"min:{c['r_min']} dep:{c['r_dep']} grp:{c['r_grp']} tit:{c['r_tit']}")
print(f"  favorito goleador baja {diag['scorer_fav_drop']:+.2f} pp · campo {diag['field_pct']}%")
