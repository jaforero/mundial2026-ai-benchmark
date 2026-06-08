# ChatGPT Mundial 2026 — Modelo v8.5 Integrado

**Fecha de consolidación:** 2026-06-07 16:42 UTC  
**Versión operativa:** `ChatGPT Mundial 2026 · Modelo v8.5`  
**Base:** Fase 8.4A-TM + Fase 8.4B-Consensus  
**Decisión central:** adoptar SofaScore/datafc como capa de validación de mercado, sin cambiar goleadores ni scorelines por xG todavía.

---

# Resumen Ejecutivo

El **Modelo v8.5** consolida la mejor versión disponible con los datos actuales:

1. **48 selecciones:** se mantiene y adopta **v8.4A-TM**, combinando Elo actual 2026 con capa Transfermarkt de talento/profundidad.
2. **72 partidos — probabilidades:** se adopta **v8.4B-Consensus**, integrando The Odds API como señal principal de mercado y SofaScore/datafc como validación secundaria.
3. **72 partidos — marcadores:** se mantienen los scorelines de **v8.4A-TM**. No se recalculan por xG porque SofaScore/datafc no entregó shots/xG, lineups ni match stats.
4. **Top 10 goleadores:** se mantiene **v8.4A-TM proxy**. No se recalibra por player-level real porque no hay squads/player stats/lineups/xG jugador vía datafc.
5. **xG/O-U:** sigue pendiente.

La mejora más sólida de v8.5 está en **probabilidades 1X2 y validación de mercado**. La parte más débil sigue siendo **goleadores y marcadores exactos sin xG/O-U**.

---

# 1. Estado del Modelo

| Componente                        | Base técnica        | Estado v8.5        | Justificación                                                      |
|:----------------------------------|:--------------------|:-------------------|:-------------------------------------------------------------------|
| 48 selecciones / Camino al título | Fase 8.4A-TM        | Adoptado en v8.5   | Elo actual 2026 + Transfermarkt talento/profundidad                |
| 72 partidos / Probabilidades 1X2  | Fase 8.4B-Consensus | Adoptado en v8.5   | The Odds API + SofaScore/datafc como validación de mercado         |
| 72 partidos / Marcadores          | Fase 8.4A-TM        | Conservado en v8.5 | No se cambia por xG porque no hay shots/xG/O-U/lineups disponibles |
| Top 10 goleadores                 | Fase 8.4A-TM Proxy  | Conservado en v8.5 | Transfermarkt/ruta como proxy; sin player-stats/xG real            |
| xG/xGA                            | Pendiente           | No incorporado     | TheStatsAPI bloqueado; datafc no activó shots/xG                   |
| Player-level real                 | Pendiente           | No incorporado     | datafc no entregó squads/player stats/lineups                      |

---

# 2. Validación de Datos Externos

| Fuente                     | Señal                                | Estado v8.5                                       | Uso                                         |
|:---------------------------|:-------------------------------------|:--------------------------------------------------|:--------------------------------------------|
| World Football Elo Ratings | Elo actual junio 2026                | Incorporado desde Fase 8.2D                       | Fuerte para selecciones, no para scorelines |
| The Odds API               | Odds 1X2                             | 1,502 filas 1X2; 72 partidos                      | Fuerte para probabilidades 1X2              |
| Transfermarkt              | Talento/profundidad/edad/experiencia | 48 selecciones incorporadas                       | Proxy, no xG                                |
| SofaScore/datafc           | Fixtures/standings/details/odds      | 264 odds rows; 8 partidos con consenso            | Validación de mercado; no player-level      |
| TheStatsAPI                | xG/player-level                      | Bloqueado por plan/API key sin suscripción activa | No incorporado                              |

## 2.1 Disponibilidad SofaScore/datafc

| SofaScore/datafc   | Disponible   |
|:-------------------|:-------------|
| season_id_2026     | True         |
| standings          | True         |
| match_data         | True         |
| odds               | True         |
| squads             | False        |
| player_stats       | False        |
| shots_xG           | False        |
| lineups            | False        |

## 2.2 Métricas de consenso de mercado

| Métrica                           |   Resultado |
|:----------------------------------|------------:|
| Filas SofaScore odds              |         264 |
| Eventos 1X2 SofaScore parseados   |          10 |
| Eventos cruzados con The Odds API |          10 |
| Partidos con consenso aplicado    |           8 |
| Consenso alto                     |          10 |
| Divergencia moderada              |           0 |
| Divergencia fuerte                |           0 |

---

# 3. Ranking de 48 Selecciones — Modelo v8.5

| Selección            | R32   | Octavos   | Cuartos   | Semis   | Final   | Campeón   |   Elo_2026 | market_value_m_eur   |   avg_age_tm |   wc_particip |
|:---------------------|:------|:----------|:----------|:--------|:--------|:----------|-----------:|:---------------------|-------------:|--------------:|
| España               | 99.9% | 82.3%     | 55.5%     | 42.5%   | 27.9%   | 17.2%     |       2155 | €1,220.00m           |         26.8 |            18 |
| Francia              | 99.9% | 90.9%     | 63.5%     | 42.1%   | 26.0%   | 13.5%     |       2062 | €1,520.00m           |         27   |            17 |
| Inglaterra           | 99.9% | 81.6%     | 55.2%     | 35.1%   | 20.6%   | 10.6%     |       2021 | €1,360.00m           |         27.2 |            17 |
| Argentina            | 99.9% | 67.3%     | 48.1%     | 31.3%   | 18.9%   | 10.4%     |       2114 | €782.50m             |         29.1 |            20 |
| Portugal             | 99.9% | 76.3%     | 49.5%     | 28.0%   | 14.8%   | 6.9%      |       1986 | €1,010.00m           |         28   |            10 |
| Brasil               | 99.9% | 65.5%     | 43.5%     | 24.9%   | 13.2%   | 6.9%      |       1991 | €923.20m             |         29.2 |            23 |
| Alemania             | 99.9% | 69.8%     | 37.0%     | 20.8%   | 10.2%   | 4.9%      |       1932 | €947.00m             |         28.1 |            21 |
| Países Bajos         | 98.4% | 55.9%     | 36.5%     | 18.8%   | 9.2%    | 4.5%      |       1944 | €804.20m             |         27.8 |            12 |
| Marruecos            | 97.7% | 54.1%     | 33.1%     | 15.9%   | 7.4%    | 3.4%      |       1824 | €498.30m             |         26.4 |             8 |
| Bélgica              | 97.7% | 65.7%     | 36.9%     | 15.8%   | 7.2%    | 3.1%      |       1893 | €547.50m             |         27.6 |            15 |
| Colombia             | 95.2% | 51.3%     | 24.6%     | 11.4%   | 4.7%    | 2.1%      |       1977 | €302.35m             |         30.1 |             7 |
| Croacia              | 92.7% | 49.9%     | 21.8%     | 10.4%   | 4.4%    | 1.9%      |       1908 | €387.30m             |         28.3 |             7 |
| Uruguay              | 95.3% | 39.3%     | 21.9%     | 10.2%   | 4.1%    | 1.8%      |       1892 | €359.30m             |         28.8 |            16 |
| Senegal              | 90.0% | 51.7%     | 23.6%     | 10.0%   | 4.0%    | 1.6%      |       1867 | €478.10m             |         27.1 |             4 |
| México               | 96.4% | 55.8%     | 22.5%     | 8.3%    | 3.0%    | 1.4%      |       1875 | €191.85m             |         27.9 |            18 |
| Estados Unidos       | 88.6% | 49.4%     | 22.5%     | 8.4%    | 3.2%    | 1.3%      |       1726 | €385.65m             |         26.9 |            12 |
| Suiza                | 96.4% | 55.0%     | 22.6%     | 7.9%    | 2.9%    | 1.2%      |       1891 | €332.50m             |         28.3 |            13 |
| Noruega              | 86.7% | 44.8%     | 20.4%     | 8.2%    | 2.9%    | 1.1%      |       1917 | €589.90m             |         26.8 |             4 |
| Japón                | 85.5% | 34.8%     | 16.8%     | 6.6%    | 2.4%    | 1.0%      |       1906 | €270.85m             |         27.8 |             8 |
| Ecuador              | 90.8% | 41.8%     | 16.7%     | 6.3%    | 2.3%    | 0.9%      |       1935 | €368.70m             |         26.1 |             5 |
| Türkiye              | 79.8% | 41.4%     | 16.6%     | 5.9%    | 2.1%    | 0.7%      |       1911 | €473.70m             |         27.7 |             3 |
| Canadá               | 89.4% | 43.3%     | 15.5%     | 4.6%    | 1.4%    | 0.5%      |       1788 | €196.65m             |         27.1 |             3 |
| Austria              | 79.8% | 21.9%     | 8.3%      | 2.9%    | 0.9%    | 0.4%      |       1830 | €242.20m             |         28.6 |             9 |
| Costa de Marfil      | 79.3% | 30.6%     | 10.2%     | 3.3%    | 0.9%    | 0.4%      |       1695 | €522.10m             |         25.9 |             4 |
| Suecia               | 65.3% | 21.2%     | 8.6%      | 2.8%    | 0.8%    | 0.4%      |       1712 | €406.08m             |         27.6 |            13 |
| Corea del Sur        | 81.4% | 34.9%     | 10.9%     | 3.1%    | 0.8%    | 0.4%      |       1758 | €139.05m             |         28.1 |            12 |
| Argelia              | 76.5% | 20.6%     | 7.9%      | 2.6%    | 0.7%    | 0.3%      |       1760 | €256.90m             |         26.9 |             5 |
| Egipto               | 76.8% | 27.2%     | 7.9%      | 2.1%    | 0.5%    | 0.3%      |       1696 | €116.48m             |         29.1 |             4 |
| Paraguay             | 52.4% | 19.7%     | 5.7%      | 1.6%    | 0.4%    | 0.2%      |       1833 | €153.65m             |         29   |            10 |
| Australia            | 57.7% | 23.1%     | 6.6%      | 1.8%    | 0.4%    | 0.2%      |       1777 | €77.45m              |         27.4 |             7 |
| Chequia              | 64.9% | 21.8%     | 5.5%      | 1.3%    | 0.3%    | 0.2%      |       1740 | €188.18m             |         27.6 |             2 |
| Escocia              | 54.5% | 15.0%     | 4.3%      | 1.0%    | 0.2%    | 0.1%      |       1782 | €170.25m             |         29.2 |             9 |
| Irán                 | 69.8% | 22.6%     | 5.3%      | 1.2%    | 0.2%    | 0.1%      |       1772 | €32.05m              |         30.4 |             7 |
| Ghana                | 32.2% | 7.9%      | 1.9%      | 0.4%    | 0.1%    | 0.0%      |       1510 | €234.60m             |         26.8 |             5 |
| Túnez                | 27.1% | 5.9%      | 1.4%      | 0.3%    | 0.1%    | 0.0%      |       1628 | €69.95m              |         26.7 |             7 |
| Bosnia y Herzegovina | 49.2% | 13.1%     | 2.7%      | 0.5%    | 0.2%    | 0.0%      |       1595 | €151.60m             |         26.4 |             2 |
| RD Congo             | 39.5% | 8.9%      | 1.9%      | 0.4%    | 0.1%    | 0.0%      |       1661 | €143.90m             |         29.1 |             1 |
| Panamá               | 27.9% | 6.2%      | 1.3%      | 0.3%    | 0.1%    | 0.0%      |       1730 | €34.55m              |         30.4 |             2 |
| Uzbekistán           | 30.7% | 6.1%      | 1.1%      | 0.2%    | 0.1%    | 0.0%      |       1718 | €85.33m              |         28.5 |             1 |
| Sudáfrica            | 26.9% | 5.8%      | 0.9%      | 0.2%    | 0.1%    | 0.0%      |       1528 | €49.25m              |         26.8 |             4 |
| Arabia Saudita       | 26.7% | 4.3%      | 0.8%      | 0.2%    | 0.1%    | 0.0%      |       1569 | €40.68m              |         28.5 |             7 |
| Qatar                | 28.8% | 5.2%      | 0.8%      | 0.1%    | 0.1%    | 0.0%      |       1421 | €19.93m              |         29.5 |             2 |
| Cabo Verde           | 16.8% | 2.3%      | 0.3%      | 0.1%    | 0.0%    | 0.0%      |       1578 | €54.50m              |         29.7 |             1 |
| Jordania             | 11.8% | 1.4%      | 0.3%      | 0.1%    | 0.0%    | 0.0%      |       1685 | €20.00m              |         28.8 |             1 |
| Nueva Zelanda        | 16.6% | 2.7%      | 0.4%      | 0.1%    | 0.0%    | 0.0%      |       1562 | €34.35m              |         28.1 |             3 |
| Irak                 | 8.3%  | 1.3%      | 0.2%      | 0.1%    | 0.0%    | 0.0%      |       1618 | €21.20m              |         26.9 |             2 |
| Haití                | 10.7% | 1.4%      | 0.2%      | 0.1%    | 0.0%    | 0.0%      |       1548 | €55.90m              |         27.6 |             2 |
| Curazao              | 8.2%  | 1.0%      | 0.2%      | 0.0%    | 0.0%    | 0.0%      |       1434 | €25.78m              |         28   |             1 |

---

# 4. Predicción de 72 Partidos — Modelo v8.5

**Lectura de columnas:**

- `Marcador 8.4B-Consensus`: marcador vigente v8.5, heredado de v8.4A-TM.
- `Prob. A-E-B 8.4A-TM`: probabilidad anterior con The Odds API + Transfermarkt.
- `Prob. A-E-B 8.4B-Consensus`: probabilidad v8.5 con consenso The Odds API + SofaScore.
- `MarketConsensusFlag`: nivel de acuerdo entre señales de mercado disponibles.

|   M | Grupo   | Equipo A             | Marcador 8.4B-Consensus   | Equipo B             | Prob. A-E-B 8.4A-TM   | Prob. A-E-B 8.4B-Consensus   | Confianza 8.4B-Consensus   | MarketConsensusFlag   | Nota 8.4B-Consensus                                                      |
|----:|:--------|:---------------------|:--------------------------|:---------------------|:----------------------|:-----------------------------|:---------------------------|:----------------------|:-------------------------------------------------------------------------|
|   1 | A       | México               | 2-0                       | Sudáfrica            | 71-19-9               | 68-21-11                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   2 | A       | Corea del Sur        | 1-1                       | Chequia              | 37-30-33              | 36-30-33                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   3 | B       | Canadá               | 1-0                       | Bosnia y Herzegovina | 57-25-19              | 56-25-19                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|   4 | D       | Estados Unidos       | 1-0                       | Paraguay             | 51-27-22              | 51-27-22                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|   5 | C       | Haití                | 0-1                       | Escocia              | 14-23-63              | 15-22-63                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   6 | D       | Australia            | 0-1                       | Türkiye              | 19-26-55              | 20-26-54                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   7 | C       | Brasil               | 1-0                       | Marruecos            | 54-26-21              | 57-25-18                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   8 | B       | Qatar                | 0-2                       | Suiza                | 7-16-77               | 7-15-77                      | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   9 | E       | Costa de Marfil      | 1-1                       | Ecuador              | 29-31-39              | 29-31-39                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  10 | E       | Alemania             | 3-0                       | Curazao              | 89-9-2                | 92-6-2                       | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|  11 | F       | Países Bajos         | 1-0                       | Japón                | 52-26-22              | 49-26-25                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|  12 | F       | Suecia               | 1-0                       | Túnez                | 49-29-22              | 49-29-22                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  13 | H       | Arabia Saudita       | 0-1                       | Uruguay              | 11-21-67              | 11-21-68                     | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  14 | H       | España               | 3-0                       | Cabo Verde           | 86-11-3               | 86-11-3                      | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  15 | G       | Irán                 | 1-0                       | Nueva Zelanda        | 54-26-20              | 54-26-20                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  16 | G       | Bélgica              | 1-0                       | Egipto               | 61-23-16              | 61-23-16                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  17 | I       | Francia              | 1-0                       | Senegal              | 63-23-14              | 63-23-14                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  18 | I       | Irak                 | 0-2                       | Noruega              | 6-15-79               | 6-15-79                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  19 | J       | Argentina            | 2-1                       | Argelia              | 68-22-11              | 67-22-11                     | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  20 | J       | Austria              | 2-0                       | Jordania             | 73-17-9               | 74-17-9                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  21 | L       | Ghana                | 1-0                       | Panamá               | 48-28-24              | 48-28-24                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  22 | L       | Inglaterra           | 1-0                       | Croacia              | 59-25-16              | 59-25-16                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  23 | K       | Portugal             | 2-0                       | RD Congo             | 77-16-6               | 78-16-6                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  24 | K       | Uzbekistán           | 0-2                       | Colombia             | 11-21-69              | 11-21-68                     | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  25 | A       | Chequia              | 1-0                       | Sudáfrica            | 50-28-22              | 50-28-22                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  26 | B       | Suiza                | 1-0                       | Bosnia y Herzegovina | 61-24-15              | 61-24-15                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  27 | B       | Canadá               | 2-0                       | Qatar                | 73-19-8               | 73-19-8                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  28 | A       | México               | 2-1                       | Corea del Sur        | 57-25-18              | 57-25-18                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  29 | C       | Brasil               | 3-0                       | Haití                | 88-9-3                | 88-9-3                       | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  30 | C       | Escocia              | 0-1                       | Marruecos            | 18-27-55              | 18-27-55                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  31 | D       | Türkiye              | 1-0                       | Paraguay             | 49-28-23              | 49-28-23                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  32 | D       | Estados Unidos       | 1-0                       | Australia            | 55-25-20              | 55-25-20                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  33 | E       | Alemania             | 1-0                       | Costa de Marfil      | 61-23-17              | 60-23-17                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  34 | E       | Ecuador              | 2-0                       | Curazao              | 81-13-5               | 82-13-5                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  35 | F       | Países Bajos         | 1-0                       | Suecia               | 58-24-18              | 58-24-18                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  36 | F       | Túnez                | 0-1                       | Japón                | 20-28-51              | 20-28-52                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  37 | H       | Uruguay              | 1-0                       | Cabo Verde           | 69-20-11              | 69-20-11                     | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  38 | H       | España               | 3-0                       | Arabia Saudita       | 85-12-3               | 85-12-3                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  39 | G       | Bélgica              | 1-0                       | Irán                 | 67-21-12              | 67-21-12                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  40 | G       | Nueva Zelanda        | 0-1                       | Egipto               | 17-25-58              | 17-25-58                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  41 | I       | Noruega              | 1-0                       | Senegal              | 39-28-33              | 39-28-33                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  42 | I       | Francia              | 2-0                       | Irak                 | 84-13-3               | 84-13-3                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  43 | J       | Argentina            | 2-0                       | Austria              | 61-25-14              | 61-25-14                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  44 | J       | Jordania             | 0-1                       | Argelia              | 13-23-63              | 13-23-64                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  45 | L       | Inglaterra           | 2-0                       | Ghana                | 75-17-7               | 76-17-7                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  46 | L       | Panamá               | 0-1                       | Croacia              | 13-22-65              | 13-22-65                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  47 | K       | Portugal             | 2-0                       | Uzbekistán           | 79-15-6               | 79-15-6                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  48 | K       | Colombia             | 2-0                       | RD Congo             | 67-22-12              | 66-22-12                     | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  49 | C       | Escocia              | 0-3                       | Brasil               | 11-19-70              | 11-19-70                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  50 | C       | Marruecos            | 2-0                       | Haití                | 77-17-6               | 77-17-6                      | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  51 | B       | Suiza                | 1-0                       | Canadá               | 42-29-29              | 42-29-29                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  52 | B       | Bosnia y Herzegovina | 1-0                       | Qatar                | 58-25-18              | 57-25-18                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  53 | A       | Chequia              | 0-2                       | México               | 18-25-58              | 18-25-57                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  54 | A       | Sudáfrica            | 0-1                       | Corea del Sur        | 24-29-47              | 24-29-47                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  55 | E       | Curazao              | 0-2                       | Costa de Marfil      | 6-16-77               | 6-16-78                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  56 | E       | Ecuador              | 0-1                       | Alemania             | 23-27-51              | 23-27-50                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  57 | F       | Japón                | 1-1                       | Suecia               | 44-28-28              | 44-28-28                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  58 | F       | Túnez                | 0-1                       | Países Bajos         | 12-22-66              | 12-22-66                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  59 | D       | Türkiye              | 1-1                       | Estados Unidos       | 37-28-35              | 37-28-35                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  60 | D       | Paraguay             | 1-1                       | Australia            | 40-29-31              | 40-29-31                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  61 | I       | Noruega              | 0-1                       | Francia              | 17-25-58              | 17-25-58                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  62 | I       | Senegal              | 2-0                       | Irak                 | 73-18-9               | 73-18-9                      | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  63 | G       | Egipto               | 1-1                       | Irán                 | 41-30-28              | 41-30-28                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  64 | G       | Nueva Zelanda        | 0-2                       | Bélgica              | 7-17-76               | 7-17-76                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  65 | H       | Cabo Verde           | 1-1                       | Arabia Saudita       | 36-29-35              | 36-29-35                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  66 | H       | Uruguay              | 0-1                       | España               | 17-25-58              | 17-25-58                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  67 | L       | Panamá               | 0-2                       | Inglaterra           | 8-16-77               | 8-16-76                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  68 | L       | Croacia              | 1-0                       | Ghana                | 54-27-19              | 54-27-19                     | Media-Alta                 | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  69 | J       | Argelia              | 0-1                       | Austria              | 34-30-36              | 34-30-36                     | Baja                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  70 | J       | Jordania             | 0-3                       | Argentina            | 4-14-82               | 4-14-82                      | Alta                       | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  71 | K       | Colombia             | 1-1                       | Portugal             | 27-29-44              | 27-29-44                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |
|  72 | K       | RD Congo             | 1-1                       | Uzbekistán           | 40-29-31              | 40-29-31                     | Media                      | nan                   | Sin cobertura SofaScore odds en esta muestra; se conserva v8.4A.         |

---

# 5. Partidos Cubiertos por Consenso SofaScore + The Odds API

|   M | Grupo   | Equipo A      | Marcador 8.4B-Consensus   | Equipo B   | Prob. A-E-B 8.4A-TM   | Prob. A-E-B 8.4B-Consensus   | Confianza 8.4B-Consensus   | MarketConsensusFlag   | Nota 8.4B-Consensus                                                      |
|----:|:--------|:--------------|:--------------------------|:-----------|:----------------------|:-----------------------------|:---------------------------|:----------------------|:-------------------------------------------------------------------------|
|   1 | A       | México        | 2-0                       | Sudáfrica  | 71-19-9               | 68-21-11                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   2 | A       | Corea del Sur | 1-1                       | Chequia    | 37-30-33              | 36-30-33                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   5 | C       | Haití         | 0-1                       | Escocia    | 14-23-63              | 15-22-63                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   6 | D       | Australia     | 0-1                       | Türkiye    | 19-26-55              | 20-26-54                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   7 | C       | Brasil        | 1-0                       | Marruecos  | 54-26-21              | 57-25-18                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|   8 | B       | Qatar         | 0-2                       | Suiza      | 7-16-77               | 7-15-77                      | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|  10 | E       | Alemania      | 3-0                       | Curazao    | 89-9-2                | 92-6-2                       | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |
|  11 | F       | Países Bajos  | 1-0                       | Japón      | 52-26-22              | 49-26-25                     | Media-Alta                 | Consenso alto         | SofaScore y The Odds API son consistentes; aumenta confianza de mercado. |

---

# 6. Detalle de Consenso SofaScore vs The Odds API

|   game_id | home_team   | away_team            |   sofa_odds_home |   sofa_odds_draw |   sofa_odds_away | p_sofa_home_no_vig   | p_sofa_draw_no_vig   | p_sofa_away_no_vig   | p_market_home_no_vig   | p_market_draw_no_vig   | p_market_away_no_vig   | p_consensus_home   | p_consensus_draw   | p_consensus_away   | max_abs_delta_sofa_theodds   | MarketConsensusFlag   |
|----------:|:------------|:---------------------|-----------------:|-----------------:|-----------------:|:---------------------|:---------------------|:---------------------|:-----------------------|:-----------------------|:-----------------------|:-------------------|:-------------------|:-------------------|:-----------------------------|:----------------------|
|  15186526 | Qatar       | Switzerland          |            12    |             6.25 |             1.22 | 7.8%                 | 15.1%                | 77.1%                | 7.5%                   | 15.1%                  | 77.4%                  | 7.6%               | 15.1%              | 77.4%              | 0.4%                         | Consenso alto         |
|  15186710 | Mexico      | South Africa         |             1.4  |             4.33 |             8    | 66.8%                | 21.6%                | 11.7%                | 67.0%                  | 21.6%                  | 11.4%                  | 67.0%              | 21.6%              | 11.5%              | 0.3%                         | Consenso alto         |
|  15186720 | South Korea | Czechia              |             2.6  |             3.1  |             2.75 | 35.9%                | 30.1%                | 34.0%                | 36.2%                  | 30.4%                  | 33.5%                  | 36.1%              | 30.3%              | 33.6%              | 0.5%                         | Consenso alto         |
|  15186836 | Canada      | Bosnia & Herzegovina |             1.8  |             3.7  |             4.5  | 53.0%                | 25.8%                | 21.2%                | 52.7%                  | 26.2%                  | 21.1%                  | 52.8%              | 26.1%              | 21.1%              | 0.5%                         | Consenso alto         |
|  15186850 | Brazil      | Morocco              |             1.62 |             3.8  |             5.75 | 58.5%                | 25.0%                | 16.5%                | 59.0%                  | 24.4%                  | 16.6%                  | 58.9%              | 24.6%              | 16.6%              | 0.5%                         | Consenso alto         |
|  15186853 | Haiti       | Scotland             |             5.5  |             4.75 |             1.5  | 17.2%                | 19.9%                | 63.0%                | 14.4%                  | 21.8%                  | 63.8%                  | 15.1%              | 21.3%              | 63.6%              | 2.7%                         | Consenso alto         |
|  15186873 | USA         | Paraguay             |             1.95 |             3.4  |             4    | 48.5%                | 27.8%                | 23.7%                | 48.1%                  | 27.8%                  | 24.1%                  | 48.2%              | 27.8%              | 24.0%              | 0.4%                         | Consenso alto         |
|  15186874 | Australia   | Türkiye              |             4.75 |             3.6  |             1.75 | 19.9%                | 26.2%                | 53.9%                | 20.0%                  | 26.2%                  | 53.7%                  | 20.0%              | 26.2%              | 53.8%              | 0.2%                         | Consenso alto         |
|  15186899 | Germany     | Curaçao              |             1.03 |            19    |            41    | 92.6%                | 5.0%                 | 2.3%                 | 92.6%                  | 5.5%                   | 1.9%                   | 92.6%              | 5.4%               | 2.0%               | 0.5%                         | Consenso alto         |
|  15186945 | Netherlands | Japan                |             1.95 |             3.8  |             3.5  | 48.3%                | 24.8%                | 26.9%                | 48.0%                  | 26.2%                  | 25.8%                  | 48.1%              | 25.8%              | 26.1%              | 1.4%                         | Consenso alto         |

---

# 7. Capa Transfermarkt — Talento y Profundidad

| Selección            |   squad_size |   avg_age_tm |   wc_particip | foreigners_pct   | market_value_m_eur   | avg_market_value_m_eur   |   tm_squad_signal |
|:---------------------|-------------:|-------------:|--------------:|:-----------------|:---------------------|:-------------------------|------------------:|
| Francia              |           26 |         27   |            17 | 73.1%            | €1,520.00m           | €58.58m                  |              1.57 |
| Inglaterra           |           26 |         27.2 |            17 | 19.2%            | €1,360.00m           | €52.43m                  |              1.53 |
| España               |           26 |         26.8 |            18 | 34.6%            | €1,220.00m           | €47.03m                  |              1.42 |
| Portugal             |           26 |         28   |            10 | 80.8%            | €1,010.00m           | €38.67m                  |              1.11 |
| Alemania             |           26 |         28.1 |            21 | 26.9%            | €947.00m             | €36.42m                  |              1.23 |
| Brasil               |           26 |         29.2 |            23 | 73.1%            | €923.20m             | €35.51m                  |              1.07 |
| Países Bajos         |           26 |         27.8 |            12 | 92.3%            | €804.20m             | €30.93m                  |              1.04 |
| Argentina            |           25 |         29.1 |            20 | 92.0%            | €782.50m             | €31.30m                  |              0.96 |
| Noruega              |           26 |         26.8 |             4 | 84.6%            | €589.90m             | €22.69m                  |              0.65 |
| Bélgica              |           26 |         27.6 |            15 | 88.5%            | €547.50m             | €21.06m                  |              0.89 |
| Costa de Marfil      |           26 |         25.9 |             4 | 100.0%           | €522.10m             | €20.08m                  |              0.44 |
| Marruecos            |           26 |         26.4 |             8 | 92.3%            | €498.30m             | €19.17m                  |              0.63 |
| Senegal              |           26 |         27.1 |             4 | 100.0%           | €478.10m             | €18.39m                  |              0.57 |
| Türkiye              |           26 |         27.7 |             3 | 42.3%            | €473.70m             | €18.22m                  |              0.45 |
| Suecia               |           26 |         27.6 |            13 | 88.5%            | €406.08m             | €15.62m                  |              0.68 |
| Croacia              |           26 |         28.3 |             7 | 92.3%            | €387.30m             | €14.90m                  |              0.41 |
| Estados Unidos       |           26 |         26.9 |            12 | 73.1%            | €385.65m             | €14.83m                  |              0.64 |
| Ecuador              |           26 |         26.1 |             5 | 92.3%            | €368.70m             | €14.18m                  |              0.31 |
| Uruguay              |           26 |         28.8 |            16 | 100.0%           | €359.30m             | €13.82m                  |              0.48 |
| Suiza                |           26 |         28.3 |            13 | 92.3%            | €332.50m             | €12.79m                  |              0.45 |
| Colombia             |           26 |         30.1 |             7 | 96.2%            | €302.35m             | €11.63m                  |             -0.05 |
| Japón                |           26 |         27.8 |             8 | 88.5%            | €270.85m             | €10.42m                  |              0.3  |
| Argelia              |           26 |         26.9 |             5 | 88.5%            | €256.90m             | €9.88m                   |              0.21 |
| Austria              |           25 |         28.6 |             9 | 88.0%            | €242.20m             | €9.69m                   |              0.15 |
| Ghana                |           27 |         26.8 |             5 | 96.3%            | €234.60m             | €8.69m                   |              0.13 |
| Canadá               |           25 |         27.1 |             3 | 92.0%            | €196.65m             | €7.87m                   |             -0.01 |
| México               |           26 |         27.9 |            18 | 53.8%            | €191.85m             | €7.38m                   |              0.26 |
| Chequia              |           26 |         27.6 |             2 | 34.6%            | €188.18m             | €7.24m                   |             -0.16 |
| Escocia              |           26 |         29.2 |             9 | 69.2%            | €170.25m             | €6.55m                   |             -0.16 |
| Paraguay             |           26 |         29   |            10 | 88.5%            | €153.65m             | €5.91m                   |             -0.16 |
| Bosnia y Herzegovina |           26 |         26.4 |             2 | 96.2%            | €151.60m             | €5.83m                   |             -0.34 |
| RD Congo             |           26 |         29.1 |             1 | 100.0%           | €143.90m             | €5.53m                   |             -0.63 |
| Corea del Sur        |           26 |         28.1 |            12 | 73.1%            | €139.05m             | €5.35m                   |             -0.05 |
| Egipto               |           26 |         29.1 |             4 | 34.6%            | €116.48m             | €4.48m                   |             -0.53 |
| Uzbekistán           |           26 |         28.5 |             1 | 42.3%            | €85.33m              | €3.28m                   |             -0.84 |
| Australia            |           26 |         27.4 |             7 | 80.8%            | €77.45m              | €2.98m                   |             -0.4  |
| Túnez                |           26 |         26.7 |             7 | 76.9%            | €69.95m              | €2.69m                   |             -0.5  |
| Haití                |           26 |         27.6 |             2 | 96.2%            | €55.90m              | €2.15m                   |             -0.85 |
| Cabo Verde           |           26 |         29.7 |             1 | 100.0%           | €54.50m              | €2.10m                   |             -1.28 |
| Sudáfrica            |           26 |         26.8 |             4 | 26.9%            | €49.25m              | €1.89m                   |             -0.79 |
| Arabia Saudita       |           26 |         28.5 |             7 | 3.8%             | €40.68m              | €1.56m                   |             -0.91 |
| Panamá               |           26 |         30.4 |             2 | 92.3%            | €34.55m              | €1.33m                   |             -1.58 |
| Nueva Zelanda        |           26 |         28.1 |             3 | 69.2%            | €34.35m              | €1.32m                   |             -1.11 |
| Irán                 |           26 |         30.4 |             7 | 34.6%            | €32.05m              | €1.23m                   |             -1.38 |
| Curazao              |           26 |         28   |             1 | 100.0%           | €25.78m              | €0.99m                   |             -1.41 |
| Irak                 |           26 |         26.9 |             2 | 61.5%            | €21.20m              | €0.81m                   |             -1.33 |
| Jordania             |           25 |         28.8 |             1 | 56.0%            | €20.00m              | €0.80m                   |             -1.65 |
| Qatar                |           26 |         29.5 |             2 | 3.8%             | €19.93m              | €0.77m                   |             -1.65 |

---

# 8. Top 10 Goleadores — Modelo v8.5

|   Ranking 8.4A-TM | Jugador           | Selección   |   Goles esperados 8.4A-TM | Probabilidad 8.4A-TM   |   Ranking | Rol ofensivo                               |   Partidos esperados selección | Prob. titularidad   |   Minutos esperados / partido | Riesgo rotación   | Disponibilidad médica   |
|------------------:|:------------------|:------------|--------------------------:|:-----------------------|----------:|:-------------------------------------------|-------------------------------:|:--------------------|------------------------------:|:------------------|:------------------------|
|                 1 | Kylian Mbappé     | Francia     |                      5.13 | 99.49%                 |         1 | Finalizador principal + penales            |                           6.05 | 96%                 |                            82 | Bajo-Medio        | Alta                    |
|                 2 | Harry Kane        | Inglaterra  |                      4.79 | 96.07%                 |         2 | 9 principal + penales                      |                           5.82 | 94%                 |                            82 | Bajo-Medio        | Alta                    |
|                 3 | Erling Haaland    | Noruega     |                      4.26 | 93.46%                 |         3 | 9 principal, máxima cuota de xG            |                           4.62 | 98%                 |                            88 | Bajo              | Alta                    |
|                 4 | Lionel Messi      | Argentina   |                      3.77 | 85.07%                 |         4 | Creador-finalizador + balón parado/penales |                           5.52 | 85%                 |                            74 | Medio-Alto        | Media-Alta              |
|                 5 | Mikel Oyarzabal   | España      |                      3.63 | 75.65%                 |         5 | Delantero / falso 9                        |                           5.9  | 73%                 |                            66 | Medio-Alto        | Media-Alta              |
|                 6 | Vinícius Júnior   | Brasil      |                      3.41 | 90.14%                 |         6 | Extremo finalizador                        |                           5.46 | 91%                 |                            79 | Medio             | Alta                    |
|                 7 | Julián Álvarez    | Argentina   |                      3.34 | 77.07%                 |         7 | Delantero móvil / presión / definición     |                           5.52 | 77%                 |                            69 | Medio             | Alta                    |
|                 8 | Lamine Yamal      | España      |                      3.24 | 91.19%                 |         8 | Extremo creador-finalizador                |                           5.9  | 88%                 |                            74 | Medio             | Media-Alta              |
|                 9 | Luis Díaz         | Colombia    |                      2.88 | 88.17%                 |         9 | Principal amenaza ofensiva                 |                           4.9  | 94%                 |                            82 | Bajo              | Alta                    |
|                10 | Cristiano Ronaldo | Portugal    |                      2.79 | 67.68%                 |        10 | 9 de área + penales                        |                           5.6  | 68%                 |                            61 | Alto              | Media                   |

**Nota:** la tabla de goleadores se conserva como proxy v8.4A-TM. No incorpora player xG real, lineups ni minutos esperados porque SofaScore/datafc no entregó todavía esas capas.

---

# 9. Metodología Técnica

## 9.1 Selecciones

El modelo de selecciones mantiene la estructura:

```text
Strength_v8.5_country =
  Strength_8.2D_EloActual
+ Transfermarkt_TalentDepthLayer
```

La capa Transfermarkt usa:

```text
TM_SquadSignal =
  0.50 · TalentZ
+ 0.20 · AvgValueZ
+ 0.18 · ExperienceZ
+ 0.12 · PrimeAgeZ
- 0.20 · AgingPenalty
```

Luego:

```text
p_phase_8.4A =
  p_phase_8.2D × exp(s_phase × TM_SquadSignal)
```

La sensibilidad aumenta con la profundidad de fase, pero se mantiene moderada porque Transfermarkt es proxy de talento, no rendimiento observado.

---

## 9.2 Probabilidades 1X2

La capa principal sigue siendo The Odds API. SofaScore entra como validador secundario.

Para partidos con odds SofaScore:

```text
p_market_consensus =
  0.75 · p_TheOddsAPI_no_vig
+ 0.25 · p_SofaScore_no_vig
```

Luego:

```text
p_v8.5 =
  normalize(
    0.30 · p_v8.4A
  + 0.70 · p_market_consensus
  )
```

Para partidos sin cobertura SofaScore:

```text
p_v8.5 = p_v8.4A
```

---

## 9.3 Marcadores

Los marcadores quedan conservados desde v8.4A-TM:

```text
Marcador_v8.5 = Marcador_v8.4A-TM
```

No se recalculan por xG porque:

```text
shots_data = no disponible
lineups_data = no disponible
match_stats_data = no disponible
player_stats_data = no disponible
```

---

## 9.4 Goleadores

La capa de goleadores conserva el proxy:

```text
ExpectedGoals_Player_v8.5 =
  ExpectedGoals_Player_8.4A-TM
```

No se recalibra con SofaScore porque no hay:

```text
squads
player_stats
lineups
shots/xG
minutes
```

---

# 10. Análisis de Riesgo e Incertidumbre

## 10.1 Riesgos de primer orden

| Riesgo | Impacto |
|---|---|
| Odds tempranas | Pueden moverse fuertemente con lesiones, convocatorias o lineups |
| SofaScore odds incompletas | Solo validan parcialmente el mercado |
| Sin xG/O-U | Limita scorelines exactos |
| Sin player-level | Limita goleadores |
| Transfermarkt como proxy | Puede sesgar por edad, liga, visibilidad y mercado europeo |

## 10.2 Riesgos de segundo orden

| Riesgo | Impacto |
|---|---|
| Sobreponderar mercado | Puede absorber sesgo de demanda pública |
| Mantener scorelines sin xG | Puede subestimar partidos abiertos o cerrados |
| Formato de 48 equipos | Puede alterar tasas históricas de empate y rotación |
| Tercera fecha de grupos | Puede generar incentivos no lineales |
| Lesiones de última hora | Pueden romper supuestos de talento y ruta |

---

# 11. Supuestos Ocultos

| Supuesto | Evaluación |
|---|---|
| The Odds API es señal principal de mercado suficientemente robusta | Razonable por cobertura multi-bookmaker |
| SofaScore aporta validación independiente | Razonable, pero parcial |
| Transfermarkt aproxima talento/profundidad | Razonable, pero no es xG |
| Marcadores pueden mantenerse sin xG | Prudente, pero menos preciso |
| Goleadores no deben moverse sin player-level | Correcto metodológicamente |

---

# 12. Mejor Contraargumento

El mejor contraargumento contra v8.5 es:

> “Sin xG/O-U ni lineups, la actualización de probabilidades no necesariamente mejora los marcadores exactos.”

Este contraargumento es sólido. Por eso v8.5 distingue explícitamente entre:

```text
probabilidades 1X2 mejoradas
vs
marcadores conservados
```

y no vende xG donde no existe.

---

# 13. Información que Cambiaría la Conclusión

La versión v8.5 debería recalcularse si se obtiene:

1. Over/Under 2.5 y líneas de goles.
2. xG/xGA de equipo.
3. Shots/xG vía SofaScore o proveedor alterno.
4. Lineups probables.
5. Player stats y minutos.
6. Lesiones y suspensiones.
7. Penaleros confirmados.
8. Odds Golden Boot.
9. Nuevas odds 1X2 más cercanas a los partidos.

---

# 14. Próximos Pasos

## Fase 8.6 — Over/Under & Goal Lines

Objetivo:

```text
Traducir probabilidades 1X2 + líneas de goles en marcadores más robustos.
```

Fuentes candidatas:

- The Odds API totals.
- SofaScore odds adicionales si hay mercado O/U.
- Bookmakers con líneas de goles.

## Fase 8.7 — Player-Level & xG

Objetivo:

```text
Actualizar goleadores y scorelines con shots/xG/lineups/player stats.
```

Fuentes candidatas:

- SofaScore/datafc si activa `shots_data`, `lineups_data`, `player_stats_data`.
- Enetpulse.
- Stats Perform/Opta.
- Sportmonks.
- TheStatsAPI si se activa plan.

---

# 15. Conclusión Final

El **Modelo v8.5** debe adoptarse como versión integrada actual porque mejora el sistema en dos frentes:

1. Mantiene la mejor lectura estructural de selecciones con Elo + Transfermarkt.
2. Mejora probabilidades de partidos con consenso de mercado The Odds API + SofaScore/datafc.

Pero no debe presentarse como una versión con xG ni player-level real.

```text
v8.5 = mejor versión operativa actual
v8.5 ≠ versión final con xG/player-level
```

---

## Nivel de confianza

**Medio-Alto** para selecciones y probabilidades 1X2.  
**Medio** para marcadores exactos.  
**Medio-Bajo** para goleadores sin player-level.

## Factores que podrían cambiar la conclusión

- xG/xGA,
- over-under,
- lineups,
- lesiones,
- player stats,
- minutos esperados,
- penaleros,
- odds Golden Boot,
- cuotas más cercanas al partido.

## Acción recomendada

Usar **ChatGPT Mundial 2026 · Modelo v8.5** como versión integrada actual para comparación con otras IAs, dejando claro que SofaScore/datafc fue adoptado como validación de mercado y que xG/player-level siguen pendientes.
