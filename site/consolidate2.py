# -*- coding: utf-8 -*-
"""
Consolidación FINAL de las 3 IAs en sus versiones definitivas + consenso.
  - Claude  : motor v2 (Dixon-Coles + validación cruzada 2022)        -> results_v2.json
  - ChatGPT : camino al título v4 (player+team, 60k MC) + 72 partidos v5 (climate)
  - Gemini  : camino al título Hybrid AI (Bayes causal + DRL) + 72 partidos v5 (bio-termo)
Consenso: campeón por media + mediana (renorm), rondas por media (las 3 completas),
grupos por puntos esperados homogéneos, 72 partidos por promedio + pluralidad de marcador.
"""
import json, re, statistics, math, csv
from collections import defaultdict, Counter

HERE = "/home/claude/wc2026"; UP = "/mnt/user-data/uploads"; CG = f"{HERE}/src_fase7"

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
cl = json.load(open(f"{HERE}/results_v5.json", encoding="utf-8"))
_v1 = json.load(open(f"{HERE}/results.json", encoding="utf-8"))
GROUPS = _v1["groups"]; cl_elo = _v1["elo"]; ALL = [t for g in GROUPS.values() for t in g]
claude_title = cl["title"]; claude_reach = cl["reach"]; claude_group = cl["group_win"]; claude_adv = cl["advance"]
claude_fix2 = {frozenset((f["a"],f["b"])): f for f in cl["fixtures"]}
# --- FASE 7: capa de recalibración v7 (sobre v5/v6). Sobrescribe campeón/reach y
#     los marcadores/probabilidades de partido (manteniendo xG y grupo de v5). ---
try:
    V7 = json.load(open(f"{HERE}/results_v7.json", encoding="utf-8"))
    claude_title = V7["title"]; claude_reach = V7["reach"]
    _m7 = {frozenset((m["a"],m["b"])): m for m in V7["matches"]}
    for key, f in claude_fix2.items():
        m = _m7.get(key)
        if m:
            f["pA"], f["pD"], f["pB"], f["score"] = m["pA"], m["pD"], m["pB"], m["score"]
            f["high_unc"] = m["high_unc"]; f["unc"] = m["unc"]
    CLAUDE_VERSION = "v7"
except FileNotFoundError:
    CLAUDE_VERSION = "v5"
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

# ChatGPT v8.5 (CSV: 8.4A-TM selecciones + 8.4B-Consensus probabilidades) y Gemini v10
CG85 = "/home/claude/wc2026/cg85"   # CSVs extraídos del paquete v8.5

# --- Ranking 48 (v8.4A-TM) ---
cg_reach = {}
with open(f"{CG85}/ChatGPT_v8_5_Ranking_48_Selecciones.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        t = cn(row["Selección"])
        if t in ALL:
            cg_reach[t] = {r: round(float(row[c]),4) for r,c in
                [("R32","R32"),("R16","Octavos"),("QF","Cuartos"),("SF","Semis"),("FINAL","Final"),("CAMPEON","Campeón")]}

gm_reach = parse_reach(f"{UP}/Gemini_Pronostico_Completo_v10.md")
cg_title = {t: cg_reach[t]["CAMPEON"] for t in cg_reach}
gm_title = {t: gm_reach[t]["CAMPEON"] for t in gm_reach}
for t in ALL:
    cg_title.setdefault(t,0.0); gm_title.setdefault(t,0.0)

# --- 72 partidos v8.5 (probabilidades 8.4B-Consensus = Odds API + SofaScore + modelo) ---
cg_matches = {}
with open(f"{CG85}/ChatGPT_v8_5_72_Partidos.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        a, b = cn(row["Equipo A"]), cn(row["Equipo B"])
        sc = (row.get("Marcador 8.4B-Consensus") or row.get("Marcador 8.4A-TM","")).replace(" ","")
        prob = row.get("Prob. A-E-B 8.4B-Consensus") or row.get("Prob. A-E-B 8.3B-Odds","")
        pm = re.match(r"(\d+)-(\d+)-(\d+)", prob.replace(" ",""))
        if not pm: continue
        cg_matches[frozenset((a,b))] = {"a":a,"b":b,"pA":float(pm.group(1)),"pD":float(pm.group(2)),"pB":float(pm.group(3)),"score":sc}

# ---------- Gemini v8: 72 partidos ----------
gm_matches = {}
gtxt = open(f"{UP}/Gemini_Pronostico_Completo_v10.md", encoding="utf-8").read()
for line in gtxt.splitlines():
    if "vs" not in line or "**" not in line or not line.strip().startswith("|"): continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    mvs = re.match(r"\*\*(.+?)\s+vs\s+(.+?)\*\*", cells[0])
    if not mvs or len(cells) < 5: continue
    a, b = cn(mvs.group(1)), cn(mvs.group(2))
    sc = cells[1].replace(" ", "")
    try: pA, pD, pB = num(cells[2]), num(cells[3]), num(cells[4])
    except: continue
    if pA == 0 and pD == 0 and pB == 0: continue
    gm_matches[frozenset((a, b))] = {"a":a,"b":b,"pA":pA,"pD":pD,"pB":pB,"score":sc}

# ---------- Top 10 goleadores (Bota de Oro) ----------
def _clean_note(s): return s.replace('"',"'").replace("**","").strip()
# ChatGPT goleadores (CSV v8.5 — 8.4A-TM: Bota de Oro congelada, xG ajustado por Transfermarkt)
cg_scorers = []
with open(f"{CG85}/ChatGPT_v8_5_Top10_Goleadores.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        xg = row.get("Goles esperados 8.4A-TM") or row.get("Goles esperados v7-G","0")
        cg_scorers.append({"rank":int(row["Ranking"]),"player":row["Jugador"].strip(),"team":cn(row["Selección"]),
                           "prob":round(float(row["Prob. Bota de Oro"]),2),"xg":round(float(xg),2),
                           "note":_clean_note(row.get("Justificación",""))})
# Gemini (tabla MD dentro del archivo v8)
GCODE={"ING":"Inglaterra","PBA":"Países Bajos","FRA":"Francia","BRA":"Brasil","ALE":"Alemania","COL":"Colombia",
       "ARG":"Argentina","ESP":"España","URU":"Uruguay","POR":"Portugal","NOR":"Noruega","ESC":"Escocia"}
gm_scorers = []; _insec=False
for line in gtxt.splitlines():
    if "Top 10 Goleadores" in line: _insec=True; continue
    if _insec and line.startswith("## "): break
    if _insec and line.strip().startswith("|"):
        c=[x.strip() for x in line.strip().strip("|").split("|")]
        if len(c)<4 or not c[0].replace("*","").strip().isdigit(): continue
        m=re.match(r"\*\*(.+?)\*\*\s*\(([A-Z]{3})\)", c[1])
        if not m: continue
        gm_scorers.append({"rank":int(c[0].replace("*","")),"player":m.group(1).strip(),
                           "team":GCODE.get(m.group(2),m.group(2)),"prob":num(c[2]),"note":_clean_note(c[4]) if len(c)>4 else ""})
# Claude v6 (capa de goleadores sobre el modelo de selección)
try:
    cl_scorers = json.load(open(f"{HERE}/claude_scorers_v7.json", encoding="utf-8"))
except FileNotFoundError:
    cl_scorers = []
# Consenso de goleadores: media de las IAs que listan al jugador + nº de IAs (ahora hasta 3)
_allp={}
for s in cl_scorers: _allp.setdefault(s["player"],{})["cl"]=s
for s in cg_scorers: _allp.setdefault(s["player"],{})["cg"]=s
for s in gm_scorers: _allp.setdefault(s["player"],{})["gm"]=s
scorers_consensus=[]
for p,d in _allp.items():
    probs=[d[k]["prob"] for k in ("cl","cg","gm") if k in d]
    team=(d.get("cl") or d.get("cg") or d.get("gm"))["team"]
    scorers_consensus.append({"player":p,"team":team,"prob":round(sum(probs)/len(probs),2),"models":len(probs),
                              "cl":d.get("cl",{}).get("prob"),"cg":d.get("cg",{}).get("prob"),"gm":d.get("gm",{}).get("prob")})
scorers_consensus.sort(key=lambda x:(-x["prob"]))
scorers_consensus=scorers_consensus[:10]

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
   "version":"v5","mc":"60.000 simulaciones Monte Carlo",
   "title":"Ensamble: Dixon-Coles (datos) + Machine Learning (gradient boosting Poisson), validado OOS",
   "html":"""
<p><b>Qué es el v5.</b> Un <b>ensamble</b> que promedia dos motores y supera a cada uno por separado fuera de muestra:
λ = 0.4·(Dixon-Coles data-driven) + 0.6·(Machine Learning). El peso 0.4/0.6 es el <b>óptimo del backtesting</b> de 4
Mundiales (la curva de RPS es plana entre 0.4 y 0.5, así que el ensamble es robusto). El componente ML es un
<b>gradient boosting con pérdida de Poisson</b> (sklearn) entrenado sobre miles de partidos internacionales reales.</p>
<p><b>Novedades del v5.</b> (1) <b>Corrección del bracket</b>: la construcción de los octavos (R32) se reescribió para
garantizar una biyección exacta —32 clasificados en 16 partidos, cada equipo una sola vez—; en el v4 algunos equipos se
contaban dos veces y aparecían con R32 &gt; 100% (Inglaterra 120.9%, Croacia 130.9%). (2) <b>Peso del ensamble afinado</b>
a 0.4/0.6 por el backtest. (3) <b>Siembra del cuadro por Elo</b> (los ganadores fuertes enfrentan a los terceros) con
salvaguarda de no cruzar equipos del mismo grupo. Una <b>aserción automática</b> aborta la generación si cualquier
probabilidad supera 100%.</p>
<p><b>Factores integrados en el ML</b> (los que pediste, donde son fiables):</p>
<pre>• Estado/ranking actual  → World Football Elo a jun-2026, recalculado
                            de resultados reales (más actual que el ranking
                            FIFA, que se congela entre ventanas)
• Forma reciente         → goles a favor/en contra, últimos 10 partidos
• Histórico de Mundiales → partidos jugados y % de victoria en Copas
• Localía / sede neutral</pre>
<p><b>Por qué ensamble y no "solo deep learning".</b> Lo probé de forma honesta sobre <b>4 Mundiales (2010–2022),
192 partidos OOS</b>. El ML solo y el Dixon-Coles solo quedan parejos (RPS 0.2012 y 0.2016), pero el <b>ensamble</b> de
ambos los supera a los dos: <b>RPS 0.2002, mejora del 17.0% sobre el azar</b>. Por eso es el modelo v5.</p>
<p><b>Validación FUERA DE MUESTRA</b> (reajuste solo con datos previos a cada Mundial, predicción de sus 48 partidos
reales): backtesting reproducible con código sobre Mundiales reales — ver el panel de backtesting.</p>
<p class="methlim"><b>Honestidad sobre ranking y nóminas:</b> el ranking FIFA oficial se publica en una página renderizada por
JavaScript y no es extraíble de forma fiable; se usó el Elo calculado (mejor predictor y más actual). Las <b>nóminas</b> se
reflejan vía la <b>forma reciente</b> como aproximación; un verdadero modelo jugador-por-jugador exigiría valores de plantilla
(p. ej. Transfermarkt) que no tengo auditados — no los invento (ChatGPT también usó las convocatorias como señal agregada).</p>""",
   "title_en":"Ensemble: Dixon-Coles (data) + Machine Learning (gradient boosting Poisson), OOS-validated",
   "html_en":"""
<p><b>What v5 is.</b> An <b>ensemble</b> that averages two engines and beats each one separately out of sample:
λ = 0.4·(data-driven Dixon-Coles) + 0.6·(Machine Learning). The 0.4/0.6 weight is the <b>backtest optimum</b> over 4
World Cups (the RPS curve is flat between 0.4 and 0.5, so the ensemble is robust). The ML component is a <b>gradient
boosting model with Poisson loss</b> (sklearn) trained on thousands of real international matches.</p>
<p><b>What is new in v5.</b> (1) <b>Bracket fix</b>: the round-of-32 construction was rewritten to guarantee an exact
bijection —32 qualifiers into 16 matches, each team exactly once—; in v4 some teams were counted twice and showed R32
&gt; 100% (England 120.9%, Croatia 130.9%). (2) <b>Ensemble weight tuned</b> to 0.4/0.6 by the backtest. (3) <b>Bracket
seeded by Elo</b> (strong winners face third-placed teams) with a same-group guard. An <b>automatic assertion</b> aborts
generation if any probability exceeds 100%.</p>
<p><b>Factors integrated in the ML</b> (the ones you asked for, where reliable):</p>
<pre>• Current state/ranking → World Football Elo as of Jun-2026, recomputed
                          from real results (more current than the FIFA
                          ranking, which freezes between windows)
• Recent form          → goals for/against, last 10 matches
• World Cup history     → matches played and win % at World Cups
• Home / neutral venue</pre>
<p><b>Why an ensemble and not "deep learning alone".</b> I tested it honestly over <b>4 World Cups (2010–2022),
192 OOS matches</b>. ML alone and Dixon-Coles alone are roughly tied (RPS 0.2012 and 0.2016), but the <b>ensemble</b> of
the two beats both: <b>RPS 0.2002, a 17.0% improvement over chance</b>. Hence the v5 model.</p>
<p><b>OUT-OF-SAMPLE validation</b> (refit using only pre-tournament data for each World Cup, predicting its 48 real
matches): reproducible backtest with code over real World Cups — see the backtesting panel.</p>
<p class="methlim"><b>Honesty about ranking and squads:</b> the official FIFA ranking is published on a JavaScript-rendered
page and cannot be scraped reliably; the computed Elo was used (a better and more current predictor). <b>Squads</b> are
reflected via <b>recent form</b> as a proxy; a true player-by-player model would require audited squad values (e.g.
Transfermarkt) that I do not have — I will not invent them (ChatGPT also used call-ups only as an aggregate signal).</p>"""},
 "chatgpt": {
   "version":"v8.5","mc":"Elo + Transfermarkt (8.4A-TM) · probabilidades por consenso de mercado (Odds API + SofaScore, 8.4B-Consensus)",
   "title":"Ensamble calibrado histórico + Nivel 2 (núcleo FIFA/Elo reforzado + anti-sesgo de mercado)",
   "html":"""
<p><b>Recalibración Fase 7.</b> Mantiene la arquitectura v6.2 y reajusta las probabilidades; añade además un <b>Top 10 de goleadores</b> (Bota de Oro) con goles esperados por jugador.</p>
<p><b>Recalibración Fase 8 (v8).</b> Integra <b>The Odds API</b>: las probabilidades 1X2 son ahora una mezcla del 40% del modelo vigente y 60% del mercado sin margen de casa. Los marcadores (<b>Scoreline Lite</b>) se ajustan al <b>ancla histórica de empates</b> (~22%) y la tasa proyectada cae de 25% (Fase 7) a 22.2%, dentro del rango defendible. Los goleadores quedan congelados desde v6.4-G por falta de datos player-level/xG.</p>
<p><b>Recalibración Fase 8.5 (8.4A-TM + 8.4B-Consensus).</b> Selecciones combinan Elo 2026 con una capa <b>Transfermarkt</b> de talento, profundidad y edad. Las probabilidades 1X2 pasan a un <b>consenso de mercado</b>: The Odds API (1.502 filas) como señal principal y <b>SofaScore/datafc</b> como validación secundaria, con bandera de consenso cuando ambas fuentes coinciden. Marcadores y goleadores se conservan (8.4A-TM); xG y datos player-level siguen pendientes por falta de suscripción activa.</p>
<p><b>Qué es.</b> Evolución del v6 con los hallazgos del <b>Backtesting Nivel 2</b>: refuerza el núcleo estructural
<b>FIFA/Elo</b>, mantiene plantilla, player-level, forma y experiencia como <b>capas de ajuste</b> (no dominantes), y
añade una <b>penalización de sesgo de mercado</b> para no sobrevalorar a las ligas europeas más líquidas.</p>
<p><b>Fórmula de fuerza (Strength v6.2).</b></p>
<pre>0.24 FIFA-Elo + 0.20 WorldFootballElo + 0.14 SquadMarketTalent
+ 0.12 PlayerLevel + 0.10 RecentForm + 0.08 AttackDefense
+ 0.05 TournamentExperience + 0.04 ClimateAltitude + 0.03 UpsetRobustness</pre>
<p><b>Probabilidad por fase.</b> Monte Carlo (fuerza, sorteo, ruta, clima, riesgo de plantel, matriz de terceros,
varianza de eliminación) y luego calibración histórica con un nuevo término anti-sesgo de mercado:</p>
<pre>p_fase = normalize_por_fase( sigmoid(
   α + β·logit(p_cruda) + γ·VolatilidadHistórica + δ·DificultadRuta
   − η·PenalizaciónSobreconfianza − θ·PenalizaciónSesgoMercado ) )</pre>
<p>con la restricción de masa Σ por fase = 32 / 16 / 8 / 4 / 2 / 1 equipos.</p>
<p><b>Novedades v6.2.</b> Mayor peso a FIFA/Elo (24%) y clima reducido a contextual (4%); corrección positiva moderada a
outsiders tácticos (Marruecos, Colombia, Senegal, Uruguay, Japón); regularización prudente de favoritos con dudas de
ruta, edad o knockout. España sigue 1ª, sin ventaja excesiva; Francia, Inglaterra y Argentina forman el bloque de élite.</p>""",
   "title_en":"Historically-calibrated ensemble + Level 2 (reinforced FIFA/Elo core + anti-market-bias)",
   "html_en":"""
<p><b>Phase 7 recalibration.</b> It keeps the v6.2 architecture and re-tunes the probabilities; it also adds a <b>Top 10 of scorers</b> (Golden Boot) with expected goals per player.</p>
<p><b>Phase 8 recalibration (v8).</b> Integrates <b>The Odds API</b>: 1X2 probabilities are now a blend of 40% current model and 60% market without house margin. Scorelines (<b>Scoreline Lite</b>) are anchored to the <b>historical draw rate</b> (~22%) and the projected rate drops from 25% (Phase 7) to 22.2%, within the defensible range. Scorers stay frozen from v6.4-G due to lack of player-level / xG data.</p>
<p><b>Phase 8.5 recalibration (8.4A-TM + 8.4B-Consensus).</b> Selections combine 2026 Elo with a <b>Transfermarkt</b> layer of talent, depth and age. 1X2 probabilities move to a <b>market consensus</b>: The Odds API (1,502 rows) as the main signal and <b>SofaScore/datafc</b> as secondary validation, with a consensus flag when both sources agree. Scorelines and scorers are kept (8.4A-TM); xG and player-level data remain pending due to no active subscription.</p>
<p><b>What it is.</b> An evolution of v6 with the <b>Level 2 Backtesting</b> findings: it reinforces the structural
<b>FIFA/Elo</b> core, keeps squad, player-level, form and experience as <b>adjustment layers</b> (not dominant), and
adds a <b>market-bias penalty</b> so the most liquid European leagues are not overvalued.</p>
<p><b>Strength formula (Strength v6.2).</b></p>
<pre>0.24 FIFA-Elo + 0.20 WorldFootballElo + 0.14 SquadMarketTalent
+ 0.12 PlayerLevel + 0.10 RecentForm + 0.08 AttackDefense
+ 0.05 TournamentExperience + 0.04 ClimateAltitude + 0.03 UpsetRobustness</pre>
<p><b>Per-stage probability.</b> Monte Carlo (strength, draw, route, climate, squad risk, third-place matrix, knockout
variance) then historical calibration with a new anti-market-bias term:</p>
<pre>p_stage = normalize_per_stage( sigmoid(
   α + β·logit(p_raw) + γ·HistoricalVolatility + δ·RouteDifficulty
   − η·OverconfidencePenalty − θ·MarketSkewPenalty ) )</pre>
<p>with the mass constraint Σ per stage = 32 / 16 / 8 / 4 / 2 / 1 teams.</p>
<p><b>What is new in v6.2.</b> Higher weight on FIFA/Elo (24%) and climate reduced to contextual (4%); moderate positive
correction for tactical outsiders (Morocco, Colombia, Senegal, Uruguay, Japan); prudent regularization of favorites with
route, age or knockout doubts. Spain stays #1 without an excessive edge; France, England and Argentina form the elite block.</p>"""},
 "gemini": {
   "version":"v10","mc":"Ensamble físico-estadístico + ancla empírica de empates",
   "title":"Redes de Presión Local + Decaimiento del Campeón + UTCI + Penalización Contrafáctica",
   "html":"""
<p><b>Qué es.</b> Ensamble físico-estadístico que <b>abandona la "memoria histórica estática" de los escudos</b> (el
enfoque Heritage AI del v6). Ahora mide la resiliencia por la <b>carga de estrés cognitivo actual</b> de cada plantilla:
los minutos de eliminación directa acumulados en Champions y Libertadores forman las <b>Redes de Presión Local</b>.</p>
<p><b>Ecuaciones (apéndice técnico V7).</b></p>
<pre>xG_base = λ₀ · exp( β₁·ΔElo − β₂·Lesiones + β₃·ValorPlantilla )
xG_termo = xG_base · e^(−κ·(UTCI − 28)) · [1 − α·max(0, altitud − 1500)]
xG_V7 = xG_termo · (1 + ρ_LPN) · (1 − δ_campeón) · ω_local
P(x,y) = Poisson(xG_V7_A) · Poisson(xG_V7_B)</pre>
<p><b>ρ_LPN</b> (Red de Presión Local) = minutos de los titulares 25/26 jugados bajo PPDA muy bajo en fases KO de
Champions/Libertadores; <b>δ_campeón</b> = penalización de hasta 8% al campeón vigente (Argentina); <b>ω_local</b> =
aura de localía asimétrica (castiga a México, premia a EE.UU./Canadá). Datos forenses de minutos bajo presión (Opta,
StatsBomb) sustituyen los priors históricos del v6.</p>
<p><b>Recalibración Fase 8 (v8).</b> Añade <b>regresión isotónica</b> (corrige el exceso de confianza en favoritos y colistas), un parámetro de empates <b>ρ dinámico</b> (más empates en partidos parejos) y una <b>matriz bayesiana de inactividad</b> para el nuevo <b>Top 10 de goleadores</b>. Donde faltan datos, revierte al promedio de la confederación en vez de inventar parámetros.</p>
<p><b>Recalibración empírica Fase 9 (v9).</b> Calibración por <b>Temperature Scaling</b> (T=1.12): aplana las probabilidades para que ningún equipo supere ~17% de título, mejorando el RPS fuera de muestra. El parámetro de empates <b>ρ</b> se ancla en la <b>tasa empírica de empates de los Mundiales 1998–2022 (~25.4%)</b>, y los minutos de los goleadores usan una <b>distribución Beta</b> con cortes de reportes clínicos a junio de 2026.</p>
<p><b>Recalibración Fase 10 (v10).</b> Auditoría de muestreo: revisa la ventana de empates y adopta el <b>ancla del 21.88%</b> (tasa real de la fase de grupos 2010–2022, alineada con el backtest de Claude). En vez de inflar empates como en v9, los <b>desinfla</b>, lo que premia marginalmente a las potencias tácticas. Aplica filtros de inactividad clínica en goleadores (excluye a Darwin Núñez por desacondicionamiento).</p>
<p><b>Efecto en v7.</b> La cúspide cambia: <b>Francia toma el nº 1 (19.5%)</b> por el volumen puro de minutos KO de su
plantilla; <b>Argentina cae al 3º (13.5%)</b> por el decaimiento del campeón; y <b>Brasil y Alemania bajan</b> al
neutralizar su "gravedad de escudo". España se sostiene 2ª (16%) por el efecto Premier/LaLiga.</p>
<p class="methlim"><b>Autocrítica del modelo:</b> asume que los minutos de élite de clubes se transfieren linealmente al
plano de selecciones, y reparte el "Aura de Localía" de forma asimétrica entre tres anfitriones con datos limitados —
un vector de alta inestabilidad para los Grupos A, B y D.</p>""",
   "title_en":"Local Pressure Networks + Champion Decay + UTCI + Counterfactual Penalty",
   "html_en":"""
<p><b>What it is.</b> A physics-statistical ensemble that <b>abandons the "static historical memory" of the crests</b>
(the v6 Heritage AI approach). It now measures resilience through each squad's <b>current cognitive stress load</b>:
the knockout minutes accumulated in the Champions League and Libertadores form the <b>Local Pressure Networks</b>.</p>
<p><b>Equations (V7 technical appendix).</b></p>
<pre>xG_base = λ₀ · exp( β₁·ΔElo − β₂·Injuries + β₃·SquadValue )
xG_termo = xG_base · e^(−κ·(UTCI − 28)) · [1 − α·max(0, altitude − 1500)]
xG_V7 = xG_termo · (1 + ρ_LPN) · (1 − δ_champion) · ω_home
P(x,y) = Poisson(xG_V7_A) · Poisson(xG_V7_B)</pre>
<p><b>ρ_LPN</b> (Local Pressure Network) = starters' 25/26 minutes played under very low PPDA in Champions/Libertadores
knockout stages; <b>δ_champion</b> = up to 8% penalty on the reigning champion (Argentina); <b>ω_home</b> = asymmetric
home aura (penalizes Mexico, rewards USA/Canada). Forensic under-pressure minute data (Opta, StatsBomb) replaces the v6
historical priors.</p>
<p><b>Phase 8 recalibration (v8).</b> It adds <b>isotonic regression</b> (correcting overconfidence in favorites and minnows), a <b>dynamic draw parameter ρ</b> (more draws in close matches) and a <b>Bayesian inactivity matrix</b> for the new <b>Top 10 of scorers</b>. Where data is missing, it reverts to the confederation average instead of fabricating parameters.</p>
<p><b>Empirical recalibration Phase 9 (v9).</b> <b>Temperature scaling</b> (T=1.12) flattens probabilities so no team exceeds ~17% title chance, improving out-of-sample RPS. The draw parameter <b>ρ</b> is anchored to the <b>empirical draw rate of the 1998–2022 World Cups (~25.4%)</b>, and scorer minutes use a <b>Beta distribution</b> with clinical-report cutoffs as of June 2026.</p>
<p><b>Phase 10 recalibration (v10).</b> Sampling audit: revisits the draw window and adopts the <b>21.88% anchor</b> (real group-stage rate for 2010–2022, aligned with the Claude backtest). Instead of inflating draws as in v9, it <b>deflates</b> them, marginally favoring tactical powers. Adds clinical-inactivity filters to scorers (excludes Darwin Núñez due to deconditioning).</p>
<p><b>Effect in v7.</b> The top tier shifts: <b>France takes #1 (19.5%)</b> on the sheer volume of its squad's KO
minutes; <b>Argentina drops to 3rd (13.5%)</b> due to champion decay; and <b>Brazil and Germany fall</b> as their
"crest gravity" is neutralized. Spain holds 2nd (16%) on the Premier/LaLiga effect.</p>
<p class="methlim"><b>Model self-critique:</b> it assumes club elite minutes transfer linearly to the national-team
level, and splits the "Home Aura" asymmetrically across three hosts with limited data — a high-instability vector for
Groups A, B and D.</p>"""},
}

# ---------- Backtesting / validación (paneles desplegables por IA) ----------
BACKTEST = {
 "claude": {
   "title":"Backtesting OOS reproducible · 4 Mundiales (2010–2022)",
   "html":"""
<p><b>Qué hace.</b> Backtest <b>calculado con código sobre resultados reales</b> y reproducible
(<code>models/claude/code/backtest_claude_v4.py</code>). Para cada Mundial 2010, 2014, 2018 y 2022 el ensamble se ajusta
<b>solo con datos previos al torneo</b> y predice sus 48 partidos de grupos reales: <b>192 partidos fuera de muestra</b>.</p>
<p><b>Métricas (promedio por partido).</b></p>
<pre>Modelo                  RPS    Brier  LogLoss  MAE goles  Marcador
Dixon-Coles solo      0.2016  0.5766  0.9795    1.3320     13.5%
Machine Learning solo 0.2012  0.5749  0.9718    1.3140     12.0%
ENSAMBLE (v4)         0.2002  0.5731  0.9708    1.3153     13.5%
Baseline uniforme     0.2413  0.6667  1.0986       —          —</pre>
<p><b>Resultados.</b> El <b>ensamble mejora 17.02% sobre el azar</b> (RPS) y supera a cada componente por separado
(0.2002 &lt; 0.2012 ML &lt; 0.2016 DC), confirmando que combinar estadística + machine learning aporta. Por Mundial:
2010 0.1897 · 2014 0.1905 · 2018 0.1906 · 2022 0.2301 (el más difícil, por sorpresas como Arabia Saudí 2-1 Argentina).</p>
<p class="methlim"><b>Honestidad metodológica.</b> Mide calibración a <b>nivel de partido de grupos</b>; una validación a
nivel de <b>campeón</b> (tipo "campeón en Top N") exigiría simular el torneo completo de cada edición —trabajo futuro.
Brier es multiclase (V/E/D, rango 0–2); las métricas entre IAs <b>solo son comparables bajo la misma convención y los
mismos datos</b>.</p>""",
   "title_en":"Reproducible OOS backtesting · 4 World Cups (2010–2022)",
   "html_en":"""
<p><b>What it does.</b> A backtest <b>computed with code over real results</b> and reproducible
(<code>models/claude/code/backtest_claude_v4.py</code>). For each World Cup 2010, 2014, 2018 and 2022 the ensemble is
fit <b>using only pre-tournament data</b> and predicts its 48 real group matches: <b>192 out-of-sample matches</b>.</p>
<p><b>Metrics (per-match average).</b></p>
<pre>Model                  RPS    Brier  LogLoss  Goals MAE  Scoreline
Dixon-Coles only      0.2016  0.5766  0.9795    1.3320     13.5%
Machine Learning only 0.2012  0.5749  0.9718    1.3140     12.0%
ENSEMBLE (v4)         0.2002  0.5731  0.9708    1.3153     13.5%
Uniform baseline      0.2413  0.6667  1.0986       —          —</pre>
<p><b>Results.</b> The <b>ensemble improves 17.02% over chance</b> (RPS) and beats each component on its own
(0.2002 &lt; 0.2012 ML &lt; 0.2016 DC), confirming that combining statistics + machine learning adds value. By World Cup:
2010 0.1897 · 2014 0.1905 · 2018 0.1906 · 2022 0.2301 (the hardest, due to upsets like Saudi Arabia 2-1 Argentina).</p>
<p class="methlim"><b>Methodological honesty.</b> It measures <b>group-stage match-level</b> calibration; a <b>champion</b>-level
validation ("champion in Top N") would require simulating each full tournament —future work. Brier is multiclass (W/D/L,
range 0–2); cross-AI metrics <b>are only comparable under the same convention and data</b>.</p>"""},
 "chatgpt": {
   "title":"Backtesting Nivel 2 · validación del núcleo v6 → v6.2",
   "html":"""
<p><b>Qué hace.</b> Valida el modelo sobre los Mundiales 2010, 2014, 2018 y 2022 en dos capas: el <b>Nivel 1</b> probó
el núcleo estructural (FIFA + Elo + localía + grupo real + calibración histórica) y el <b>Nivel 2</b> evalúa dónde ese
núcleo es más débil (octavos, cuartos, outsiders, plantillas envejecidas, calidad por líneas, xG/xGA, mercado).</p>
<p><b>Resultados del Nivel 1 (identificación de élite).</b></p>
<pre>Campeón real en Top 4        4/4   muy fuerte
Campeón real en Top 8        4/4   muy fuerte
Finalistas en Top 8          7/8   fuerte
Semifinalistas en Top 12    15/16  muy fuerte
Cuartofinalistas en Top 8   21/32  medio
Octavofinalistas en Top 16  49/64  bueno</pre>
<p><b>Hallazgo central.</b> El núcleo FIFA/Elo es sólido en la cúspide, pero el ranking y el mercado <b>subestiman a
outsiders tácticos</b> y no capturan bien octavos/cuartos. De ahí nace la recalibración hacia el <b>v6.2</b>: variables
de plantilla, edad, mercado y player-level entran como <b>capas de ajuste</b>, no como dominantes.</p>
<p><b>Honestidad metodológica.</b> El propio reporte advierte que <b>no es un backtesting player-level completo</b>: eso
exigiría reconstruir odds, valores de mercado y convocatorias pretorneo auditados año por año. Por eso el v6.2 es una
evolución prudente, no una validación final estilo casa de apuestas.</p>""",
   "title_en":"Level 2 Backtesting · validating the v6 core → v6.2",
   "html_en":"""
<p><b>What it does.</b> It validates the model on the 2010, 2014, 2018 and 2022 World Cups in two layers: <b>Level 1</b>
tested the structural core (FIFA + Elo + home advantage + real group + historical calibration), and <b>Level 2</b>
assesses where that core is weakest (round of 16, quarters, outsiders, aging squads, line quality, xG/xGA, market).</p>
<p><b>Level 1 results (elite identification).</b></p>
<pre>Real champion in Top 4        4/4   very strong
Real champion in Top 8        4/4   very strong
Finalists in Top 8            7/8   strong
Semifinalists in Top 12      15/16  very strong
Quarterfinalists in Top 8    21/32  medium
Round-of-16 sides in Top 16  49/64  good</pre>
<p><b>Core finding.</b> The FIFA/Elo core is solid at the top, but ranking and market <b>underrate tactical
outsiders</b> and miss the round of 16/quarters. Hence the recalibration toward <b>v6.2</b>: squad, age, market and
player-level variables enter as <b>adjustment layers</b>, not as dominant ones.</p>
<p><b>Methodological honesty.</b> The report itself warns this is <b>not a full player-level backtest</b>: that would
require reconstructing audited pre-tournament odds, market values and call-ups year by year. So v6.2 is a prudent
evolution, not a bookmaker-style final validation.</p>"""},
 "gemini": {
   "title":"Backtesting y validación · Mundiales 2010–2022",
   "html":"""
<p><b>Qué hace.</b> Evalúa el modelo <i>out-of-sample</i> sobre los Mundiales 2010, 2014, 2018 y 2022. Para evitar sesgo
de retrospectiva, el motor se bloquea el día previo al partido inaugural de cada edición y solo asimila Elo del ciclo
clasificatorio anterior, valor de plantilla (Transfermarkt), partes médicos y climatología de las sedes.</p>
<p><b>Métricas de calibración.</b></p>
<pre>Brier Score (error probabilístico)  V6: 0.192  vs  casas de apuestas: 0.205  →  −6.34%
Log-Loss / entropía cruzada         V6: 0.584  (buena calibración de colas)</pre>
<p><b>Aciertos del backtesting.</b> En 2018 el filtro detectó la densidad de veteranos de Croacia y predijo su final
(donde un modelo de solo xG la eliminaba). En 2014 el motor térmico aplicó descuentos de hasta 28% al xG europeo en
sedes de calor extremo y anticipó los colapsos de España e Italia en primera ronda.</p>
<p><b>Fallos reconocidos (cisnes negros).</b> Argentina 1-2 Arabia Saudí (2022): el modelo asignó 88.4% a Argentina y no
capturó la complacencia inicial. Brasil 1-7 Alemania (2014): daba a Brasil 55.4% por localía; la desintegración
psicológica tras la baja de Neymar rompió la distribución de Poisson.</p>
<p><b>Conclusión que alimenta el v7.</b> El backtesting mostró un <b>sesgo de supervivencia</b>: los modelos se
"enamoran" de la historia. De ahí nace el <b>Factor de Decaimiento del Campeón</b> (−8% al campeón vigente) y el giro
del v7 hacia la carga real de minutos de élite en lugar del pedigrí del escudo.</p>""",
   "title_en":"Backtesting & validation · World Cups 2010–2022",
   "html_en":"""
<p><b>What it does.</b> It evaluates the model <i>out-of-sample</i> on the 2010, 2014, 2018 and 2022 World Cups. To avoid
hindsight bias, the engine is locked the day before each tournament's opening match and only ingests Elo from the prior
qualifying cycle, squad value (Transfermarkt), medical reports and venue climatology.</p>
<p><b>Calibration metrics.</b></p>
<pre>Brier Score (probability error)  V6: 0.192  vs  bookmakers: 0.205  →  −6.34%
Log-Loss / cross-entropy         V6: 0.584  (good tail calibration)</pre>
<p><b>Backtesting hits.</b> In 2018 the filter detected Croatia's veteran density and predicted its final run (where an
xG-only model eliminated them). In 2014 the thermal engine applied up to 28% xG discounts to European sides in
extreme-heat venues and anticipated the first-round collapses of Spain and Italy.</p>
<p><b>Acknowledged failures (black swans).</b> Argentina 1-2 Saudi Arabia (2022): the model assigned 88.4% to Argentina
and missed the early complacency. Brazil 1-7 Germany (2014): it gave Brazil 55.4% on home advantage; the psychological
collapse after Neymar's injury broke the Poisson distribution.</p>
<p><b>Conclusion feeding into v7.</b> Backtesting revealed a <b>survivorship bias</b>: models "fall in love" with
history. That is the origin of the <b>Champion Decay Factor</b> (−8% to the reigning champion) and the v7 shift toward
real elite-minutes load instead of crest pedigree.</p>"""},
}

# ---------- calendario REAL (openfootball, dominio público) + mejores terceros ----------
import os as _os
_SCHED_PATH=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"wc_schedule.json")
if not _os.path.exists(_SCHED_PATH): _SCHED_PATH="wc_schedule.json"
REAL_SCHED=json.load(open(_SCHED_PATH,encoding="utf-8"))  # clave 'A|B' (orden alfabético) -> {date,iso,grp,md}
def _inject_md(mlist):
    for m in mlist:
        a,b=m.get("a",""),m.get("b","")
        e=REAL_SCHED.get("|".join(sorted((a,b))))
        if e: m["md"]=e["md"]; m["date"]=e["date"]; m["grp"]=e["grp"]; m["iso"]=e["iso"]; m["kickoff"]=e.get("kickoff"); m["venue"]=e.get("venue")
_inject_md(cons_matches)
for flist in [cl["fixtures"], list(cg_matches.values()), list(gm_matches.values())]:
    _inject_md(flist)
# 8 mejores terceros
_thirds=[]
for g in sorted(GROUPS):
    row=group_proj[g]["Consenso"]
    if len(row)>=3: _thirds.append((g,row[2][0],row[2][1]))
_thirds.sort(key=lambda x:-x[2])
best_thirds=[x[0] for x in _thirds[:8]]

DATA={"groups":GROUPS,"elo":cl_elo,"meth":METH,"backtest":BACKTEST,
 "claude":{"title":claude_title,"reach":claude_reach,"group_win":claude_group,"advance":claude_adv,
           "fixtures":cl["fixtures"],"params":cl["params"],"N":cl["N"],"version":CLAUDE_VERSION,"scorers":cl_scorers},
 "chatgpt":{"title":cg_title,"reach":to_round_keyed(cg_reach),"version":"v8.5",
            "matches":[{**{k:m[k] for k in("a","b","pA","pD","pB","score")},**{k:m[k] for k in("md","date","grp") if k in m}} for m in cg_matches.values()],
            "scorers":cg_scorers},
 "gemini":{"title":gm_title,"reach":to_round_keyed(gm_reach),"version":"v10",
           "matches":[{**{k:m[k] for k in("a","b","pA","pD","pB","score")},**{k:m[k] for k in("md","date","grp") if k in m}} for m in gm_matches.values()],
           "scorers":gm_scorers},
 "consensus":{"title":consensus_title,"title_median":consensus_title_median,
              "title_stat":{t:{k:round(v[k],2) for k in("mean","median","min","max")} for t,v in title_stat.items()},
              "reach":consensus_reach,"matches":cons_matches,"agree_counter":dict(agree),
              "scorers":scorers_consensus},
 "group_proj":group_proj,"best_thirds":best_thirds,"schedule_dates":REAL_SCHED}
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
