# Gemini · modelo v7 · Local Pressure Networks

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

## Backtesting reportado (v6, Mundiales 2010–2022)

| Métrica | v6 | Casas de apuestas |
|---|---:|---:|
| Brier Score | 0.192 | 0.205 |
| Log-Loss / entropía cruzada | 0.584 | — |

El backtesting reveló un sesgo de supervivencia ("enamorarse de la historia") que originó el Factor de Decaimiento del Campeón del v7.

## Estructura

```
gemini/
├── code/                                                ← código Python del modelo v7
│   ├── README.md                                          apéndice técnico matemático (ecuaciones LaTeX)
│   ├── Gemini_V7_Fase_Grupos_Poisson.py                   motor matemático: xG dinámico + Poisson bivariada (Dixon-Coles)
│   ├── Gemini_V7_CaminoMundial_MonteCarlo.py              simulador del árbol de eliminación directa (10.000 iteraciones)
│   └── Gemini_V7_Backtesting_Engine.py                    auditoría Brier Score + entropía cruzada vs Mundiales anteriores
└── forecasts/                                            ← reportes narrativos consolidados
    ├── Gemini_Predictivo_V7_Local_Pressure_Networks.md     camino al título 48 selecciones (v7)
    ├── Gemini_Pronostico_72_Partidos_Fase_Grupo_v7.md      72 partidos + apéndice técnico (v7)
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
