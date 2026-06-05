# -*- coding: utf-8 -*-
"""
Consolidación FINAL de las 3 IAs en sus versiones definitivas + consenso.
  - Claude  : motor v2 (Dixon-Coles + validación cruzada 2022)        -> results_v2.json
  - ChatGPT : camino al título v4 (player+team, 60k MC) + 72 partidos v5 (climate)
  - Gemini  : camino al título Hybrid AI (Bayes causal + DRL) + 72 partidos v5 (bio-termo)
Consenso: campeón por media + mediana (renorm), rondas por media (las 3 completas),
grupos por puntos esperados homogéneos, 72 partidos por promedio + pluralidad de marcador.
"""
import json, re, statistics, math
from collections import defaultdict, Counter

HERE = "/home/claude/wc2026"; UP = "/mnt/user-data/uploads"

# ---------- canonicalización de nombres ----------
CANON = {
 "Bosnia y Herzegovina":"Bosnia","Bosnia-Herz.":"Bosnia","Bosnia-Herzegovina":"Bosnia","Bosnia":"Bosnia",
 "Turquía":"Türkiye","Türkiye":"Türkiye","Turkiye":"Türkiye",
 "Arabia Saudita":"Arabia Saudí","Arabia S.":"Arabia Saudí","Arabia Saudí":"Arabia Saudí",
 "Irak":"Iraq","Iraq":"Iraq","Corea Sur":"Corea del Sur","Corea del Sur":"Corea del Sur",
 "Costa Marfil":"Costa de Marfil","Costa de Marfil":"Costa de Marfil",
 "N. Zelanda":"Nueva Zelanda","Nueva Zelanda":"Nueva Zelanda",
 "EE.UU.":"Estados Unidos","EEUU":"Estados Unidos","Estados Unidos":"Estados Unidos",
 "RD Congo":"RD Congo","Congo DR":"RD Congo","Cabo Verde":"Cabo Verde","Curazao":"Curazao",
}
def cn(n):
    n = n.strip().replace("**","")
    return CANON.get(n, n)

def num(s):
    s = s.strip().replace("%","").replace("<","").replace("*","").strip()
    try: return float(s)
    except: return 0.0

# ---------- Claude v4 (ENSAMBLE Dixon-Coles v3 + ML, validado OOS 2018/2022) ----------
cl = json.load(open(f"{HERE}/results_v4.json", encoding="utf-8"))
_v1 = json.load(open(f"{HERE}/results.json", encoding="utf-8"))
GROUPS = _v1["groups"]; cl_elo = _v1["elo"]; ALL = [t for g in GROUPS.values() for t in g]
claude_title = cl["title"]; claude_reach = cl["reach"]; claude_group = cl["group_win"]; claude_adv = cl["advance"]
claude_fix2 = {frozenset((f["a"],f["b"])): f for f in cl["fixtures"]}
ROUNDS = ["R32","R16","QF","SF","FINAL","CAMPEON"]

# ---------- parser genérico de tabla "camino al título" ----------
def parse_reach(path):
    txt = open(path, encoding="utf-8").read()
    reach = {}
    for line in txt.splitlines():
        if not line.strip().startswith("|"): continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7: continue
        # detectar columna de ranking inicial (Gemini v6: | rank | Selección | ...)
        first = cells[0].replace("**","").strip()
        if first.isdigit() and len(cells) >= 8:
            name = cn(cells[1]); valcells = cells[2:8]
        else:
            name = cn(cells[0]); valcells = cells[1:7]
        if name not in ALL: continue
        try: vals = [num(c) for c in valcells]
        except: continue
        reach[name] = dict(zip(ROUNDS, vals))
    return reach

# ChatGPT v6 (camino) y Gemini v6 Heritage AI (camino)
cg_reach = parse_reach(f"{UP}/ChatGPT_Camino_al_Titulo_v6_Completo.md")
gm_reach = parse_reach(f"{UP}/Gemini_Predictivo_V6_Heritage_AI_y_Apend.md")
cg_title = {t: cg_reach[t]["CAMPEON"] for t in cg_reach}
gm_title = {t: gm_reach[t]["CAMPEON"] for t in gm_reach}
# rellenar equipos faltantes con 0 (tablas vienen completas, por seguridad)
for t in ALL:
    cg_title.setdefault(t,0.0); gm_title.setdefault(t,0.0)

# ---------- ChatGPT v5: 72 partidos ----------
cg_matches = {}
ctxt = open(f"{UP}/ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6.md", encoding="utf-8").read()
for line in ctxt.splitlines():
    if not line.strip().startswith("|"): continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 9: continue
    if cells[0] in ("M","---") or not cells[0].isdigit(): continue
    a, b = cn(cells[4]), cn(cells[6])
    sc = cells[5].replace(" ","")
    pm = re.match(r"(\d+)-(\d+)-(\d+)", cells[7].replace(" ",""))
    if not pm: continue
    pA,pD,pB = float(pm.group(1)),float(pm.group(2)),float(pm.group(3))
    cg_matches[frozenset((a,b))] = {"a":a,"b":b,"pA":pA,"pD":pD,"pB":pB,"score":sc}

# ---------- Gemini v6: 72 partidos ----------
gm_matches = {}
gtxt = open(f"{UP}/Gemini_Pronostico_72_Partidos_Fase_Grupo_v6.md", encoding="utf-8").read()
for line in gtxt.splitlines():
    if "vs" not in line or "**" not in line or not line.strip().startswith("|"): continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    mvs = re.match(r"\*\*(.+?)\s+vs\s+(.+?)\*\*", cells[0])
    if not mvs or len(cells) < 5: continue
    a, b = cn(mvs.group(1)), cn(mvs.group(2))
    sc = cells[1].replace(" ", "")
    try:
        pA, pD, pB = num(cells[2]), num(cells[3]), num(cells[4])
    except: continue
    if pA == 0 and pD == 0 and pB == 0: continue
    gm_matches[frozenset((a, b))] = {"a":a,"b":b,"pA":pA,"pD":pD,"pB":pB,"score":sc}

# ---------- consenso: campeón ----------
def stat(dC,dG,dCh):
    out={}
    for t in ALL:
        vals=[d.get(t) for d in (dC,dCh,dG) if d.get(t) is not None]
        if vals: out[t]={"vals":vals,"mean":sum(vals)/len(vals),"median":statistics.median(vals),
                         "min":min(vals),"max":max(vals)}
    return out
title_stat = stat(claude_title, gm_title, cg_title)
sm=sum(v["mean"] for v in title_stat.values()); smed=sum(v["median"] for v in title_stat.values())
consensus_title={t:round(100*v["mean"]/sm,3) for t,v in title_stat.items()}
consensus_title_median={t:round(100*v["median"]/smed,3) for t,v in title_stat.items()}

# ---------- consenso: rondas (las 3 completas) ----------
consensus_reach={r:{} for r in ROUNDS}
for r in ROUNDS:
    for t in ALL:
        vals=[]
        if t in claude_reach[r]: vals.append(claude_reach[r][t])
        if t in cg_reach: vals.append(cg_reach[t][r])
        if t in gm_reach: vals.append(gm_reach[t][r])
        if vals: consensus_reach[r][t]=round(sum(vals)/len(vals),2)

# ---------- grupos: puntos esperados homogéneos ----------
def xpoints(matches):
    pts=defaultdict(float)
    for m in matches.values():
        pts[m["a"]]+=3*m["pA"]/100+m["pD"]/100
        pts[m["b"]]+=3*m["pB"]/100+m["pD"]/100
    return pts
claude_simple={k:{"a":v["a"],"b":v["b"],"pA":v["pA"],"pD":v["pD"],"pB":v["pB"]} for k,v in claude_fix2.items()}
xp={"Claude":xpoints(claude_simple),"ChatGPT":xpoints(cg_matches),"Gemini":xpoints(gm_matches)}
group_proj={}
for gl,teams in GROUPS.items():
    row={}
    for mdl in ("Claude","ChatGPT","Gemini"):
        order=sorted(teams,key=lambda t:-xp[mdl].get(t,0))
        row[mdl]=[(t,round(xp[mdl].get(t,0),2)) for t in order]
    cons=sorted(teams,key=lambda t:-sum(xp[m].get(t,0) for m in xp)/3)
    row["Consenso"]=[(t,round(sum(xp[m].get(t,0) for m in xp)/3,2)) for t in cons]
    group_proj[gl]=row

# ---------- 72 partidos: consenso ----------
def oriented(m,a,b):
    if m["a"]==a: return m["pA"],m["pD"],m["pB"],m["score"]
    ga,gb=m["score"].split("-"); return m["pB"],m["pD"],m["pA"],f"{gb}-{ga}"
def _H(p): return -sum(x*math.log(x,2) for x in p if x>0)
def composite_index(vecs):
    """vecs: lista de (pA,pD,pB) normalizadas. Devuelve (pool_log %, idx_acuerdo 0-100, idx_confianza 0-100)."""
    n=len(vecs)
    # pool logarítmico (media geométrica renormalizada) — combinación estándar de pronósticos
    g=[1.0,1.0,1.0]
    for v in vecs:
        for k in range(3): g[k]*=max(v[k],1e-9)
    g=[x**(1.0/n) for x in g]; sg=sum(g); g=[x/sg for x in g]
    # índice de acuerdo: 1 - divergencia Jensen-Shannon normalizada (base log2(3))
    mean=[sum(v[k] for v in vecs)/n for k in range(3)]
    jsd=_H(mean)-sum(_H(v) for v in vecs)/n
    agree=max(0.0,min(1.0,1-jsd/math.log(3,2)))
    # índice compuesto de confianza: fuerza del favorito (reescalada desde 1/3) y acuerdo
    pf=max(g); pf_sc=max(0.0,min(1.0,(pf-1/3)/(2/3)))
    conf=round(100*(0.6*pf_sc+0.4*agree))
    return [round(100*x,1) for x in g], round(100*agree), int(conf)

cons_matches=[]; agree=Counter()
for fx in cl["fixtures"]:
    a,b,gl=fx["a"],fx["b"],fx["group"]; key=frozenset((a,b))
    rows={"Claude":(fx["pA"],fx["pD"],fx["pB"],fx["score"]),
          "ChatGPT":oriented(cg_matches[key],a,b),
          "Gemini":oriented(gm_matches[key],a,b)}
    pA=sum(r[0] for r in rows.values())/3; pD=sum(r[1] for r in rows.values())/3; pB=sum(r[2] for r in rows.values())/3
    s=pA+pD+pB; pA,pD,pB=100*pA/s,100*pD/s,100*pB/s
    # resultado de consenso (0=gana local A, 1=empate, 2=gana visitante B)
    cons_oc = 0 if (pA>=pD and pA>=pB) else (2 if (pB>=pD and pB>=pA) else 1)
    # marcadores modales de cada IA, con su resultado y goles
    msc=[]
    for m in rows:
        hg,ag = map(int, rows[m][3].split("-"))
        oc = 0 if hg>ag else (2 if ag>hg else 1)
        msc.append((rows[m][3], oc, hg, ag))
    cnt_all = Counter(x[0] for x in msc); maj = cnt_all.most_common(1)[0]
    if maj[1] >= 2:
        # 2+ IAs coinciden en el marcador -> ese es el consenso honesto (aunque sea 1-1 en
        # un partido parejo donde el favorito marginal sea otro: es el fenómeno Poisson real)
        modal = maj[0]
    else:
        # las 3 difieren: elegir el marcador coherente con el favorito del consenso (1X2)
        cand = [x for x in msc if x[1]==cons_oc] or msc
        modal = min(cand, key=lambda x:(x[2]+x[3], x[2]))[0]
    def fav(r): return 0 if r[0]>=r[1] and r[0]>=r[2] else (2 if r[2]>=r[1] else 1)
    a_=Counter([fav(rows[m]) for m in rows]).most_common(1)[0][1]; agree[a_]+=1
    # índice compuesto: combina las probabilidades de las 3 IAs (pool log + acuerdo + confianza)
    nv=[]
    for m in rows:
        v=rows[m][:3]; sv=sum(v) or 1.0; nv.append((v[0]/sv,v[1]/sv,v[2]/sv))
    p_log, agree_idx, conf_idx = composite_index(nv)
    cons_matches.append({"group":gl,"a":a,"b":b,"pA":round(pA,1),"pD":round(pD,1),"pB":round(pB,1),
        "score":modal,"agree":a_,"p_log":p_log,"agree_idx":agree_idx,"conf_idx":conf_idx,
        "xg":{"Claude":[fx["eg_a"],fx["eg_b"]]},
        "by":{m:{"pA":round(rows[m][0],1),"pD":round(rows[m][1],1),"pB":round(rows[m][2],1),"score":rows[m][3]} for m in rows}})

def to_round_keyed(team_keyed):
    out = {r: {} for r in ROUNDS}
    for t, dd in team_keyed.items():
        for r in ROUNDS:
            if r in dd: out[r][t] = dd[r]
    return out

# ---------- metodología completa de cada IA (para paneles desplegables) ----------
METH = {
 "claude": {
   "version":"v4","mc":"60.000 corridas",
   "title":"Ensamble: Dixon-Coles (datos) + Machine Learning (gradient boosting Poisson), validado OOS",
   "html":"""
<p><b>Qué es el v4.</b> Un <b>ensamble</b> que promedia dos motores y supera a cada uno por separado fuera de muestra:
λ = ½·(Dixon-Coles data-driven) + ½·(Machine Learning). El componente ML es un <b>gradient boosting con pérdida de
Poisson</b> (sklearn) entrenado sobre miles de partidos internacionales reales.</p>
<p><b>Factores integrados en el ML</b> (los que pediste, donde son fiables):</p>
<pre>• Estado/ranking actual  → World Football Elo a jun-2026, recalculado
                            de resultados reales (más actual que el ranking
                            FIFA, que se congela entre ventanas)
• Forma reciente         → goles a favor/en contra, últimos 10 partidos
• Histórico de Mundiales → partidos jugados y % de victoria en Copas
• Localía / sede neutral</pre>
<p><b>Por qué ensamble y no "solo deep learning".</b> Lo probé de forma honesta. En la validación OOS, el ML solo dio
RPS 0.2138 (mejora 12.7%) — <b>ligeramente peor</b> que el Dixon-Coles solo (0.2127, 13.1%). El deep learning puro
sobreajusta con datos escasos por selección. El <b>ensamble</b> de ambos da <b>RPS 0.2122 (mejora 13.3%)</b>, mejor que
cualquiera por separado: por eso es el modelo v4.</p>
<p><b>Validación FUERA DE MUESTRA</b> (reajuste solo con datos previos a cada Mundial, predicción de sus 48 partidos
reales): es la única de las cuatro IAs con desempeño medido contra Mundiales reales.</p>
<p class="methlim"><b>Honestidad sobre ranking y nóminas:</b> el ranking FIFA oficial se publica en una página renderizada por
JavaScript y no es extraíble de forma fiable; se usó el Elo calculado (mejor predictor y más actual). Las <b>nóminas</b> se
reflejan vía la <b>forma reciente</b> como aproximación; un verdadero modelo jugador-por-jugador exigiría valores de plantilla
(p. ej. Transfermarkt) que no tengo auditados — no los invento (ChatGPT también usó las convocatorias como señal agregada).</p>""",
   "title_en":"Ensemble: Dixon-Coles (data) + Machine Learning (gradient boosting Poisson), OOS-validated",
   "html_en":"""
<p><b>What v4 is.</b> An <b>ensemble</b> that averages two engines and beats each one separately out of sample:
λ = ½·(data-driven Dixon-Coles) + ½·(Machine Learning). The ML component is a <b>gradient boosting model with Poisson
loss</b> (sklearn) trained on thousands of real international matches.</p>
<p><b>Factors integrated in the ML</b> (the ones you asked for, where reliable):</p>
<pre>• Current state/ranking → World Football Elo as of Jun-2026, recomputed
                          from real results (more current than the FIFA
                          ranking, which freezes between windows)
• Recent form          → goals for/against, last 10 matches
• World Cup history     → matches played and win % at World Cups
• Home / neutral venue</pre>
<p><b>Why an ensemble and not "deep learning alone".</b> I tested it honestly. In OOS validation, ML alone scored
RPS 0.2138 (12.7% gain) — <b>slightly worse</b> than Dixon-Coles alone (0.2127, 13.1%). Pure deep learning overfits
with scarce data per team. The <b>ensemble</b> of the two yields <b>RPS 0.2122 (13.3% gain)</b>, better than either
alone: hence the v4 model.</p>
<p><b>OUT-OF-SAMPLE validation</b> (refit using only pre-tournament data for each World Cup, predicting its 48 real
matches): it is the only one of the four AIs with performance measured against real World Cups.</p>
<p class="methlim"><b>Honesty about ranking and squads:</b> the official FIFA ranking is published on a JavaScript-rendered
page and cannot be scraped reliably; the computed Elo was used (a better and more current predictor). <b>Squads</b> are
reflected via <b>recent form</b> as a proxy; a true player-by-player model would require audited squad values (e.g.
Transfermarkt) that I do not have — I will not invent them (ChatGPT also used call-ups only as an aggregate signal).</p>"""},
 "chatgpt": {
   "version":"v6","mc":"60.000–80.000 corridas",
   "title":"Ensamble calibrado histórico + team-level + player-level + climate-aware",
   "html":"""
<p><b>Qué es.</b> Evolución del v5 que añade una capa de <b>calibración histórica</b> para reducir la sobreconfianza
de los favoritos, penalizar rutas de cuadro difíciles y redistribuir probabilidad hacia outsiders plausibles.</p>
<p><b>Fórmula de fuerza (Strength v6).</b></p>
<pre>0.17 FIFA-Elo + 0.15 WorldFootballElo + 0.14 SquadMarketTalent
+ 0.12 PlayerLevel + 0.10 RecentForm + 0.09 AttackDefense
+ 0.08 ClimateAltitude + 0.07 HostTravelRest
+ 0.05 TournamentExperience + 0.03 UpsetRobustness</pre>
<p><b>Probabilidad por fase.</b> Primero una probabilidad cruda por Monte Carlo (fuerza, sorteo, ruta, clima, riesgo de
plantel, matriz de terceros, varianza de eliminación); luego calibración histórica:</p>
<pre>p_fase = normalize_por_fase( sigmoid(
   α + β·logit(p_cruda) + γ·VolatilidadHistórica
   + δ·DificultadRuta − η·PenalizaciónSobreconfianza ) )</pre>
<p>con la restricción de masa Σ por fase = 32 / 16 / 8 / 4 / 2 / 1 equipos.</p>
<p><b>Novedades v6.</b> Shrinkage de favoritos, calibración por fase, penalización de ruta, volatilidad histórica de
Mundiales recientes, regularización del título (ningún equipo supera un umbral irreal), mejor masa para outsiders y
control de baja muestra. Los 72 partidos incorporan ajuste climático explícito por sede.</p>""",
   "title_en":"Historically-calibrated + team-level + player-level + climate-aware ensemble",
   "html_en":"""
<p><b>What it is.</b> An evolution of v5 that adds a <b>historical-calibration</b> layer to reduce favorites'
overconfidence, penalize hard bracket routes and redistribute probability toward plausible outsiders.</p>
<p><b>Strength formula (Strength v6).</b></p>
<pre>0.17 FIFA-Elo + 0.15 WorldFootballElo + 0.14 SquadMarketTalent
+ 0.12 PlayerLevel + 0.10 RecentForm + 0.09 AttackDefense
+ 0.08 ClimateAltitude + 0.07 HostTravelRest
+ 0.05 TournamentExperience + 0.03 UpsetRobustness</pre>
<p><b>Per-stage probability.</b> First a raw Monte Carlo probability (strength, draw, route, climate, squad risk,
third-place matrix, knockout variance); then historical calibration:</p>
<pre>p_stage = normalize_per_stage( sigmoid(
   α + β·logit(p_raw) + γ·HistoricalVolatility
   + δ·RouteDifficulty − η·OverconfidencePenalty ) )</pre>
<p>with the mass constraint Σ per stage = 32 / 16 / 8 / 4 / 2 / 1 teams.</p>
<p><b>What is new in v6.</b> Favorite shrinkage, per-stage calibration, route penalty, historical volatility from recent
World Cups, title regularization (no team exceeds an unrealistic threshold), better mass for outsiders and low-sample
control. The 72 matches incorporate an explicit per-venue climate adjustment.</p>"""},
 "gemini": {
   "version":"v6 · Heritage AI","mc":"Ensamble híbrido",
   "title":"Redes Bayesianas + Termodinámica + Motor DRL + 3 capas psico-históricas",
   "html":"""
<p><b>Qué es.</b> Ensamble híbrido que fusiona telemetría biomecánica, análisis estocástico, termodinámica del entorno
y <b>memoria institucional histórica</b> (Heritage AI). Tres capas psico-históricas: <b>Prior Bayesiano de Pedigrí
Mundialista</b>, <b>Índice de Elasticidad Cognitiva bajo presión</b> y <b>Efecto de Gravedad Táctica</b>.</p>
<p><b>Ecuaciones (apéndice técnico).</b></p>
<pre>xG_base = λ₀ · exp( β₁·ΔElo − β₂·Lesiones + β₃·ValorPlantilla )
xG_thermo = xG_base · e^(−κ·(UTCI − 28)) · [1 − α·max(0, altitud − 1500)]
xG_V6 = xG_thermo · (1 + γ_heritage) · σ_clutch
P(x,y) = Poisson(xG_V6_A) · Poisson(xG_V6_B)</pre>
<p>λ₀ ≈ 1.35 (tasa media de gol mundialista); UTCI = índice de estrés térmico; γ_heritage = multiplicador de resiliencia
histórica (positivo para potencias consolidadas); σ_clutch = conversión bajo presión extrema.</p>
<p><b>Efecto en v6.</b> El prior histórico eleva a potencias tradicionales: Argentina y Francia encabezan y <b>Brasil
sube al podio (14%)</b> por su pedigrí. La propia Gemini advierte el riesgo de "regresión al romanticismo" — incorporar
historia puede infravalorar a emergentes altamente tecnificados.</p>
<p class="methlim"><b>Autocrítica del modelo:</b> la "Elasticidad Cognitiva" se calibra con muestras minúsculas
(tandas de penales de selección), un tamaño de efecto estadísticamente débil.</p>""",
   "title_en":"Bayesian Networks + Thermodynamics + DRL engine + 3 psycho-historical layers",
   "html_en":"""
<p><b>What it is.</b> A hybrid ensemble fusing biomechanical telemetry, stochastic analysis, environmental thermodynamics
and <b>historical institutional memory</b> (Heritage AI). Three psycho-historical layers: a <b>Bayesian World Cup
Pedigree Prior</b>, a <b>Cognitive Elasticity Index under pressure</b> and a <b>Tactical Gravity Effect</b>.</p>
<p><b>Equations (technical appendix).</b></p>
<pre>xG_base = λ₀ · exp( β₁·ΔElo − β₂·Injuries + β₃·SquadValue )
xG_thermo = xG_base · e^(−κ·(UTCI − 28)) · [1 − α·max(0, altitude − 1500)]
xG_V6 = xG_thermo · (1 + γ_heritage) · σ_clutch
P(x,y) = Poisson(xG_V6_A) · Poisson(xG_V6_B)</pre>
<p>λ₀ ≈ 1.35 (average World Cup scoring rate); UTCI = thermal-stress index; γ_heritage = historical-resilience
multiplier (positive for established powers); σ_clutch = conversion under extreme pressure.</p>
<p><b>Effect in v6.</b> The historical prior lifts traditional powers: Argentina and France lead and <b>Brazil rises to
the podium (14%)</b> for its pedigree. Gemini itself warns of the risk of "regression to romanticism" — encoding history
can undervalue highly technical emerging sides.</p>
<p class="methlim"><b>Model self-critique:</b> "Cognitive Elasticity" is calibrated on tiny samples (national-team
penalty shootouts), a statistically weak effect size.</p>"""},
}

DATA={"groups":GROUPS,"elo":cl_elo,"meth":METH,
 "claude":{"title":claude_title,"reach":claude_reach,"group_win":claude_group,"advance":claude_adv,
           "fixtures":cl["fixtures"],"params":cl["params"],"N":cl["N"],"version":"v4"},
 "chatgpt":{"title":cg_title,"reach":to_round_keyed(cg_reach),"version":"v6",
            "matches":[{k:m[k] for k in("a","b","pA","pD","pB","score")} for m in cg_matches.values()]},
 "gemini":{"title":gm_title,"reach":to_round_keyed(gm_reach),"version":"v6 · Heritage AI",
           "matches":[{k:m[k] for k in("a","b","pA","pD","pB","score")} for m in gm_matches.values()]},
 "consensus":{"title":consensus_title,"title_median":consensus_title_median,
              "title_stat":{t:{k:round(v[k],2) for k in("mean","median","min","max")} for t,v in title_stat.items()},
              "reach":consensus_reach,"matches":cons_matches,"agree_counter":dict(agree)},
 "group_proj":group_proj}
json.dump(DATA, open(f"{HERE}/consolidated.json","w",encoding="utf-8"), ensure_ascii=False)

# diagnóstico
print("Partidos -> ChatGPT v6:%d  Gemini v6:%d  (alineados con Claude: %d / %d)"%(
    len(cg_matches),len(gm_matches),len(set(claude_fix2)&set(cg_matches)&set(gm_matches)),72))
print("Reach completo -> ChatGPT:%d  Gemini:%d  Claude:48"%(len(cg_reach),len(gm_reach)))
print("\n=== CAMPEÓN (top 12 por mediana de consenso) ===")
print(f"{'Selección':16s}{'Claude':>8s}{'ChatGPT':>8s}{'Gemini':>8s}{'CONS.med':>9s}{'CONS.media':>11s}{'rango':>12s}")
for t,_ in sorted(consensus_title_median.items(),key=lambda x:-x[1])[:12]:
    s=title_stat[t]
    print(f"{t:16s}{claude_title.get(t,0):7.1f}%{cg_title.get(t,0):7.1f}%{gm_title.get(t,0):7.1f}%"
          f"{consensus_title_median[t]:8.1f}%{consensus_title[t]:10.1f}%   {s['min']:.1f}-{s['max']:.1f}")
print("\nAcuerdo por partido (3=unánime,2=mayoría):", dict(agree))
print("Guardado consolidated.json")
