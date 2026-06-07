# Gemini · modelo v10 (Fase 10 · ancla empírica 21.88% · Local Pressure Networks)

Ensamble físico-estadístico que **abandona la memoria histórica de los escudos** del v6 y mide la resiliencia por la carga de estrés cognitivo actual de la plantilla.

## Qué es

Cadena de modelado:

```
xG_base   = λ₀ · exp( β₁·ΔElo − β₂·Lesiones + β₃·ValorPlantilla )
xG_termo  = xG_base · e^(−κ·(UTCI − 28)) · [1 − α·max(0, altitud − 1500)]
xG_V7     = xG_termo · (1 + ρ_LPN) · (1 − δ_campeón) · ω_local
P(x,y)    = Poisson(xG_V7_A) · Poisson(xG_V7_B)
```

Tres vectores contemporáneos:

- **ρ_LPN** (Red de Presión Local) = minutos de los titulares 25/26 jugados bajo PPDA muy bajo en fases KO de Champions/Libertadores.
- **δ_campeón** (Factor de Decaimiento del Campeón) = penalización de hasta 8% al campeón vigente (Argentina).
- **ω_local** (Aura de Localía Asimétrica) = castiga a México (hiper-tensión mediática), premia a EE.UU./Canadá (entornos controlados).

Sobre estos vectores se mantiene el motor bio-termodinámico UTCI del v6.

**Recalibración Fase 8 (v8):** regresión isotónica anti-sobreconfianza, parámetro de empates ρ dinámico, matriz bayesiana de inactividad para el nuevo **Top 10 de goleadores** (Bota de Oro), y reversión al promedio de confederación donde faltan datos (sin inventar parámetros).

**Recalibración empírica Fase 9 (v9):** calibración por *Temperature Scaling* (T=1.12) que aplana las probabilidades (ningún equipo supera ~17% de título y mejora el RPS fuera de muestra); parámetro de empates ρ anclado a la **tasa empírica de empates de los Mundiales 1998–2022 (~25.4%)**; minutos de goleadores por **distribución Beta** con cortes de reportes clínicos a junio de 2026.

**Recalibración Fase 10 (v10):** auditoría de muestreo. Revisa la ventana de empates y adopta el **ancla del 21.88%** (tasa real de la fase de grupos 2010–2022, alineada con el backtest de Claude). En lugar de inflar empates como v9, los **desinfla**, premiando marginalmente a las potencias tácticas. Aplica filtros de inactividad clínica en goleadores (excluye a Darwin Núñez por desacondicionamiento).

## Backtesting reportado (v6, Mundiales 2010–2022)

| Métrica | v6 | Casas de apuestas |
|---|---:|---:|
| Brier Score | 0.192 | 0.205 |
| Log-Loss / entropía cruzada | 0.584 | — |

El backtesting reveló un sesgo de supervivencia ("enamorarse de la historia") que originó el Factor de Decaimiento del Campeón del v7.

## Estructura

```
gemini/
├── code/                                                ← código Python del modelo
│   ├── README.md                                          apéndice técnico matemático (ecuaciones LaTeX)
│   ├── Gemini_v10_Simulador_Selecciones.py / _Partidos.py / _Goleadores.py / _Auditoria_Incertidumbre.py                   código v8: selecciones, partidos, goleadores y calibración
│   ├── Gemini_V7_Fase_Grupos_Poisson.py                   motor xG dinámico + Poisson bivariada (Dixon-Coles)
│   ├── Gemini_V7_CaminoMundial_MonteCarlo.py              simulador del árbol de eliminación directa
│   └── Gemini_V7_Backtesting_Engine.py                    auditoría Brier Score + entropía cruzada
└── forecasts/                                            ← reporte consolidado v8
    ├── Gemini_Pronostico_Completo_v10.md                   48 selecciones + 72 partidos + Top 10 goleadores + apéndice + código
    └── Gemini_Backtesting_y_Validacion_Estadistica_v6.md   reporte de backtesting (v6)
```

## Reproducir

```bash
pip install numpy pandas scipy scikit-learn

# Integrar los datos de equipos en un DataFrame estándar antes de instanciar los simuladores
python code/Gemini_V7_Fase_Grupos_Poisson.py
python code/Gemini_V7_CaminoMundial_MonteCarlo.py
python code/Gemini_V7_Backtesting_Engine.py
```
