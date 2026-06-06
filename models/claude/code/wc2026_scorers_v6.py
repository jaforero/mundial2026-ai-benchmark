# -*- coding: utf-8 -*-
"""
Claude · Modelo de Goleadores v6 (Bota de Oro)
================================================
Capa de JUGADOR construida sobre el modelo de SELECCIÓN de Claude (v5,
Dixon-Coles + ML). No inventa datos: ancla la oportunidad de gol en la
salida real del motor de equipo y descompone el resto en factores explícitos.

Descomposición:
    E_goles(jugador) = G_equipo(T)               # goles que el equipo marca en todo el torneo
                       × cuota_rol(p)             # fracción de goles del equipo que aporta el jugador
                       × penales(p)               # bonus si es lanzador principal
                       × titularidad(p)           # prob. de ser titular  -> MINUTOS
                       × disponibilidad(p)        # riesgo físico/lesión   -> MINUTOS (separado de la forma)
                       × forma(p)                 # estado de forma        -> TASA de gol por minuto

G_equipo(T) = partidos_esperados(T) × goles_esperados_por_partido(T), ambos del motor de Claude:
    partidos_esperados = 3 (grupos) + Σ_ronda P(alcanza ronda)        (de 'reach')
    goles_por_partido  = promedio de λ (goles esperados) de T en sus partidos (de 'fixtures')

Bota de Oro: se estima por SIMULACIÓN de Monte Carlo. En cada torneo simulado
cada candidato marca Goles ~ Poisson(E_goles), más un "campo" de goleadores
ocultos (otros jugadores) para no asignar el 100% de la probabilidad al top.
Gana quien más marca (empates repartidos). P(Bota) = victorias / simulaciones.

NOTA METODOLÓGICA (riesgo físico vs forma): son factores SEPARADOS.
  - disponibilidad (riesgo físico) actúa sobre los MINUTOS (cuánto juega / rotación).
  - forma actúa sobre la TASA de gol por minuto (eficacia cuando juega).

Los atributos por jugador (rol, penales, titularidad, disponibilidad, forma) son
las ENTRADAS EDITABLES del modelo. Aquí se derivan del pool de candidatos élite
documentado en el proyecto (datos de jugador de ChatGPT/Gemini) y de priores
futbolísticos estándar; G_equipo y la simulación son aportación propia de Claude.
"""
import json, statistics
import numpy as np

HERE = "/home/claude/wc2026"
TEAM = json.load(open(f"{HERE}/results_v5.json", encoding="utf-8"))
REACH = TEAM["reach"]; FIX = TEAM["fixtures"]
ROUNDS = ["R32","R16","QF","SF","FINAL"]   # partidos jugados además de los 3 de grupo

def expected_matches(team):
    em = 3.0
    for r in ROUNDS:
        em += REACH.get(r, {}).get(team, 0.0) / 100.0
    return em

def xg_per_match(team):
    """Promedio de goles esperados (λ) del equipo en sus 3 partidos de grupo (motor Dixon-Coles)."""
    vals = []
    for f in FIX:
        if f["a"] == team: vals.append(f["la"])
        elif f["b"] == team: vals.append(f["lb"])
    return statistics.mean(vals) if vals else 1.0

def team_tournament_goals(team):
    return expected_matches(team) * xg_per_match(team)

# ---------------------------------------------------------------------------
# Pool de candidatos élite (unión de los Top 10 documentados de ChatGPT y Gemini).
# Atributos = entradas del modelo. Bases:
#   role_share : fracción de goles del equipo que concentra el jugador (prior por rol)
#   pen        : 1.12 lanzador principal · 1.05 compartido · 1.0 no
#   starter    : prob. de ser titular (titularidad)         -> minutos
#   avail      : disponibilidad por riesgo físico/lesión 0-1 -> minutos (SEPARADO de forma)
#   form       : multiplicador de estado de forma ~0.85-1.15 -> tasa de gol
# ---------------------------------------------------------------------------
P = [
 # player, team, role_share, pen, starter, avail, form, nota
 ("Harry Kane","Inglaterra",0.30,1.12,0.96,0.95,1.06,"Titular fijo y lanzador de penales; forma alta. Leve descuento por gestión de minutos."),
 ("Kylian Mbappé","Francia",0.32,1.12,0.96,0.85,1.08,"Central + penales; riesgo físico medio por fatiga muscular y rotaciones en grupos."),
 ("Erling Haaland","Noruega",0.34,1.05,0.98,0.95,1.12,"Máxima tasa de gol por 90; su techo lo marca la ruta esperada de Noruega."),
 ("Cody Gakpo","Países Bajos",0.26,1.0,0.90,0.90,1.05,"Absorbe la finalización neerlandesa; titular salvo rotaciones puntuales."),
 ("Vinícius Júnior","Brasil",0.24,1.0,0.92,0.85,1.02,"Extremo explosivo; riesgo de sustitución por carga y calor en Norteamérica."),
 ("Luis Díaz","Colombia",0.27,1.0,0.94,0.92,1.05,"Amenaza principal e inamovible; sin penales a favor, lo que limita el techo."),
 ("Jamal Musiala","Alemania",0.22,1.0,0.88,0.88,1.00,"Recuperación física confirmada; comparte cuota de gol con otros atacantes."),
 ("Bukayo Saka","Inglaterra",0.19,1.0,0.82,0.75,0.95,"Gestión de minutos por cuidado del tendón; comparte cuota con Kane y Foden."),
 ("Lionel Messi","Argentina",0.24,1.12,0.85,0.85,1.00,"Penales y balón parado sostienen el upside; se descuenta administración física."),
 ("Julián Álvarez","Argentina",0.22,1.0,0.72,0.65,0.95,"Riesgo físico alto (molestias) y competencia interna por la cuota de gol."),
 ("Lamine Yamal","España",0.20,1.0,0.85,0.70,0.95,"Protocolo de cuidado: difícil que complete partidos; perfil más creador que 9."),
 ("Mikel Oyarzabal","España",0.23,1.05,0.75,0.85,0.95,"España proyecta muchos partidos; incertidumbre de rol y penales compartidos."),
 ("Cristiano Ronaldo","Portugal",0.26,1.12,0.70,0.80,0.90,"Penales sostienen el upside; edad y rol reducen minutos y forma esperada."),
 ("Darwin Núñez","Uruguay",0.24,1.0,0.68,0.70,0.85,"Riesgo físico alto por desacondicionamiento; titularidad no garantizada."),
]

cands = []
for player, team, share, pen, starter, avail, form, nota in P:
    G_T = team_tournament_goals(team)
    eg = G_T * share * pen * starter * avail * form
    cands.append({"player":player,"team":team,"eg":eg,"starter":round(starter*100),
                  "avail":round(avail*100),"form":form,"G_T":round(G_T,2),"note":nota})

# ---------------- Simulación Monte Carlo de la Bota de Oro ----------------
# Los goles de un torneo están SOBREDISPERSOS respecto a Poisson (rachas, hat-tricks):
# usamos binomial negativa vía mezcla Gamma-Poisson, que reparte mejor las sorpresas
# y evita que el de mayor media gane casi siempre (más realista que Poisson pura).
rng = np.random.default_rng(2026)
N = 300_000
R_DISP = 2.8   # dispersión: var = mu + mu^2/R_DISP (menor R = más sorpresas)

def nb_goals(mu, size):
    mu = np.asarray(mu, dtype=float)
    lam = rng.gamma(shape=R_DISP, scale=mu / R_DISP, size=size)   # Gamma con media mu
    return rng.poisson(lam).astype(float)

egs = np.array([c["eg"] for c in cands])
goals = nb_goals(np.broadcast_to(egs, (N, len(cands))), (N, len(cands)))

# "Campo": mejor goleador fuera del pool. Fuera del top-14 élite, los goleadores
# de torneo promedian bastante menos, así que el campo es modesto (no debe ganar
# la mayoría de las veces: históricamente la Bota la gana un candidato reconocido).
K_FIELD, MU_FIELD = 12, 1.85
field = nb_goals(MU_FIELD, (N, K_FIELD)).max(axis=1)

# desempate suave aleatorio (asistencias/minutos) para no inflar empates exactos
goals += rng.uniform(0, 0.01, size=goals.shape)
field += rng.uniform(0, 0.01, size=field.shape)

best_cand = goals.max(axis=1)
cand_wins = (goals == best_cand[:, None]) & (best_cand >= field)[:, None]
win_counts = np.zeros(len(cands))
ties = cand_wins.sum(axis=1)
mask = (ties >= 1)
for j in range(len(cands)):
    win_counts[j] = np.sum(cand_wins[mask, j] / ties[mask])
probs = win_counts / N * 100.0

for c, p in zip(cands, probs):
    c["prob"] = round(float(p), 2)
    c["xg"] = round(c["eg"], 2)

cands.sort(key=lambda x: -x["prob"])
top10 = cands[:10]
for i, c in enumerate(top10, 1):
    c["rank"] = i

out = [{"rank":c["rank"],"player":c["player"],"team":c["team"],"prob":c["prob"],"xg":c["xg"],
        "starter":c["starter"],"avail":c["avail"],"note":c["note"]} for c in top10]
json.dump(out, open(f"{HERE}/claude_scorers_v6.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

field_win = 100.0 - sum(c["prob"] for c in cands)
print("Claude · Bota de Oro v6  (campo/otros: %.1f%%)" % field_win)
print("%-2s %-18s %-14s %6s %6s  %s" % ("#","Jugador","Selección","P(Bota)","xG","titular/disp"))
for c in top10:
    print("%-2d %-18s %-14s %5.1f%% %6.2f  %d%%/%d%%" %
          (c["rank"], c["player"], c["team"], c["prob"], c["xg"], c["starter"], c["avail"]))
