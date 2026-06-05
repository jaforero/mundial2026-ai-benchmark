# Toolkit Analítico Gemini V7.0 - Copa Mundial 2026

## Descripción General
Este repositorio contiene el código fuente para replicar la arquitectura predictiva V7.0 (Local Pressure Networks & Contrafactual AI). El modelo abandona el sesgo histórico estático y evalúa las probabilidades a través de métricas biomecánicas contemporáneas y termodinámica de estadios.

## Archivos Incluidos
1. `Gemini_V7_Fase_Grupos_Poisson.py`: Motor matemático que calcula el xG dinámico y procesa la distribución de Poisson bivariada ajustada (Dixon-Coles).
2. `Gemini_V7_CaminoMundial_MonteCarlo.py`: Simulador que ejecuta 10,000 iteraciones del árbol de eliminación directa para generar la matriz del "Camino al Título".
3. `Gemini_V7_Backtesting_Engine.py`: Herramienta de auditoría para medir el Brier Score y la Entropía Cruzada contra datos de Mundiales anteriores.

## Apéndice Técnico Matemático

### 1. Ecuación de Tasa de Goles Esperados Base (xG_base)
$$xG_{base\_A} = \lambda_0 \cdot \exp\left( \beta_1 (\Delta Elo_{A-B}) - \beta_2 (\text{Med}_A) + \beta_3 (\text{Valor}_{plantilla}) \right)$$

### 2. Modificador Bio-Termodinámico (xG_termo)
$$xG_{termo\_A} = xG_{base\_A} \cdot e^{-\kappa_A (\text{UTCI} - 28)} \cdot \left[ 1 - \alpha \cdot \max(0, h - 1500) \right]$$

### 3. Integración V7.0: Redes de Presión Local (LPN)
$$xG_{V7\_A} = xG_{termo\_A} \cdot \left( 1 + \rho_{LPN\_A} \right) \cdot \left( 1 - \delta_{campeon\_A} \right) \cdot \omega_{local\_A}$$
* **$\rho_{LPN\_A}$**: Minutos jugados bajo PPDA élite en competiciones de clubes top.
* **$\delta_{campeon\_A}$**: Descuento paramétrico (8%) por síndrome de "Depresión del Ganador".
* **$\omega_{local\_A}$**: Multiplicador de Aura Local asimétrica.

## Instrucciones de Uso
Requiere las bibliotecas `numpy`, `pandas`, `scipy` y `scikit-learn`. Integre las variables de los equipos en un DataFrame estándar de Pandas antes de instanciar las clases del simulador.
