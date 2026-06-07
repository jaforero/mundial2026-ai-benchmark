# Backtest de la Recalibración — Claude v7.1 (auditoría con datos)

*Validación fuera de muestra sobre **192 partidos reales** de fase de grupos de los Mundiales 2010, 2014, 2018 y 2022. Para cada torneo el modelo se ajusta SOLO con datos previos. Se prueban las transformaciones de la Fase 7 (inflación de empate y encogimiento/temperatura) midiendo si mejoran el acierto fuera de muestra y si acercan la tasa de empates a la real.*

## 1. Línea base (motor ensamble, sin transformar)

- **RPS 0.2002** · LogLoss 0.9708 · Brier 0.5731
- Tasa de empate **real 21.88%** vs **proyectada 27.70%** → el modelo **sobre-predice** empates por 5.82 pp.

## 2. ¿La inflación de empate ayuda? — NO

| β | RPS | LogLoss | Tasa empate proy. | Brecha vs real (pp) |
| :---: | :---: | :---: | :---: | :---: |
| 0.00 | 0.2002 | 0.9708 | 27.70% | 5.82 |
| 0.05 | 0.2008 | 0.9748 | 28.94% | 7.07 |
| 0.10 | 0.2014 | 0.9795 | 30.19% | 8.31 |
| 0.15 | 0.2021 | 0.9848 | 31.43% | 9.56 |
| 0.20 | 0.2030 | 0.9908 | 32.68% | 10.80 |
| 0.25 | 0.2039 | 0.9974 | 33.93% | 12.05 |
| 0.30 | 0.2049 | 1.0046 | 35.17% | 13.30 |

**Hallazgo.** El RPS empeora de forma **monótona** al inflar empates y la brecha con la tasa real **crece**. El β óptimo por datos es **0.00** (y el que mejor iguala la tasa real también es 0.00). La premisa de que un modelo de goles independientes subestima empates es **falsa** para este ensamble: ya los sobre-predice. **Decisión: se elimina la inflación de empate** (β = 0).

## 3. ¿El encogimiento (anti-sobreconfianza) ayuda? — NO

| T | RPS | LogLoss | Brier |
| :---: | :---: | :---: | :---: |
| 0.90 | 0.1995 | 0.9691 | 0.5709 |
| 0.95 | 0.1998 | 0.9697 | 0.5719 |
| 1.00 | 0.2002 | 0.9708 | 0.5731 |
| 1.05 | 0.2007 | 0.9722 | 0.5745 |
| 1.10 | 0.2012 | 0.9738 | 0.5759 |
| 1.15 | 0.2018 | 0.9756 | 0.5775 |
| 1.20 | 0.2024 | 0.9774 | 0.5790 |
| 1.25 | 0.2031 | 0.9794 | 0.5807 |

**Hallazgo.** El óptimo está en **T ≈ 0.90** (afilar, no encoger): el motor está **bien calibrado o ligeramente subconfiado** a nivel de partido. Encoger (T > 1, que era el supuesto de la Fase 7) **empeora** RPS y LogLoss. La mejora por afilar es mínima (dentro del ruido para 192 partidos), así que **no se aplica encogimiento ni afilado**: se conserva la probabilidad cruda del motor. **Decisión: se elimina el encogimiento.**

## 4. Qué cambia en el modelo (v7 → v7.1)

- **Se elimina** la inflación de empate (la evidencia la refuta).
- **Se elimina** el encogimiento de selecciones y de goleadores (sin respaldo; el motor ya está calibrado). El campeón vuelve a su valor crudo validado (España ≈ 18.2%).
- **Se elimina** el ajuste de marcador hacia el empate (era parte del sesgo refutado).
- **Se conserva** lo que aporta valor sin distorsionar probabilidades: la **bandera de incertidumbre** por partido (informativa) y el **desglose de riesgos** por goleador (minutos, rol, dificultad de grupo, dependencia, titularidad).

## 5. Limitaciones

- El backtest valida la **calibración a nivel de partido** (192 resultados). La calibración a **nivel de campeón** no es testeable de forma directa con solo 4 campeones; se infiere del motor de partido (bien calibrado) y se reporta esa limitación en lugar de inventar un ajuste.
- La mejora por afilar (T≈0.90) es de magnitud pequeña y podría ser ruido; por eso se opta por **no** distorsionar y mantener la probabilidad cruda.
- Los riesgos por goleador siguen derivados del pool documentado, no de una base oficial de convocados.

## 6. Conclusión

La auditoría con datos **valida el motor base** (RPS 0.2002, ~17% mejor que el azar) y **descarta** los ajustes por criterio de la Fase 7. La mejora real no fue añadir más transformaciones, sino **quitar las que no se sostienen** y dejar que el pronóstico sea la salida honesta del modelo validado, acompañada de señales de incertidumbre y riesgo. Calibrar contra datos, no contra criterio.

> Código: `code/backtest_recalibration_v7.py` · resultados: `data/backtest_recalibration_v7_results.json`. Reproducible: ajuste OOS por torneo, 192 partidos, barridos de β y T.