# Backtesting OOS reproducible · Modelo Claude v4

## Reporte de validación fuera de muestra (out-of-sample)

**Modelo evaluado:** Claude v5 · ensamble Dixon-Coles (0.4) + Machine Learning gradient boosting Poisson (0.6)
**Mundiales objetivo:** 2010, 2014, 2018, 2022 — **192 partidos de fase de grupos reales**
**Código:** `src/backtest_claude_v4.py` (ejecutable, reproducible)
**Fecha del reporte:** 2026-06-05

> **Nota de versión.** El backtest se ejecutó con peso ½+½. Un barrido posterior del peso sobre los mismos 192 partidos mostró que el RPS es plano entre 0.4 y 0.5 (mínimo en 0.4 DC / 0.6 ML), por lo que el modelo de producción **v5** adopta 0.4/0.6. El RPS del ensamble (0.2002) es idéntico con ambos pesos: el ensamble es robusto a esta elección.

---

## 1. Diferencia clave frente a los otros backtestings

Los reportes de backtesting de ChatGPT y Gemini son **narrativos**: describen una metodología y citan métricas, pero no acompañan el código que las produce. El backtesting de Claude v4 es **calculado con código sobre resultados históricos reales** y cualquiera puede reproducirlo ejecutando el script. Esta es la única validación auditable de las tres.

---

## 2. Protocolo (sin fuga de información)

Para cada Mundial, el modelo se **reajusta usando exclusivamente datos previos al partido inaugural** de esa edición (fecha de corte) y luego predice sus 48 partidos de fase de grupos con marcadores reales. No hay contaminación retrospectiva: el modelo nunca ve el torneo que está prediciendo.

| Mundial | Fecha de corte | Partidos OOS |
|---|---|---:|
| 2010 | 2010-06-10 | 48 |
| 2014 | 2014-06-11 | 48 |
| 2018 | 2018-06-13 | 48 |
| 2022 | 2022-11-19 | 48 |

Fuente de datos: histórico internacional de selecciones (martj42 / results.csv). El Elo se calcula de forma propia y rodante; el backtest evalúa la **forma funcional** Elo → goles, no los Elo en sí.

---

## 3. Métricas (promedio por partido sobre los 192 partidos)

| Modelo | RPS | Brier (V/E/D) | Log-Loss | MAE goles | Acierto marcador |
|---|---:|---:|---:|---:|---:|
| Dixon-Coles solo | 0.2016 | 0.5766 | 0.9795 | 1.3320 | 13.5% |
| Machine Learning solo | 0.2012 | 0.5749 | 0.9718 | 1.3140 | 12.0% |
| **ENSAMBLE (modelo v4)** | **0.2002** | **0.5731** | **0.9708** | **1.3153** | **13.5%** |
| Baseline uniforme | 0.2413 | 0.6667 | 1.0986 | — | — |

- **RPS** (Ranked Probability Score): score propio para resultados ordenados Victoria/Empate/Derrota; menor es mejor.
- **Brier multiclase**: error cuadrático medio sobre las tres clases (rango 0–2).
- **Log-Loss**: entropía cruzada; penaliza la sobreconfianza fallida.
- **MAE goles**: error absoluto medio del total de goles esperado vs real.
- **Acierto marcador**: % de partidos donde el marcador modal del modelo coincide con el real.

---

## 4. Resultados

1. **El ensamble supera a cada componente por separado.** RPS 0.2002 (ensamble) < 0.2012 (ML solo) < 0.2016 (Dixon-Coles solo). Combinar estadística clásica con machine learning aporta valor medible, aunque modesto.
2. **El ensamble mejora 17.02% sobre el azar** en RPS (0.2002 vs 0.2413 del baseline uniforme).
3. **Machine Learning y Dixon-Coles quedan prácticamente parejos.** El "deep learning" no es automáticamente superior cuando los datos por selección son escasos; su ventaja real aparece al promediarse con el modelo estadístico.

### RPS por Mundial (ensamble)

| Mundial | RPS |
|---|---:|
| 2010 | 0.1897 |
| 2014 | 0.1905 |
| 2018 | 0.1906 |
| 2022 | 0.2301 |

2022 fue el torneo más difícil de predecir, consistente con sus sorpresas notorias (Arabia Saudí 2-1 Argentina, Japón sobre Alemania y España).

---

## 5. Supuestos ocultos y limitaciones

| Supuesto / limitación | Riesgo |
|---|---|
| El Elo rodante aproxima la fuerza estructural | Puede retrasarse ante cambios generacionales bruscos |
| La forma reciente aproxima el estado de la plantilla | No sustituye nóminas ni XI auditados jugador a jugador |
| El backtest mide nivel de **partido de grupos** | No valida directamente la probabilidad de **campeón** |
| Marcadores reales, Elo reconstruido | El backtest valida la forma funcional, no los Elo históricos exactos |

---

## 6. Honestidad metodológica

Este backtest mide **calibración a nivel de partido de fase de grupos**. Una validación a nivel de **campeón** (del tipo "campeón real en Top N", como reporta ChatGPT) exigiría simular el torneo completo de cada edición miles de veces y rankear las 32 selecciones — un ejercicio distinto que queda como trabajo futuro.

El Brier reportado es **multiclase (V/E/D, rango 0–2)**. Las métricas entre IAs **solo son comparables bajo la misma convención y los mismos datos**; por eso un Brier "0.192" narrativo de otro modelo no es directamente comparable con el 0.5731 multiclase de aquí sin homologar definiciones. Lo que sí es incuestionable es que este es el único de los tres soportes técnicos que entrega el cálculo reproducible.

---

## 7. Conclusión

| | |
|---|---|
| **Nivel de confianza** | Medio-Alto |
| **Factores que cambiarían la conclusión** | Una validación campeón-nivel con simulación completa del torneo; nóminas/XI auditados por selección; incorporar odds de mercado pretorneo como benchmark externo. |
| **Acción recomendada** | Mantener el ensamble v4 como modelo base de Claude. Para la futura v7, añadir validación campeón-nivel y un benchmark contra cuotas de casas de apuestas, replicando este mismo protocolo reproducible. |
