"""
ChatGPT_v6_2_Camino_Titulo_48_Selecciones.py

Reproduce la tabla "Camino al Título · ChatGPT v6.2" para 48 selecciones.

Notas de replicabilidad:
- Parte de la tabla v6 congelada previamente.
- Aplica multiplicadores v6.2 derivados del Backtesting Nivel 2 metodológico.
- Normaliza por fase para que:
    R32      = 32 equipos esperados
    Octavos = 16 equipos esperados
    Cuartos = 8 equipos esperados
    Semis   = 4 equipos esperados
    Final   = 2 equipos esperados
    Campeón = 1 equipo esperado

Ejecución:
    python ChatGPT_v6_2_Camino_Titulo_48_Selecciones.py
"""

from pathlib import Path
import pandas as pd

OUTPUT_DIR = Path("outputs_chatgpt_v6_2")
OUTPUT_DIR.mkdir(exist_ok=True)

STAGES = ["R32", "Octavos", "Cuartos", "Semis", "Final", "Campeón"]
TARGET_TOTALS = {
    "R32": 3200.0,
    "Octavos": 1600.0,
    "Cuartos": 800.0,
    "Semis": 400.0,
    "Final": 200.0,
    "Campeón": 100.0,
}

BASE_V6_ROWS = [
    ("España",99.8,79.5,53.6,40.7,26.4,16.2),
    ("Francia",99.8,86.9,60.1,39.5,24.1,12.3),
    ("Inglaterra",99.8,80.5,55.5,36.1,21.6,11.2),
    ("Argentina",99.8,65.8,47.6,31.2,18.8,10.3),
    ("Portugal",99.8,77.5,51.7,30.1,16.4,7.9),
    ("Brasil",99.8,64.3,41.8,23.7,12.5,6.4),
    ("Alemania",99.8,70.9,38.4,22.0,11.1,5.5),
    ("Países Bajos",97.7,55.7,36.3,18.5,9.0,4.4),
    ("Bélgica",99.2,68.4,40.5,18.1,8.7,3.9),
    ("Marruecos",96.4,52.4,31.2,14.7,6.7,3.0),
    ("Croacia",92.6,50.1,22.0,10.6,4.5,2.0),
    ("Colombia",93.3,48.8,22.5,10.2,4.1,1.8),
    ("Uruguay",94.6,38.5,21.0,9.6,3.9,1.7),
    ("Estados Unidos",88.1,50.6,23.6,9.1,3.6,1.5),
    ("México",96.2,56.2,23.0,8.7,3.2,1.5),
    ("Senegal",88.6,49.8,22.1,9.2,3.6,1.4),
    ("Suiza",96.2,55.7,23.4,8.3,3.1,1.3),
    ("Noruega",85.5,43.3,19.3,7.7,2.8,1.1),
    ("Japón",84.0,33.4,15.4,5.9,2.1,0.9),
    ("Ecuador",89.1,40.0,15.4,5.8,2.1,0.8),
    ("Türkiye",79.5,41.5,16.9,6.1,2.2,0.8),
    ("Canadá",88.6,43.5,15.9,4.9,1.5,0.6),
    ("Austria",80.0,22.8,9.0,3.3,1.0,0.5),
    ("Suecia",66.8,22.8,9.7,3.3,1.0,0.5),
    ("Costa de Marfil",78.9,30.4,10.0,3.3,0.9,0.4),
    ("Corea del Sur",81.0,35.4,11.3,3.3,0.9,0.4),
    ("Argelia",75.9,20.3,7.7,2.5,0.7,0.3),
    ("Egipto",76.9,27.8,8.2,2.2,0.6,0.3),
    ("Australia",58.2,24.3,7.2,2.0,0.5,0.2),
    ("Paraguay",52.6,20.3,6.1,1.8,0.5,0.2),
    ("Chequia",65.8,23.3,6.3,1.6,0.4,0.2),
    ("Escocia",55.7,16.2,4.9,1.2,0.3,0.1),
    ("Irán",70.8,24.3,6.1,1.5,0.3,0.1),
    ("Bosnia y Herzegovina",50.6,14.2,3.1,0.6,0.2,0.05),
    ("Ghana",32.4,8.1,2.0,0.4,0.1,0.05),
    ("Túnez",27.3,6.1,1.5,0.3,0.1,0.05),
    ("RD Congo",39.5,9.1,2.0,0.4,0.1,0.04),
    ("Uzbekistán",31.4,6.6,1.3,0.3,0.1,0.03),
    ("Panamá",28.3,6.6,1.4,0.3,0.1,0.03),
    ("Arabia Saudita",27.3,4.6,0.9,0.2,0.1,0.02),
    ("Sudáfrica",27.3,6.1,1.0,0.2,0.1,0.02),
    ("Qatar",30.4,6.1,1.0,0.2,0.1,0.02),
    ("Jordania",12.1,1.5,0.3,0.1,0.04,0.01),
    ("Nueva Zelanda",17.2,3.0,0.5,0.1,0.04,0.01),
    ("Irak",8.6,1.5,0.3,0.1,0.04,0.01),
    ("Cabo Verde",17.2,2.5,0.4,0.1,0.04,0.01),
    ("Curazao",8.6,1.2,0.2,0.04,0.02,0.01),
    ("Haití",11.1,1.6,0.3,0.1,0.03,0.01),
]

# Multiplicadores prudentes v6 -> v6.2 derivados del Backtesting Nivel 2 metodológico.
V62_MULTIPLIERS = {
    "España": [1.00,1.00,1.00,1.00,1.00,1.00],
    "Francia": [1.00,1.01,1.02,1.02,1.02,1.03],
    "Inglaterra": [1.00,1.00,0.99,0.98,0.97,0.97],
    "Argentina": [1.00,1.00,0.99,0.98,0.98,0.98],
    "Portugal": [1.00,0.99,0.98,0.97,0.96,0.96],
    "Brasil": [1.00,1.00,1.01,1.01,1.01,1.02],
    "Alemania": [1.00,0.99,0.99,0.99,0.98,0.98],
    "Países Bajos": [1.00,1.00,1.00,1.01,1.01,1.02],
    "Bélgica": [0.99,0.99,0.98,0.97,0.96,0.95],
    "Marruecos": [1.01,1.03,1.06,1.08,1.10,1.12],
    "Croacia": [1.00,1.01,1.03,1.03,1.04,1.04],
    "Colombia": [1.01,1.03,1.06,1.08,1.09,1.10],
    "Uruguay": [1.00,1.01,1.03,1.04,1.04,1.05],
    "Estados Unidos": [1.01,1.01,1.02,1.02,1.02,1.02],
    "México": [1.00,1.01,1.02,1.02,1.02,1.03],
    "Senegal": [1.01,1.03,1.06,1.08,1.10,1.10],
    "Suiza": [1.00,1.00,1.00,1.00,1.00,1.00],
    "Noruega": [1.01,1.03,1.06,1.08,1.08,1.08],
    "Japón": [1.01,1.03,1.07,1.09,1.10,1.10],
    "Ecuador": [1.01,1.03,1.06,1.07,1.07,1.07],
    "Türkiye": [1.00,1.01,1.02,1.02,1.02,1.02],
    "Canadá": [1.01,1.02,1.03,1.03,1.03,1.03],
    "Austria": [1.00,0.99,0.99,0.98,0.98,0.98],
    "Suecia": [0.99,0.98,0.98,0.97,0.97,0.97],
    "Costa de Marfil": [1.01,1.03,1.06,1.07,1.08,1.08],
    "Corea del Sur": [1.01,1.02,1.03,1.03,1.03,1.03],
    "Argelia": [1.01,1.03,1.06,1.08,1.08,1.08],
    "Egipto": [1.01,1.02,1.04,1.05,1.05,1.05],
    "Australia": [1.00,0.99,0.99,0.99,0.98,0.98],
    "Paraguay": [1.00,1.00,1.00,1.00,1.00,1.00],
    "Chequia": [1.00,0.99,0.98,0.98,0.97,0.97],
    "Escocia": [0.99,0.98,0.97,0.96,0.96,0.96],
    "Irán": [1.00,0.99,0.98,0.97,0.96,0.96],
    "Bosnia y Herzegovina": [0.99,0.98,0.97,0.96,0.96,0.96],
    "Ghana": [1.01,1.03,1.06,1.08,1.08,1.08],
    "Túnez": [1.01,1.02,1.04,1.05,1.05,1.05],
    "RD Congo": [1.01,1.02,1.04,1.05,1.05,1.05],
    "Uzbekistán": [0.99,0.98,0.97,0.96,0.96,0.96],
    "Panamá": [1.00,1.00,1.00,1.00,1.00,1.00],
    "Arabia Saudita": [1.00,1.00,1.00,1.00,1.00,1.00],
    "Sudáfrica": [1.01,1.02,1.03,1.03,1.03,1.03],
    "Qatar": [0.99,0.98,0.97,0.96,0.96,0.96],
    "Jordania": [0.99,0.98,0.97,0.96,0.96,0.96],
    "Nueva Zelanda": [0.99,0.98,0.97,0.96,0.96,0.96],
    "Irak": [0.99,0.98,0.97,0.96,0.96,0.96],
    "Cabo Verde": [1.00,1.00,1.00,1.00,1.00,1.00],
    "Curazao": [0.99,0.98,0.97,0.96,0.96,0.96],
    "Haití": [0.99,0.98,0.97,0.96,0.96,0.96],
}

def scale_with_cap(values, target, cap=99.8):
    """Normaliza una columna para que sume el total esperado por fase."""
    vals = pd.Series(values, dtype=float).copy()
    fixed = pd.Series(False, index=vals.index)

    for _ in range(50):
        remaining_target = target - vals[fixed].sum()
        if remaining_target <= 0:
            vals[~fixed] = 0
            break

        scale = remaining_target / vals[~fixed].sum()
        vals.loc[~fixed] *= scale

        newly_capped = (vals > cap) & (~fixed)
        if not newly_capped.any():
            break

        vals.loc[newly_capped] = cap
        fixed = fixed | newly_capped

    return vals.clip(0, cap)

def build_v62_table():
    df = pd.DataFrame(BASE_V6_ROWS, columns=["Selección"] + STAGES)

    adjusted = df.copy()
    for idx, row in adjusted.iterrows():
        multipliers = V62_MULTIPLIERS.get(row["Selección"], [1.0] * len(STAGES))
        for stage, multiplier in zip(STAGES, multipliers):
            adjusted.loc[idx, stage] = float(row[stage]) * multiplier

    # Normalización por fase
    for stage in STAGES:
        adjusted[stage] = scale_with_cap(adjusted[stage], TARGET_TOTALS[stage], cap=99.8)

    # Orden final por campeón
    adjusted = adjusted.sort_values("Campeón", ascending=False).reset_index(drop=True)
    return adjusted

def format_percent(x):
    return "<0.1%" if x < 0.05 else f"{x:.1f}%"

def write_outputs(df):
    csv_path = OUTPUT_DIR / "Camino_al_Titulo_ChatGPT_v6_2.csv"
    md_path = OUTPUT_DIR / "Camino_al_Titulo_ChatGPT_v6_2.md"

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    formatted = df.copy()
    for stage in STAGES:
        formatted[stage] = formatted[stage].apply(format_percent)

    md = "# Camino al Título · ChatGPT v6.2\n\n"
    md += formatted.to_markdown(index=False)
    md += "\n"
    md_path.write_text(md, encoding="utf-8")

    print(f"CSV generado: {csv_path}")
    print(f"Markdown generado: {md_path}")

if __name__ == "__main__":
    final_df = build_v62_table()
    write_outputs(final_df)
