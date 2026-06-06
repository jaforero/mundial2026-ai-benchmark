# ChatGPT_v7_simulacion_selecciones.py
import pandas as pd

STAGES = ["R32", "Octavos", "Cuartos", "Semis", "Final", "Campeón"]
TARGETS = {"R32": 3200, "Octavos": 1600, "Cuartos": 800, "Semis": 400, "Final": 200, "Campeón": 100}

def scale_with_cap(values, target, cap=99.8):
    vals = pd.Series(values, dtype=float).copy()
    fixed = pd.Series(False, index=vals.index)
    for _ in range(50):
        remaining = target - vals[fixed].sum()
        if remaining <= 0:
            vals[~fixed] = 0
            break
        factor = remaining / vals[~fixed].sum()
        vals.loc[~fixed] *= factor
        capped = (vals > cap) & (~fixed)
        if not capped.any():
            break
        vals.loc[capped] = cap
        fixed |= capped
    return vals.clip(0, cap)

def recalibrate_country_table(df_v62, multipliers):
    out = df_v62.copy()
    for idx, row in out.iterrows():
        team = row["Selección"]
        team_mult = multipliers.get(team, [1, 1, 1, 1, 1, 1])
        for stage, m in zip(STAGES, team_mult):
            out.loc[idx, stage] = float(row[stage]) * m

    for stage in STAGES:
        out[stage] = scale_with_cap(out[stage], TARGETS[stage])

    return out.sort_values("Campeón", ascending=False).reset_index(drop=True)

# Uso:
# df_v62 = pd.read_csv("Camino_al_Titulo_ChatGPT_v6_2.csv")
# df_v7 = recalibrate_country_table(df_v62, MULTIPLIERS_V7)
# df_v7.to_csv("Camino_al_Titulo_ChatGPT_Fase_7.csv", index=False)
