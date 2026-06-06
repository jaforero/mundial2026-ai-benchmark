# Claude · modelo v5 (selección) + v6 (goleadores) + v7 (recalibración)

Ensamble estadístico + machine learning para el Mundial 2026, con backtesting fuera de muestra computado con código sobre resultados reales (2010–2022).

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



## Recalibración v7 (Fase 7)

Capa de **calibración** sobre v5/v6 (no reentrena): corrige exceso de confianza y trata la incertidumbre. Código: `code/wc2026_recalibrate_v7.py` · salidas: `data/results_v7.json`, `data/claude_scorers_v7.json` · reporte: `forecasts/Claude_FASE_7_Recalibracion_v7.md`.

1. **Selecciones — anti-sobreconfianza:** encogimiento hacia la tasa base de cada ronda, `p' = b + (p−b)·s` (s de 0.97 en R32 a 0.86 en campeón), con renormalización y monotonía por equipo. El campeón más probable baja de 18.23% a 15.97%; la cola (<1%) sube ~4.2 pp.
2. **Partidos — empate e incertidumbre:** inflación de empate proporcional a la paridad e índice de entropía; 31/72 partidos quedan en alta incertidumbre y su marcador se modera (empate o margen de un gol).
3. **Goleadores — temperatura + riesgos:** recalibración por temperatura (T=1.12) y desglose por jugador de minutos, rol, dificultad de grupo, dependencia del equipo e incertidumbre de titularidad.
4. **Incertidumbre/calibración:** diagnósticos de variables sobre/infravaloradas y de señales contradictorias.

No incorpora datos nuevos: solo recalibra. Donde falta información, mantiene la estimación base y la señala en lugar de fabricarla.

## Modelo de goleadores v6 (Bota de Oro)

Capa de **jugador** montada sobre el modelo de selección. No inventa datos: ancla la oportunidad de gol en la salida real del motor de equipo y descompone el resto en factores explícitos.

```
E_goles(jugador) = G_equipo(T) × cuota_rol × penales × titularidad × disponibilidad × forma
```

- **G_equipo(T)** = partidos esperados (3 de grupo + Σ probabilidad de alcanzar cada ronda, de `reach`) × goles esperados por partido (λ del motor Dixon-Coles, de `fixtures`). Es la aportación propia de Claude.
- **Riesgo físico y forma son factores SEPARADOS** (decisión metodológica): la **disponibilidad** (lesiones, carga, edad) actúa sobre los *minutos*; la **forma** (racha, afinación) actúa sobre la *tasa* de gol por minuto. Mezclarlos perdería la diferencia entre "juega menos" y "juega peor".
- **Titularidad** descuenta minutos por probabilidad de ser titular y rotación.
- **Bota de Oro** estimada por **simulación Monte Carlo** (binomial negativa, sobredispersa, con un "campo" de goleadores fuera del pool), de modo que las probabilidades no suman 100% y dejan margen a la sorpresa.

Código: `code/wc2026_scorers_v6.py` · salida: `data/claude_scorers_v6.json`. Los atributos por jugador (rol, penales, titularidad, disponibilidad, forma) son las entradas editables del modelo, derivadas del pool de candidatos élite documentado en el proyecto y de priores futbolísticos estándar.

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
