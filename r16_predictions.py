# -*- coding: utf-8 -*-
"""
Módulo de OCTAVOS (M89–M96) · Benchmark IA Mundial 2026
========================================================
Prepara y carga el nuevo pronóstico de las 3 IAs sobre el cuadro REAL de octavos.

Comandos:
  python scripts/r16_predictions.py prompt
      Genera el prompt estandarizado (idéntico para Claude, ChatGPT y Gemini) con el
      cuadro real de octavos ya formado. Pégalo en cada IA cuando cierren los 16avos.

  python scripts/r16_predictions.py load claude.json chatgpt.json gemini.json
      Valida las 3 respuestas, calcula el consenso (mayoría 2/3 para clasificado y
      marcador; promedio de confianza) y las integra en data/consolidated.json
      (campos pred/cg/gm/cons de las llaves M89–M96, fase R16).

Esquema JSON que debe devolver cada IA (lista de 8 objetos):
  [{"code":"M89","a":"Paraguay","b":"Francia","sc90":"0-2","et":"No","pens":"No",
    "winner":"Francia","conf":78,
    "p90":{"a":14,"e":22,"b":64},        # probabilidades a 90' (suman 100)
    "p_adv":81}]                          # prob. de que 'winner' clasifique (0-100)
  - sc90: marcador a 90'; si empate, et/pens indican cómo se define ("Sí"/"No").
  - conf y p_adv en %, enteros. p90 opcional pero recomendado (se guarda para RPS).

Tras cargar, regenerar el sitio (site/build_compare.py) para que el tablero
"Mundial de las IAs" y las pestañas muestren y puntúen los octavos.
"""
import json, sys, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONSOLIDATED = os.path.join(ROOT, "data", "consolidated.json")
KO_RESULTS = os.path.join(ROOT, "ko_results.json")
R16_CODES = [f"M{i}" for i in range(89, 105)]  # octavos→final (M89-M104); el cuadro real (ko_real) valida qué llaves existen
FIELD = {"claude": "pred", "chatgpt": "cg", "gemini": "gm"}

def load_state():
    D = json.load(open(CONSOLIDATED, encoding="utf-8"))
    kr = {s["code"]: s for s in D.get("ko_real", [])}
    # refrescar cruces con los resultados más recientes si ko_results.json trae más llaves
    try:
        res = {r["code"]: r for r in json.load(open(KO_RESULTS, encoding="utf-8"))}
    except Exception:
        res = {r["code"]: r for r in D.get("ko_results", [])}
    win = {c: r["winner"] for c, r in res.items() if r.get("winner")}
    feeders = {"M89": ("M74", "M77"), "M90": ("M73", "M75"), "M91": ("M76", "M78"), "M92": ("M79", "M80"),
               "M93": ("M83", "M84"), "M94": ("M81", "M82"), "M95": ("M86", "M88"), "M96": ("M85", "M87"),
               "M97": ("M89", "M90"), "M98": ("M93", "M94"), "M99": ("M91", "M92"), "M100": ("M95", "M96"),
               "M101": ("M97", "M98"), "M102": ("M99", "M100"), "M103": ("M101", "M102"), "M104": ("M101", "M102")}
    for c in R16_CODES:
        s = kr.get(c)
        if not s or c not in feeders:
            continue
        f1, f2 = feeders[c]
        s["a"] = s.get("a") or win.get(f1)
        s["b"] = s.get("b") or win.get(f2)
        s["status"] = "formed" if s["a"] and s["b"] else ("partial" if s["a"] or s["b"] else "pending")
    return D, kr

def cmd_prompt():
    D, kr = load_state()
    ties, missing = [], []
    for c in R16_CODES:
        s = kr.get(c)
        if not s:
            continue
        if s["status"] == "formed":
            ties.append(f'  {c}: {s["a"]} vs {s["b"]}')
        else:
            f1 = s["sa"].replace("G-", "ganador de ")
            f2 = s["sb"].replace("G-", "ganador de ")
            a = s["a"] or f"({f1})"
            b = s["b"] or f"({f2})"
            ties.append(f'  {c}: {a} vs {b}   ← AÚN SIN DEFINIR')
            missing.append(c)
    warn = ""
    if missing:
        warn = (f"\n⚠️ Aviso: {len(missing)} llave(s) aún sin definir ({', '.join(missing)}). "
                "Lo ideal es generar este prompt cuando los 16 dieciseisavos hayan terminado.\n")
    prompt = f"""Eres un modelo de pronóstico deportivo. El Mundial FIFA 2026 cerró su fase de grupos y
sus dieciseisavos de final. Este es el CUADRO REAL de OCTAVOS DE FINAL (no una proyección):

{chr(10).join(ties)}
{warn}
Tu tarea: pronostica cada una de las 8 llaves usando toda la información disponible del torneo
(resultados reales de la fase de grupos y de los dieciseisavos, estado de forma, bajas, sedes).

Para CADA llave entrega:
1. Marcador a 90 minutos (sc90).
2. Si termina empatada a 90': ¿se define en prórroga (et) o penales (pens)?
3. Clasificado (winner) — debe ser uno de los dos equipos de la llave.
4. Probabilidades a 90' en % enteros que sumen 100: victoria A (p90.a), empate (p90.e), victoria B (p90.b).
5. Probabilidad de clasificación del winner (p_adv, 0-100).
6. Confianza global del pronóstico (conf, 0-100; usa p_adv como referencia).

Responde ÚNICAMENTE con un JSON válido (sin texto adicional), lista de 8 objetos con este esquema exacto:
[{{"code":"M89","a":"...","b":"...","sc90":"X-Y","et":"Sí|No","pens":"Sí|No","winner":"...","conf":NN,"p90":{{"a":NN,"e":NN,"b":NN}},"p_adv":NN}}]

Usa exactamente los nombres de equipo tal como aparecen en el cuadro de arriba.
No agregues claves extra ni envoltorios: la respuesta debe ser solo la lista de 8 objetos.
Explica tu metodología en un mensaje aparte solo si se te pide."""
    print(prompt)

_SC = re.compile(r"^\d{1,2}-\d{1,2}$")

def _validate(name, arr, kr, expected):
    errs = []
    if not isinstance(arr, list) or not arr:
        return [f"{name}: se esperaba una lista de llaves"]
    seen = set()
    for o in arr:
        c = o.get("code")
        if c not in R16_CODES: errs.append(f"{name} {c}: código inválido"); continue
        if c in seen: errs.append(f"{name} {c}: duplicado"); continue
        seen.add(c)
        s = kr[c]
        teams = {s.get("a"), s.get("b")} - {None}
        if teams and not teams.issubset({o.get("a"), o.get("b")}):
            errs.append(f"{name} {c}: equipos {o.get('a')}/{o.get('b')} no coinciden con el cuadro real {s.get('a')}/{s.get('b')}")
        if not _SC.match(str(o.get("sc90", ""))): errs.append(f"{name} {c}: sc90 inválido ({o.get('sc90')})")
        else:
            ga, gb = map(int, o["sc90"].split("-"))
            tie = ga == gb
            if tie and o.get("et") not in ("Sí", "Si", "No"): errs.append(f"{name} {c}: empate a 90' requiere et Sí/No")
            if not tie and (o.get("et") in ("Sí","Si") or o.get("pens") in ("Sí","Si")):
                errs.append(f"{name} {c}: sc90 {o['sc90']} no es empate pero marca prórroga/penales")
            if tie:
                w, wa = o.get("winner"), o.get("a")
                # ganador debe ser coherente con et/pens (no validable más allá de pertenencia)
        if o.get("winner") not in (o.get("a"), o.get("b")): errs.append(f"{name} {c}: winner fuera de la llave")
        cf = o.get("conf")
        if not (isinstance(cf, (int, float)) and 1 <= cf <= 99): errs.append(f"{name} {c}: conf fuera de rango")
        p = o.get("p90")
        if p:
            tot = (p.get("a", 0) + p.get("e", 0) + p.get("b", 0))
            if abs(tot - 100) > 1: errs.append(f"{name} {c}: p90 suma {tot}, debe sumar 100")
    if expected is not None and seen != expected:
        errs.append(f"{name}: llaves {sorted(seen)} no coinciden con las demás IAs {sorted(expected)}")
    return errs

def _consensus(preds):
    """preds: dict ia->obj para una llave. Mayoría 2/3; marcador = moda o el del ganador mayoritario."""
    ws = Counter(p["winner"] for p in preds.values())
    winner, votes = ws.most_common(1)[0]
    scs = Counter(p["sc90"] for p in preds.values())
    sc90, sc_votes = scs.most_common(1)[0]
    if sc_votes == 1:  # sin moda: mediana de goles por lado entre quienes votaron al ganador del consenso
        import statistics
        cands = [p for p in preds.values() if p["winner"] == winner] or list(preds.values())
        _hup = lambda x: int(x + 0.5)   # half-up: evita que el redondeo banker infle el margen con 2 votantes
        ga = _hup(statistics.median([int(p["sc90"].split("-")[0]) for p in cands]))
        gb = _hup(statistics.median([int(p["sc90"].split("-")[1]) for p in cands]))
        sc90 = f"{ga}-{gb}"
    ga, gb = map(int, sc90.split("-"))
    tie = ga == gb
    et = "Sí" if tie and Counter(p.get("et") for p in preds.values()).get("Sí", 0) >= 2 else ("Sí" if tie else "No")
    pens = "Sí" if tie and Counter(p.get("pens") for p in preds.values()).get("Sí", 0) >= 2 else "No"
    confs = [p.get("conf", 0) for p in preds.values() if p["winner"] == winner]
    conf = round(sum(confs) / max(len(confs), 1))
    out = {"sc90": sc90, "et": et if tie else "No", "pens": pens, "winner": winner, "conf": conf}
    p90s = [p["p90"] for p in preds.values() if p.get("p90")]
    if len(p90s) == len(preds):
        a = round(sum(x["a"] for x in p90s) / len(p90s)); e = round(sum(x["e"] for x in p90s) / len(p90s))
        out["p90"] = {"a": a, "e": e, "b": 100 - a - e}
    pas = [p.get("p_adv") for p in preds.values() if p.get("p_adv") is not None and p["winner"] == winner]
    if pas: out["p_adv"] = round(sum(pas) / len(pas))
    return out

def cmd_load(paths):
    if len(paths) != 3:
        print("Uso: load claude.json chatgpt.json gemini.json"); sys.exit(1)
    D, kr = load_state()
    ias = ["claude", "chatgpt", "gemini"]
    data, errs = {}, []
    expected = None
    for ia, p in zip(ias, paths):
        arr = json.load(open(p, encoding="utf-8"))
        errs += _validate(ia, arr, kr, expected)
        if expected is None: expected = {o.get("code") for o in arr if o.get("code") in R16_CODES}
        data[ia] = {o["code"]: o for o in arr if o.get("code") in R16_CODES}
    if errs:
        print("ERRORES DE VALIDACIÓN — no se guardó nada:")
        [print("  ✗", e) for e in errs]; sys.exit(1)
    strip = lambda o: {k: o[k] for k in ("sc90", "et", "pens", "winner", "conf", "p90", "p_adv") if k in o}
    loaded = sorted(expected, key=lambda c: int(c[1:]))
    for c in loaded:
        s = kr[c]
        preds = {ia: data[ia][c] for ia in ias}
        for ia in ias: s[FIELD[ia]] = strip(preds[ia])
        s["cons"] = _consensus(preds)
        # congelar equipos según lo entregado (ya validado contra el cuadro real)
        s["a"] = s["a"] or preds["claude"]["a"]
        s["b"] = s["b"] or preds["claude"]["b"]
        s["status"] = "formed" if s["a"] and s["b"] else s.get("status", "pending")
    json.dump(D, open(CONSOLIDATED, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"✓ Predicciones integradas en data/consolidated.json: {', '.join(loaded)} (pred/cg/gm/cons).")
    print("  Siguiente paso: regenerar index.html con site/build_compare.py para publicarlas.")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "prompt": cmd_prompt()
    elif cmd == "load": cmd_load(sys.argv[2:])
    else: print(__doc__)
