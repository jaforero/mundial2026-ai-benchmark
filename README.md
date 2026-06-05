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

- **Claude v5** — Ensamble que promedia un motor estadístico **Dixon-Coles** (fuerzas de ataque/defensa estimadas por máxima verosimilitud sobre miles de partidos internacionales reales) con un modelo de **machine learning** (gradient boosting con pérdida de Poisson sobre Elo, forma reciente e histórico de Mundiales). Peso del ensamble afinado por backtesting (0.4 DC / 0.6 ML). Único modelo **validado fuera de muestra con código reproducible** sobre 4 Mundiales (2010–2022, 192 partidos).
- **ChatGPT v6.2** — Ensamble calibrado históricamente con los ajustes del Backtesting Nivel 2: núcleo FIFA/Elo reforzado (24%) y penalización de sesgo de mercado anti-Europa.
- **Gemini v7** — Local Pressure Networks: abandona el "pedigrí del escudo" del v6 y mide resiliencia por minutos de élite de la plantilla actual, con factor de decaimiento del campeón vigente (−8% a Argentina) y aura de localía asimétrica.

El **consenso** toma la **mediana** de las tres IAs para la probabilidad de título (robusta frente a un modelo atípico), promedia las probabilidades de cada partido y resuelve el marcador por mayoría. Cada partido lleva además un **índice de confianza (0–100)** que combina la fuerza del favorito con el grado de acuerdo entre las tres IAs (pool logarítmico + divergencia de Jensen-Shannon).

> **Nota honesta sobre los límites:** es un pronóstico previo al torneo, no una predicción infalible. Y el consenso no puede validarse empíricamente entre las tres IAs porque solo Claude existía en 2018/2022; se aplica el método de combinación teóricamente superior, documentado en el código.

---

## Estructura del repositorio

Organización **por IA**: cada modelo vive en su propia carpeta, con código (cuando está disponible), datos y reportes. Esto facilita comparar metodologías y reproducir cada uno por separado.

```
mundial2026-ia-benchmark/
├── index.html                  ← la página (autocontenida; es lo único necesario para que funcione)
├── CNAME, robots.txt, sitemap.xml, 404.html, favicon.svg, og-image.png  ← assets del sitio
├── IgraSans.woff2, IgraSans.otf  ← tipografía de marca
├── README.md, requirements.txt, .gitignore
│
├── data/
│   └── consolidated.json       ← datos unificados de las 3 IAs + consenso (alimenta index.html)
│
├── site/                       ← pipeline que construye la página
│   ├── consolidate2.py             combina las 3 IAs → consolidated.json (índice de confianza)
│   └── build_compare.py            genera index.html a partir de consolidated.json
│
└── models/                     ← un subdirectorio por IA, con la misma estructura interna
    ├── claude/                     v5 · ensamble Dixon-Coles + Machine Learning
    │   ├── README.md
    │   ├── code/                       código Python completo y reproducible
    │   ├── data/                       salidas del modelo (results_v5.json, backtest_*.json)
    │   └── forecasts/                  reporte de backtesting
    │
    ├── chatgpt/                    v6.2 · ensamble calibrado histórico + Nivel 2
    │   ├── README.md
    │   ├── code/                       scripts Python reproducibles + README propio
    │   └── forecasts/                  camino al título, 72 partidos, backtesting Nivel 2
    │
    └── gemini/                     v7 · Local Pressure Networks
        ├── README.md
        ├── code/                       motor xG + simulador del cuadro + backtesting engine
        └── forecasts/                  camino al título, 72 partidos + apéndice técnico, backtesting v6
```

**Reproducibilidad por IA.** Las tres IAs entregan código fuente reproducible junto a sus reportes: Claude (ensamble v5 + backtest OOS), ChatGPT (scripts del camino al título, los 72 partidos y los backtestings Nivel 1/2) y Gemini (motor xG, simulador del cuadro y backtesting engine v7). Cada IA tiene su README explicando qué hay y cómo correrlo.

---

## Publicar en `mundial.javierforero.co`

El sitio usa un **subdominio propio**. El archivo `CNAME` ya contiene `mundial.javierforero.co`. Como tu repositorio de usuario `jaforero.github.io` ya está ocupado por otro dominio, este proyecto va en **un repositorio aparte**.

**1. Sube el repositorio** a `https://github.com/jaforero/mundial2026-ia-benchmark` (o el nombre que prefieras).

**2. Configura el DNS** en tu proveedor del dominio `javierforero.co` — añade un registro:

| Tipo  | Nombre / Host | Valor / Apunta a        |
|-------|---------------|-------------------------|
| CNAME | `mundial`     | `jaforero.github.io`    |

**3. Activa GitHub Pages:** en el repo → **Settings → Pages** → *Source* = `main` / carpeta `/ (root)`. En **Custom domain** escribe `mundial.javierforero.co` (GitHub lo detecta del archivo `CNAME`) y guarda.

**4. Espera la verificación del DNS** (de minutos a un par de horas) y marca **Enforce HTTPS**. GitHub emite el certificado TLS automáticamente.

Listo: el sitio quedará en `https://mundial.javierforero.co/`.

---

## Reproducir los modelos (opcional)

Cada IA tiene su propio README con instrucciones específicas:

- **Claude** — ver `models/claude/README.md`. Código completo del ensamble v5 (Dixon-Coles + Machine Learning) y del backtesting OOS sobre 4 Mundiales.
- **ChatGPT** — ver `models/chatgpt/README.md`. Scripts reproducibles de la tabla camino al título v6.2, los 72 partidos y los backtestings Nivel 1 y Nivel 2.
- **Gemini** — ver `models/gemini/README.md`. Motor matemático xG (Poisson bivariada + Dixon-Coles), simulador Monte Carlo del cuadro y backtesting engine v7.

Para regenerar la página del consenso a partir de los pronósticos de las tres IAs:

```bash
pip install -r requirements.txt

# 1. Consolidar las 3 IAs (consume las fuentes y genera consolidated.json)
python site/consolidate2.py

# 2. Generar la página final
python site/build_compare.py
```

---

## Atribución

- **Datos de partidos internacionales:** [martj42/international_results](https://github.com/martj42/international_results) (resultados de selecciones desde 1872).
- **Pronósticos:** generados con Claude (Anthropic), ChatGPT (OpenAI) y Gemini (Google). Cada IA tiene su carpeta dedicada en `models/`, con su código (cuando lo aporta) y sus reportes.
- **Análisis, modelado, consolidación y diseño:** Javier Forero.

---

## Autor

**Javier Forero** — Estadístico y consultor en Analítica Avanzada, IA y Transformación Digital.

- 🌐 [www.javierforero.com](https://www.javierforero.com)
- 💼 [linkedin.com/in/jforero](https://www.linkedin.com/in/jforero/)
- 🔗 [bit.ly/m/jforero](https://bit.ly/m/jforero)

---

*Proyecto con fines divulgativos y de análisis. Las predicciones son estimaciones estadísticas previas al torneo, no garantías de resultado.*
