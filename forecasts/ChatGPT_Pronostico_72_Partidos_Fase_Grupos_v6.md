# ChatGPT Pronóstico 72 Partidos Fase de Grupos v6

## Modelo v6-M · Marcadores calibrados

**Archivo:** `ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6.md`  
**Versión:** ChatGPT v6-M  
**Tipo de modelo:** modelo de marcadores por partido, basado en fuerza v6 calibrada histórica + match-level ensemble  
**Alcance:** 72 partidos de fase de grupos del Mundial FIFA 2026  
**Formato de probabilidad:** Equipo A – Empate – Equipo B  
**Lectura del marcador:** marcador modal más probable dentro de la distribución de goles, no promedio esperado.

---

## 1. Resumen ejecutivo

Esta versión actualiza el pronóstico de marcadores de los 72 partidos usando los factores del modelo **ChatGPT v6** de probabilidades por selección, pero adaptados a un modelo específico de marcador por partido.

El cambio clave es pasar de una lógica de fuerza global:

```text
Probabilidad de avanzar por selección
```

a una lógica específica de partido:

```text
Marcador esperado = función de fuerza v6 + ataque/defensa + contexto + clima + ruta + volatilidad
```

Por tanto, esta versión no solo responde qué equipo es más fuerte, sino **cómo se espera que esa ventaja se exprese en goles**.

---

## 2. Data y factores usados

| Bloque | Uso dentro del modelo v6-M | Impacto esperado |
|---|---|---|
| Ranking FIFA oficial | Prior estructural de fuerza | Alto |
| World Football Elo | Rendimiento competitivo reciente | Alto |
| Valor y profundidad de plantilla | Talento, banca y techo competitivo | Medio-Alto |
| Convocatorias / lectura player-level | Calidad por líneas y disponibilidad | Alto |
| Fuerza v6 por selección | Prior calibrado de probabilidad de avanzar | Muy alto |
| Clima por sede | Ritmo, fatiga, presión alta y goles esperados | Alto |
| Altitud | Ajuste especial en Ciudad de México | Alto |
| Localía | México, Estados Unidos y Canadá | Alto |
| Viaje y descanso | Fatiga logística y adaptación | Medio |
| Dificultad de grupo | Incentivos, presión y posible rotación | Medio |
| Volatilidad histórica | Control de sorpresas y sobreconfianza | Alto |

---

## 3. Fórmula compacta del modelo v6-M

```text
MatchEdge_v6M =
  0.24 · ΔStrength_v6
+ 0.16 · ΔAttackVsDefense
+ 0.12 · ΔMidfieldControl
+ 0.10 · ΔGoalkeeperDefense
+ 0.09 · ΔPlayerAvailability
+ 0.08 · ΔBenchDepth
+ 0.08 · ΔClimateFit
+ 0.06 · ΔHostTravelRest
+ 0.04 · ΔGroupPressure
+ 0.03 · ΔUpsetRobustness
```

Luego se calcula el total esperado de goles:

```text
GoalTotal_v6M =
  2.62
- 0.25 · EffectiveHeat
- 0.12 · Humidity
- 0.08 · TacticalCaution
+ 0.16 · StrengthGap
+ 0.10 · AttackQualityCombined
- 0.07 · DefensiveStrengthCombined
```

Finalmente:

```text
λ_A = max(0.15, GoalTotal_v6M/2 + MatchEdge_v6M/2)
λ_B = max(0.15, GoalTotal_v6M/2 - MatchEdge_v6M/2)
```

Y para cada marcador posible:

```text
P(score = x,y) = Pois(x; λ_A) · Pois(y; λ_B)
```

El marcador reportado es:

```text
Marcador_modal = argmax P(score = x,y)
```

---

## 4. Capa climática y contextual

La capa climática es una de las diferencias principales frente a versiones anteriores.

| Tipo de sede | Efecto esperado |
|---|---|
| Miami / Monterrey | Baja ritmo, sube fatiga, sube probabilidad de empate |
| Houston / Dallas | Calor alto, parcialmente mitigado por domo/AC |
| Guadalajara | Calor + posible lluvia/tormenta; reduce intensidad sostenida |
| Nueva York / Nueva Jersey / Filadelfia / Kansas City | Calor húmedo o continental; afecta presión y resistencia |
| Atlanta | Clima mitigado por domo |
| Vancouver / Toronto / Seattle / Boston / San Francisco | Condiciones más templadas o favorables |
| Ciudad de México | Altitud relevante; favorece aclimatación y localía mexicana |

---

## 5. Regla de confianza

| Confianza | Criterio operativo |
|---|---|
| Alta | Favorito ≥ 67% y baja volatilidad contextual |
| Media-Alta | Favorito fuerte, pero con algún factor de riesgo |
| Media | Favorito razonable entre 55% y 66% |
| Baja | Favorito menor a 55%, empate muy probable o riesgo de sorpresa alto |

---

## 6. Tabla completa de pronóstico · 72 partidos

| M | Grupo | Sede | Riesgo climático | Equipo A | Marcador v6-M | Equipo B | Prob. A-E-B | Favorito | Riesgo sorpresa | Confianza | Nota técnica |
|---:|:---:|---|---|---|:---:|---|:---:|---|---:|:---:|---|
| 1 | A | Ciudad de México | Templado + altitud | México | 2-0 | Sudáfrica | 75-18-7 | México | 25% | Alta | Altitud/localía elevan la ventaja mexicana; Sudáfrica sufre más el contexto. |
| 2 | A | Guadalajara | Calor + tormentas vespertinas | Corea del Sur | 1-1 | Chequia | 39-29-32 | Corea del Sur | 61% | Baja | Partido muy parejo; calor reduce ritmo y aumenta empate. |
| 3 | B | Toronto | Templado | Canadá | 1-0 | Bosnia y Herzegovina | 62-23-15 | Canadá | 38% | Media-Alta | Localía y clima templado favorecen a Canadá. |
| 4 | D | Los Ángeles | Cálido moderado | Estados Unidos | 1-0 | Paraguay | 53-26-21 | Estados Unidos | 47% | Media | Localía compensa la resistencia competitiva de Paraguay. |
| 5 | C | Boston | Moderado | Haití | 0-1 | Escocia | 15-23-62 | Escocia | 38% | Media | Escocia superior por fuerza estructural, pero sin margen amplio. |
| 6 | D | Vancouver | Templado | Australia | 0-1 | Türkiye | 21-26-53 | Türkiye | 47% | Media | Türkiye superior; clima fresco ayuda a sostener intensidad. |
| 7 | C | Nueva York / Nueva Jersey | Calor húmedo | Brasil | 1-1 | Marruecos | 43-29-28 | Brasil | 57% | Baja | Marruecos es outsider fuerte; calor y matchup táctico suben empate. |
| 8 | B | San Francisco / Bahía | Fresco | Qatar | 0-2 | Suiza | 9-21-70 | Suiza | 30% | Alta | Clima fresco y fuerza suiza reducen margen de Qatar. |
| 9 | E | Filadelfia | Calor húmedo | Costa de Marfil | 1-1 | Ecuador | 34-28-38 | Ecuador | 62% | Baja | Calor favorece a Costa de Marfil; Ecuador conserva leve edge. |
| 10 | E | Houston | Calor húmedo + domo mitigado | Alemania | 3-0 | Curazao | 81-16-3 | Alemania | 19% | Alta | Domo mitiga estrés térmico; diferencia de plantilla domina. |
| 11 | F | Dallas | Calor extremo mitigado | Países Bajos | 1-0 | Japón | 57-25-18 | Países Bajos | 43% | Media | Japón mantiene estructura competitiva; Países Bajos tiene más techo. |
| 12 | F | Monterrey | Calor extremo | Suecia | 1-1 | Túnez | 46-30-24 | Suecia | 54% | Baja | Calor extremo reduce ventaja europea y eleva empate. |
| 13 | H | Miami | Calor + humedad extremos | Arabia Saudita | 0-1 | Uruguay | 10-23-67 | Uruguay | 33% | Alta | Humedad reduce margen, pero Uruguay mantiene superioridad. |
| 14 | H | Atlanta | Domo / calor mitigado | España | 3-0 | Cabo Verde | 82-17-1 | España | 18% | Alta | Domo permite expresar superioridad técnica de España. |
| 15 | G | Los Ángeles | Cálido moderado | Irán | 1-0 | Nueva Zelanda | 60-24-16 | Irán | 40% | Media | Irán superior por ranking y experiencia competitiva. |
| 16 | G | Seattle | Templado/fresco | Bélgica | 1-0 | Egipto | 62-24-14 | Bélgica | 38% | Media | Bélgica conserva calidad; Egipto puede hacer partido cerrado. |
| 17 | I | Nueva York / Nueva Jersey | Calor húmedo | Francia | 1-0 | Senegal | 59-25-16 | Francia | 41% | Media | Senegal gana por clima/físico; Francia compensa con profundidad. |
| 18 | I | Boston | Moderado | Irak | 0-2 | Noruega | 7-19-74 | Noruega | 26% | Alta | Noruega tiene ventaja clara por talento diferencial. |
| 19 | J | Kansas City | Calor continental | Argentina | 2-1 | Argelia | 65-23-12 | Argentina | 35% | Media-Alta | Calor reduce margen argentino, pero la jerarquía pesa. |
| 20 | J | San Francisco / Bahía | Fresco | Austria | 2-0 | Jordania | 70-20-10 | Austria | 30% | Alta | Clima fresco favorece estructura e intensidad austríaca. |
| 21 | L | Toronto | Templado | Ghana | 1-1 | Panamá | 42-29-29 | Ghana | 58% | Baja | Alta paridad; Ghana con leve ventaja física. |
| 22 | L | Dallas | Calor extremo mitigado | Inglaterra | 1-0 | Croacia | 64-23-13 | Inglaterra | 36% | Media-Alta | Profundidad inglesa supera experiencia croata en escenario mitigado. |
| 23 | K | Houston | Calor húmedo + domo mitigado | Portugal | 2-0 | RD Congo | 78-17-5 | Portugal | 22% | Alta | Portugal domina por talento y profundidad. |
| 24 | K | Ciudad de México | Templado + altitud | Uzbekistán | 0-2 | Colombia | 10-21-69 | Colombia | 31% | Alta | Altitud y adaptación regional favorecen claramente a Colombia. |
| 25 | A | Atlanta | Domo / calor mitigado | Chequia | 1-0 | Sudáfrica | 51-27-22 | Chequia | 49% | Media | Domo reduce ventaja térmica sudafricana; Chequia ligeramente superior. |
| 26 | B | Los Ángeles | Cálido moderado | Suiza | 1-0 | Bosnia y Herzegovina | 60-24-16 | Suiza | 40% | Media | Suiza superior en orden táctico y rating. |
| 27 | B | Vancouver | Templado | Canadá | 2-0 | Qatar | 70-20-10 | Canadá | 30% | Alta | Localía y clima fresco elevan la ventaja canadiense. |
| 28 | A | Guadalajara | Calor + tormentas vespertinas | México | 2-1 | Corea del Sur | 61-23-16 | México | 39% | Media | Calor y apoyo local inclinan un duelo competitivo. |
| 29 | C | Filadelfia | Calor húmedo | Brasil | 3-0 | Haití | 84-14-2 | Brasil | 16% | Alta | Brasil domina y se adapta mejor al calor que Haití. |
| 30 | C | Boston | Moderado | Escocia | 0-1 | Marruecos | 14-23-63 | Marruecos | 37% | Media-Alta | Marruecos más fuerte por plantilla, transición y solidez. |
| 31 | D | San Francisco / Bahía | Fresco | Türkiye | 1-0 | Paraguay | 56-25-19 | Türkiye | 44% | Media | Türkiye tiene ventaja de rating; Paraguay mantiene riesgo competitivo. |
| 32 | D | Seattle | Templado/fresco | Estados Unidos | 1-0 | Australia | 54-25-21 | Estados Unidos | 46% | Media | Localía y menor desgaste inclinan a EE. UU. |
| 33 | E | Toronto | Templado | Alemania | 1-0 | Costa de Marfil | 59-25-16 | Alemania | 41% | Media | Alemania superior, pero Costa de Marfil puede cerrar espacios. |
| 34 | E | Kansas City | Calor continental | Ecuador | 2-0 | Curazao | 80-16-4 | Ecuador | 20% | Alta | Ecuador se adapta bien a calor y ritmo físico. |
| 35 | F | Houston | Calor húmedo + domo mitigado | Países Bajos | 1-0 | Suecia | 58-24-18 | Países Bajos | 42% | Media | Domo mitiga calor; superioridad neerlandesa moderada. |
| 36 | F | Monterrey | Calor extremo | Túnez | 1-1 | Japón | 22-30-48 | Japón | 52% | Baja | Calor reduce presión japonesa y aumenta empate. |
| 37 | H | Miami | Calor + humedad extremos | Uruguay | 1-0 | Cabo Verde | 68-22-10 | Uruguay | 32% | Alta | Humedad baja ritmo, pero Uruguay conserva control. |
| 38 | H | Atlanta | Domo / calor mitigado | España | 3-0 | Arabia Saudita | 81-17-2 | España | 19% | Alta | España domina en condiciones mitigadas. |
| 39 | G | Los Ángeles | Cálido moderado | Bélgica | 1-0 | Irán | 62-24-14 | Bélgica | 38% | Media | Irán es incómodo; Bélgica mantiene mayor calidad. |
| 40 | G | Vancouver | Templado | Nueva Zelanda | 0-1 | Egipto | 18-24-58 | Egipto | 42% | Media | Clima fresco modera a Egipto, pero sigue superior. |
| 41 | I | Nueva York / Nueva Jersey | Calor húmedo | Noruega | 0-1 | Senegal | 29-28-43 | Senegal | 57% | Baja | Calor y físico senegalés neutralizan parte del talento noruego. |
| 42 | I | Filadelfia | Calor húmedo | Francia | 2-0 | Irak | 78-18-4 | Francia | 22% | Alta | Diferencia de calidad amplia; calor solo reduce margen. |
| 43 | J | Dallas | Calor extremo mitigado | Argentina | 2-0 | Austria | 67-22-11 | Argentina | 33% | Alta | Mitigación climática favorece control argentino. |
| 44 | J | San Francisco / Bahía | Fresco | Jordania | 0-1 | Argelia | 14-23-63 | Argelia | 37% | Media-Alta | Argelia superior; clima fresco reduce ventaja térmica adicional. |
| 45 | L | Boston | Moderado | Inglaterra | 2-0 | Ghana | 77-18-5 | Inglaterra | 23% | Alta | Condiciones moderadas favorecen control inglés. |
| 46 | L | Toronto | Templado | Panamá | 0-1 | Croacia | 14-24-62 | Croacia | 38% | Media-Alta | Croacia controla, pero no se proyecta goleada. |
| 47 | K | Houston | Calor húmedo + domo mitigado | Portugal | 2-0 | Uzbekistán | 79-17-4 | Portugal | 21% | Alta | Portugal superior en todas las líneas. |
| 48 | K | Guadalajara | Calor + tormentas vespertinas | Colombia | 2-0 | RD Congo | 67-21-12 | Colombia | 33% | Alta | Colombia mejora por adaptación, calidad y contexto. |
| 49 | C | Miami | Calor + humedad extremos | Escocia | 0-3 | Brasil | 7-18-75 | Brasil | 25% | Alta | Humedad castiga más a Escocia; Brasil tiene ventaja técnica y climática. |
| 50 | C | Atlanta | Domo / calor mitigado | Marruecos | 2-0 | Haití | 80-17-3 | Marruecos | 20% | Alta | Marruecos domina con estructura y profundidad. |
| 51 | B | Vancouver | Templado | Suiza | 1-1 | Canadá | 34-29-37 | Canadá | 63% | Baja | Localía y clima favorecen levemente a Canadá; empate modal. |
| 52 | B | Seattle | Templado/fresco | Bosnia y Herzegovina | 1-1 | Qatar | 47-27-26 | Bosnia y Herzegovina | 53% | Baja | Clima fresco reduce ventaja adaptativa de Qatar. |
| 53 | A | Ciudad de México | Templado + altitud | Chequia | 0-2 | México | 13-22-65 | México | 35% | Media-Alta | Altitud y localía elevan la ventaja mexicana. |
| 54 | A | Monterrey | Calor extremo | Sudáfrica | 1-1 | Corea del Sur | 25-29-46 | Corea del Sur | 54% | Baja | Calor extremo ayuda a Sudáfrica y reduce ventaja coreana. |
| 55 | E | Filadelfia | Calor húmedo | Curazao | 0-2 | Costa de Marfil | 7-19-74 | Costa de Marfil | 26% | Alta | Costa de Marfil se adapta bien al calor y domina físicamente. |
| 56 | E | Nueva York / Nueva Jersey | Calor húmedo | Ecuador | 1-1 | Alemania | 28-29-43 | Alemania | 57% | Baja | Calor/humedad reducen margen alemán y favorecen empate. |
| 57 | F | Dallas | Calor extremo mitigado | Japón | 1-1 | Suecia | 39-29-32 | Japón | 61% | Baja | Japón ligeramente superior, pero empate muy plausible. |
| 58 | F | Kansas City | Calor continental | Túnez | 0-1 | Países Bajos | 10-23-67 | Países Bajos | 33% | Media-Alta | Calor reduce margen neerlandés, no la superioridad. |
| 59 | D | Los Ángeles | Cálido moderado | Türkiye | 1-1 | Estados Unidos | 41-28-31 | Türkiye | 59% | Baja | Partido cerrado: EE. UU. compensa con localía. |
| 60 | D | San Francisco / Bahía | Fresco | Paraguay | 1-1 | Australia | 35-29-36 | Australia | 64% | Baja | Fuerzas cercanas y clima neutro favorecen empate modal. |
| 61 | I | Boston | Moderado | Noruega | 0-1 | Francia | 13-22-65 | Francia | 35% | Media-Alta | Francia superior; Noruega mantiene amenaza individual. |
| 62 | I | Toronto | Templado | Senegal | 2-0 | Irak | 78-17-5 | Senegal | 22% | Alta | Senegal domina por físico, estructura y ranking. |
| 63 | G | Seattle | Templado/fresco | Egipto | 1-1 | Irán | 38-29-33 | Egipto | 62% | Baja | Partido táctico cerrado, alta probabilidad de empate. |
| 64 | G | Vancouver | Templado | Nueva Zelanda | 0-2 | Bélgica | 4-17-79 | Bélgica | 21% | Alta | Bélgica domina en calidad y profundidad. |
| 65 | H | Houston | Calor húmedo + domo mitigado | Cabo Verde | 1-1 | Arabia Saudita | 35-29-36 | Arabia Saudita | 64% | Baja | Partido parejo; mitigación térmica modera diferencias. |
| 66 | H | Guadalajara | Calor + tormentas vespertinas | Uruguay | 0-1 | España | 17-25-58 | España | 42% | Media | Calor y perfil uruguayo reducen margen español. |
| 67 | L | Nueva York / Nueva Jersey | Calor húmedo | Panamá | 0-2 | Inglaterra | 5-18-77 | Inglaterra | 23% | Alta | Panamá se adapta al calor, pero la brecha es amplia. |
| 68 | L | Filadelfia | Calor húmedo | Croacia | 1-1 | Ghana | 51-28-21 | Croacia | 49% | Baja | Calor y físico ghanés reducen ventaja croata. |
| 69 | J | Kansas City | Calor continental | Argelia | 1-0 | Austria | 42-29-29 | Argelia | 58% | Baja | Calor y adaptación inclinan un partido parejo. |
| 70 | J | Dallas | Calor extremo mitigado | Jordania | 0-3 | Argentina | 2-16-82 | Argentina | 18% | Alta | Diferencia de talento muy amplia, con clima mitigado. |
| 71 | K | Miami | Calor + humedad extremos | Colombia | 1-1 | Portugal | 26-29-45 | Portugal | 55% | Baja | Humedad y resiliencia colombiana hacen el empate muy plausible. |
| 72 | K | Atlanta | Domo / calor mitigado | RD Congo | 1-1 | Uzbekistán | 39-28-33 | RD Congo | 61% | Baja | Partido equilibrado; leve ventaja física de RD Congo. |

---

## 7. Partidos de mayor incertidumbre

Los partidos con mayor riesgo de sorpresa o empate son:

| Partido | Motivo principal |
|---|---|
| Corea del Sur vs Chequia | Fuerzas muy parejas y calor en Guadalajara |
| Brasil vs Marruecos | Marruecos tiene perfil táctico de outsider fuerte |
| Suecia vs Túnez | Calor extremo de Monterrey reduce ventaja europea |
| Ghana vs Panamá | Diferencia estrecha y estilos físicos |
| Suiza vs Canadá | Localía canadiense equilibra fuerza suiza |
| Sudáfrica vs Corea del Sur | Calor extremo sube probabilidad de empate |
| Ecuador vs Alemania | Calor/humedad favorecen resistencia ecuatoriana |
| Japón vs Suecia | Estilos tácticos equilibrados |
| Türkiye vs Estados Unidos | Localía estadounidense vs fuerza turca |
| Paraguay vs Australia | Partido de fuerzas cercanas |
| Egipto vs Irán | Partido táctico, cerrado y de bajo margen |
| Cabo Verde vs Arabia Saudita | Paridad competitiva |
| Croacia vs Ghana | Calor y físico ghanés reducen ventaja croata |
| Argelia vs Austria | Calor de Kansas City cambia el edge |
| Colombia vs Portugal | Humedad extrema en Miami sube volatilidad |

---

## 8. Cambios principales frente a v5

| Partido | Cambio / justificación v6-M |
|---|---|
| México vs Sudáfrica | Sube México por altitud y fuerza v6 calibrada |
| Brasil vs Marruecos | Se mantiene empate por perfil táctico marroquí y clima |
| Francia vs Senegal | Se reduce margen francés por físico/clima |
| Noruega vs Senegal | Senegal se mantiene ligeramente arriba por clima y robustez |
| Ecuador vs Alemania | Empate muy plausible por humedad y adaptación ecuatoriana |
| Colombia vs Portugal | Empate mantiene alta plausibilidad por clima y matchup |
| Croacia vs Ghana | Se reduce ventaja croata por edad, calor y físico rival |
| Argelia vs Austria | Argelia gana leve edge por clima/calor |
| Uruguay vs España | España sigue favorita, pero margen bajo |
| Canadá vs Suiza | Canadá queda levemente arriba por localía y clima |

---

## 9. Supuestos ocultos

| Supuesto | Riesgo |
|---|---|
| Strength_v6 representa fuerza real | Puede cambiar con XI titulares y lesiones |
| Player-level agregado aproxima convocatorias | Falta auditoría completa jugador por jugador |
| Clima promedio representa condiciones del partido | Depende de horario y WBGT real |
| Domo/AC se usa plenamente | Puede variar según operación del estadio |
| Poisson captura la distribución de goles | Simplifica dependencia táctica |
| Tercera fecha mantiene incentivos esperados | Rotaciones pueden alterar fuerza real |
| El marcador modal es la mejor predicción puntual | No necesariamente es el resultado más intuitivo |

---

## 10. Mejor contraargumento

El mejor contraargumento es que el modelo v6-M aún no incorpora:

- Odds de mercado.
- XI titulares reales.
- xG/xGA recientes por selección.
- Datos médicos confirmados.
- Árbitros asignados.
- WBGT real por hora.
- Confirmación de techo abierto/cerrado.
- Matriz oficial completa de terceros clasificados.

Por eso, aunque esta versión es más robusta que v5, todavía no debe presentarse como un modelo final equivalente a una casa de apuestas.

---

## 11. Qué información podría cambiar estos marcadores

| Información nueva | Impacto esperado |
|---|---|
| XI titulares reales | Cambia ataque/defensa por líneas |
| Lesiones finales | Puede mover 1–4 pp en probabilidades |
| Odds de mercado | Mejora calibración |
| xG/xGA reciente | Ajusta ataque y defensa real |
| WBGT por horario | Ajusta clima y goles esperados |
| Árbitros | Cambia riesgo de tarjetas/penales |
| Estado del grupo en tercera fecha | Cambia rotación y motivación |
| Techo abierto/cerrado | Afecta Dallas, Houston y Atlanta |

---

## 12. Nivel de confianza

**Nivel de confianza:** Medio-Alto

La versión v6-M es metodológicamente superior a v5 porque usa la fuerza v6 calibrada históricamente y la traduce a marcadores mediante variables específicas de partido. La principal limitación es la falta de odds, XI titulares reales y datos climáticos horarios.

---

## 13. Acción recomendada

Usar este archivo como la versión principal:

```text
ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6.md
```

Para una futura v7, recalibrar con:

1. Actualización FIFA final.
2. Odds de mercado.
3. XI titulares probables.
4. Lesiones confirmadas.
5. xG/xGA recientes.
6. WBGT real por horario.
7. Confirmación de domos/techos.
8. Árbitros.
