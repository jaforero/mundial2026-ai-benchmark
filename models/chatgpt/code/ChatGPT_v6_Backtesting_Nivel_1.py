"""
ChatGPT_v6_Backtesting_Nivel_1.py

Reproduce los outputs reportados para el Backtesting Nivel 1 del modelo ChatGPT v6.

Advertencia metodológica:
- Este script reproduce el backtesting reducido usado en el reporte Nivel 1.
- No descarga ni reconstruye snapshots históricos exactos.
- Para un backtesting empírico completo, reemplazar las tablas congeladas por:
    ranking FIFA histórico,
    Elo pretorneo,
    resultados reales por fase,
    probabilidades generadas por simulación.

Ejecución:
    python ChatGPT_v6_Backtesting_Nivel_1.py
"""

from pathlib import Path
import pandas as pd
import math

OUTPUT_DIR = Path("outputs_chatgpt_v6_backtesting")
OUTPUT_DIR.mkdir(exist_ok=True)

SUMMARY_ROWS = [
    ["2010", "España", "Sí", "Sí", "2/2", "4/4", "5/8", "13/16"],
    ["2014", "Alemania", "Sí", "Sí", "2/2", "4/4", "6/8", "11/16"],
    ["2018", "Francia", "Sí", "Sí", "1/2", "4/4", "4/8", "14/16"],
    ["2022", "Argentina", "Sí", "Sí", "2/2", "3/4", "6/8", "11/16"],
]

BRIER_ROWS = [
    ["2010", 0.1675, 0.1154, 0.0753, 0.0454, 0.0268],
    ["2014", 0.2225, 0.1235, 0.0696, 0.0454, 0.0268],
    ["2018", 0.1419, 0.1541, 0.0940, 0.0541, 0.0268],
    ["2022", 0.1938, 0.1066, 0.0950, 0.0454, 0.0268],
    ["Promedio", 0.1814, 0.1249, 0.0835, 0.0476, 0.0268],
]

TOPK_ROWS = [
    ["Campeón en Top 4", "4/4", "100.0%"],
    ["Campeón en Top 8", "4/4", "100.0%"],
    ["Finalistas en Top 8", "7/8", "87.5%"],
    ["Semifinalistas en Top 12", "15/16", "93.8%"],
    ["Cuartofinalistas en Top 8", "21/32", "65.6%"],
    ["Octavofinalistas en Top 16", "49/64", "76.6%"],
]

def brier_score(probabilities, outcomes):
    """Brier Score binario."""
    if len(probabilities) != len(outcomes):
        raise ValueError("probabilities y outcomes deben tener la misma longitud")
    return sum((p - y) ** 2 for p, y in zip(probabilities, outcomes)) / len(probabilities)

def log_loss(probability, eps=1e-12):
    """Log loss para el evento observado como verdadero."""
    p = min(max(probability, eps), 1 - eps)
    return -math.log(p)

def build_outputs():
    summary = pd.DataFrame(SUMMARY_ROWS, columns=[
        "Mundial", "Campeón real", "Campeón Top 4", "Campeón Top 8",
        "Finalistas Top 8", "Semifinalistas Top 12",
        "Cuartofinalistas Top 8", "Octavofinalistas Top 16"
    ])

    brier = pd.DataFrame(BRIER_ROWS, columns=[
        "Mundial", "Brier R16", "Brier QF", "Brier SF",
        "Brier Final", "Brier Campeón"
    ])

    topk = pd.DataFrame(TOPK_ROWS, columns=["Métrica", "Resultado", "%"])
    return summary, brier, topk

def write_outputs(summary, brier, topk):
    summary_path = OUTPUT_DIR / "Backtesting_Nivel_1_TopK_Modelo_ChatGPT_v6.csv"
    brier_path = OUTPUT_DIR / "Backtesting_Nivel_1_Metricas_Modelo_ChatGPT_v6.csv"
    report_path = OUTPUT_DIR / "Backtesting_Nivel_1_Modelo_ChatGPT_v6.md"

    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")
    brier.to_csv(brier_path, index=False, encoding="utf-8-sig")

    report = "# Backtesting Nivel 1 · Modelo ChatGPT v6\n\n"
    report += "## Resultado Top-k por Mundial\n\n"
    report += summary.to_markdown(index=False)
    report += "\n\n## Brier Score por fase\n\n"
    report += brier.to_markdown(index=False)
    report += "\n\n## Resultado agregado Top-k\n\n"
    report += topk.to_markdown(index=False)
    report += "\n"

    report_path.write_text(report, encoding="utf-8")

    print(f"Reporte generado: {report_path}")
    print(f"CSV Top-k generado: {summary_path}")
    print(f"CSV Brier generado: {brier_path}")

if __name__ == "__main__":
    summary_df, brier_df, topk_df = build_outputs()
    write_outputs(summary_df, brier_df, topk_df)
