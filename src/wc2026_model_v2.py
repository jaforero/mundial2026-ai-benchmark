# -*- coding: utf-8 -*-
"""
=============================================================================
 MOTOR DE GOLES v2 — Dixon-Coles multiplicativo (ataque/defensa por equipo)
=============================================================================
 Mejora respecto a v1 (supremacía lineal + total fijo):
   - Forma log-lineal canónica:  log λ = base + ataque_i − defensa_rival + localía
   - El TOTAL de goles ya depende del enfrentamiento (dos ofensivos => más goles)
   - Asimetría ataque/defensa por equipo (tilt) donde hay subíndices Elo públicos
   - Corrección Dixon-Coles (rho) para marcadores bajos
   - Salida por partido: matriz completa -> top marcadores, O/U 2.5, BTTS,
     portería a cero, goles esperados, puntos esperados, confianza (entropía)
 Calibrado para reproducir el benchmark Opta y un promedio de goles de Mundial.
=============================================================================
"""
import json, math
import numpy as np
from collections import defaultdict
from scipy.stats import poisson

# Reutilizamos la tabla de fuerza, grupos y anfitriones de v1 (sin re-ejecutar su main)
from wc2026_model import elo, ELO, GROUPS, HOSTS, ALL_TEAMS, ROUNDS

rng = np.random.default_rng(20260604)

# -----------------------------------------------------------------------------
# Parámetros del motor (calibrados abajo)
# -----------------------------------------------------------------------------
mu_elo = float(np.mean([elo[t] for t in ALL_TEAMS]))   # Elo medio del torneo
# --- Parámetros CALIBRADOS POR VALIDACIÓN CRUZADA contra el Mundial 2022 ---
# El backtest OOS prefirió KAPPA≈0.44-0.56 (media 6-fold 0.49) frente al 0.58
# que sugería ajustar solo a Opta: 2022 indica suavizar la ventaja del favorito.
KAPPA   = 0.50     # fuerza (Elo) -> ventaja de gol (log) — media de validación cruzada
LOG_BASE = math.log(1.29)   # nivel de goles base, fijado para promedio ~2.69 (norma Mundial 2018/2022)
HOME_LOG = 0.20    # ventaja de localía (solo anfitriones)
DC_RHO   = -0.04   # dependencia Dixon-Coles (backtest 2022: cercano a 0)
GOAL_DAMP = 0.90   # amortiguación de la supremacía en goleadas

# Subíndices ataque−defensa (international-football.net, citados en los docs fuente).
# tilt>0 = identidad ofensiva ; tilt<0 = identidad defensiva. Solo donde hay dato.
TILT = {"España": +0.14, "Argentina": -0.02, "México": -0.23, "Suiza": +0.02}

# -----------------------------------------------------------------------------
# Capa de FORMA RECIENTE (amistosos de preparación mayo–junio 2026)
# Fuente: resultados citados en los documentos y en la prensa de preparación.
# El Elo de junio-2026 YA integra resultados hasta principios de junio, por lo que
# esta capa se mantiene DELIBERADAMENTE PEQUEÑA (±0.08 log máx.) para no duplicar
# señal; aporta el matiz de la dinámica más reciente donde hay dato fiable.
# Valor = diferencia de gol media de los últimos amistosos (acotada).
RECENT = {  # equipo: dif. de gol reciente representativa
    "México": +4, "Corea del Sur": +5, "Estados Unidos": +1, "Australia": +3,
    "Canadá": +2, "Brasil": +4, "Alemania": +4, "España": +2, "Uruguay": +1,
    "Francia": +2, "Senegal": -1, "Argentina": +1, "Japón": +1, "Curazao": -5,
    "Uzbekistán": -1,
}
FORM_W = 0.018   # peso por gol de diferencia reciente (acotado a ±0.08 abajo)

def form_adj(team):
    """Ajuste de forma en log-goles, pequeño y acotado, 0 si no hay dato fiable."""
    d = RECENT.get(team, 0)
    return max(-0.08, min(0.08, FORM_W * d))

def strength(team):
    """Fuerza estandarizada en 'unidades log' a partir del Elo."""
    return KAPPA * (elo[team] - mu_elo) / 400.0

def off_def(team):
    """Rating ofensivo y defensivo del equipo (log-goles, centrados en 0)."""
    s = strength(team); t = TILT.get(team, 0.0)
    off = s + 0.5 * t          # ofensivos marcan algo más
    dfn = s - 0.5 * t          # ofensivos defienden algo menos (dfn alto = mejor defensa)
    return off, dfn

def lambdas(a, b, home_a=False, home_b=False):
    """Tasas de gol esperadas (λ) con la forma Dixon-Coles multiplicativa,
    incluyendo localía y un pequeño término de forma reciente."""
    oa, da = off_def(a); ob, db = off_def(b)
    # supremacía amortiguada en extremos (rendimientos decrecientes)
    sup_a = GOAL_DAMP * (oa - db); sup_b = GOAL_DAMP * (ob - da)
    la = math.exp(LOG_BASE + sup_a + form_adj(a) + (HOME_LOG if home_a else 0.0))
    lb = math.exp(LOG_BASE + sup_b + form_adj(b) + (HOME_LOG if home_b else 0.0))
    return la, lb

# -----------------------------------------------------------------------------
# Matriz de marcadores con corrección Dixon-Coles
# -----------------------------------------------------------------------------
def score_matrix(la, lb, kmax=8):
    pa = poisson.pmf(np.arange(kmax + 1), la)
    pb = poisson.pmf(np.arange(kmax + 1), lb)
    M = np.outer(pa, pb)
    tau = {(0,0):1 - la*lb*DC_RHO, (0,1):1 + la*DC_RHO,
           (1,0):1 + lb*DC_RHO,   (1,1):1 - DC_RHO}
    for (i,j),t in tau.items():
        M[i,j] *= t
    M /= M.sum()
    return M

def match_detail(a, b, home_a=False, home_b=False, top=5):
    """Distribución completa del partido -> diccionario rico de métricas."""
    la, lb = lambdas(a, b, home_a, home_b)
    M = score_matrix(la, lb)
    n = M.shape[0]
    pA = float(np.tril(M, -1).sum())   # A marca más
    pB = float(np.triu(M, 1).sum())    # B marca más
    pD = float(np.trace(M))
    # top marcadores exactos
    flat = [((i, j), float(M[i, j])) for i in range(n) for j in range(n)]
    flat.sort(key=lambda x: -x[1])
    top_scores = [(f"{i}-{j}", round(100*p, 1)) for (i, j), p in flat[:top]]
    # mercados derivados
    idx = np.arange(n)
    over25 = float(sum(M[i, j] for i in range(n) for j in range(n) if i + j >= 3))
    btts   = float(sum(M[i, j] for i in range(1, n) for j in range(1, n)))
    cs_a   = float(M[:, 0].sum())      # B no marca -> A portería a cero
    cs_b   = float(M[0, :].sum())      # A no marca -> B portería a cero
    eg_a   = float((idx[:, None] * M).sum())
    eg_b   = float((idx[None, :] * M).sum())
    # confianza = 1 - entropía normalizada del triple (pA,pD,pB)
    probs = np.array([pA, pD, pB]); probs = probs / probs.sum()
    H = -np.sum([p*math.log(p) for p in probs if p > 0]) / math.log(3)
    conf = round(100 * (1 - H), 0)
    return {
        "a": a, "b": b, "la": round(la, 2), "lb": round(lb, 2),
        "pA": round(100*pA, 1), "pD": round(100*pD, 1), "pB": round(100*pB, 1),
        "score": top_scores[0][0], "p_score": top_scores[0][1],
        "top_scores": top_scores,
        "over25": round(100*over25, 1), "under25": round(100*(1-over25), 1),
        "btts": round(100*btts, 1),
        "cs_a": round(100*cs_a, 1), "cs_b": round(100*cs_b, 1),
        "eg_a": round(eg_a, 2), "eg_b": round(eg_b, 2),
        "xpts_a": round(3*pA + pD, 2), "xpts_b": round(3*pB + pD, 2),
        "conf": conf,
    }

# -----------------------------------------------------------------------------
# Simulación (muestreo) reutilizando estructura de v1 con el nuevo motor
# -----------------------------------------------------------------------------
def sim_goals(a, b, ha=False, hb=False):
    la, lb = lambdas(a, b, ha, hb)
    return rng.poisson(la), rng.poisson(lb)

def sim_knockout(a, b, ha=False, hb=False):
    """Eliminatoria modelada con λ: 90' Poisson -> prórroga Poisson(λ·30/90)
    -> penales (logística sobre Elo, cercana a 50/50)."""
    ga, gb = sim_goals(a, b, ha, hb)
    if ga != gb: return a if ga > gb else b
    # Prórroga: dos tiempos de 15' = 30' efectivos -> escala 30/90 sobre λ
    la, lb = lambdas(a, b, ha, hb)
    et = 30.0/90.0
    ga2, gb2 = rng.poisson(la*et), rng.poisson(lb*et)
    if ga2 != gb2: return a if ga2 > gb2 else b
    # Penales: leve ventaja al de mayor Elo (penales son casi aleatorios)
    diff = elo[a] - elo[b] + (40 if ha else 0) - (40 if hb else 0)
    pa = min(0.60, max(0.40, 0.5 + 0.00025*diff))
    return a if rng.random() < pa else b

def sim_group(teams):
    pts={t:0 for t in teams}; gf={t:0 for t in teams}; ga={t:0 for t in teams}
    h2h=defaultdict(lambda:[0,0,0])
    for i in range(4):
        for j in range(i+1,4):
            a,b=teams[i],teams[j]; ha=a in HOSTS; hb=b in HOSTS
            x,y=sim_goals(a,b,ha,hb)
            gf[a]+=x;ga[a]+=y;gf[b]+=y;ga[b]+=x
            if x>y: pts[a]+=3;h2h[a][0]+=3
            elif x<y: pts[b]+=3;h2h[b][0]+=3
            else: pts[a]+=1;pts[b]+=1;h2h[a][0]+=1;h2h[b][0]+=1
    ranked=sorted(teams,key=lambda t:(pts[t],gf[t]-ga[t],gf[t],h2h[t][0],rng.random()),reverse=True)
    rec={t:(pts[t],gf[t]-ga[t],gf[t]) for t in teams}
    return ranked, rec

THIRD_CLUSTERS={"A":list("CEFHI"),"B":list("EFGIJ"),"C":list("ABFGH"),"D":list("BEFIJ"),
    "E":list("ABDGH"),"G":list("AEHIJ"),"I":list("CDFGH"),"K":list("DEIJL"),"L":list("EHIJK")}
WINNER_VS_RUNNER={"F":"B","H":"D","J":"H"}
RUNNER_VS_RUNNER=[("E","I"),("A","C"),("G","K"),("L","F")]

def build_r32(winners,runners,thirds_by_group):
    matches=[];used=set();qual=set(thirds_by_group)
    for gw in ["A","B","C","D","E","G","I","K","L"]:
        cl=[g for g in THIRD_CLUSTERS[gw] if g in qual and g not in used]
        pick=cl[0] if cl else next((g for g in qual if g not in used and g!=gw),None)
        if pick: used.add(pick); matches.append((winners[gw],thirds_by_group[pick]))
        else: matches.append((winners[gw],runners[gw]))
    for gw,gr in WINNER_VS_RUNNER.items(): matches.append((winners[gw],runners[gr]))
    for g1,g2 in RUNNER_VS_RUNNER: matches.append((runners[g1],runners[g2]))
    return matches

def sim_tournament(track):
    winners={};runners={};third_rows=[]
    for gl,teams in GROUPS.items():
        ranked,rec=sim_group(teams)
        winners[gl]=ranked[0];runners[gl]=ranked[1]
        for pos,t in enumerate(ranked): track["pos"][t][pos]+=1
        track["group_win"][ranked[0]]+=1
        track["advance"][ranked[0]]+=1;track["advance"][ranked[1]]+=1
        third_rows.append((gl,ranked[2],rec[ranked[2]]))
    scored=sorted(third_rows,key=lambda r:(r[2][0],r[2][1],r[2][2],rng.random()),reverse=True)[:8]
    thirds_by_group={gl:t for gl,t,_ in scored}
    for gl,t,_ in scored: track["advance"][t]+=1; track["third_adv"][t]+=1
    bracket=build_r32(winners,runners,thirds_by_group)
    alive=[]
    for a,b in bracket:
        track["reach"]["R32"][a]+=1;track["reach"]["R32"][b]+=1
        alive.append(sim_knockout(a,b,a in HOSTS,b in HOSTS))
    for rnd in ["R16","QF","SF","FINAL"]:
        for t in alive: track["reach"][rnd][t]+=1
        alive=[sim_knockout(alive[k],alive[k+1],alive[k] in HOSTS,alive[k+1] in HOSTS)
               for k in range(0,len(alive),2)]
    track["reach"]["CAMPEON"][alive[0]]+=1

def run(n=40000):
    track={"group_win":defaultdict(int),"advance":defaultdict(int),"third_adv":defaultdict(int),
           "pos":defaultdict(lambda:[0,0,0,0]),"reach":{r:defaultdict(int) for r in ROUNDS}}
    for _ in range(n): sim_tournament(track)
    return track,n

if __name__ == "__main__":
    # 1) Validación del motor de goles a nivel partido (sin simular torneo)
    tot=[];draws=0;ng=0
    detail={}
    for gl,teams in GROUPS.items():
        for i in range(4):
            for j in range(i+1,4):
                a,b=teams[i],teams[j]
                d=match_detail(a,b,a in HOSTS,b in HOSTS)
                d["group"]=gl; detail[f"{a}|{b}"]=d
                tot.append(d["la"]+d["lb"]); draws+=d["pD"]; ng+=1
    print(f"Partidos: {ng} | goles esperados/juego (media λA+λB): {np.mean(tot):.3f}")
    print(f"Tasa de empate media: {draws/ng:.1f}% | rango goles esperados: {min(tot):.2f}–{max(tot):.2f}")

    # 2) Validación del torneo vs Opta
    track,N=run(40000)
    champ=sorted(track["reach"]["CAMPEON"].items(),key=lambda x:-x[1])
    print(f"\n=== TÍTULO (v2, N={N}) ===")
    for t,c in champ[:10]:
        print(f"{t:16s}{100*c/N:6.2f}%   (Claude v1 / Opta refs)")
    print(f"\nEspaña QF {100*track['reach']['QF']['España']/N:.1f}% (Opta 52.1) "
          f"SF {100*track['reach']['SF']['España']/N:.1f}% (39.0) "
          f"Final {100*track['reach']['FINAL']['España']/N:.1f}% (25.6)")

    # ---- 3) EXPORTAR resultados enriquecidos (para la página comparativa) ----
    def pct(d,t): return round(100.0*d.get(t,0)/N, 4)
    out = {"N":N, "engine":"v2-DixonColes-xval2022",
           "params":{"KAPPA":KAPPA,"LOG_BASE_goals":round(math.exp(LOG_BASE),3),
                     "HOME_LOG":HOME_LOG,"DC_RHO":DC_RHO},
           "title":{},"group_win":{},"advance":{},"third_adv":{},"pos":{},
           "reach":{r:{} for r in ROUNDS}, "fixtures":[]}
    for t in ALL_TEAMS:
        out["title"][t]=pct(track["reach"]["CAMPEON"],t)
        out["group_win"][t]=pct(track["group_win"],t)
        out["advance"][t]=pct(track["advance"],t)
        out["third_adv"][t]=pct(track["third_adv"],t)
        out["pos"][t]=[round(100*x/N,3) for x in track["pos"][t]]
        for r in ROUNDS: out["reach"][r][t]=pct(track["reach"][r],t)
    # 72 partidos con TODA la riqueza distribucional
    for gl,teams in GROUPS.items():
        for i in range(4):
            for j in range(i+1,4):
                a,b=teams[i],teams[j]
                d=match_detail(a,b,a in HOSTS,b in HOSTS); d["group"]=gl
                out["fixtures"].append(d)
    json.dump(out, open("/home/claude/wc2026/results_v2.json","w",encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("\nGuardado results_v2.json (motor v2 enriquecido)")
