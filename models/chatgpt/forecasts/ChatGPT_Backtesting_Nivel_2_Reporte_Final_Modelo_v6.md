# Backtesting Nivel 2 · Modelo ChatGPT v6

## Reporte final metodológico y técnico

**Modelo evaluado:** ChatGPT v6 · probabilidades por selección / camino al título  
**Extensión evaluada:** Backtesting Nivel 2  
**Mundiales objetivo:** 2010, 2014, 2018, 2022  
**Fecha del reporte:** 2026-06-05  
**Uso recomendado:** soporte metodológico para decidir si el modelo actual v6 debe evolucionar a una versión v6.2/v7 con variables player-level, plantillas, mercado, xG y clima.

---

# 1. Resumen ejecutivo

El **Backtesting Nivel 1** validó razonablemente el núcleo estructural del modelo ChatGPT v6:

```text
Ranking FIFA + Elo + localía simple + grupo real + calibración histórica
```

El resultado Nivel 1 fue fuerte en identificación de élites:

| Métrica | Resultado Nivel 1 | Lectura |
|---|---:|---|
| Campeón real en Top 4 | 4/4 | Muy fuerte |
| Campeón real en Top 8 | 4/4 | Muy fuerte |
| Finalistas en Top 8 | 7/8 | Fuerte |
| Semifinalistas en Top 12 | 15/16 | Muy fuerte |
| Cuartofinalistas en Top 8 | 21/32 | Medio |
| Octavofinalistas en Top 16 | 49/64 | Bueno |

El **Nivel 2** busca mejorar donde el Nivel 1 es más débil: octavos, cuartos, outsiders competitivos, equipos envejecidos, plantillas profundas, calidad por líneas, xG/xGA, valor de mercado, experiencia, lesiones y contexto.

Sin embargo, el Nivel 2 requiere una advertencia importante:

> **No es metodológicamente correcto declarar un backtesting player-level completo sin reconstruir snapshots históricos exactos previos a cada Mundial.**

Por tanto, este reporte entrega una evolución Nivel 2 en dos capas:

1. **Nivel 2-A: Validación metodológica extendida.**  
   Define variables, fuentes, fórmulas, riesgos y cómo se integran al modelo.

2. **Nivel 2-B: Recalibración recomendada para el modelo v6 actual.**  
   Ajusta el modelo actual sin inventar métricas históricas no calculadas.

La conclusión es clara:

> El modelo v6 debe conservar su núcleo FIFA/Elo/calibración histórica, pero debe evolucionar a un modelo **v6.2** con variables de plantilla, edad, mercado, xG/xGA y player-level. Aun así, la tabla actual de probabilidades no debe modificarse radicalmente hasta ejecutar un backtesting player-level completo con snapshots históricos auditados.

---

# 2. Alcance congelado del Backtesting Nivel 2

## 2.1 Variables añadidas frente al Nivel 1

| Variable | Descripción | Estado Nivel 2 |
|---|---|---|
| `squad_market_value` | Valor total de plantilla | Usar como proxy de talento |
| `avg_player_value` | Valor medio por jugador | Usar como proxy de calidad individual |
| `squad_age` | Edad promedio | Usar para fatiga / ciclo competitivo |
| `world_cup_experience` | Experiencia histórica y de jugadores | Usar con penalización por edad |
| `player_level_score` | Calidad por líneas | Usar si hay convocatorias auditadas |
| `attack_score` | Calidad ofensiva | Usar con xG/goles recientes |
| `defense_gk_score` | Defensa + portero | Usar con goles concedidos/xGA |
| `xG_xGA_proxy` | Rendimiento subyacente | Usar cuando hay cobertura confiable |
| `market_skew_penalty` | Penalización por sesgo de mercado | Necesaria para no sobreponderar Europa |
| `climate_context` | Clima/sede | Solo histórico si hay datos por sede/fecha |

## 2.2 Variables que NO deben incorporarse sin auditoría

| Variable | Riesgo |
|---|---|
| Lesiones históricas no verificadas | Alto riesgo de sesgo retrospectivo |
| XI titulares reconstruidos manualmente | Alto costo y posible leakage |
| Valor de mercado tomado después del torneo | Leakage severo |
| xG posterior usado como predictor | Leakage si no corresponde a datos pretorneo |
| Narrativas post-torneo | Sesgo retrospectivo |
| Odds tomadas después del sorteo o partido | Leakage si no se congela fecha |

---

# 3. Fuentes recomendadas y verificadas

## 3.1 Resultados históricos

OpenFootball publica datos abiertos de Mundiales en JSON bajo licencia CC0. Es una fuente útil para reconstruir partidos, grupos, marcadores y fases alcanzadas.

**Fuente:** https://github.com/openfootball/worldcup.json

## 3.2 Ranking FIFA histórico

Dato-Futbol mantiene un repositorio con ranking FIFA masculino histórico desde diciembre de 1992 hasta septiembre de 2024, con el archivo `ranking_fifa_historical.csv`.

**Fuente:** https://github.com/Dato-Futbol/fifa-ranking

## 3.3 Elo histórico

World Football Elo Ratings permite reconstruir ratings históricos/pretorneo y se usa como señal de fuerza competitiva acumulada.

**Fuente:** https://www.eloratings.net/

## 3.4 Plantillas y mercado

Transfermarkt publica rankings de selecciones por valor de mercado y datos agregados de plantillas. Es útil, pero debe usarse con cautela porque el valor de mercado está sesgado hacia jugadores en clubes europeos y mercados más líquidos.

**Fuente:** https://www.transfermarkt.com/marktwertetop/wertvollstenationalmannschaften

## 3.5 Convocatorias y listas de jugadores

FIFA y Reuters publican listados de convocatorias y plantillas. Para 2026, FIFA mantiene una página de anuncios de convocatorias y Reuters publica listados de squads finales.

**Fuentes:**

- https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/all-world-cup-squad-announcements
- https://www.reuters.com/sports/soccer/world-cup-2026-list-26-man-squads-finals-2026-06-02/

## 3.6 xG/xGA y eventos

StatsBomb liberó datos de la Copa Mundial 2022 y también tiene datos abiertos de otras competiciones. FBref publica estadísticas de Mundial, incluyendo métricas relacionadas con xG cuando están disponibles.

**Fuentes:**

- https://blogarchive.statsbomb.com/news/statsbomb-release-free-2022-world-cup-data/
- https://fbref.com/en/comps/1/2022/2022-World-Cup-Stats

---

# 4. Fórmula Nivel 2 propuesta

El modelo Nivel 2 extiende el núcleo N1:

```text
Strength_N1 =
  0.45 · FIFA_score
+ 0.45 · Elo_score
+ 0.07 · HostAdvantage
+ 0.03 · GroupRelativeStrength
```

hacia una versión extendida:

```text
Strength_N2 =
  0.30 · Strength_N1
+ 0.15 · SquadMarketTalent
+ 0.12 · PlayerLevelScore
+ 0.10 · RecentCompetitiveForm
+ 0.10 · AttackDefenseBalance
+ 0.08 · TournamentExperience
+ 0.06 · SquadCycleAge
+ 0.05 · xG_xGA_Proxy
+ 0.04 · UpsetRobustness
```

Luego se aplica calibración histórica:

```text
p_phase_N2 =
  normalize_by_phase(
    sigmoid(
      α_phase
    + β_phase · logit(p_phase_raw)
    + γ_phase · HistoricalVolatility
    + δ_phase · PathDifficulty
    - η_phase · OverconfidencePenalty
    - θ_phase · MarketSkewPenalty
    )
  )
```

Con restricción por fase:

```text
Σ p_R16      = 16
Σ p_QF       = 8
Σ p_SF       = 4
Σ p_Final    = 2
Σ p_Champion = 1
```

Para 2026, con formato ampliado:

```text
Σ p_R32      = 32
Σ p_R16      = 16
Σ p_QF       = 8
Σ p_SF       = 4
Σ p_Final    = 2
Σ p_Champion = 1
```

---

# 5. Componentes del Nivel 2

## 5.1 SquadMarketTalent

```text
SquadMarketTalent =
  0.55 · normalize(log(1 + MarketValue))
+ 0.25 · normalize(AvgPlayerValue)
+ 0.20 · normalize(DepthScore)
```

## 5.2 PlayerLevelScore

```text
PlayerLevelScore =
  0.30 · XI_Quality
+ 0.20 · Attack_Quality
+ 0.15 · Midfield_Control
+ 0.15 · Defense_GK_Stability
+ 0.10 · Bench_Impact
+ 0.10 · Availability_Form
```

## 5.3 RecentCompetitiveForm

```text
RecentCompetitiveForm =
  weighted_results_last_24_months
· opponent_strength_adjustment
· match_importance_weight
```

## 5.4 AttackDefenseBalance

```text
AttackDefenseBalance =
  0.40 · AttackScore
+ 0.35 · DefenseScore
+ 0.15 · GoalkeeperScore
+ 0.10 · SetPieceProfile
```

## 5.5 SquadCycleAge

```text
SquadCycleAge =
  - abs(avg_age - optimal_age_band)
  - veteran_fatigue_penalty
  + prime_age_core_bonus
```

## 5.6 xG_xGA_Proxy

```text
xG_xGA_Proxy =
  0.50 · normalized_xG_for
- 0.35 · normalized_xG_against
+ 0.15 · shot_quality_balance
```

## 5.7 MarketSkewPenalty

```text
MarketSkewPenalty =
  UEFA_market_bias
+ low_liquidity_market_penalty
+ overvaluation_of_bench_players
```

Este componente evita que el modelo favorezca en exceso a equipos europeos solo porque sus jugadores están valorizados en mercados más líquidos.

---

# 6. Diseño del backtesting Nivel 2

## 6.1 Mundiales incluidos

| Mundial | Estado recomendado |
|---|---|
| 2010 | Usar Nivel 2 parcial |
| 2014 | Usar Nivel 2 parcial |
| 2018 | Mejor cobertura player-level y mercado |
| 2022 | Mejor cobertura para xG, squads y eventos |

## 6.2 Variables objetivo

| Fase | Variable binaria |
|---|---|
| Octavos | `reached_R16` |
| Cuartos | `reached_QF` |
| Semifinal | `reached_SF` |
| Final | `reached_Final` |
| Campeón | `Champion` |

## 6.3 Métricas

| Métrica | Uso |
|---|---|
| Brier Score | Calibración probabilística por fase |
| Log Loss | Penalización de probabilidades malas para campeón |
| Top-k Accuracy | Validación ejecutiva de favoritos |
| Calibration Curve | Sobreconfianza / subconfiabilidad |
| Ablation Test | Qué componente agrega valor |
| Ranked Probability Score | Profundidad esperada por selección |

---

# 7. Resultado de la evaluación Nivel 2

## 7.1 Resultado metodológico

El Nivel 2 **sí aporta valor esperado** frente al Nivel 1 en estas áreas:

| Área | Mejora esperada |
|---|---|
| Cuartos y octavos | Alta |
| Outsiders tácticos | Alta |
| Equipos envejecidos | Media-Alta |
| Equipos con alta plantilla pero bajo equilibrio | Media-Alta |
| Equipos africanos y asiáticos subvalorados | Media |
| Campeón | Media |
| Finalistas | Media |
| Fase de grupos | Media |

La razón es que el Nivel 1 ya captura relativamente bien a las élites por FIFA/Elo, pero no explica bien:

- Por qué Marruecos 2022 podía llegar lejos.
- Por qué Croacia 2018/2022 sobre-rendía.
- Por qué Alemania 2018 estaba sobrevalorada si se miraba solo ranking/reputación.
- Por qué Brasil/Portugal/Inglaterra pueden tener alto talento pero no garantía de título.
- Por qué equipos físicos y tácticos pueden alterar cruces.

## 7.2 Resultado cuantitativo prudente

No se declara una tabla definitiva de Brier Nivel 2 porque no se han reconstruido en esta sesión todos los snapshots históricos exactos de:

- valor de mercado pretorneo,
- squads históricos,
- edad promedio por equipo,
- xG/xGA pretorneo,
- lesiones,
- odds,
- XI titulares.

Por rigor, este reporte no inventa métricas Nivel 2 cerradas. La conclusión se expresa como:

```text
Nivel 2 mejora la especificación del modelo y justifica la evolución,
pero requiere ingesta histórica auditada para declarar métricas finales.
```

---

# 8. Ablation test recomendado

Para medir realmente el valor incremental del Nivel 2, se deben comparar estas variantes:

| Modelo | Variables |
|---|---|
| N1 | FIFA + Elo + localía + grupo |
| N2-A | N1 + valor de plantilla |
| N2-B | N2-A + edad/experiencia |
| N2-C | N2-B + player-level |
| N2-D | N2-C + xG/xGA |
| N2-E | N2-D + clima/contexto |
| N2-F | N2-E + penalización de mercado |
| v6.2 final | Mejor combinación según Brier/LogLoss |

---

# 9. Decisión para el modelo actual v6

## 9.1 ¿Se debe cambiar el modelo v6 actual?

**Sí, pero de forma controlada.**

La estructura v6 debe evolucionar hacia **v6.2**, pero no debe reemplazarse por completo. El núcleo FIFA/Elo/calibración histórica queda validado como estructura base.

## 9.2 Nueva fórmula recomendada para v6.2

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

El cambio frente a v6 es:

- Baja ligeramente el peso del mercado.
- Sube el control FIFA/Elo.
- Mantiene player-level, pero no lo sobredimensiona.
- Mantiene clima como contextual, no como variable estructural dominante.
- Refuerza calibración histórica y penalización de sobreconfianza.

---

# 10. Impacto esperado sobre la tabla 2026

La tabla actual de probabilidades v6 no debería cambiar radicalmente. El Nivel 2 sugiere ajustes más finos:

| Selección | Ajuste esperado |
|---|---|
| España | Mantener favorita; no subir demasiado por talento |
| Francia | Mantener top 2; cuidado con sobrepeso de mercado |
| Inglaterra | Mantener top 3; controlar historial de knockout |
| Argentina | Mantener top 4; penalización moderada por edad |
| Portugal | Mantener top 5; ajustar riesgo defensivo |
| Brasil | Mantener top 6; no sobreponderar reputación histórica |
| Alemania | Mantener contender; no sobrecompensar plantilla |
| Marruecos | Mantener outsider fuerte; player-level táctico ayuda |
| Croacia | Mantener outsider; experiencia compensa edad, pero con límite |
| Colombia | Mantener outsider relevante; mejora por equilibrio y contexto |
| Senegal | Puede subir levemente por físico y robustez |
| Japón | Puede subir levemente por disciplina táctica |
| Uruguay | Mantener por competitividad y experiencia |

---

# 11. Propuesta de actualización del modelo v6 a v6.2

## 11.1 Tabla de pesos recomendada

| Componente | v6 | v6.2 recomendado |
|---|---:|---:|
| FIFA/Elo oficial | 17% | 24% |
| World Football Elo | 15% | 20% |
| Talento de plantilla | 14% | 14% |
| Player-level | 12% | 12% |
| Forma reciente | 10% | 10% |
| Ataque/defensa | 9% | 8% |
| Clima/altitud | 8% | 4% |
| Localía/viaje/descanso | 7% | incluido en contexto |
| Experiencia | 5% | 5% |
| Robustez anti-sorpresa | 3% | 3% |

## 11.2 Razón del ajuste

El Nivel 2 sugiere que el mercado y el player-level ayudan, pero pueden introducir ruido si no están auditados. Por eso el modelo debe seguir anclado en FIFA/Elo y usar el resto como ajustes calibrados.

---

# 12. Recomendación final

## Decisión

```text
Pasar de ChatGPT v6 a ChatGPT v6.2
```

pero **no declarar aún un v7 final**.

## Justificación

- Nivel 1 validó el núcleo estructural.
- Nivel 2 justifica añadir plantillas, player-level, mercado, xG y edad.
- Pero Nivel 2 no debe cerrar métricas finales sin snapshots históricos auditados.

## Acción técnica

1. Mantener la tabla v6 como baseline validado.
2. Crear una tabla v6.2 con ajustes moderados.
3. No hacer cambios agresivos hasta incorporar odds, xG y datos históricos completos.
4. Documentar que v6.2 es una evolución metodológica, no una validación final completa.

---

# 13. Limitaciones

| Limitación | Implicación |
|---|---|
| No hay snapshots completos de mercado histórico en esta sesión | No declarar Brier Nivel 2 final |
| No hay player-level auditado histórico | No estimar impacto individual con precisión |
| xG completo solo está bien cubierto en torneos recientes | Nivel 2 es más fuerte para 2018/2022 que 2010/2014 |
| Odds no incorporadas | Falta benchmark colectivo |
| Clima histórico no reconstruido por partido | No validar clima con precisión |
| No hay backtesting de marcadores | Solo probabilidades por fase |

---

# 14. Criterios para pasar a v7

Pasar a v7 solo si se completa:

| Criterio | Estado requerido |
|---|---|
| Ranking FIFA histórico | Completo |
| Elo histórico | Completo |
| Squads históricos | Completo |
| Valor de mercado pretorneo | Auditado |
| Edad promedio por selección | Completo |
| xG/xGA | Al menos 2018/2022 completo |
| Odds pretorneo | Incorporado |
| Matriz de fases reales | Completa |
| Brier / LogLoss / calibración | Calculado |
| Ablation test | Calculado |

---

# 15. Conclusión final

El **Backtesting Nivel 2** confirma metodológicamente que el modelo debe evolucionar más allá de FIFA/Elo, pero también muestra que la evolución debe ser prudente.

La conclusión más importante es:

> El modelo v6 no debe reemplazarse; debe refinarse hacia v6.2.

La versión v6.2 debe mantener el corazón FIFA/Elo/calibración histórica y añadir plantillas, player-level, mercado, xG y experiencia como capas de ajuste, no como dominantes absolutos.

---

# 16. Nivel de confianza

**Nivel de confianza:** Medio-Alto

La confianza es alta en la dirección metodológica y media en la cuantificación final Nivel 2, porque faltan snapshots históricos completos para declarar métricas cerradas.

---

# 17. Factores que podrían cambiar la conclusión

1. Disponibilidad de odds históricas pretorneo.
2. Datos xG/xGA completos para 2010–2022.
3. Valores de mercado pretorneo auditados.
4. Convocatorias históricas completas en formato estructurado.
5. Lesiones pretorneo verificadas.
6. Clima histórico por sede y hora.
7. Resultados de ablation test completo.
8. Curvas de calibración reales.

---

# 18. Acción recomendada

Adoptar **ChatGPT v6.2** como siguiente versión metodológica y no pasar todavía a v7.

La siguiente tarea recomendada es producir:

```text
Camino_al_Titulo_ChatGPT_v6_2.md
```

con la tabla de probabilidades 2026 ajustada de forma moderada según los hallazgos del Nivel 2.
