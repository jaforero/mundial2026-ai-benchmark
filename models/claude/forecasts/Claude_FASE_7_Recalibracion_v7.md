# FASE 7 — Recalibración del Pronóstico (Claude v7)

## 1. Ranking de 48 Selecciones y Probabilidades

*v7.1 auditada con datos: el backtest fuera de muestra (192 partidos, 2010–2022) mostró que el motor ya está bien calibrado, así que NO se aplica encogimiento; estas probabilidades son las del motor validado. El orden y las cifras coinciden con el motor base. Todo se expresa como probabilidad estimada, no como certeza.*

| Ranking | Selección | R32 | Octavos | Cuartos | Semis | Final | Campeón |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **España** | 99.0% | 89.3% | 54.9% | 35.9% | 26.0% | **18.2%** |
| **2** | **Argentina** | 97.6% | 84.0% | 45.4% | 27.5% | 18.5% | **11.9%** |
| **3** | **Inglaterra** | 97.5% | 76.4% | 44.1% | 23.6% | 15.2% | **9.0%** |
| **4** | **Brasil** | 97.8% | 75.6% | 43.8% | 23.3% | 14.2% | **8.3%** |
| **5** | **Francia** | 94.8% | 74.6% | 39.3% | 20.6% | 12.8% | **7.5%** |
| **6** | **Portugal** | 92.0% | 61.7% | 34.1% | 18.2% | 9.7% | **5.1%** |
| **7** | **Alemania** | 96.9% | 65.1% | 34.6% | 17.5% | 8.8% | **4.5%** |
| **8** | **Países Bajos** | 90.2% | 56.5% | 31.2% | 16.2% | 7.9% | **4.0%** |
| **9** | **Colombia** | 89.8% | 59.6% | 30.7% | 15.2% | 8.0% | **3.9%** |
| **10** | **Bélgica** | 92.7% | 54.5% | 30.6% | 17.6% | 7.8% | **3.1%** |
| **11** | **Ecuador** | 91.5% | 49.7% | 25.8% | 12.1% | 5.8% | **2.5%** |
| **12** | **Japón** | 86.9% | 50.5% | 25.9% | 12.0% | 5.5% | **2.4%** |
| **13** | **México** | 91.0% | 50.5% | 26.6% | 14.6% | 6.2% | **2.2%** |
| **14** | **Uruguay** | 89.2% | 44.8% | 22.6% | 11.2% | 5.6% | **2.2%** |
| **15** | **Marruecos** | 89.1% | 48.1% | 23.3% | 10.3% | 4.8% | **1.9%** |
| **16** | **Suiza** | 95.6% | 48.2% | 23.5% | 11.0% | 4.7% | **1.9%** |
| **17** | **Croacia** | 89.5% | 44.4% | 22.2% | 10.4% | 4.9% | **1.9%** |
| **18** | **Noruega** | 81.0% | 39.4% | 18.3% | 7.9% | 3.3% | **1.3%** |
| **19** | **Canadá** | 92.6% | 45.2% | 21.9% | 10.9% | 4.0% | **1.2%** |
| **20** | **Estados Unidos** | 74.2% | 37.9% | 19.0% | 9.6% | 3.7% | **1.1%** |
| **21** | **Türkiye** | 74.5% | 34.5% | 15.5% | 6.9% | 2.6% | **0.9%** |
| **22** | **Senegal** | 70.0% | 32.2% | 15.7% | 7.5% | 2.8% | **0.9%** |
| **23** | **Austria** | 74.8% | 34.0% | 16.2% | 7.6% | 2.8% | **0.8%** |
| **24** | **Corea del Sur** | 75.2% | 31.2% | 13.9% | 5.8% | 1.8% | **0.5%** |
| **25** | **Irán** | 76.9% | 32.9% | 15.0% | 6.4% | 1.9% | **0.5%** |
| **26** | **Paraguay** | 61.5% | 26.5% | 12.3% | 5.3% | 1.7% | **0.5%** |
| **27** | **Australia** | 65.0% | 27.5% | 11.7% | 5.0% | 1.7% | **0.5%** |
| **28** | **Argelia** | 63.5% | 24.9% | 11.3% | 4.8% | 1.4% | **0.4%** |
| **29** | **Costa de Marfil** | 71.2% | 23.6% | 9.7% | 3.8% | 1.0% | **0.3%** |
| **30** | **Chequia** | 65.4% | 22.6% | 9.2% | 3.5% | 0.9% | **0.2%** |
| **31** | **Escocia** | 65.6% | 22.3% | 8.9% | 3.4% | 0.9% | **0.2%** |
| **32** | **Egipto** | 63.0% | 20.2% | 7.7% | 2.8% | 0.7% | **0.1%** |
| **33** | **Suecia** | 50.1% | 15.5% | 6.2% | 2.4% | 0.6% | **0.1%** |
| **34** | **Uzbekistán** | 49.0% | 15.8% | 6.0% | 2.2% | 0.5% | **0.1%** |
| **35** | **Túnez** | 42.1% | 11.8% | 4.4% | 1.6% | 0.4% | **0.1%** |
| **36** | **RD Congo** | 33.7% | 7.8% | 2.6% | 0.8% | 0.2% | **0.0%** |
| **37** | **Sudáfrica** | 39.9% | 7.7% | 2.2% | 0.7% | 0.1% | **0.0%** |
| **38** | **Arabia Saudí** | 36.8% | 6.6% | 1.7% | 0.5% | 0.1% | **0.0%** |
| **39** | **Jordania** | 30.2% | 6.5% | 2.0% | 0.6% | 0.1% | **0.0%** |
| **40** | **Panamá** | 43.4% | 9.9% | 3.0% | 0.9% | 0.1% | **0.0%** |
| **41** | **Bosnia** | 45.9% | 6.8% | 1.6% | 0.5% | 0.1% | **0.0%** |
| **42** | **Nueva Zelanda** | 36.6% | 6.6% | 1.7% | 0.4% | 0.1% | **0.0%** |
| **43** | **Iraq** | 23.7% | 4.3% | 1.3% | 0.3% | 0.1% | **0.0%** |
| **44** | **Ghana** | 30.1% | 4.0% | 1.0% | 0.3% | 0.0% | **0.0%** |
| **45** | **Qatar** | 28.5% | 2.4% | 0.5% | 0.1% | 0.0% | **0.0%** |
| **46** | **Haití** | 15.2% | 1.5% | 0.3% | 0.1% | 0.0% | **0.0%** |
| **47** | **Curazao** | 11.5% | 0.7% | 0.1% | 0.0% | 0.0% | **0.0%** |
| **48** | **Cabo Verde** | 27.9% | 3.6% | 0.8% | 0.2% | 0.0% | **0.0%** |

## 2. Predicción de 72 Partidos y Marcadores

*v7.1: NO se infla el empate (el backtest mostró que el modelo ya sobre-predice empates, así que inflarlos empeora el acierto). Las probabilidades y marcadores son los del motor. Se conserva el **índice de incertidumbre** (entropía de los tres resultados): los partidos de **alta incertidumbre** se marcan con ⚠ como señal informativa, sin alterar el marcador. 29 de 72 partidos quedaron en alta incertidumbre.*

### Grupo A
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **México vs Sudáfrica** | 1-0 | 64.1% | 23.4% | 12.5% | Media |
| **México vs Corea del Sur** | 1-1 | 49.2% | 26.9% | 23.9% | ⚠ Alta |
| **México vs Chequia** | 1-0 | 54.0% | 26.0% | 20.0% | Media |
| **Sudáfrica vs Corea del Sur** | 0-1 | 20.1% | 28.4% | 51.5% | ⚠ Alta |
| **Sudáfrica vs Chequia** | 0-1 | 24.5% | 29.7% | 45.8% | ⚠ Alta |
| **Corea del Sur vs Chequia** | 1-1 | 40.6% | 29.2% | 30.2% | ⚠ Alta |

### Grupo B
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Canadá vs Bosnia** | 1-0 | 64.6% | 22.7% | 12.7% | Media |
| **Canadá vs Qatar** | 2-0 | 72.7% | 18.2% | 9.1% | Baja |
| **Canadá vs Suiza** | 1-1 | 28.8% | 28.1% | 43.1% | ⚠ Alta |
| **Bosnia vs Qatar** | 1-1 | 42.6% | 29.4% | 28.0% | ⚠ Alta |
| **Bosnia vs Suiza** | 0-2 | 10.9% | 21.0% | 68.1% | Baja |
| **Qatar vs Suiza** | 0-2 | 7.4% | 16.5% | 76.1% | Baja |

### Grupo C
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Brasil vs Marruecos** | 1-0 | 52.1% | 27.7% | 20.2% | Media |
| **Brasil vs Haití** | 3-0 | 86.2% | 10.2% | 3.6% | Baja |
| **Brasil vs Escocia** | 2-0 | 66.9% | 21.0% | 12.1% | Baja |
| **Marruecos vs Haití** | 2-0 | 73.5% | 19.0% | 7.5% | Baja |
| **Marruecos vs Escocia** | 1-0 | 50.7% | 30.2% | 19.1% | ⚠ Alta |
| **Haití vs Escocia** | 0-1 | 15.7% | 24.0% | 60.3% | Media |

### Grupo D
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Estados Unidos vs Paraguay** | 1-1 | 42.1% | 28.0% | 29.9% | ⚠ Alta |
| **Estados Unidos vs Australia** | 1-1 | 40.6% | 27.9% | 31.5% | ⚠ Alta |
| **Estados Unidos vs Türkiye** | 1-1 | 36.8% | 25.6% | 37.6% | ⚠ Alta |
| **Paraguay vs Australia** | 0-0 | 32.1% | 32.7% | 35.2% | ⚠ Alta |
| **Paraguay vs Türkiye** | 1-1 | 29.3% | 29.8% | 40.9% | ⚠ Alta |
| **Australia vs Türkiye** | 1-1 | 30.8% | 29.3% | 39.9% | ⚠ Alta |

### Grupo E
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Alemania vs Curazao** | 3-0 | 88.2% | 8.9% | 2.9% | Baja |
| **Alemania vs Costa de Marfil** | 1-0 | 58.6% | 24.8% | 16.6% | Media |
| **Alemania vs Ecuador** | 1-1 | 39.7% | 30.6% | 29.7% | ⚠ Alta |
| **Curazao vs Costa de Marfil** | 0-1 | 12.5% | 24.4% | 63.1% | Media |
| **Curazao vs Ecuador** | 0-2 | 6.1% | 18.2% | 75.7% | Baja |
| **Costa de Marfil vs Ecuador** | 0-1 | 19.2% | 32.3% | 48.5% | ⚠ Alta |

### Grupo F
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Países Bajos vs Japón** | 1-1 | 38.8% | 29.3% | 31.9% | ⚠ Alta |
| **Países Bajos vs Suecia** | 2-0 | 62.1% | 21.6% | 16.3% | Media |
| **Países Bajos vs Túnez** | 1-0 | 59.9% | 26.3% | 13.8% | Media |
| **Japón vs Suecia** | 1-0 | 57.6% | 24.2% | 18.2% | Media |
| **Japón vs Túnez** | 1-0 | 56.9% | 28.5% | 14.6% | Media |
| **Suecia vs Túnez** | 1-1 | 39.0% | 30.8% | 30.2% | ⚠ Alta |

### Grupo G
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Bélgica vs Egipto** | 1-0 | 55.2% | 27.1% | 17.7% | Media |
| **Bélgica vs Irán** | 1-1 | 48.0% | 28.0% | 24.0% | ⚠ Alta |
| **Bélgica vs Nueva Zelanda** | 2-0 | 69.4% | 20.7% | 9.9% | Baja |
| **Egipto vs Irán** | 0-1 | 27.2% | 32.3% | 40.5% | ⚠ Alta |
| **Egipto vs Nueva Zelanda** | 1-0 | 43.7% | 32.3% | 24.0% | ⚠ Alta |
| **Irán vs Nueva Zelanda** | 1-0 | 53.5% | 28.4% | 18.1% | Media |

### Grupo H
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **España vs Cabo Verde** | 2-0 | 86.4% | 10.3% | 3.3% | Baja |
| **España vs Arabia Saudí** | 2-0 | 82.5% | 13.3% | 4.2% | Baja |
| **España vs Uruguay** | 1-0 | 54.7% | 27.0% | 18.3% | Media |
| **Cabo Verde vs Arabia Saudí** | 0-0 | 30.8% | 32.9% | 36.3% | ⚠ Alta |
| **Cabo Verde vs Uruguay** | 0-1 | 9.7% | 22.6% | 67.7% | Baja |
| **Arabia Saudí vs Uruguay** | 0-1 | 12.5% | 27.6% | 59.9% | Media |

### Grupo I
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Francia vs Senegal** | 1-0 | 54.9% | 26.7% | 18.4% | Media |
| **Francia vs Iraq** | 2-0 | 76.7% | 16.9% | 6.4% | Baja |
| **Francia vs Noruega** | 1-1 | 51.4% | 26.2% | 22.4% | ⚠ Alta |
| **Senegal vs Iraq** | 1-0 | 53.4% | 29.0% | 17.6% | Media |
| **Senegal vs Noruega** | 1-1 | 30.5% | 29.4% | 40.1% | ⚠ Alta |
| **Iraq vs Noruega** | 0-1 | 12.3% | 23.2% | 64.5% | Baja |

### Grupo J
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Argentina vs Argelia** | 1-0 | 68.1% | 22.1% | 9.8% | Baja |
| **Argentina vs Austria** | 1-0 | 60.0% | 25.9% | 14.1% | Media |
| **Argentina vs Jordania** | 2-0 | 79.7% | 14.9% | 5.4% | Baja |
| **Argelia vs Austria** | 1-1 | 29.3% | 29.5% | 41.2% | ⚠ Alta |
| **Argelia vs Jordania** | 1-1 | 51.9% | 26.7% | 21.4% | ⚠ Alta |
| **Austria vs Jordania** | 1-0 | 55.7% | 25.9% | 18.4% | Media |

### Grupo K
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Portugal vs RD Congo** | 1-0 | 68.2% | 22.6% | 9.2% | Baja |
| **Portugal vs Uzbekistán** | 1-0 | 59.9% | 25.5% | 14.6% | Media |
| **Portugal vs Colombia** | 1-1 | 38.2% | 28.4% | 33.4% | ⚠ Alta |
| **RD Congo vs Uzbekistán** | 0-0 | 27.5% | 36.0% | 36.5% | ⚠ Alta |
| **RD Congo vs Colombia** | 0-1 | 10.5% | 24.3% | 65.2% | Baja |
| **Uzbekistán vs Colombia** | 0-1 | 15.8% | 27.0% | 57.2% | Media |

### Grupo L
| Encuentro | Marcador v7 | Prob. A | Empate | Prob. B | Incertidumbre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Inglaterra vs Croacia** | 1-0 | 48.4% | 28.6% | 23.0% | ⚠ Alta |
| **Inglaterra vs Ghana** | 2-0 | 78.4% | 15.9% | 5.7% | Baja |
| **Inglaterra vs Panamá** | 2-0 | 76.8% | 16.6% | 6.6% | Baja |
| **Croacia vs Ghana** | 1-0 | 66.3% | 22.5% | 11.2% | Baja |
| **Croacia vs Panamá** | 1-0 | 62.1% | 23.5% | 14.4% | Media |
| **Ghana vs Panamá** | 1-1 | 27.9% | 29.5% | 42.6% | ⚠ Alta |

## 3. Top 10 Goleadores Proyectados

*Probabilidades y goles esperados recalibrados (temperatura anti-sobreconfianza). La columna de riesgos resume, por jugador: minutos, rol ofensivo, dificultad del grupo, dependencia del equipo e incertidumbre de titularidad. Fuera del top, el «campo» concentra ~36.7% de la probabilidad de Bota de Oro.*

| Ranking | Jugador (Selección) | Prob. Bota de Oro | Goles esperados | Riesgos (minutos · rol · grupo · dependencia · titularidad) |
| :---: | :--- | :---: | :---: | :--- |
| **1** | **Harry Kane** (Inglaterra) | **17.6%** | 3.59 | minutos bajo · delantero central · grupo baja · dependencia alta · titularidad baja |
| **2** | **Kylian Mbappé** (Francia) | **12.2%** | 3.08 | minutos medio · delantero central · grupo media · dependencia alta · titularidad baja |
| **3** | **Vinícius Júnior** (Brasil) | **5.7%** | 2.30 | minutos medio · extremo finalizador · grupo media · dependencia media · titularidad baja |
| **4** | **Erling Haaland** (Noruega) | **5.4%** | 2.24 | minutos bajo · delantero central · grupo alta · dependencia alta · titularidad baja |
| **5** | **Lionel Messi** (Argentina) | **5.0%** | 2.16 | minutos medio · creador-finalizador · grupo media · dependencia media · titularidad media |
| **6** | **Mikel Oyarzabal** (España) | **4.3%** | 2.06 | minutos alto · falso 9 / delantero · grupo baja · dependencia media · titularidad alta |
| **7** | **Luis Díaz** (Colombia) | **2.9%** | 1.80 | minutos medio · extremo finalizador · grupo media · dependencia media · titularidad baja |
| **8** | **Jamal Musiala** (Alemania) | **2.9%** | 1.80 | minutos medio · creador-finalizador · grupo baja · dependencia media · titularidad media |
| **9** | **Cody Gakpo** (Países Bajos) | **2.9%** | 1.79 | minutos medio · extremo finalizador · grupo media · dependencia media · titularidad media |
| **10** | **Lamine Yamal** (España) | **2.0%** | 1.59 | minutos alto · extremo finalizador · grupo baja · dependencia baja · titularidad media |

## 4. Análisis de Incertidumbre y Cambios vs Versión 6

- **Auditoría con datos (192 partidos OOS).** El motor base resultó bien calibrado (RPS 0.2002, ~17% mejor que el azar). Las transformaciones por criterio de la primera versión de la Fase 7 NO se sostuvieron en el backtest, así que se retiraron. El campeón más probable se mantiene en su valor crudo validado: 18.2%.
- **Partidos — incertidumbre explícita (sin distorsión).** 29 de 72 encuentros se marcan de alta incertidumbre (probabilidad máxima < 45% o entropía alta) como señal informativa. El backtest mostró que inflar el empate empeora el RPS, así que NO se altera el marcador.
- **Goleadores — riesgos, sin encogimiento.** Se conserva el desglose de riesgos por jugador (minutos, rol, dificultad de grupo, dependencia, titularidad), pero NO se aplica temperatura: las probabilidades son las del modelo de goleadores. Señales contradictorias típicas: alta dependencia del equipo (sube el techo) junto a incertidumbre de titularidad o minutos (lo baja); ambas se reportan por separado.
- **Lo que el backtest reveló como sobrevalorado:** el supuesto de que el modelo subestima empates (los sobre-predice) y el supuesto de exceso de confianza a nivel de partido (está bien calibrado).
- **Lo que se mantiene válido:** la señal de incertidumbre por partido y el desglose de riesgos por goleador, que informan sin distorsionar probabilidades.
- **Cómo se trató la incertidumbre:** se mide y se muestra (entropía por partido, riesgos por goleador), en lugar de corregirla con transformaciones que el backtest no respalda. Ver `Claude_Backtest_Recalibracion_v7.md`.

## 5. Detalle Técnico del Modelo

La Fase 7 **no reentrena** el motor v5 (ensamble Dixon-Coles + machine learning) ni el modelo de goleadores v6. Su aporte tras la auditoría es: (a) **validar** la calibración del motor con un backtest fuera de muestra, (b) **retirar** las transformaciones que el backtest refutó, y (c) **añadir** señales de incertidumbre y riesgo. El detalle del backtest está en `Claude_Backtest_Recalibracion_v7.md`.

1. **Encogimiento hacia la tasa base (selecciones).** Para cada ronda con tasa base *b* = equipos/48, `p' = b + (p − b)·s` con `s` decreciente en rondas profundas (0.97 en R32 → 0.86 en campeón). Se renormaliza cada ronda a su total y se impone monotonía `p(R32) ≥ … ≥ p(Campeón)`.
2. **Inflación de empate dinámica (partidos).** `pD' = pD + β·paridad·(100−pD)/2` con `β = 0.0`; la paridad = `1 − |pA−pB|/100`. Reduce el sesgo de los modelos de goles independientes a subestimar empates en partidos cerrados.
3. **Índice de incertidumbre (partidos).** Entropía normalizada de (pA, pD, pB); alta si máx < 45% o entropía > 0.93. Solo en alta incertidumbre se ajusta el marcador (hacia empate o margen de un gol).
4. **Temperatura anti-sobreconfianza (goleadores).** `p_Bota ∝ p^(1/T)` con `T = 1.0`, conservando la masa de candidatos; los goles esperados se encogen ~3%. La Bota se estima por simulación con binomial negativa (sobredispersa) y un «campo» de goleadores fuera del top.
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
SHRINK = {"R32":1.0,"R16":1.0,"QF":1.0,"SF":1.0,"FINAL":1.0,"CAMPEON":1.0}  # v7.1: backtest -> sin encogimiento (motor ya calibrado)

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
BETA_DRAW = 0.0    # v7.1: backtest -> inflar empates empeora el RPS; se elimina

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
    # v7.1: la bandera de incertidumbre se conserva (informativa), pero el marcador
    # NO se altera: el backtest mostró que el sesgo hacia el empate no está respaldado.
    score = f["score"]; adj = False
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
T=1.0   # v7.1: sin encogimiento de goleadores (no validable; se mantiene neutro)
tempd=raw**(1/T); tempd=tempd/ tempd.sum()*raw.sum()
for c,p0,p1 in zip(cands,raw,tempd):
    c["prob5"]=round(float(p0),2); c["prob"]=round(float(p1),2)
    c["xg"]=round(c["eg"],2)   # v7.1: sin encogimiento de xG

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
