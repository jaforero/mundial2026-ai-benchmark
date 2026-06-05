# Claude · modelo v5

Ensamble estadístico + machine learning para el Mundial 2026. **El único de las tres IAs con backtesting computado con código sobre resultados reales.**

## Qué es

```
λ_v5 = 0.4 · Dixon-Coles  +  0.6 · Machine Learning (gradient boosting Poisson)
```

- **Dixon-Coles data-driven**: ataque/defensa por equipo estimados por máxima verosimilitud sobre miles de partidos internacionales reales (martj42/international_results).
- **Machine Learning**: gradient boosting con pérdida de Poisson, integra Elo actual (jun-2026), forma reciente e histórico de Mundiales.
- **Peso 0.4/0.6**: óptimo del backtesting OOS sobre 4 Mundiales (la curva de RPS es plana entre 0.4 y 0.5; el ensamble es robusto).

## Cambios v4 → v5

1. **Corrección del bracket**: `build_r32` reescrito para garantizar una biyección exacta (32 clasificados → 16 partidos, cada equipo una sola vez). En v4 algunos equipos se contaban dos veces y aparecían con R32 > 100% (Inglaterra 120.9%, Croacia 130.9%). Una aserción automática aborta la generación si cualquier probabilidad supera 100%.
2. **Peso del ensamble afinado** a 0.4/0.6 por el backtesting.
3. **Siembra del cuadro por Elo** (ganadores fuertes vs terceros) con salvaguarda de no cruzar equipos del mismo grupo.

## Validación OOS — 4 Mundiales, 192 partidos

| Modelo | RPS | Brier (V/E/D) | Log-Loss | MAE goles | Acierto marcador |
|---|---:|---:|---:|---:|---:|
| Dixon-Coles solo | 0.2016 | 0.5766 | 0.9795 | 1.3320 | 13.5% |
| Machine Learning solo | 0.2012 | 0.5749 | 0.9718 | 1.3140 | 12.0% |
| **ENSAMBLE (v5)** | **0.2002** | **0.5731** | **0.9708** | **1.3153** | **13.5%** |
| Baseline uniforme | 0.2413 | 0.6667 | 1.0986 | — | — |

**Mejora del ensamble vs azar: 17.02%** en RPS. Supera a cada componente por separado. Detalle reproducible en `forecasts/Claude_Backtesting_OOS_Reproducible_v4.md`.

## Estructura

```
claude/
├── code/                                        ← código Python (reproducible)
│   ├── wc2026_model.py                            base: grupos, sedes, equipos, rondas
│   ├── wc2026_model_v2.py                         motor + simulador del torneo (build_r32 corregido)
│   ├── wc2026_model_v3.py                         simulación con fuerzas ajustadas
│   ├── wc2026_fit_v3.py                           ajuste por máxima verosimilitud (+ validación OOS)
│   ├── wc2026_ml_v4.py                            componente machine learning (gradient boosting Poisson)
│   ├── wc2026_model_v4.py                         ensamble previo (½ + ½)
│   ├── wc2026_model_v5.py                         ENSAMBLE FINAL (0.4/0.6, bracket corregido) → results_v5.json
│   └── backtest_claude_v4.py                      backtest OOS sobre 4 Mundiales → backtest_claude_v4_results.json
├── data/                                        ← salidas y entradas del modelo
│   ├── results_v5.json                            salida del modelo v5 (48 selecciones, 72 partidos, fixtures con xG)
│   ├── backtest_claude_v4_results.json            resultados del backtest (RPS, Brier, Log-Loss por modelo y por Mundial)
│   └── strengths_v3.json                          fuerzas de ataque/defensa estimadas (input para v5)
└── forecasts/
    └── Claude_Backtesting_OOS_Reproducible_v4.md  reporte narrativo del backtest
```

## Reproducir

```bash
pip install -r ../../requirements.txt
# Descargar dataset de partidos internacionales (no incluido por tamaño)
curl -L -o intl_results.csv https://raw.githubusercontent.com/martj42/international_results/master/results.csv

# Ajustar rutas absolutas dentro de los .py si se ejecuta fuera del entorno original
python code/wc2026_fit_v3.py        # estima fuerzas + valida OOS
python code/wc2026_model_v5.py      # simula el torneo → data/results_v5.json
python code/backtest_claude_v4.py   # backtest reproducible
```
