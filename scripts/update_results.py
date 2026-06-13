# -*- coding: utf-8 -*-
"""
Actualiza results.json con los marcadores oficiales más recientes, sin intervención manual.

Fuente: openfootball/worldcup.json — datos de dominio público, SIN API key ni límites.
  https://github.com/openfootball/worldcup.json  (archivo 2026/worldcup.json)

Qué hace:
  1. Descarga el feed de openfootball.
  2. Traduce los nombres de equipo (inglés -> nombres canónicos del proyecto) con scripts/name_map.json.
  3. Rellena ga/gb de cada partido YA JUGADO (score.ft) en results.json, respetando la orientación a/b.
  4. Solo reescribe results.json si hubo cambios (para que el commit del Action sea limpio).

Uso local:  python scripts/update_results.py
En CI:      lo ejecuta .github/workflows/update-results.yml de forma programada.

Devuelve código de salida 0 siempre; imprime "CHANGED" si modificó el archivo (útil para el workflow).
"""
import json, sys, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESULTS = os.path.join(ROOT, "results.json")
NAME_MAP = os.path.join(HERE, "name_map.json")
FEED_URL = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"

def log(*a): print(*a, file=sys.stderr)

def fetch_feed():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "mundial-ia-benchmark/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

SCHEDULE = os.path.join(ROOT, "data", "wc_schedule.json")

def main():
    name_map = json.load(open(NAME_MAP, encoding="utf-8"))
    results = json.load(open(RESULTS, encoding="utf-8"))
    feed = fetch_feed()
    # calendario local (fecha/hora/sede reales) para completar campos faltantes
    sched = {}
    try:
        sched = json.load(open(SCHEDULE, encoding="utf-8"))
    except Exception:
        pass

    def canon(t): return name_map.get(t, t)
    def skey(a, b): return "|".join(sorted((a, b)))

    # marcadores finales del feed, indexados por par de equipos canónico
    finals = {}
    for m in feed.get("matches", []):
        sc = m.get("score") or {}
        ft = sc.get("ft")
        if not ft or len(ft) != 2:        # aún no jugado / sin marcador final
            continue
        a, b = canon(m.get("team1", "")), canon(m.get("team2", ""))
        finals[frozenset((a, b))] = (a, b, int(ft[0]), int(ft[1]))

    changed = 0
    for row in results.get("results", []):
        # completar hora/sede reales si faltan (no cuenta como cambio de resultado)
        e = sched.get(skey(row["a"], row["b"]))
        if e:
            if not row.get("kickoff") and e.get("kickoff"): row["kickoff"] = e["kickoff"]; changed += 1
            if not row.get("venue") and e.get("venue"): row["venue"] = e["venue"]; changed += 1
        if row.get("ga") is not None and row.get("gb") is not None:
            continue                       # ya cargado, no tocar el marcador
        key = frozenset((row["a"], row["b"]))
        if key not in finals:
            continue                       # todavía no hay marcador oficial
        fa, fb, g1, g2 = finals[key]
        ga, gb = (g1, g2) if fa == row["a"] else (g2, g1)   # orientar a la orden a/b del proyecto
        row["ga"], row["gb"] = ga, gb
        changed += 1
        log(f"+ {row['a']} {ga}-{gb} {row['b']}  ({row.get('fecha','')})")

    if changed:
        from datetime import datetime, timezone
        results["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with open(RESULTS, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=1)
        log(f"results.json actualizado: {changed} partido(s) nuevos.")
        print("CHANGED")
    else:
        log("Sin cambios: no hay partidos nuevos con marcador final.")
        print("NOCHANGE")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"ERROR: {e}")
        # salir 0 para no marcar el workflow en rojo por una caída temporal del feed
        print("ERROR")
