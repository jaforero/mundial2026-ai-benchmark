# FASE 7 — Recalibración del Pronóstico (Claude v7)

## 1. Ranking de 48 Selecciones y Probabilidades

*Recalibración: se aplicó un encogimiento hacia la tasa base de cada ronda para corregir el exceso de confianza detectado en v6. El favorito baja -2.26 pp y la cola de baja probabilidad (<1%) sube +4.24 pp en conjunto; el orden se conserva. Todo se expresa como probabilidad estimada, no como certeza.*

| Ranking | Selección | R32 | Octavos | Cuartos | Semis | Final | Campeón |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **España** | 98.0% | 86.5% | 51.8% | 33.1% | 23.4% | **16.0%** |
| **2** | **Argentina** | 96.7% | 81.4% | 43.1% | 25.6% | 16.8% | **10.5%** |
| **3** | **Inglaterra** | 96.5% | 74.3% | 41.9% | 22.1% | 13.9% | **8.0%** |
| **4** | **Brasil** | 96.9% | 73.5% | 41.6% | 21.8% | 13.0% | **7.4%** |
| **5** | **Francia** | 94.0% | 72.5% | 37.5% | 19.4% | 11.8% | **6.7%** |
| **6** | **Portugal** | 91.3% | 60.3% | 32.7% | 17.2% | 9.1% | **4.7%** |
| **7** | **Alemania** | 96.0% | 63.5% | 33.2% | 16.6% | 8.2% | **4.2%** |
| **8** | **Países Bajos** | 89.5% | 55.3% | 30.1% | 15.4% | 7.5% | **3.7%** |
| **9** | **Colombia** | 89.1% | 58.2% | 29.6% | 14.5% | 7.5% | **3.6%** |
| **10** | **Bélgica** | 91.9% | 53.4% | 29.5% | 16.7% | 7.4% | **2.9%** |
| **11** | **Ecuador** | 90.7% | 48.9% | 25.1% | 11.8% | 5.6% | **2.4%** |
| **12** | **Japón** | 86.3% | 49.6% | 25.1% | 11.7% | 5.3% | **2.4%** |
| **13** | **México** | 90.2% | 49.6% | 25.8% | 14.0% | 5.9% | **2.2%** |
| **14** | **Uruguay** | 88.5% | 44.3% | 22.1% | 10.9% | 5.5% | **2.2%** |
| **15** | **Marruecos** | 88.4% | 47.4% | 22.8% | 10.1% | 4.7% | **1.9%** |
| **16** | **Croacia** | 88.8% | 43.9% | 21.8% | 10.2% | 4.8% | **1.9%** |
| **17** | **Suiza** | 94.8% | 47.5% | 22.9% | 10.7% | 4.6% | **1.9%** |
| **18** | **Noruega** | 80.5% | 39.0% | 18.1% | 7.9% | 3.4% | **1.4%** |
| **19** | **Canadá** | 91.8% | 44.6% | 21.5% | 10.7% | 4.0% | **1.3%** |
| **20** | **Estados Unidos** | 74.0% | 37.7% | 18.9% | 9.4% | 3.7% | **1.2%** |
| **21** | **Türkiye** | 74.3% | 34.5% | 15.6% | 7.0% | 2.8% | **1.0%** |
| **22** | **Senegal** | 69.9% | 32.3% | 15.7% | 7.6% | 3.0% | **1.0%** |
| **23** | **Austria** | 74.6% | 34.0% | 16.3% | 7.7% | 2.9% | **1.0%** |
| **24** | **Corea del Sur** | 74.9% | 31.3% | 14.1% | 6.1% | 2.1% | **0.7%** |
| **25** | **Irán** | 76.5% | 32.9% | 15.2% | 6.6% | 2.2% | **0.7%** |
| **26** | **Paraguay** | 61.7% | 26.8% | 12.7% | 5.6% | 2.0% | **0.7%** |
| **27** | **Australia** | 65.1% | 27.8% | 12.1% | 5.4% | 2.0% | **0.7%** |
| **28** | **Argelia** | 63.6% | 25.3% | 11.8% | 5.2% | 1.7% | **0.6%** |
| **29** | **Costa de Marfil** | 71.0% | 24.0% | 10.3% | 4.2% | 1.4% | **0.5%** |
| **30** | **Escocia** | 65.6% | 22.8% | 9.5% | 3.9% | 1.3% | **0.5%** |
| **31** | **Chequia** | 65.4% | 23.2% | 9.8% | 4.0% | 1.3% | **0.5%** |
| **32** | **Egipto** | 63.1% | 20.9% | 8.4% | 3.3% | 1.1% | **0.4%** |
| **33** | **Suecia** | 50.6% | 16.4% | 7.0% | 3.0% | 1.1% | **0.4%** |
| **34** | **Uzbekistán** | 49.6% | 16.7% | 6.9% | 2.8% | 1.0% | **0.4%** |
| **35** | **Túnez** | 42.9% | 12.9% | 5.3% | 2.3% | 0.8% | **0.4%** |
| **36** | **RD Congo** | 34.7% | 9.0% | 3.7% | 1.6% | 0.7% | **0.3%** |
| **37** | **Sudáfrica** | 40.7% | 8.9% | 3.4% | 1.4% | 0.6% | **0.3%** |
| **38** | **Arabia Saudí** | 37.6% | 7.9% | 2.9% | 1.3% | 0.6% | **0.3%** |
| **39** | **Jordania** | 31.3% | 7.9% | 3.2% | 1.4% | 0.6% | **0.3%** |
| **40** | **Panamá** | 44.1% | 11.1% | 4.0% | 1.6% | 0.6% | **0.3%** |
| **41** | **Bosnia** | 46.5% | 8.2% | 2.9% | 1.2% | 0.6% | **0.3%** |
| **42** | **Nueva Zelanda** | 37.5% | 7.9% | 2.9% | 1.2% | 0.6% | **0.3%** |
| **43** | **Iraq** | 25.0% | 5.8% | 2.5% | 1.1% | 0.6% | **0.3%** |
| **44** | **Ghana** | 31.2% | 5.5% | 2.2% | 1.1% | 0.5% | **0.3%** |
| **45** | **Qatar** | 29.6% | 3.9% | 1.8% | 0.9% | 0.5% | **0.3%** |
| **46** | **Haití** | 16.8% | 3.1% | 1.6% | 0.9% | 0.5% | **0.3%** |
| **47** | **Curazao** | 13.2% | 2.3% | 1.4% | 0.8% | 0.5% | **0.3%** |
| **48** | **Cabo Verde** | 29.0% | 5.1% | 2.0% | 1.0% | 0.5% | **0.3%** |

## 2. Predicción de 72 Partidos y Marcadores

*Se infló la probabilidad de empate en partidos parejos y se calculó un índice de incertidumbre (entropía de los tres resultados). Los partidos de **alta incertidumbre** se marcan con ⚠; en ellos el marcador se ajustó hacia el empate o a un margen de un gol cuando el riesgo lo justifica. 31 de 72 partidos quedaron en alta incertidumbre y 18 marcadores se ajustaron.*

### Grupo A
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **México vs Sudáfrica** | 1-0 | 60.7% | 27.5% | 11.8% | Media |
| **México vs Corea del Sur** | 1-1 | 45.2% | 32.9% | 21.9% | ⚠ Alta |
| **México vs Chequia** | 1-0 | 50.1% | 31.4% | 18.5% | ⚠ Alta |
| **Sudáfrica vs Corea del Sur** | 0-1 | 18.6% | 33.8% | 47.6% | ⚠ Alta |
| **Sudáfrica vs Chequia** | 0-1 | 22.4% | 35.8% | 41.8% | ⚠ Alta |
| **Corea del Sur vs Chequia** | 1-1 *(ajustado)* | 36.6% | 36.2% | 27.2% | ⚠ Alta |

### Grupo B
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Canadá vs Bosnia** | 1-0 | 61.2% | 26.8% | 12.0% | Media |
| **Canadá vs Qatar** | 2-0 | 69.8% | 21.5% | 8.7% | Baja |
| **Canadá vs Suiza** | 1-1 | 26.1% | 34.9% | 39.0% | ⚠ Alta |
| **Bosnia vs Qatar** | 1-1 *(ajustado)* | 38.6% | 36.0% | 25.4% | ⚠ Alta |
| **Bosnia vs Suiza** | 0-2 | 10.4% | 24.7% | 64.9% | Baja |
| **Qatar vs Suiza** | 0-2 | 7.1% | 19.4% | 73.5% | Baja |

### Grupo C
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Brasil vs Marruecos** | 1-0 | 48.2% | 33.1% | 18.7% | ⚠ Alta |
| **Brasil vs Haití** | 3-0 | 84.6% | 11.9% | 3.5% | Baja |
| **Brasil vs Escocia** | 2-0 | 63.6% | 24.9% | 11.5% | Media |
| **Marruecos vs Haití** | 2-0 | 70.7% | 22.0% | 7.2% | Baja |
| **Marruecos vs Escocia** | 1-0 | 46.9% | 35.5% | 17.7% | ⚠ Alta |
| **Haití vs Escocia** | 0-1 | 14.7% | 28.6% | 56.6% | Media |

### Grupo D
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Estados Unidos vs Paraguay** | 1-1 | 38.0% | 35.0% | 27.0% | ⚠ Alta |
| **Estados Unidos vs Australia** | 1-1 *(ajustado)* | 36.5% | 35.1% | 28.4% | ⚠ Alta |
| **Estados Unidos vs Türkiye** | 1-1 *(ajustado)* | 32.7% | 33.7% | 33.5% | ⚠ Alta |
| **Paraguay vs Australia** | 1-1 *(ajustado)* | 28.7% | 39.9% | 31.4% | ⚠ Alta |
| **Paraguay vs Türkiye** | 1-1 *(ajustado)* | 26.5% | 36.6% | 36.9% | ⚠ Alta |
| **Australia vs Türkiye** | 1-1 *(ajustado)* | 27.7% | 36.4% | 35.9% | ⚠ Alta |

### Grupo E
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Alemania vs Curazao** | 3-0 | 86.8% | 10.4% | 2.9% | Baja |
| **Alemania vs Costa de Marfil** | 1-0 | 54.9% | 29.6% | 15.5% | Media |
| **Alemania vs Ecuador** | 1-1 *(ajustado)* | 35.8% | 37.5% | 26.8% | ⚠ Alta |
| **Curazao vs Costa de Marfil** | 0-1 | 11.8% | 28.5% | 59.7% | Media |
| **Curazao vs Ecuador** | 0-2 | 5.9% | 20.9% | 73.2% | Baja |
| **Costa de Marfil vs Ecuador** | 0-1 | 17.7% | 37.6% | 44.8% | ⚠ Alta |

### Grupo F
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Países Bajos vs Japón** | 1-1 *(ajustado)* | 34.8% | 36.5% | 28.7% | ⚠ Alta |
| **Países Bajos vs Suecia** | 2-0 | 58.4% | 26.3% | 15.3% | Media |
| **Países Bajos vs Túnez** | 1-0 | 56.3% | 30.7% | 13.0% | Media |
| **Japón vs Suecia** | 1-0 | 53.8% | 29.3% | 17.0% | Media |
| **Japón vs Túnez** | 1-0 | 53.3% | 33.0% | 13.7% | Media |
| **Suecia vs Túnez** | 1-1 *(ajustado)* | 35.1% | 37.7% | 27.2% | ⚠ Alta |

### Grupo G
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Bélgica vs Egipto** | 1-0 | 51.4% | 32.1% | 16.5% | Media |
| **Bélgica vs Irán** | 1-1 | 44.0% | 34.0% | 22.0% | ⚠ Alta |
| **Bélgica vs Nueva Zelanda** | 2-0 | 66.3% | 24.2% | 9.5% | Baja |
| **Egipto vs Irán** | 1-1 *(ajustado)* | 24.6% | 38.8% | 36.6% | ⚠ Alta |
| **Egipto vs Nueva Zelanda** | 1-1 *(ajustado)* | 39.8% | 38.3% | 21.9% | ⚠ Alta |
| **Irán vs Nueva Zelanda** | 1-0 | 49.7% | 33.5% | 16.8% | Media |

### Grupo H
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **España vs Cabo Verde** | 2-0 | 84.8% | 12.0% | 3.2% | Baja |
| **España vs Arabia Saudí** | 2-0 | 80.5% | 15.4% | 4.1% | Baja |
| **España vs Uruguay** | 1-0 | 50.9% | 32.1% | 17.0% | Media |
| **Cabo Verde vs Arabia Saudí** | 1-1 *(ajustado)* | 27.6% | 39.9% | 32.5% | ⚠ Alta |
| **Cabo Verde vs Uruguay** | 0-1 | 9.3% | 26.2% | 64.6% | Baja |
| **Arabia Saudí vs Uruguay** | 0-1 | 11.8% | 31.8% | 56.4% | Media |

### Grupo I
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Francia vs Senegal** | 1-0 | 51.1% | 31.8% | 17.1% | Media |
| **Francia vs Iraq** | 2-0 | 74.2% | 19.6% | 6.2% | Baja |
| **Francia vs Noruega** | 1-1 | 47.4% | 32.0% | 20.7% | ⚠ Alta |
| **Senegal vs Iraq** | 1-0 | 49.6% | 34.0% | 16.4% | Media |
| **Senegal vs Noruega** | 1-1 *(ajustado)* | 27.4% | 36.4% | 36.2% | ⚠ Alta |
| **Iraq vs Noruega** | 0-1 | 11.6% | 27.2% | 61.1% | Media |

### Grupo J
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Argentina vs Argelia** | 1-0 | 65.0% | 25.7% | 9.3% | Baja |
| **Argentina vs Austria** | 1-0 | 56.4% | 30.3% | 13.3% | Media |
| **Argentina vs Jordania** | 2-0 | 77.4% | 17.3% | 5.2% | Baja |
| **Argelia vs Austria** | 1-1 *(ajustado)* | 26.5% | 36.3% | 37.2% | ⚠ Alta |
| **Argelia vs Jordania** | 1-1 | 47.9% | 32.3% | 19.8% | ⚠ Alta |
| **Austria vs Jordania** | 1-0 | 51.9% | 31.0% | 17.1% | Media |

### Grupo K
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Portugal vs RD Congo** | 1-0 | 65.1% | 26.1% | 8.8% | Baja |
| **Portugal vs Uzbekistán** | 1-0 | 56.3% | 30.0% | 13.7% | Media |
| **Portugal vs Colombia** | 1-1 *(ajustado)* | 34.2% | 35.9% | 29.9% | ⚠ Alta |
| **RD Congo vs Uzbekistán** | 1-1 *(ajustado)* | 24.7% | 42.4% | 32.8% | ⚠ Alta |
| **RD Congo vs Colombia** | 0-1 | 10.0% | 28.1% | 62.0% | Media |
| **Uzbekistán vs Colombia** | 0-1 | 14.8% | 31.7% | 53.5% | Media |

### Grupo L
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Inglaterra vs Croacia** | 1-0 | 44.4% | 34.5% | 21.1% | ⚠ Alta |
| **Inglaterra vs Ghana** | 2-0 | 76.0% | 18.4% | 5.5% | Baja |
| **Inglaterra vs Panamá** | 2-0 | 74.3% | 19.3% | 6.4% | Baja |
| **Croacia vs Ghana** | 1-0 | 63.0% | 26.3% | 10.6% | Media |
| **Croacia vs Panamá** | 1-0 | 58.5% | 27.9% | 13.6% | Media |
| **Ghana vs Panamá** | 1-1 *(ajustado)* | 25.3% | 36.1% | 38.6% | ⚠ Alta |

## 3. Top 10 Goleadores Proyectados

*Probabilidades y goles esperados recalibrados (temperatura anti-sobreconfianza). La columna de riesgos resume, por jugador: minutos, rol ofensivo, dificultad del grupo, dependencia del equipo e incertidumbre de titularidad. Fuera del top, el «campo» concentra ~37.6% de la probabilidad de Bota de Oro.*

| Ranking | Jugador (Selección) | Prob. Bota de Oro | Goles esperados | Riesgos (minutos · rol · grupo · dependencia · titularidad) |
| :---: | :--- | :---: | :---: | :--- |
| **1** | **Harry Kane** (Inglaterra) | **15.6%** | 3.43 | minutos bajo · delantero central · grupo baja · dependencia alta · titularidad baja |
| **2** | **Kylian Mbappé** (Francia) | **11.3%** | 2.95 | minutos medio · delantero central · grupo media · dependencia alta · titularidad baja |
| **3** | **Vinícius Júnior** (Brasil) | **5.8%** | 2.20 | minutos medio · extremo finalizador · grupo media · dependencia media · titularidad baja |
| **4** | **Erling Haaland** (Noruega) | **5.6%** | 2.17 | minutos bajo · delantero central · grupo alta · dependencia alta · titularidad baja |
| **5** | **Lionel Messi** (Argentina) | **5.0%** | 2.06 | minutos medio · creador-finalizador · grupo media · dependencia media · titularidad media |
| **6** | **Mikel Oyarzabal** (España) | **4.3%** | 1.95 | minutos alto · falso 9 / delantero · grupo baja · dependencia media · titularidad alta |
| **7** | **Jamal Musiala** (Alemania) | **3.2%** | 1.73 | minutos medio · creador-finalizador · grupo baja · dependencia media · titularidad media |
| **8** | **Luis Díaz** (Colombia) | **3.2%** | 1.73 | minutos medio · extremo finalizador · grupo media · dependencia media · titularidad baja |
| **9** | **Cody Gakpo** (Países Bajos) | **3.1%** | 1.72 | minutos medio · extremo finalizador · grupo media · dependencia media · titularidad media |
| **10** | **Lamine Yamal** (España) | **2.2%** | 1.51 | minutos alto · extremo finalizador · grupo baja · dependencia baja · titularidad media |

## 4. Análisis de Incertidumbre y Cambios vs Versión 6

- **Selecciones — exceso de confianza corregido.** El campeón más probable pasa de 18.2% (v6) a 16.0% (v7). Cambios principales: España -2.26 pp, Argentina -1.37 pp, Inglaterra -0.96 pp, Brasil -0.87 pp, Francia -0.76 pp, Portugal -0.43 pp. Ninguna selección se elimina ni cambia de orden de forma brusca; la masa se redistribuye desde los favoritos hacia el grupo perseguidor.
- **Partidos — incertidumbre explícita.** 31 de 72 encuentros se clasifican de alta incertidumbre (probabilidad máxima < 45% o entropía alta); en esos casos el empate gana peso y el marcador se modera. Esto evita marcadores categóricos en partidos parejos.
- **Goleadores — recalibración y riesgos.** El favorito a la Bota baja +1.64 pp; se añade el desglose de riesgos por jugador. Señales contradictorias típicas: alta dependencia del equipo (sube el techo) junto a incertidumbre de titularidad o minutos (lo baja); ambas se reportan por separado.
- **Variables sobrevaloradas (se atenúan):** la concentración de probabilidad en el favorito de cada categoría y la confianza en rondas profundas de las selecciones top.
- **Variables infravaloradas (se refuerzan):** la probabilidad de empate en partidos parejos, el peso de la cola de selecciones de probabilidad media-baja y el riesgo físico/titularidad de los goleadores.
- **Cómo se corrigió la incertidumbre:** encogimiento hacia la tasa base por ronda (selecciones), inflación de empate proporcional a la paridad e índice de entropía (partidos) y recalibración por temperatura con un «campo» explícito (goleadores).

## 5. Detalle Técnico del Modelo

La capa de recalibración v7 **no reentrena** el motor v5 (ensamble Dixon-Coles + machine learning) ni el modelo de goleadores v6: los toma como base y ajusta su calibración.

1. **Encogimiento hacia la tasa base (selecciones).** Para cada ronda con tasa base *b* = equipos/48, `p' = b + (p − b)·s` con `s` decreciente en rondas profundas (0.97 en R32 → 0.86 en campeón). Se renormaliza cada ronda a su total y se impone monotonía `p(R32) ≥ … ≥ p(Campeón)`.
2. **Inflación de empate dinámica (partidos).** `pD' = pD + β·paridad·(100−pD)/2` con `β = 0.22`; la paridad = `1 − |pA−pB|/100`. Reduce el sesgo de los modelos de goles independientes a subestimar empates en partidos cerrados.
3. **Índice de incertidumbre (partidos).** Entropía normalizada de (pA, pD, pB); alta si máx < 45% o entropía > 0.93. Solo en alta incertidumbre se ajusta el marcador (hacia empate o margen de un gol).
4. **Temperatura anti-sobreconfianza (goleadores).** `p_Bota ∝ p^(1/T)` con `T = 1.12`, conservando la masa de candidatos; los goles esperados se encogen ~3%. La Bota se estima por simulación con binomial negativa (sobredispersa) y un «campo» de goleadores fuera del top.
- **Limitaciones (sin inventar datos):** la capa solo recalibra; no incorpora datos nuevos de plantillas, lesiones o convocatorias oficiales. Los atributos por jugador (rol, cuota, titularidad, disponibilidad, forma) son entradas editables derivadas del pool documentado, no de una base oficial. Las probabilidades de Bota de Oro son de alta varianza por naturaleza. Donde falta información, se mantiene la estimación base y se señala la incertidumbre en lugar de fabricar un valor.

## 6. Códigos Python Separados

### Bloque 1: Simulación / recalibración de selecciones
```python
import json, math, statistics
import numpy as np
# (carga de results_v5.json, groups y elo — ver cabecera del script)

# BLOQUE 1 — SELECCIONES: encogimiento hacia la tasa base por ronda
#   p' = base + (p - base)·s   (s<1 reduce el exceso de confianza)
#   luego se renormaliza cada ronda a su total (nº de equipos) y se
#   impone monotonía p(R32) >= p(R16) >= ... >= p(CAMPEON) por equipo.
# =====================================================================
SHRINK = {"R32":0.97,"R16":0.95,"QF":0.92,"SF":0.90,"FINAL":0.88,"CAMPEON":0.86}

def recalibrate_reach(reach5):
    out = {r: {} for r in ROUND_ORDER}
    for r in ROUND_ORDER:
        base = ROUND_TEAMS[r] / 48.0 * 100.0           # tasa base de la ronda (%)
        s = SHRINK[r]
        shr = {t: base + (reach5[r].get(t, 0.0) - base) * s for t in TEAMS}
        shr = {t: max(0.0, min(100.0, v)) for t, v in shr.items()}
        total = sum(shr.values()); target = ROUND_TEAMS[r] * 100.0
        out[r] = {t: v * target / total for t, v in shr.items()} if total > 0 else shr
    # monotonía por equipo
    for t in TEAMS:
        for i in range(1, len(ROUND_ORDER)):
            a, b = ROUND_ORDER[i-1], ROUND_ORDER[i]
            if out[b][t] > out[a][t]:
                out[b][t] = out[a][t]
    return {r: {t: round(out[r][t], 2) for t in TEAMS} for r in ROUND_ORDER}

reach7 = recalibrate_reach(REACH5)
title7 = dict(reach7["CAMPEON"])
# renormalizar campeón a 100 tras la monotonía
s = sum(title7.values()); title7 = {t: round(v*100.0/s, 4) for t, v in title7.items()}

# =====================================================================
```

### Bloque 2: Simulación / recalibración de partidos
```python
# BLOQUE 2 — PARTIDOS: inflación de empate en partidos parejos +
#   índice de incertidumbre (entropía normalizada) + ajuste de marcador.
# =====================================================================
BETA_DRAW = 0.22   # cuánto se infla el empate en función de la paridad

def shannon(ps):
    return -sum(p*math.log(p) for p in ps if p > 0) / math.log(3)  # 0..1

def modal_draw(la, lb):
    m = (la + lb) / 2.0
    g = 0 if m < 0.75 else (1 if m < 1.6 else 2)
    return f"{g}-{g}"

def recalibrate_match(f):
    pA, pD, pB = f["pA"], f["pD"], f["pB"]
    closeness = 1 - abs(pA - pB) / 100.0                      # 0..1 (1 = parejo)
    pD2 = pD + BETA_DRAW * closeness * (100 - pD) * 0.5        # inflar empate
    rest = 100 - pD2
    s = pA + pB
    pA2, pB2 = (pA*rest/s, pB*rest/s) if s > 0 else (rest/2, rest/2)
    ps = [pA2/100, pD2/100, pB2/100]
    unc = shannon(ps)                                          # índice de incertidumbre
    high = (max(ps) < 0.45) or (unc > 0.93)
    # ajuste de marcador: solo si alta incertidumbre
    score = f["score"]
    la, lb = f.get("la", 1.2), f.get("lb", 1.0)
    adj = False
    if high:
        if pD2 >= max(pA2, pB2) - 3:                          # empate manda o casi
            score = modal_draw(la, lb); adj = True
        else:                                                  # acotar margen a 1
            try:
                ga, gb = map(int, f["score"].split("-"))
                if abs(ga-gb) >= 2:
                    if ga > gb: score = f"{gb+1}-{gb}"
                    else:       score = f"{ga}-{ga+1}"
                    adj = True
            except: pass
    return {"a":f["a"],"b":f["b"],"pA":round(pA2,1),"pD":round(pD2,1),"pB":round(pB2,1),
            "score":score,"unc":round(unc,3),"high_unc":high,"adj":adj,
            "pA5":pA,"pD5":pD,"pB5":pB,"score5":f["score"]}

matches7 = [recalibrate_match(f) for f in FIX]

# =====================================================================
```

### Bloque 3: Top goleadores (recalibración + riesgos)
```python
# BLOQUE 3 — GOLEADORES: recalibración por temperatura + desglose de riesgos.
#   Reutiliza la descomposición v6 (goles de equipo × cuota × penales ×
#   titularidad × disponibilidad × forma) con la reach RECALIBRADA (v7),
#   aplica temperatura para reducir sobreconfianza y clasifica riesgos.
# =====================================================================
# candidatos (mismos del v6) con rol explícito para el desglose de riesgo
# player, team, role, role_share, pen, starter, avail, form
CAND = [
 ("Harry Kane","Inglaterra","Delantero central",0.30,1.12,0.96,0.95,1.06),
 ("Kylian Mbappé","Francia","Delantero central",0.32,1.12,0.96,0.85,1.08),
 ("Erling Haaland","Noruega","Delantero central",0.34,1.05,0.98,0.95,1.12),
 ("Cody Gakpo","Países Bajos","Extremo finalizador",0.26,1.0,0.90,0.90,1.05),
 ("Vinícius Júnior","Brasil","Extremo finalizador",0.24,1.0,0.92,0.85,1.02),
 ("Luis Díaz","Colombia","Extremo finalizador",0.27,1.0,0.94,0.92,1.05),
 ("Jamal Musiala","Alemania","Creador-finalizador",0.22,1.0,0.88,0.88,1.00),
 ("Bukayo Saka","Inglaterra","Extremo finalizador",0.19,1.0,0.82,0.75,0.95),
 ("Lionel Messi","Argentina","Creador-finalizador",0.24,1.12,0.85,0.85,1.00),
 ("Julián Álvarez","Argentina","Delantero móvil",0.22,1.0,0.72,0.65,0.95),
 ("Lamine Yamal","España","Extremo finalizador",0.20,1.0,0.85,0.70,0.95),
 ("Mikel Oyarzabal","España","Falso 9 / delantero",0.23,1.05,0.75,0.85,0.95),
 ("Cristiano Ronaldo","Portugal","Delantero central",0.26,1.12,0.70,0.80,0.90),
 ("Darwin Núñez","Uruguay","Delantero central",0.24,1.0,0.68,0.70,0.85),
]
ROUND_PLAY = ["R32","R16","QF","SF","FINAL"]
def exp_matches(team): return 3.0 + sum(reach7[r].get(team,0.0)/100.0 for r in ROUND_PLAY)
def xg_match(team):
    v=[f["la"] for f in FIX if f["a"]==team]+[f["lb"] for f in FIX if f["b"]==team]
    return statistics.mean(v) if v else 1.0
def team_goals(team): return exp_matches(team)*xg_match(team)

# dificultad de grupo: Elo medio de los rivales de grupo
def group_difficulty(team):
    for g, ts in GROUPS.items():
        if team in ts:
            opps=[ELO.get(o,1500) for o in ts if o!=team]
            return statistics.mean(opps) if opps else 1500
    return 1500
gd_all=[group_difficulty(c[1]) for c in CAND]
gd_lo,gd_hi=min(gd_all),max(gd_all)
def lvl(x,a,b): return "Baja" if x<a else ("Media" if x<b else "Alta")
def lvl_inv(x,a,b): return "Bajo" if x>b else ("Medio" if x>a else "Alto")

cands=[]
for player,team,role,share,pen,starter,avail,form in CAND:
    G=team_goals(team); eg=G*share*pen*starter*avail*form
    cands.append(dict(player=player,team=team,role=role,share=share,pen=pen,
                      starter=starter,avail=avail,form=form,eg=eg,G=G,gd=group_difficulty(team)))

# --- recalibración por temperatura sobre P(Bota) simulada (anti-sobreconfianza) ---
rng=np.random.default_rng(2026); N=300_000; R_DISP=2.8
def nb(mu,size):
    mu=np.asarray(mu,float); lam=rng.gamma(R_DISP,mu/R_DISP,size); return rng.poisson(lam).astype(float)
egs=np.array([c["eg"] for c in cands])
goals=nb(np.broadcast_to(egs,(N,len(cands))),(N,len(cands)))
field=nb(1.85,(N,12)).max(axis=1)
goals+=rng.uniform(0,.01,goals.shape); field+=rng.uniform(0,.01,field.shape)
best=goals.max(axis=1); win=(goals==best[:,None])&(best>=field)[:,None]
ties=win.sum(axis=1); m=ties>=1; raw=np.array([ (win[m,j]/ties[m]).sum() for j in range(len(cands))])/N*100
# temperatura T>1 aplana la parte alta (reduce sobreconfianza del favorito)
T=1.12
tempd=raw**(1/T); tempd=tempd/ tempd.sum()*raw.sum()   # conserva masa de candidatos
for c,p0,p1 in zip(cands,raw,tempd):
    c["prob5"]=round(float(p0),2); c["prob"]=round(float(p1),2)
    c["xg"]=round(c["eg"]*0.97,2)   # leve encogimiento de xG (sobreconfianza)

# riesgos
for c in cands:
    mins=c["starter"]*c["avail"]
    c["r_min"]=lvl_inv(mins,0.72,0.88)
    c["r_dep"]=lvl(c["share"],0.22,0.28)
    c["r_grp"]=lvl(c["gd"],gd_lo+(gd_hi-gd_lo)*0.33,gd_lo+(gd_hi-gd_lo)*0.66)
    c["r_tit"]=lvl(1-c["starter"],0.08,0.18)
    c["min_pct"]=round(mins*100)

cands.sort(key=lambda x:-x["prob"]); top=cands[:10]
for i,c in enumerate(top,1): c["rank"]=i
scorers7=[{ "rank":c["rank"],"player":c["player"],"team":c["team"],"prob":c["prob"],"xg":c["xg"],
           "starter":round(c["starter"]*100),"avail":round(c["avail"]*100),"role":c["role"],
           "r_min":c["r_min"],"r_dep":c["r_dep"],"r_grp":c["r_grp"],"r_tit":c["r_tit"],
           "note":f"Rol {c['role'].lower()}; minutos {c['r_min'].lower()}, dependencia {c['r_dep'].lower()}, "
                  f"dificultad de grupo {c['r_grp'].lower()}, incertidumbre de titularidad {c['r_tit'].lower()}."}
          for c in top]

# =====================================================================
```

### Bloque 4: Análisis de incertidumbre / calibración
```python
# BLOQUE 4 — INCERTIDUMBRE Y CALIBRACIÓN: diagnósticos
# =====================================================================
def topn(d,n=5): return sorted(d.items(),key=lambda x:-x[1])[:n]
champ5=topn(V5["title"]); champ7=topn(title7)
deltas={t: round(title7[t]-V5["title"][t],2) for t in TEAMS}
high_unc_matches=[m for m in matches7 if m["high_unc"]]
adj_matches=[m for m in matches7 if m["adj"]]

diag={
 "champ_v5_top": champ5, "champ_v7_top": champ7,
 "fav_drop": round(V5["title"][champ5[0][0]]-title7[champ5[0][0]],2),
 "tail_lift": round(sum(title7[t] for t in TEAMS if title7[t]<1)-sum(V5["title"][t] for t in TEAMS if V5["title"][t]<1),2),
 "n_high_unc": len(high_unc_matches), "n_adj": len(adj_matches),
 "scorer_fav_drop": round(max(c["prob5"] for c in cands)-max(c["prob"] for c in cands),2),
 "field_pct": round(100-sum(c["prob"] for c in cands),1),
 "biggest_deltas": sorted(deltas.items(),key=lambda x:-abs(x[1]))[:8],
}
```
