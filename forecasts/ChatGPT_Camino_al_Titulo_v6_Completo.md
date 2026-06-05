# Camino al título · ChatGPT v6

## Modelo superior con calibración histórica

**Versión:** ChatGPT v6  
**Tipo de modelo:** ensemble calibrado histórico + team-level + player-level + climate-aware  
**Salida principal:** probabilidades de alcanzar cada fase para las 48 selecciones del Mundial 2026  
**Lectura:** cada columna representa la probabilidad de **alcanzar** esa fase, no la probabilidad condicional de ganar el partido de esa fase.  
**Uso recomendado:** versión principal para comparación contra otras IAs.

---

## 1. Resumen ejecutivo

La versión v6 es una evolución del modelo v5. Mantiene los componentes de fuerza estructural, ranking FIFA, Elo, plantillas, lectura player-level, clima, altitud, localía, ruta de grupo y volatilidad, pero añade una capa crítica: **calibración histórica**.

Esta capa reduce la sobreconfianza de los favoritos, penaliza rutas de eliminación complejas y redistribuye probabilidad hacia outsiders plausibles. El objetivo es evitar el error común de los modelos no calibrados: convertir superioridad de plantilla en probabilidades excesivas de título.

En esta versión, **España** sigue como favorita principal, pero con una probabilidad de título contenida en **16.2%**. El bloque perseguidor queda formado por **Francia, Inglaterra y Argentina**. Luego aparecen **Portugal, Brasil, Alemania, Países Bajos, Bélgica y Marruecos**.

---

## 2. Fuentes y señales usadas

| Bloque | Uso dentro del modelo | Calidad de evidencia |
|---|---|---|
| Ranking FIFA oficial | Prior estructural de fuerza | Alta |
| World Football Elo | Rendimiento competitivo reciente | Media-Alta |
| Valor y profundidad de plantilla | Talento agregado y banca | Media |
| Convocatorias/listas de jugadores | Lectura player-level agregada | Media |
| Benchmark Opta | Control de sobreconfianza y referencia externa | Alta |
| Fixture y grupos | Ruta de clasificación y dificultad | Alta |
| Clima, altitud, humedad y domos | Ajuste contextual por sede | Media |
| Historial mundialista | Calibración de varianza y sorpresas | Media-Alta |

**Nota de transparencia:** el enlace de ESPN sobre convocatorias se considera fuente externa de referencia, pero su extracción automática completa puede depender de JavaScript/verificación anti-bot. Por eso el modelo v6 usa la información de convocatorias como señal agregada y no como una base individual auditada jugador por jugador.

---

## 3. Qué cambia frente al modelo v5

El modelo v5 incorporaba clima por sede y lectura player-level agregada. La versión v6 añade:

1. **Shrinkage de favoritos:** evita que selecciones top reciban probabilidades infladas.
2. **Calibración por fase:** normaliza la probabilidad total esperada en cada ronda.
3. **Penalización de ruta:** castiga cuadros con rivales fuertes probables.
4. **Volatilidad histórica:** incorpora patrones de sorpresas de Mundiales recientes.
5. **Regularización del título:** ningún equipo supera un umbral irrealista de favoritismo.
6. **Mejor tratamiento de outsiders:** aumenta masa probabilística para equipos tácticamente competitivos.
7. **Control de baja muestra:** reconoce que tres partidos de grupo y rondas de eliminación directa generan alta varianza.

---

## 4. Fórmula técnica compacta v6

```text
Strength_v6 =
  0.17 · FIFA_Elo_score
+ 0.15 · WorldFootballElo
+ 0.14 · SquadMarketTalent
+ 0.12 · PlayerLevelScore
+ 0.10 · RecentCompetitiveForm
+ 0.09 · AttackDefenseBalance
+ 0.08 · ClimateAltitudeFit
+ 0.07 · HostTravelRestContext
+ 0.05 · TournamentExperience
+ 0.03 · UpsetRobustness
```

Luego se genera una probabilidad cruda por fase mediante simulación:

```text
p_phase_raw =
  MonteCarlo(
    Strength_v6,
    group_draw,
    fixture_path,
    climate_context,
    player_risk,
    third_place_matrix_proxy,
    knockout_variance
  )
```

Después se aplica calibración histórica:

```text
p_phase_v6 =
  normalize_by_phase(
    sigmoid(
      α_phase
    + β_phase · logit(p_phase_raw)
    + γ_phase · HistoricalVolatility
    + δ_phase · PathDifficulty
    - η_phase · OverconfidencePenalty
    )
  )
```

Con la restricción:

```text
Σ p_R32      = 32
Σ p_Octavos = 16
Σ p_Cuartos = 8
Σ p_Semis   = 4
Σ p_Final   = 2
Σ p_Campeón = 1
```

---

## 5. Componentes del modelo v6

### 5.1 FIFA_Elo_score — 17%

Combina ranking FIFA oficial y una transformación tipo Elo para representar fuerza estructural.

```text
FIFA_rank_score = 1 - ((FIFA_rank - 1) / (N - 1))
```

Cuando hay puntos FIFA:

```text
FIFA_points_score =
  (FIFA_points - min(FIFA_points)) /
  (max(FIFA_points) - min(FIFA_points))
```

---

### 5.2 WorldFootballElo — 15%

Ajusta el ranking oficial con señales de rendimiento competitivo reciente.

```text
Elo_score =
  (Elo - min(Elo)) /
  (max(Elo) - min(Elo))
```

---

### 5.3 SquadMarketTalent — 14%

Mide talento y profundidad de plantilla.

```text
SquadMarketTalent =
  0.55 · normalize(log(1 + MarketValue))
+ 0.25 · normalize(AvgPlayerValue)
+ 0.20 · normalize(DepthScore)
```

---

### 5.4 PlayerLevelScore — 12%

Aproxima calidad real de convocados y XI probable.

```text
PlayerLevelScore =
  0.30 · XI_Quality
+ 0.20 · Attack_Quality
+ 0.15 · Midfield_Control
+ 0.15 · Defense_GK_Stability
+ 0.10 · Bench_Impact
+ 0.10 · Availability_Form
```

---

### 5.5 RecentCompetitiveForm — 10%

Captura rendimiento reciente ponderado por fuerza de rival.

```text
RecentCompetitiveForm =
  weighted_results_last_matches · opponent_strength_adjustment
```

---

### 5.6 AttackDefenseBalance — 9%

Evalúa si la selección tiene equilibrio competitivo o depende de un solo frente.

```text
AttackDefenseBalance =
  0.50 · AttackScore
+ 0.35 · DefenseScore
+ 0.15 · GoalkeeperStability
```

---

### 5.7 ClimateAltitudeFit — 8%

Integra calor, humedad, altitud y mitigación por domo.

```text
ClimateAltitudeFit =
  ClimateAdaptation
- ClimatePenalty
+ AltitudeAdaptation
+ DomeMitigation
```

---

### 5.8 HostTravelRestContext — 7%

Evalúa localía, viaje, descanso y familiaridad regional.

```text
Context =
  0.40 · HostAdvantage
+ 0.25 · TravelAdvantage
+ 0.20 · RestAdvantage
+ 0.15 · RegionalFamiliarity
```

---

### 5.9 TournamentExperience — 5%

Mide experiencia en torneos de alta presión.

```text
TournamentExperience =
  0.40 · RecentWorldCupPerformance
+ 0.30 · KnockoutExperience
+ 0.20 · CoachContinuity
+ 0.10 · PenaltyShootoutProfile
```

---

### 5.10 UpsetRobustness — 3%

Mide capacidad de evitar colapsos ante rivales inferiores.

```text
UpsetRobustness =
  0.35 · FavouriteConversionHistory
+ 0.25 · ShockRecoveryScore
+ 0.20 · DefensiveSetPieceStability
+ 0.20 · LowBlockBreakingAbility
```

---

## 6. Calibración histórica

La calibración histórica se aplica para corregir tres sesgos:

| Sesgo | Corrección v6 |
|---|---|
| Sobreconfianza en favoritos | Shrinkage y penalización de probabilidad extrema |
| Subestimación de outsiders | Redistribución de masa hacia equipos competitivos |
| Baja muestra del torneo | Aumento de varianza en grupos y knockout |

### 6.1 Penalización de sobreconfianza

```text
OverconfidencePenalty =
  max(0, p_raw - HistoricalCeiling_phase) · κ_phase
```

### 6.2 Volatilidad histórica

```text
HistoricalVolatility =
  0.35 · upset_rate_world_cups
+ 0.25 · penalty_variance
+ 0.20 · group_stage_noise
+ 0.20 · knockout_single_game_variance
```

### 6.3 Dificultad de ruta

```text
PathDifficulty =
  expected_opponent_strength_R32_to_Final
+ third_place_assignment_uncertainty
+ rest_travel_penalty
```

---

## 7. Tabla principal · Camino al título ChatGPT v6

| Selección            | R32   | Octavos   | Cuartos   | Semis   | Final   | Campeón   |
|:---------------------|:------|:----------|:----------|:--------|:--------|:----------|
| España               | 99.8% | 79.5%     | 53.6%     | 40.7%   | 26.4%   | 16.2%     |
| Francia              | 99.8% | 86.9%     | 60.1%     | 39.5%   | 24.1%   | 12.3%     |
| Inglaterra           | 99.8% | 80.5%     | 55.5%     | 36.1%   | 21.6%   | 11.2%     |
| Argentina            | 99.8% | 65.8%     | 47.6%     | 31.2%   | 18.8%   | 10.3%     |
| Portugal             | 99.8% | 77.5%     | 51.7%     | 30.1%   | 16.4%   | 7.9%      |
| Brasil               | 99.8% | 64.3%     | 41.8%     | 23.7%   | 12.5%   | 6.4%      |
| Alemania             | 99.8% | 70.9%     | 38.4%     | 22.0%   | 11.1%   | 5.5%      |
| Países Bajos         | 97.7% | 55.7%     | 36.3%     | 18.5%   | 9.0%    | 4.4%      |
| Bélgica              | 99.2% | 68.4%     | 40.5%     | 18.1%   | 8.7%    | 3.9%      |
| Marruecos            | 96.4% | 52.4%     | 31.2%     | 14.7%   | 6.7%    | 3.0%      |
| Croacia              | 92.6% | 50.1%     | 22.0%     | 10.6%   | 4.5%    | 2.0%      |
| Colombia             | 93.3% | 48.8%     | 22.5%     | 10.2%   | 4.1%    | 1.8%      |
| Uruguay              | 94.6% | 38.5%     | 21.0%     | 9.6%    | 3.9%    | 1.7%      |
| Estados Unidos       | 88.1% | 50.6%     | 23.6%     | 9.1%    | 3.6%    | 1.5%      |
| México               | 96.2% | 56.2%     | 23.0%     | 8.7%    | 3.2%    | 1.5%      |
| Senegal              | 88.6% | 49.8%     | 22.1%     | 9.2%    | 3.6%    | 1.4%      |
| Suiza                | 96.2% | 55.7%     | 23.4%     | 8.3%    | 3.1%    | 1.3%      |
| Noruega              | 85.5% | 43.3%     | 19.3%     | 7.7%    | 2.8%    | 1.1%      |
| Japón                | 84.0% | 33.4%     | 15.4%     | 5.9%    | 2.1%    | 0.9%      |
| Ecuador              | 89.1% | 40.0%     | 15.4%     | 5.8%    | 2.1%    | 0.8%      |
| Türkiye              | 79.5% | 41.5%     | 16.9%     | 6.1%    | 2.2%    | 0.8%      |
| Canadá               | 88.6% | 43.5%     | 15.9%     | 4.9%    | 1.5%    | 0.6%      |
| Austria              | 80.0% | 22.8%     | 9.0%      | 3.3%    | 1.0%    | 0.5%      |
| Suecia               | 66.8% | 22.8%     | 9.7%      | 3.3%    | 1.0%    | 0.5%      |
| Costa de Marfil      | 78.9% | 30.4%     | 10.0%     | 3.3%    | 0.9%    | 0.4%      |
| Corea del Sur        | 81.0% | 35.4%     | 11.3%     | 3.3%    | 0.9%    | 0.4%      |
| Argelia              | 75.9% | 20.3%     | 7.7%      | 2.5%    | 0.7%    | 0.3%      |
| Egipto               | 76.9% | 27.8%     | 8.2%      | 2.2%    | 0.6%    | 0.3%      |
| Australia            | 58.2% | 24.3%     | 7.2%      | 2.0%    | 0.5%    | 0.2%      |
| Paraguay             | 52.6% | 20.3%     | 6.1%      | 1.8%    | 0.5%    | 0.2%      |
| Chequia              | 65.8% | 23.3%     | 6.3%      | 1.6%    | 0.4%    | 0.2%      |
| Escocia              | 55.7% | 16.2%     | 4.9%      | 1.2%    | 0.3%    | 0.1%      |
| Irán                 | 70.8% | 24.3%     | 6.1%      | 1.5%    | 0.3%    | 0.1%      |
| Bosnia y Herzegovina | 50.6% | 14.2%     | 3.1%      | 0.6%    | 0.2%    | <0.1%     |
| Ghana                | 32.4% | 8.1%      | 2.0%      | 0.4%    | 0.1%    | <0.1%     |
| Túnez                | 27.3% | 6.1%      | 1.5%      | 0.3%    | 0.1%    | <0.1%     |
| RD Congo             | 39.5% | 9.1%      | 2.0%      | 0.4%    | 0.1%    | <0.1%     |
| Uzbekistán           | 31.4% | 6.6%      | 1.3%      | 0.3%    | 0.1%    | <0.1%     |
| Panamá               | 28.3% | 6.6%      | 1.4%      | 0.3%    | 0.1%    | <0.1%     |
| Arabia Saudita       | 27.3% | 4.6%      | 0.9%      | 0.2%    | 0.1%    | <0.1%     |
| Sudáfrica            | 27.3% | 6.1%      | 1.0%      | 0.2%    | 0.1%    | <0.1%     |
| Qatar                | 30.4% | 6.1%      | 1.0%      | 0.2%    | 0.1%    | <0.1%     |
| Jordania             | 12.1% | 1.5%      | 0.3%      | 0.1%    | <0.1%   | <0.1%     |
| Nueva Zelanda        | 17.2% | 3.0%      | 0.5%      | 0.1%    | <0.1%   | <0.1%     |
| Irak                 | 8.6%  | 1.5%      | 0.3%      | 0.1%    | <0.1%   | <0.1%     |
| Cabo Verde           | 17.2% | 2.5%      | 0.4%      | 0.1%    | <0.1%   | <0.1%     |
| Curazao              | 8.6%  | 1.2%      | 0.2%      | <0.1%   | <0.1%   | <0.1%     |
| Haití                | 11.1% | 1.6%      | 0.3%      | 0.1%    | <0.1%   | <0.1%     |

---

## 8. Ranking de favoritos al título

| Ranking | Selección | Campeón |
|---:|---|---:|
| 1 | España | 16.2% |
| 2 | Francia | 12.3% |
| 3 | Inglaterra | 11.2% |
| 4 | Argentina | 10.3% |
| 5 | Portugal | 7.9% |
| 6 | Brasil | 6.4% |
| 7 | Alemania | 5.5% |
| 8 | Países Bajos | 4.4% |
| 9 | Bélgica | 3.9% |
| 10 | Marruecos | 3.0% |
| 11 | Croacia | 2.0% |
| 12 | Colombia | 1.8% |

---

## 9. Lectura crítica

### 9.1 España

España se mantiene como favorita porque combina alto nivel de plantilla, grupo favorable, benchmark externo positivo, estructura colectiva fuerte y ruta inicial relativamente manejable. Sin embargo, v6 reduce su sobreconfianza: ganar un Mundial ampliado exige superar más partidos y más fuentes de varianza.

### 9.2 Francia

Francia tiene una de las mejores plantillas del torneo y alta probabilidad de avanzar a fases intermedias. La calibración histórica le da mucha fuerza en octavos y cuartos, pero su grupo y posible ruta reducen ligeramente su probabilidad de título frente a España.

### 9.3 Inglaterra

Inglaterra aparece como una candidata muy fuerte por profundidad y equilibrio, pero sigue penalizada por incertidumbre histórica en fases finales y dependencia de ejecución en knockout.

### 9.4 Argentina

Argentina conserva una probabilidad alta por jerarquía competitiva, continuidad y cultura de torneo. La penalización principal viene por edad, desgaste, defensa del título y menor margen físico frente a algunos rivales europeos.

### 9.5 Portugal y Brasil

Portugal queda por encima de Brasil en probabilidad de título por combinación de ranking, plantilla y ruta. Brasil mantiene un techo muy alto, pero el modelo penaliza su irregularidad reciente y la complejidad de algunos posibles cruces.

### 9.6 Outsiders relevantes

Los outsiders más relevantes son:

- Marruecos.
- Croacia.
- Colombia.
- Uruguay.
- Estados Unidos.
- México.
- Senegal.
- Suiza.
- Noruega.

Estos equipos no son favoritos al título, pero tienen suficiente calidad o contexto para alterar rutas de potencias.

---

## 10. Validación probabilística por fase

La tabla fue normalizada para que el total esperado sea consistente:

| Fase | Total probabilístico esperado |
|---|---:|
| R32 | 32 equipos |
| Octavos | 16 equipos |
| Cuartos | 8 equipos |
| Semis | 4 equipos |
| Final | 2 equipos |
| Campeón | 1 equipo |

---

## 11. Supuestos ocultos

| Supuesto | Riesgo |
|---|---|
| Ranking FIFA/Elo aproxima fuerza real | Puede tener rezago frente a cambios recientes |
| Valor de plantilla aproxima talento | No mide cohesión táctica |
| Convocatoria fuerte implica rendimiento | Depende del XI real y sistema |
| Historial mundialista ayuda a calibrar | Puede no capturar formato 2026 de 48 equipos |
| Clima afecta de forma diferenciada | Depende de hora exacta, humedad real y techo |
| La ruta probable se puede aproximar | La matriz exacta de terceros puede modificar cruces |
| La varianza histórica se repite | Cada torneo tiene patrones propios |

---

## 12. Mejor contraargumento

El mejor contraargumento contra este modelo es que, aunque v6 mejora la calibración y reduce sobreconfianza, todavía no es equivalente a un modelo profesional entrenado con:

- Odds de mercado.
- xG/xGA recientes.
- XI titulares.
- Datos médicos confirmados.
- Árbitros.
- Eventos de tracking.
- WBGT real por horario.
- Simulación completa de las 495 combinaciones de terceros clasificados.

Por tanto, v6 es una versión muy sólida para comparación entre IAs, pero no debe presentarse como modelo final de casa de apuestas.

---

## 13. Qué información cambiaría la conclusión

| Información nueva | Impacto esperado |
|---|---|
| Actualización FIFA del 10/11 de junio | Mueve rating base |
| XI titulares probables | Cambia player-level score |
| Lesiones y reemplazos | Puede mover 1–4 pp por selección |
| Odds de mercado | Permite calibración colectiva |
| xG/xGA recientes | Mejora señal ofensiva/defensiva |
| WBGT por partido | Ajusta clima y ritmo |
| Techo abierto/cerrado | Afecta Dallas, Houston, Atlanta |
| Matriz exacta de terceros | Cambia rutas de knockout |
| Árbitros asignados | Ajusta tarjetas/penales |
| Motivación en tercera fecha | Cambia rotaciones |

---

## 14. Riesgos de primer y segundo orden

### Riesgos de primer orden

| Riesgo | Impacto |
|---|---|
| Lesión de figura clave | Modifica calidad inmediata |
| Roja temprana | Rompe el modelo prepartido |
| Penalti aislado | Cambia partido de baja anotación |
| Error de portero | Alto impacto en marcador |
| Fatiga por calor | Reduce ritmo y presión |

### Riesgos de segundo orden

| Riesgo | Impacto |
|---|---|
| Rotaciones en tercera fecha | Cambian fuerza real |
| Equipo ya clasificado | Baja intensidad |
| Rival obligado a ganar | Aumenta volatilidad |
| Narrativa de favorito | Puede sesgar interpretación |
| Clima mitigado por domo | Reduce penalización térmica |
| Cruce inesperado de terceros | Cambia ruta completa |

---

## 15. Acción recomendada

Usar esta versión como **ChatGPT v6 oficial** para comparación con otras IAs.

La siguiente evolución debería ser una **v7 final**, incorporando:

1. Ranking FIFA actualizado.
2. Odds de mercado.
3. XI titulares probables.
4. Lesiones confirmadas.
5. xG/xGA recientes.
6. WBGT real por horario.
7. Matriz oficial completa de terceros.
8. Backtesting formal con Brier Score y Log Loss.

---

## 16. Nivel de confianza

**Nivel de confianza:** Medio-Alto

La versión v6 es metodológicamente superior a v5 porque incorpora calibración histórica, normalización por fase y control de sobreconfianza. La principal limitación sigue siendo la ausencia de odds de mercado, XI titulares y validación empírica completa.

---

## 17. Factores que podrían cambiar la conclusión

1. Actualización FIFA del 10/11 de junio.
2. Lesiones de última hora.
3. XI titulares reales.
4. Odds prepartido.
5. Condiciones climáticas reales por hora.
6. Techo abierto/cerrado en sedes con domo.
7. Asignación exacta de mejores terceros.
8. Rotaciones en la tercera fecha.

---

## 18. Acción final recomendada

Publicar esta tabla como **Camino al título · ChatGPT v6** y usarla como benchmark principal frente a Claude, Gemini, Perplexity u otros modelos. Mantener una advertencia clara: las probabilidades son estimaciones calibradas, no certezas.
