# ChatGPT_v7_calibracion_incertidumbre.py
import pandas as pd
import numpy as np

def logit(p, eps=1e-6):
    p = np.clip(p, eps, 1 - eps)
    return np.log(p / (1 - p))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def temperature_shrink(prob, temperature=1.08):
    """
    Reduce sobreconfianza llevando probabilidades extremas hacia el centro.
    temperature > 1 suaviza.
    """
    return sigmoid(logit(prob) / temperature)

def brier_score(p, y):
    return np.mean((np.asarray(p) - np.asarray(y)) ** 2)

def flag_low_confidence(prob_a, prob_draw, prob_b, volatility=0.0):
    favorite = max(prob_a, prob_b)
    surprise = 1 - favorite
    if favorite < 0.55 or surprise >= 0.55 or volatility >= 0.60:
        return "Baja"
    if favorite < 0.67 or volatility >= 0.45:
        return "Media"
    return "Alta"

def normalize_phase_probabilities(df, stage, expected_total):
    factor = expected_total / df[stage].sum()
    df[stage] = df[stage] * factor
    return df

# Uso:
# df["Campeón_calibrado"] = temperature_shrink(df["Campeón"] / 100, temperature=1.08) * 100
# df = normalize_phase_probabilities(df, "Campeón_calibrado", 100)
