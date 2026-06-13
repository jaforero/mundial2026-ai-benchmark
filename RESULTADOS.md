# Cómo actualizar los resultados reales (panel "Precisión en vivo")

El panel compara cada pronóstico con el resultado oficial de la FIFA. **Es dinámico**:
la página lee `results.json` en cada carga (con anti-caché), así que basta editar ese
archivo y hacer commit — no hay que regenerar el sitio.

## Flujo cuando termina un partido

1. Abre `results.json` (en la raíz del repo).
2. Busca el partido (están los 72, ordenados por fecha y grupo).
3. Rellena `ga` (goles del equipo `a`) y `gb` (goles del equipo `b`) con el marcador final oficial.
   - Antes de jugarse están en `null`.
   - **Importante:** `ga` corresponde al equipo del campo `a` y `gb` al del campo `b`, en ese orden.
4. Actualiza la fecha del campo `updated` (opcional).
5. Commit + push. La página se actualiza sola para todos los visitantes.

```json
{
 "grupo": "A", "jornada": 1, "fecha": "Jun 11",
 "a": "México", "b": "Sudáfrica",
 "ga": 2, "gb": 0
}
```

## Cómo se puntúa

| Acierto | Puntos |
| :-- | :--: |
| Marcador exacto (p. ej. predijo 2-0 y fue 2-0) | **3** |
| Solo el resultado (ganar/empatar/perder), aunque falle el marcador | **1** |
| Fallo | 0 |

Además se calcula el **RPS** (Ranked Probability Score) usando las probabilidades 1X2
de cada modelo: mide la calidad probabilística del pronóstico (menor es mejor) y premia
a un modelo que repartió bien su confianza aunque su marcador exacto no acierte.

El leaderboard se ordena por puntos (desempate por RPS). La sección se actualiza cada vez
que cambian los datos, y muestra el progreso (X de 72 partidos jugados).

## Notas

- Los nombres de equipo en `results.json` **deben coincidir** con los del modelo
  (español, p. ej. "Corea del Sur", "Chequia", "Países Bajos"). El archivo ya viene con
  los 72 nombres correctos; solo hay que rellenar marcadores.
- Si `results.json` no existe o no tiene partidos jugados, el panel muestra un estado
  vacío amable y se activa solo cuando lleguen los primeros resultados.
- Fuente oficial: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026

---

## Actualización AUTOMÁTICA (sin tocar nada a mano)

El repo incluye un **GitHub Action** (`.github/workflows/update-results.yml`) que cada 30 minutos
trae los marcadores oficiales y actualiza `results.json` solo. No necesitas API key.

**Cómo funciona:**
- Fuente: `openfootball/worldcup.json` — datos de dominio público, sin clave ni límites de uso.
- El script `scripts/update_results.py` descarga el feed, traduce los nombres de equipo
  (inglés → español, con `scripts/name_map.json`) y rellena `ga`/`gb` de los partidos ya jugados.
- Solo hace commit cuando hay un partido nuevo, así que el historial queda limpio.
- La página lee `results.json` en vivo, de modo que el panel "Mundial de las IAs" se actualiza
  para todos los visitantes pocos minutos después de que termine cada partido.

**Para activarlo (una sola vez):**
1. Sube el repo a GitHub (si no está ya).
2. En el repositorio: **Settings → Actions → General → Workflow permissions → Read and write permissions** (para que el bot pueda hacer commit).
3. Listo. El Action corre cada 30 min. También puedes ejecutarlo a mano en la pestaña **Actions → "Actualizar resultados" → Run workflow**.

**Sigue pudiendo editarse a mano:** si alguna vez quieres corregir o adelantar un marcador,
edita `results.json` directamente; el script nunca sobrescribe un resultado ya cargado.

**Nota:** el respaldo embebido en `index.html` (para vista local) no se regenera con el Action;
no importa, porque en producción la página siempre lee el `results.json` actualizado.
