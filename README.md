# 🏆 Benchmark IA · Mundial 2026

**Tres inteligencias artificiales pronostican la Copa Mundial de la FIFA 2026. Un cuarto pronóstico las combina. Esta página las enfrenta.**

Un experimento de ciencia de datos que compara, partido a partido y selección a selección, los pronósticos de **Claude**, **ChatGPT** y **Gemini** para el Mundial 2026 (48 selecciones, 72 partidos de fase de grupos y el cuadro completo hasta la final), más un **consenso** construido sobre los tres.

🔗 **Página en vivo:** [`https://mundial.javierforero.co`](https://mundial.javierforero.co)

---

## ¿Qué incluye?

La página (`index.html`) es **autocontenida**: todo el HTML, CSS, JavaScript y los datos van embebidos en un único archivo. No depende de servidores, frameworks ni librerías externas (solo carga la tipografía de marca desde `javierforero.com`). Funciona abriéndola directamente en el navegador.

Incluye, en la parte superior, **conmutador de idioma español / inglés** (traducción completa de toda la interfaz, incluidos los nombres de las 48 selecciones y las metodologías desplegables) y **tema claro / oscuro**. Ambas preferencias se recuerdan entre visitas y el tema respeta la configuración del sistema en la primera carga.

Contiene cuatro vistas:

- **Consenso** — la combinación de los tres modelos: veredicto y podio del favorito, hallazgos clave, gráfico de divergencia entre IAs, comparador partido a partido, los 72 partidos con su **índice de confianza** y el camino al título de las 48 selecciones.
- **Claude / ChatGPT / Gemini** — el detalle de cada modelo por separado: metodología, probabilidad de campeón de las 48 selecciones y camino al título ronda por ronda.

---

## Metodología en breve

Cada IA aborda el problema con una **filosofía distinta**, y eso es parte de lo interesante:

- **Claude** — Ensamble que promedia un motor estadístico **Dixon-Coles** (fuerzas de ataque/defensa estimadas por máxima verosimilitud sobre miles de partidos internacionales reales) con un modelo de **machine learning** (gradient boosting con pérdida de Poisson sobre Elo, forma reciente e histórico de Mundiales). Es el único modelo **validado fuera de muestra** contra los Mundiales 2018 y 2022.
- **ChatGPT** — Calibración histórica con ajuste por fase del torneo.
- **Gemini** — Enfoque "Heritage AI" que pondera el pedigrí histórico de cada selección.

El **consenso** toma la **mediana** de las tres IAs para la probabilidad de título (robusta frente a un modelo atípico), promedia las probabilidades de cada partido y resuelve el marcador por mayoría. Cada partido lleva además un **índice de confianza (0–100)** que combina la fuerza del favorito con el grado de acuerdo entre las tres IAs (pool logarítmico + divergencia de Jensen-Shannon).

> **Nota honesta sobre los límites:** es un pronóstico previo al torneo, no una predicción infalible. Y el consenso no puede validarse empíricamente entre las tres IAs porque solo Claude existía en 2018/2022; se aplica el método de combinación teóricamente superior, documentado en el código.

---

## Estructura del repositorio

```
mundial2026-ia-benchmark/
├── index.html              ← la página (autocontenida; es lo único necesario para que funcione)
├── CNAME                   ← dominio personalizado: mundial.javierforero.co
├── robots.txt              ← SEO + permisos para crawlers de IA (GEO/AIG)
├── sitemap.xml             ← mapa del sitio para buscadores
├── 404.html                ← página de error de marca (redirige al inicio)
├── favicon.svg             ← ícono de marca
├── og-image.png            ← imagen de previsualización al compartir (1200×630)
├── README.md
├── requirements.txt
├── .gitignore
├── data/                   ← datos que alimentan la página
│   ├── consolidated.json       consolidado de las 3 IAs + consenso (lo que consume index.html)
│   ├── results_v4.json         salida del modelo final de Claude (ensamble)
│   ├── results_v3.json         salida del modelo Dixon-Coles ajustado
│   ├── results_v2.json         salida del motor Dixon-Coles base
│   ├── results.json            grupos, Elo y andamiaje base del torneo
│   └── strengths_v3.json       fuerzas de ataque/defensa estimadas (48 selecciones)
├── src/                    ← código de los modelos de Claude y del consolidado
│   ├── wc2026_model.py         base: grupos, Elo, equipos, rondas
│   ├── wc2026_model_v2.py      motor de goles Dixon-Coles + simulador del torneo
│   ├── wc2026_fit_v3.py        ajuste por máxima verosimilitud (+ validación OOS)
│   ├── wc2026_model_v3.py      simulación con fuerzas ajustadas
│   ├── wc2026_ml_v4.py         modelo de machine learning (gradient boosting Poisson)
│   ├── ensemble_v4.py          validación del ensamble Dixon-Coles + ML
│   ├── wc2026_model_v4.py      modelo final de Claude (ensamble) → results_v4.json
│   ├── consolidate2.py         combina las 3 IAs → consolidated.json (índice de confianza)
│   └── build_compare.py        genera index.html a partir de consolidated.json
└── forecasts/              ← pronósticos fuente de las otras dos IAs (insumos del consenso)
    ├── ChatGPT_Camino_al_Titulo_v6_Completo.md
    ├── ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6.md
    ├── Gemini_Predictivo_V6_Heritage_AI_y_Apend.md
    └── Gemini_Pronostico_72_Partidos_Fase_Grupo_v6.md
```

---

## Reproducir los modelos (opcional)

El código de `src/` se incluye con fines de **transparencia y portafolio**. Los scripts usan rutas absolutas del entorno donde se construyeron, así que para ejecutarlos en local hay que ajustar las rutas de lectura/escritura. El flujo es:

```bash
pip install -r requirements.txt

# 1. Descargar el dataset de partidos internacionales (no se incluye; ver atribución)
curl -L -o intl_results.csv https://raw.githubusercontent.com/martj42/international_results/master/results.csv

# 2. Estimar fuerzas y validar fuera de muestra
python src/wc2026_fit_v3.py

# 3. Simular el torneo con el modelo final de Claude
python src/wc2026_model_v4.py

# 4. Consolidar las 3 IAs y generar la página
python src/consolidate2.py
python src/build_compare.py
```

---

## Atribución

- **Datos de partidos internacionales:** [martj42/international_results](https://github.com/martj42/international_results) (resultados de selecciones desde 1872).
- **Pronósticos:** generados con Claude (Anthropic), ChatGPT (OpenAI) y Gemini (Google). Los archivos en `forecasts/` son las salidas de ChatGPT y Gemini usadas como insumo del consenso.
- **Análisis, modelado, consolidación y diseño:** Javier Forero.

---

## Autor

**Javier Forero** — Estadístico y consultor en Analítica Avanzada, IA y Transformación Digital.

- 🌐 [www.javierforero.com](https://www.javierforero.com)
- 💼 [linkedin.com/in/jforero](https://www.linkedin.com/in/jforero/)
- 🔗 [bit.ly/m/jforero](https://bit.ly/m/jforero)

---

*Proyecto con fines divulgativos y de análisis. Las predicciones son estimaciones estadísticas previas al torneo, no garantías de resultado.*
