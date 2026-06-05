# Código reproducible · Modelos ChatGPT Mundial 2026

Este paquete contiene scripts Python separados por entregable.

## Archivos

1. `ChatGPT_v6_2_Camino_Titulo_48_Selecciones.py`
   - Reproduce la tabla **Camino al Título · ChatGPT v6.2**.
   - Genera CSV y Markdown.

2. `ChatGPT_v6_2_Pronostico_72_Partidos_Fase_Grupos.py`
   - Reproduce el pronóstico de los 72 partidos de fase de grupos.
   - Incluye marcador, probabilidades A-E-B, favorito, riesgo y confianza.

3. `ChatGPT_v6_Backtesting_Nivel_1.py`
   - Reproduce el reporte reducido de Backtesting Nivel 1.
   - Incluye métricas Top-k y Brier reportadas.

4. `ChatGPT_v6_Backtesting_Nivel_2_Metodologico.py`
   - Reproduce el reporte metodológico Nivel 2 y la fórmula/pesos v6.2.
   - No inventa Brier/LogLoss Nivel 2 sin snapshots históricos auditados.

## Instalación mínima

```bash
pip install pandas tabulate
```

## Ejecución

```bash
python ChatGPT_v6_2_Camino_Titulo_48_Selecciones.py
python ChatGPT_v6_2_Pronostico_72_Partidos_Fase_Grupos.py
python ChatGPT_v6_Backtesting_Nivel_1.py
python ChatGPT_v6_Backtesting_Nivel_2_Metodologico.py
```

## Nota metodológica

Los scripts reproducen los resultados consolidados de la conversación y dejan explícitas las tablas y reglas de ajuste usadas.
Para un backtesting empírico completo de Nivel 2 se deben conectar fuentes históricas auditadas:
FIFA ranking histórico, World Football Elo por fecha, resultados OpenFootball, plantillas históricas,
valores Transfermarkt pretorneo, xG/xGA y odds.
