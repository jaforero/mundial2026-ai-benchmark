# ChatGPT_v7_simulacion_partidos.py
import pandas as pd

def parse_prob(prob):
    a, draw, b = [int(x) for x in prob.split("-")]
    if a + draw + b != 100:
        raise ValueError(f"Probabilidades no suman 100: {prob}")
    return a, draw, b

def favorite_from_prob(row):
    a, draw, b = parse_prob(row["Prob. A-E-B"])
    return row["Equipo A"] if a >= b else row["Equipo B"]

def surprise_risk(prob):
    a, draw, b = parse_prob(prob)
    return f"{100 - max(a, b)}%"

def apply_match_recalibration(df_matches, modifications):
    df = df_matches.copy()
    if "Marcador v6.2-M" in df.columns:
        df = df.rename(columns={"Marcador v6.2-M": "Marcador v7-M"})

    for match_id, update in modifications.items():
        score, prob, note, confidence = update
        idx = df.index[df["M"] == match_id][0]
        df.loc[idx, "Marcador v7-M"] = score
        df.loc[idx, "Prob. A-E-B"] = prob
        df.loc[idx, "Favorito"] = favorite_from_prob(df.loc[idx])
        df.loc[idx, "Riesgo sorpresa"] = surprise_risk(prob)
        df.loc[idx, "Confianza"] = confidence
        df.loc[idx, "Nota técnica"] = note

    return df

# Uso:
# df = pd.read_csv("ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6_2.csv")
# df_v7 = apply_match_recalibration(df, MODIFICATIONS_V7)
# df_v7.to_csv("ChatGPT_Pronostico_72_Partidos_Fase_Grupos_Fase_7.csv", index=False)
