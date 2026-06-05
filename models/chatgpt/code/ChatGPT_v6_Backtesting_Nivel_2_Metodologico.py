"""
ChatGPT_v6_Backtesting_Nivel_2_Metodologico.py

Genera el reporte metodológico de Backtesting Nivel 2 y la fórmula recomendada v6.2.

Advertencia:
- El Nivel 2 completo requiere snapshots históricos auditados.
- Este script reproduce el reporte metodológico y la evolución de pesos v6.2.
- No declara métricas Brier/LogLoss Nivel 2 cerradas sin datos históricos completos.

Ejecución:
    python ChatGPT_v6_Backtesting_Nivel_2_Metodologico.py
"""

from pathlib import Path
import pandas as pd

OUTPUT_DIR = Path("outputs_chatgpt_v6_backtesting")
OUTPUT_DIR.mkdir(exist_ok=True)

WEIGHTS_V62 = [
    ["FIFA/Elo oficial", 0.24, "Núcleo estructural validado en Nivel 1"],
    ["World Football Elo", 0.20, "Rendimiento competitivo reciente"],
    ["Talento de plantilla", 0.14, "Mantener sin aumentar por riesgo de sesgo de mercado"],
    ["Player-level", 0.12, "Útil, pero no dominante sin XI auditado"],
    ["Forma reciente", 0.10, "Señal competitiva de corto/mediano plazo"],
    ["Ataque/defensa", 0.08, "Balance táctico moderado"],
    ["Experiencia", 0.05, "Valor en knockout y presión"],
    ["Clima/altitud", 0.04, "Contextual, no dominante en camino al título"],
    ["Robustez anti-sorpresa", 0.03, "Control de fragilidad de favoritos"],
]

def build_weights_table():
    return pd.DataFrame(WEIGHTS_V62, columns=["Componente", "Peso v6.2", "Justificación"])

def write_report(weights):
    csv_path = OUTPUT_DIR / "Backtesting_Nivel_2_Pesos_Modelo_ChatGPT_v6_2.csv"
    md_path = OUTPUT_DIR / "Backtesting_Nivel_2_Reporte_Final_Modelo_ChatGPT_v6.md"

    weights.to_csv(csv_path, index=False, encoding="utf-8-sig")

    report = """# Backtesting Nivel 2 · Modelo ChatGPT v6

## Reporte metodológico reproducible

Este reporte define la evolución de v6 hacia v6.2, incorporando capas de plantilla,
player-level, mercado, forma reciente, experiencia y robustez anti-sorpresa.

## Fórmula recomendada v6.2

```text
Strength_v6_2 =
  0.24 · FIFA_Elo_score
+ 0.20 · WorldFootballElo
+ 0.14 · SquadMarketTalent
+ 0.12 · PlayerLevelScore
+ 0.10 · RecentCompetitiveForm
+ 0.08 · AttackDefenseBalance
+ 0.05 · TournamentExperience
+ 0.04 · ClimateAltitudeFit
+ 0.03 · UpsetRobustness
```

## Pesos

"""
    report += weights.to_markdown(index=False)
    report += """

## Advertencia

Este Nivel 2 no declara métricas finales de Brier/LogLoss porque requiere snapshots
históricos completos de mercado, convocatorias, player-level, xG/xGA y odds pretorneo.
"""
    md_path.write_text(report, encoding="utf-8")

    print(f"Reporte generado: {md_path}")
    print(f"CSV pesos generado: {csv_path}")

if __name__ == "__main__":
    weights_df = build_weights_table()
    write_report(weights_df)
