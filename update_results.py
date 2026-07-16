# -*- coding: utf-8 -*-
"""
Actualiza results.json (fase de grupos) y ko_results.json (eliminatorias) con los
marcadores oficiales más recientes, sin intervención manual.

Fuente: openfootball/worldcup.json — datos de dominio público, SIN API key ni límites.
  https://github.com/openfootball/worldcup.json  (archivo 2026/worldcup.json)

Qué hace:
  1. Descarga el feed de openfootball.
  2. Traduce los nombres de equipo (inglés -> nombres canónicos del proyecto) con scripts/name_map.json.
  3. GRUPOS: rellena ga/gb de cada partido ya jugado (score.ft) en results.json (orientación a/b).
  4. ELIMINATORIAS: a partir de cada partido knockout del feed (round = Round of 32/16, Quarter-final,
     Semi-final, Final, Match for third place) genera ko_results.json con {code, ga, gb, winner, fecha, venue}.
     El número de partido del feed (num) corresponde 1:1 al código del proyecto: num 73 -> "M73".
     El marcador ga/gb es el de los 90' (score.ft); el ganador considera prórroga (et) y penales (p).
  5. Solo reescribe cada archivo si hubo cambios (commit limpio del Action).

Uso local:  python scripts/update_results.py
En CI:      lo ejecuta .github/workflows/update-results.yml de forma programada.
"""
import json, sys, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "results.json")
KO_RESULTS = os.path.join(ROOT, "ko_results.json")
CONSOLIDATED = os.path.join(ROOT, "data", "consolidated.json")
NAME_MAP = os.path.join(HERE, "name_map.json")
SCHEDULE = os.path.join(ROOT, "data", "wc_schedule.json")
FEED_URL = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"

KO_ROUNDS = {"Round of 32", "Round of 16", "Quarter-final", "Semi-final",
             "Final", "Match for third place"}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def log(*a): print(*a, file=sys.stderr)

def fetch_feed():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "mundial-ia-benchmark/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def fmt_date(s):
    try:
        y, m, d = s.split("-")
        return f"{int(d)} {MONTHS[int(m) - 1]}"
    except Exception:
        return s or ""

# ---------------------------------------------------------------- FASE DE GRUPOS
def update_groups(feed, canon):
    data = json.load(open(RESULTS, encoding="utf-8"))
    rows = data["results"] if isinstance(data, dict) else data   # results.json real = lista plana
    sched = {}
    try:
        sched = json.load(open(SCHEDULE, encoding="utf-8"))
    except Exception:
        pass

    def skey(a, b): return "|".join(sorted((a, b)))

    finals = {}
    for m in feed.get("matches", []):
        sc = m.get("score") or {}
        ft = sc.get("ft")
        if not ft or len(ft) != 2:
            continue
        a, b = canon(m.get("team1", "")), canon(m.get("team2", ""))
        finals[frozenset((a, b))] = (a, b, int(ft[0]), int(ft[1]))

    changed = 0
    for row in rows:
        e = sched.get(skey(row["a"], row["b"]))
        if e:
            if not row.get("kickoff") and e.get("kickoff"): row["kickoff"] = e["kickoff"]; changed += 1
            if not row.get("venue") and e.get("venue"): row["venue"] = e["venue"]; changed += 1
        if row.get("ga") is not None and row.get("gb") is not None:
            continue
        key = frozenset((row["a"], row["b"]))
        if key not in finals:
            continue
        fa, fb, g1, g2 = finals[key]
        ga, gb = (g1, g2) if fa == row["a"] else (g2, g1)
        row["ga"], row["gb"] = ga, gb
        changed += 1
        log(f"+ grupo: {row['a']} {ga}-{gb} {row['b']}  ({row.get('fecha','')})")

    if changed:
        if isinstance(data, dict):
            from datetime import datetime, timezone
            data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with open(RESULTS, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        log(f"results.json actualizado: {changed} cambio(s).")
    return changed > 0

# ----------------------------------------------------------------- ELIMINATORIAS
def update_knockouts(feed, canon):
    # orientación a/b de cada llave (si ko_real ya tiene la entrada, p.ej. los 16 de R32)
    ko_real = {}
    try:
        D = json.load(open(CONSOLIDATED, encoding="utf-8"))
        ko_real = {s["code"]: s for s in D.get("ko_real", [])}
    except Exception as e:
        log(f"aviso: no se pudo leer consolidated.json ({e}); se usa la orientación del feed.")

    try:
        existing = json.load(open(KO_RESULTS, encoding="utf-8"))
        if not isinstance(existing, list): existing = []
    except Exception:
        existing = []

    out = {}
    for mm in feed.get("matches", []):
        rd = mm.get("round", "")
        num = mm.get("num")
        if rd not in KO_ROUNDS or not num:
            continue
        sc = mm.get("score") or {}
        ft = sc.get("ft")
        if not ft or len(ft) != 2:
            continue  # aún no jugado
        code = "M%d" % int(num)
        t1, t2 = canon(mm.get("team1", "")), canon(mm.get("team2", ""))
        g1, g2 = int(ft[0]), int(ft[1])
        p, et = sc.get("p"), sc.get("et")
        via, x1, x2 = None, None, None
        # ganador: 90' decisivo, si no prórroga, si no penales
        if g1 > g2:
            win = t1
        elif g2 > g1:
            win = t2
        else:
            if p and len(p) == 2 and p[0] != p[1]:
                win = t1 if p[0] > p[1] else t2
                via, x1, x2 = "pen", int(p[0]), int(p[1])
            elif et and len(et) == 2 and et[0] != et[1]:
                win = t1 if et[0] > et[1] else t2
                via, x1, x2 = "et", int(et[0]), int(et[1])
            else:
                continue  # empate sin desempate registrado: esperar al feed
        # orientar ga/gb (y el marcador del desempate) al orden a/b del proyecto
        s = ko_real.get(code)
        if s and {canon(s.get("a") or ""), canon(s.get("b") or "")} == {t1, t2}:
            if canon(s.get("a") or "") == t1:
                a, b, ga, gb = t1, t2, g1, g2
            else:
                a, b, ga, gb = t2, t1, g2, g1
                if via: x1, x2 = x2, x1
        else:
            a, b, ga, gb = t1, t2, g1, g2
        # Se escriben a/b explícitamente: sin ellos el consumidor no puede saber a qué
        # orientación corresponde ga/gb y el marcador acaba invertido (feed vs cuadro canónico).
        row = {"code": code, "a": a, "b": b, "ga": ga, "gb": gb, "winner": win,
               "fecha": fmt_date(mm.get("date", "")), "venue": mm.get("ground", "")}
        if via:
            row["via"] = via
            row["xsc"] = f"{x1}-{x2}"
        out[code] = row

    new_list = [out[c] for c in sorted(out, key=lambda c: int(c[1:]))]
    if new_list != existing:
        with open(KO_RESULTS, "w", encoding="utf-8") as f:
            json.dump(new_list, f, ensure_ascii=False, indent=1)
        for r in new_list:
            log(f"+ KO: {r['code']} {r['ga']}-{r['gb']} -> {r['winner']}")
        log(f"ko_results.json actualizado: {len(new_list)} llave(s).")
        return True
    return False

def main():
    name_map = json.load(open(NAME_MAP, encoding="utf-8"))
    def canon(t): return name_map.get(t, t)
    feed = fetch_feed()
    g = update_groups(feed, canon)
    k = update_knockouts(feed, canon)
    if g or k:
        print("CHANGED")
    else:
        log("Sin cambios: no hay partidos nuevos.")
        print("NOCHANGE")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"ERROR: {e}")
        print("ERROR")
