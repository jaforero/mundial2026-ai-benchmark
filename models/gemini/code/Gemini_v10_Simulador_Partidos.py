import numpy as np
from scipy.stats import poisson

def calcular_rho_dinamico(elo_A, elo_B, utci_impact):
    """Calibración estricta al ancla empírica del 21.88% para Fase de Grupos."""
    diff = abs(elo_A - elo_B)
    base_rho = -0.015  # Reajuste para desinflar empates
    ajuste_friccion = max(0, (100 - diff) * 0.0008)
    ajuste_clima = utci_impact * 0.015
    return base_rho + ajuste_friccion + ajuste_clima

def prob_dixon_coles_fase10(x, y, xg_A, xg_B, elo_A, elo_B, utci):
    rho = calcular_rho_dinamico(elo_A, elo_B, utci)
    prob_independiente = poisson.pmf(x, xg_A) * poisson.pmf(y, xg_B)
    
    if x == 0 and y == 0: return prob_independiente * (1 - xg_A * xg_B * rho)
    elif x == 0 and y == 1: return prob_independiente * (1 + xg_A * rho)
    elif x == 1 and y == 0: return prob_independiente * (1 + xg_B * rho)
    elif x == 1 and y == 1: return prob_independiente * (1 - rho)
    return prob_independiente
