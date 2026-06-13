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
