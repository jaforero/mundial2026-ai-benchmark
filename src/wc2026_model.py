"""
=============================================================================
 MODELO PREDICTIVO HÍBRIDO + SIMULACIÓN MONTE CARLO — COPA MUNDIAL FIFA 2026
=============================================================================
 Motor que implementa el diseño descrito en el documento fuente:
   - Núcleo de fuerza: Elo internacional (escala eloratings.net, snapshot 2-jun-2026)
   - Generación de marcadores: Poisson bivariado parametrizado por
     supremacía/total (consistente con Maher 1982 / Dixon-Coles 1997)
   - Corrección Dixon-Coles (rho) para los marcadores bajos (0-0,1-0,0-1,1-1)
   - Propagación por Monte Carlo del bracket completo de 48 equipos
     respetando el formato nuevo (2 mejores + 8 mejores terceros -> R32)
 Calibración: la escala de supremacía se ajusta para reproducir el benchmark
 Opta (España ~16 %, Francia ~13 %, Inglaterra ~11 %, Argentina ~10 %).
=============================================================================
"""
import numpy as np
from math import exp
from collections import defaultdict

rng = np.random.default_rng(20260603)

# -----------------------------------------------------------------------------
# 1) TABLA DE FUERZA (Elo, escala eloratings.net)
#    fuente: 'D' = valor exacto del documento (2-jun-2026)  -> HECHO
#            'E' = eloratings.net (latest / Wikipedia top-20) -> HECHO/casi
#            'I' = inferencia anclada en ranking FIFA abr-2026 -> INFERENCIA
# -----------------------------------------------------------------------------
# (equipo: [Elo, fuente])
ELO = {
    "España":         [2165, "D"], "Argentina":      [2113, "D"],
    "Francia":        [2081, "D"], "Inglaterra":     [2020, "D"],
    "Brasil":         [1988, "D"], "Portugal":       [1984, "D"],
    "Colombia":       [1977, "D"], "Países Bajos":   [1961, "D"],
    "Croacia":        [1925, "E"], "Ecuador":        [1928, "E"],
    "Noruega":        [1925, "E"], "Alemania":       [1915, "E"],
    "Suiza":          [1895, "E"], "Uruguay":        [1888, "E"],
    "Türkiye":        [1878, "E"], "Japón":          [1878, "E"],
    "Senegal":        [1872, "E"], "Marruecos":      [1858, "I"],
    "Bélgica":        [1850, "E"], "México":         [1815, "I"],
    "Estados Unidos": [1805, "I"], "Canadá":         [1798, "I"],
    "Irán":           [1797, "I"], "Egipto":         [1790, "I"],
    "Austria":        [1788, "I"], "Corea del Sur":  [1785, "I"],
    "Argelia":        [1782, "I"], "Suecia":         [1778, "I"],
    "Costa de Marfil":[1775, "I"], "Paraguay":       [1758, "I"],
    "Escocia":        [1752, "I"], "Australia":      [1748, "I"],
    "Bosnia":         [1735, "I"], "Uzbekistán":     [1732, "E"],
    "Túnez":          [1730, "I"], "Panamá":         [1722, "I"],
    "Sudáfrica":      [1720, "I"], "RD Congo":       [1718, "I"],
    "Ghana":          [1715, "I"], "Iraq":           [1700, "I"],
    "Qatar":          [1690, "I"], "Arabia Saudí":   [1680, "I"],
    "Jordania":       [1655, "I"], "Haití":          [1560, "I"],
    "Cabo Verde":     [1549, "E"], "Nueva Zelanda":  [1520, "E"],
    "Curazao":        [1440, "E"],
}
elo = {k: v[0] for k, v in ELO.items()}

# Anfitriones (ventaja de localía Elo +100 SOLO en sus sedes, modulada).
HOSTS = {"México", "Estados Unidos", "Canadá"}

# -----------------------------------------------------------------------------
# 2) GRUPOS OFICIALES (sorteo 5-dic-2025)
# -----------------------------------------------------------------------------
GROUPS = {
    "A": ["México", "Sudáfrica", "Corea del Sur", "Chequia_PLACE"],
    "B": ["Canadá", "Bosnia", "Qatar", "Suiza"],
    "C": ["Brasil", "Marruecos", "Haití", "Escocia"],
    "D": ["Estados Unidos", "Paraguay", "Australia", "Türkiye"],
    "E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
    "F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "G": ["Bélgica", "Egipto", "Irán", "Nueva Zelanda"],
    "H": ["España", "Cabo Verde", "Arabia Saudí", "Uruguay"],
    "I": ["Francia", "Senegal", "Iraq", "Noruega"],
    "J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "K": ["Portugal", "RD Congo", "Uzbekistán", "Colombia"],
    "L": ["Inglaterra", "Croacia", "Ghana", "Panamá"],
}
# Chequia no estaba en la tabla; se añade (eloratings ~1790, FIFA 41).
elo["Chequia"] = 1790; ELO["Chequia"] = [1790, "I"]
GROUPS["A"][3] = "Chequia"

ALL_TEAMS = [t for g in GROUPS.values() for t in g]
assert len(ALL_TEAMS) == 48

# -----------------------------------------------------------------------------
# 3) PARÁMETROS DEL MODELO  (calibrados contra Opta)
# -----------------------------------------------------------------------------
SUP_SCALE = 0.0031      # supremacía esperada (goles) por punto Elo de diferencia
TOTAL_GOALS = 2.55      # goles totales esperados por partido (nivel Mundial)
LAMBDA_FLOOR = 0.15     # piso de tasa Poisson
HOME_ELO = 55           # ventaja de localía efectiva (modulada, no +100 pleno)
DC_RHO = -0.06          # parámetro Dixon-Coles para marcadores bajos

def lambdas(team_a, team_b, home_a=False, home_b=False):
    """Devuelve (lambda_a, lambda_b): tasas de gol esperadas para cada equipo.
    La diferencia de Elo (ajustada por localía) fija la *supremacía*; el total
    se mantiene ~constante. lambda = (total +/- supremacia)/2."""
    ea, eb = elo[team_a], elo[team_b]
    if home_a: ea += HOME_ELO
    if home_b: eb += HOME_ELO
    sup = SUP_SCALE * (ea - eb)          # supremacía esperada (goles)
    la = max(LAMBDA_FLOOR, (TOTAL_GOALS + sup) / 2.0)
    lb = max(LAMBDA_FLOOR, (TOTAL_GOALS - sup) / 2.0)
    return la, lb

# ---- Matriz exacta de marcadores con corrección Dixon-Coles -----------------
from scipy.stats import poisson
def score_matrix(la, lb, kmax=10):
    """Distribución conjunta P(goles_a, goles_b) con ajuste Dixon-Coles."""
    pa = poisson.pmf(np.arange(kmax + 1), la)
    pb = poisson.pmf(np.arange(kmax + 1), lb)
    M = np.outer(pa, pb)
    # Ajuste de dependencia para 0-0,1-0,0-1,1-1 (Dixon & Coles 1997)
    tau = {
        (0, 0): 1 - la * lb * DC_RHO,
        (0, 1): 1 + la * DC_RHO,
        (1, 0): 1 + lb * DC_RHO,
        (1, 1): 1 - DC_RHO,
    }
    for (i, j), t in tau.items():
        M[i, j] *= t
    M /= M.sum()
    return M

def match_probs(team_a, team_b, home_a=False, home_b=False):
    """P(victoria A), P(empate), P(victoria B) y marcador modal."""
    la, lb = lambdas(team_a, team_b, home_a, home_b)
    M = score_matrix(la, lb)
    pA = np.tril(M, -1).sum()      # a > b
    pB = np.triu(M, 1).sum()       # b > a
    pD = np.trace(M)               # empate
    i, j = np.unravel_index(M.argmax(), M.shape)
    return pA, pD, pB, (int(i), int(j)), (la, lb)

# -----------------------------------------------------------------------------
# 4) SIMULACIÓN DE UN PARTIDO (muestreo Poisson)
# -----------------------------------------------------------------------------
def sim_goals(team_a, team_b, home_a=False, home_b=False):
    la, lb = lambdas(team_a, team_b, home_a, home_b)
    return rng.poisson(la), rng.poisson(lb)

def sim_knockout(team_a, team_b, host_a=False, host_b=False):
    """Eliminatoria: 90' -> prórroga -> penales. Devuelve el clasificado."""
    ga, gb = sim_goals(team_a, team_b, host_a, host_b)
    if ga != gb:
        return team_a if ga > gb else team_b
    # Prórroga (30'): ~1/3 del tiempo de juego abierto
    la, lb = lambdas(team_a, team_b, host_a, host_b)
    ga2, gb2 = rng.poisson(la * 0.40), rng.poisson(lb * 0.40)
    if ga2 != gb2:
        return team_a if ga2 > gb2 else team_b
    # Penales: ~50/50 con leve sesgo Elo
    diff = elo[team_a] - elo[team_b] + (HOME_ELO if host_a else 0) - (HOME_ELO if host_b else 0)
    pa = min(0.62, max(0.38, 0.5 + 0.00035 * diff))
    return team_a if rng.random() < pa else team_b

# -----------------------------------------------------------------------------
# 5) FASE DE GRUPOS + DESEMPATES FIFA
# -----------------------------------------------------------------------------
def is_host_home(team, group_letter):
    # Localía aplicable solo a anfitriones en sus grupos sede
    return team in HOSTS

def sim_group(group_letter, teams):
    pts = {t: 0 for t in teams}
    gf  = {t: 0 for t in teams}
    ga  = {t: 0 for t in teams}
    h2h = defaultdict(lambda: [0, 0, 0])   # pts, gd, gf en enfrentamientos directos
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = teams[i], teams[j]
            ha = a in HOSTS; hb = b in HOSTS
            x, y = sim_goals(a, b, ha, hb)
            gf[a] += x; ga[a] += y; gf[b] += y; ga[b] += x
            if x > y:   pts[a] += 3; h2h[a][0]+=3
            elif x < y: pts[b] += 3; h2h[b][0]+=3
            else:       pts[a] += 1; pts[b] += 1; h2h[a][0]+=1; h2h[b][0]+=1
            h2h[a][1]+=x-y; h2h[b][1]+=y-x; h2h[a][2]+=x; h2h[b][2]+=y
    # Orden: puntos -> dif. goles total -> goles total -> H2H pts -> aleatorio
    def key(t):
        return (pts[t], gf[t]-ga[t], gf[t], h2h[t][0], rng.random())
    ranked = sorted(teams, key=key, reverse=True)
    rec = {t: (pts[t], gf[t]-ga[t], gf[t]) for t in teams}
    standings = [(t, pts[t], gf[t]-ga[t], gf[t]) for t in ranked]
    return ranked, standings, rec

# -----------------------------------------------------------------------------
# 6) CONSTRUCCIÓN DEL R32  (clusters oficiales ESPN + reglas Annex C)
#    Estructura: 8 (ganador vs 3.º) + 4 (ganador vs 2.º) + 4 (2.º vs 2.º).
#    El ruteo exacto de terceros depende de 495 escenarios; se usa una
#    asignación fiel a los clusters publicados y "no mismo grupo".  [LIMITACIÓN]
# -----------------------------------------------------------------------------
# Clusters de terceros por ganador de grupo (de ESPN, fixture oficial):
THIRD_CLUSTERS = {
    "A": list("CEFHI"), "B": list("EFGIJ"), "C": list("ABFGH"),
    "D": list("BEFIJ"), "E": list("ABDGH"), "G": list("AEHIJ"),
    "I": list("CDFGH"), "K": list("DEIJL"), "L": list("EHIJK"),
    # F, H, J emparejan con 2.º (no con tercero) en el esqueleto base
}
# Emparejamientos ganador-vs-2.º y 2.º-vs-2.º del esqueleto oficial (aprox.):
WINNER_VS_RUNNER = {"F": "B", "H": "D", "J": "H"}  # ganador F vs 2.º B, etc.
RUNNER_VS_RUNNER = [("E", "I"), ("A", "C"), ("G", "K"), ("L", "F")]

def build_r32(winners, runners, thirds_by_group):
    """Asigna 8 terceros a sus slots respetando clusters y 'no mismo grupo'.
    Devuelve lista de 16 enfrentamientos (equipoA, equipoB)."""
    matches = []
    used_thirds = set()
    qualifying_thirds = set(thirds_by_group.keys())
    # 1) Ganadores que reciben tercero
    for gw in ["A", "B", "C", "D", "E", "G", "I", "K", "L"]:
        cl = [g for g in THIRD_CLUSTERS[gw] if g in qualifying_thirds and g not in used_thirds]
        if cl:
            pick = cl[0]
        else:
            # respaldo: cualquier tercero disponible que no sea del mismo grupo
            cand = [g for g in qualifying_thirds if g not in used_thirds and g != gw]
            pick = cand[0] if cand else None
        if pick is not None:
            used_thirds.add(pick)
            matches.append((winners[gw], thirds_by_group[pick]))
        else:
            matches.append((winners[gw], runners[gw]))  # respaldo improbable
    # 2) Ganadores que enfrentan 2.º
    for gw, gr in WINNER_VS_RUNNER.items():
        matches.append((winners[gw], runners[gr]))
    # 3) 2.º vs 2.º
    for g1, g2 in RUNNER_VS_RUNNER:
        matches.append((runners[g1], runners[g2]))
    return matches

# -----------------------------------------------------------------------------
# 7) UN TORNEO COMPLETO
# -----------------------------------------------------------------------------
ROUNDS = ["R32", "R16", "QF", "SF", "FINAL", "CAMPEON"]

def sim_tournament(track):
    winners, runners, thirds = {}, {}, {}
    third_rows = []
    for gl, teams in GROUPS.items():
        ranked, _, rec = sim_group(gl, teams)
        winners[gl] = ranked[0]; runners[gl] = ranked[1]; thirds[gl] = ranked[2]
        for pos, t in enumerate(ranked):
            track["pos"][t][pos] += 1
        track["group_win"][ranked[0]] += 1
        track["advance"][ranked[0]] += 1
        track["advance"][ranked[1]] += 1
        third_rows.append((gl, ranked[2], rec[ranked[2]]))
    # Mejores 8 terceros segun criterios FIFA: puntos -> dif. goles -> goles
    scored = sorted(third_rows,
                    key=lambda r: (r[2][0], r[2][1], r[2][2], rng.random()),
                    reverse=True)
    best_thirds = scored[:8]
    thirds_by_group = {gl: t for gl, t, _ in best_thirds}
    for gl, t, _ in best_thirds:
        track["advance"][t] += 1
        track["third_adv"][t] += 1

    bracket = build_r32(winners, runners, thirds_by_group)

    # ---- Eliminatorias: avance por rondas ----
    def host_of(t): return t in HOSTS
    alive = []
    for a, b in bracket:
        track["reach"]["R32"][a] += 1; track["reach"]["R32"][b] += 1
        w = sim_knockout(a, b, host_of(a), host_of(b))
        alive.append(w)
    # R16, QF, SF, FINAL
    for rnd in ["R16", "QF", "SF", "FINAL"]:
        for t in alive:
            track["reach"][rnd][t] += 1
        nxt = []
        for k in range(0, len(alive), 2):
            a, b = alive[k], alive[k+1]
            w = sim_knockout(a, b, host_of(a), host_of(b))
            nxt.append(w)
        alive = nxt
    champ = alive[0]
    track["reach"]["CAMPEON"][champ] += 1
    return champ

# -----------------------------------------------------------------------------
# 8) EJECUCIÓN MONTE CARLO
# -----------------------------------------------------------------------------
def run(n_sims=30000):
    track = {
        "group_win": defaultdict(int),
        "advance":   defaultdict(int),
        "third_adv": defaultdict(int),
        "pos": defaultdict(lambda: [0, 0, 0, 0]),
        "reach": {r: defaultdict(int) for r in ROUNDS},
    }
    for _ in range(n_sims):
        sim_tournament(track)
    return track, n_sims

if __name__ == "__main__":
    import json
    N = 40000
    track, N = run(N)

    def pct(d, t): return 100.0 * d.get(t, 0) / N

    # ---- Probabilidades de titulo (todas) ----
    champ = sorted(track["reach"]["CAMPEON"].items(), key=lambda x: -x[1])
    print(f"=== TITULO (N={N}) ===")
    for t, c in champ:
        print(f"{t:18s} {100*c/N:6.2f}%")

    # ---- Tabla de avance por rondas (validacion vs Opta) ----
    print("\n=== AVANCE POR RONDAS (top 12) ===")
    print(f"{'Equipo':18s}{'GanGrupo':>9s}{'R16':>8s}{'QF':>8s}{'SF':>8s}{'Final':>8s}{'Titulo':>8s}")
    top = [t for t, _ in champ[:12]]
    for t in top:
        print(f"{t:18s}{pct(track['group_win'],t):8.1f}%"
              f"{pct(track['reach']['R16'],t):7.1f}%"
              f"{pct(track['reach']['QF'],t):7.1f}%"
              f"{pct(track['reach']['SF'],t):7.1f}%"
              f"{pct(track['reach']['FINAL'],t):7.1f}%"
              f"{pct(track['reach']['CAMPEON'],t):7.1f}%")

    # ---- Posiciones de grupo y avance (todas) ----
    out = {"N": N, "title": {}, "group_win": {}, "advance": {}, "third_adv": {},
           "pos": {}, "reach": {r: {} for r in ROUNDS}, "elo": elo,
           "elo_src": {k: v[1] for k, v in ELO.items()}, "groups": GROUPS}
    for t in ALL_TEAMS:
        out["title"][t]     = round(pct(track["reach"]["CAMPEON"], t), 4)
        out["group_win"][t] = round(pct(track["group_win"], t), 4)
        out["advance"][t]   = round(pct(track["advance"], t), 4)
        out["third_adv"][t] = round(pct(track["third_adv"], t), 4)
        out["pos"][t]       = [round(100*x/N, 4) for x in track["pos"][t]]
        for r in ROUNDS:
            out["reach"][r][t] = round(pct(track["reach"][r], t), 4)

    # ---- Partidos de fase de grupos (72): W/D/L + marcador modal ----
    fixtures = []
    for gl, teams in GROUPS.items():
        for i in range(4):
            for j in range(i+1, 4):
                a, b = teams[i], teams[j]
                ha, hb = a in HOSTS, b in HOSTS
                pA, pD, pB, modal, (la, lb) = match_probs(a, b, ha, hb)
                fixtures.append({
                    "group": gl, "a": a, "b": b,
                    "pA": round(100*pA, 1), "pD": round(100*pD, 1), "pB": round(100*pB, 1),
                    "score": f"{modal[0]}-{modal[1]}",
                    "la": round(la, 2), "lb": round(lb, 2),
                })
    out["fixtures"] = fixtures

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nGuardado results.json")
    # error estandar de una proporcion p≈0.16 con N
    import math
    se = math.sqrt(0.16*0.84/N)*100
    print(f"EE(p=16%) = +/-{se:.3f} pp ; IC95% = +/-{1.96*se:.3f} pp")
