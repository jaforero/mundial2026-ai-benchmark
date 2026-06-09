# Analítica · GA4 (propiedad G-MQ3K8EVKV0)

El sitio envía datos a Google Analytics 4 mediante `gtag.js` (en el `<head>` de `index.html`).
Al ser un subdominio de `javierforero.co`, **no hace falta cambiar el ID de medición**.

## Eventos personalizados

| Evento | Cuándo se dispara | Parámetros |
| :-- | :-- | :-- |
| `select_tab` | Al abrir una pestaña (y la activa al cargar) | `ai_tab` (consenso/claude/chatgpt/gemini), `ai_name`, `tab_type` (consensus \| individual_model) |
| `view_scorers` | Al ver el panel de goleadores (una vez por fuente y sesión) | `scorers_source` (consenso/claude/chatgpt/gemini), `ai_name` |
| `toggle_language` | Al cambiar ES/EN | `language` |
| `toggle_theme` | Al cambiar claro/oscuro | `theme` |

Además, GA4 registra automáticamente `page_view`, país/ciudad, dispositivo, fuente de tráfico y duración.

## Cómo responder las preguntas de negocio

**¿Qué IA genera más interés?**
Informes → Engagement → Eventos → `select_tab`, desglosar por `ai_name`. (O en Exploraciones: dimensión `ai_name`, métrica «Recuento de eventos».)

**¿Cuántos usuarios llegan al panel de goleadores?**
Evento `view_scorers`: «Usuarios totales» da cuántos llegaron; desglosar por `scorers_source` indica desde qué pestaña.

**¿Qué porcentaje consulta el consenso vs. los modelos individuales?**
Evento `select_tab` desglosado por `tab_type`: `consensus` vs `individual_model`. El cociente da el porcentaje.

**¿Qué países generan más tráfico?**
Informes → Datos demográficos → País (automático, sin configuración).

## Configuración recomendada en GA4 (una sola vez)

1. **Dimensiones personalizadas** (Administrar → Definiciones personalizadas → Crear): registrar `ai_tab`, `ai_name`, `tab_type`, `scorers_source` como dimensiones de ámbito *Evento* para poder desglosar por ellas en los informes.
2. (Opcional) Marcar `view_scorers` como **conversión** si se quiere medir el «llegar a goleadores» como objetivo.
3. Los datos tardan hasta 24–48 h en aparecer en los informes estándar; en **Tiempo real** se ven de inmediato para validar la instalación.
