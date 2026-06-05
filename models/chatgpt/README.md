# ChatGPT · modelo v6.2

Ensamble calibrado históricamente con los ajustes del **Backtesting Nivel 2** (núcleo FIFA/Elo reforzado + penalización de sesgo de mercado).

## Qué es

Fórmula de fuerza:

```
Strength_v6.2 =
  0.24 · FIFA-Elo
+ 0.20 · WorldFootballElo
+ 0.14 · SquadMarketTalent
+ 0.12 · PlayerLevelScore
+ 0.10 · RecentForm
+ 0.08 · AttackDefenseBalance
+ 0.05 · TournamentExperience
+ 0.04 · ClimateAltitudeFit
+ 0.03 · UpsetRobustness
```

Probabilidad por fase: Monte Carlo + calibración histórica con un nuevo término anti-sesgo de mercado (θ · MarketSkewPenalty), bajo la restricción de masa Σ por fase = 32 / 16 / 8 / 4 / 2 / 1.

## Hallazgos del Backtesting Nivel 1 (Mundiales 2010, 2014, 2018, 2022)

| Métrica | Resultado |
|---|---:|
| Campeón real en Top 4 | 4/4 |
| Campeón real en Top 8 | 4/4 |
| Finalistas en Top 8 | 7/8 |
| Semifinalistas en Top 12 | 15/16 |
| Cuartofinalistas en Top 8 | 21/32 |
| Octavofinalistas en Top 16 | 49/64 |

Núcleo FIFA/Elo sólido en la cúspide, pero el ranking/mercado subestima outsiders tácticos → de ahí la recalibración a v6.2.

## Honestidad metodológica

El propio reporte advierte que el Nivel 2 **no es un backtesting player-level completo**: eso exigiría reconstruir odds, valores de mercado y convocatorias pretorneo auditados año por año. La v6.2 es una evolución prudente, no una validación final estilo casa de apuestas.

## Estructura

```
chatgpt/
├── code/                                              ← scripts Python reproducibles (paquete de ChatGPT)
│   ├── README.md                                        instrucciones de ejecución
│   ├── ChatGPT_v6_2_Camino_Titulo_48_Selecciones.py    reproduce la tabla camino al título (48)
│   ├── ChatGPT_v6_2_Pronostico_72_Partidos_Fase_Grupos.py  reproduce los 72 partidos
│   ├── ChatGPT_v6_Backtesting_Nivel_1.py                reproduce el backtest Nivel 1
│   └── ChatGPT_v6_Backtesting_Nivel_2_Metodologico.py   reproduce el reporte Nivel 2
└── forecasts/                                          ← reportes narrativos consolidados
    ├── ChatGPT_Camino_al_Titulo_v6_2_Completo.md
    ├── ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6_2.md
    └── ChatGPT_Backtesting_Nivel_2_Reporte_Final_Modelo_v6.md
```

## Reproducir

```bash
pip install pandas tabulate

python code/ChatGPT_v6_2_Camino_Titulo_48_Selecciones.py
python code/ChatGPT_v6_2_Pronostico_72_Partidos_Fase_Grupos.py
python code/ChatGPT_v6_Backtesting_Nivel_1.py
python code/ChatGPT_v6_Backtesting_Nivel_2_Metodologico.py
```
