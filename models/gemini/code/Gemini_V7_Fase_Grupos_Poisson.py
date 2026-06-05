import numpy as np
from scipy.stats import poisson

def calcular_xg_v7(elo_A, elo_B, med_A, val_A, utci, kappa_A, altitud, lpn_A, es_campeon, factor_local):
    # 1. Base Estocástica
    lambda_0 = 1.35
    beta1, beta2, beta3 = 0.0025, 0.15, 0.008 
    delta_elo = elo_A - elo_B
    xg_base = lambda_0 * np.exp((beta1 * delta_elo) - (beta2 * med_A) + (beta3 * val_A))
    
    # 2. Modificador Bio-Termodinámico
    alpha = 0.0001
    penalizacion_utci = np.exp(-kappa_A * max(0, utci - 28))
    penalizacion_hipoxia = 1 - (alpha * max(0, altitud - 1500))
    xg_termo = xg_base * penalizacion_utci * penalizacion_hipoxia
    
    # 3. Modificadores V7: Redes de Presión, Decaimiento y Aura Local
    delta_campeon = 0.08 if es_campeon else 0.0
    xg_v7 = xg_termo * (1 + lpn_A) * (1 - delta_campeon) * factor_local
    
    return max(0.1, xg_v7)

def dixon_coles_prob(x, y, xg_A, xg_B, rho=-0.05):
    base_prob = poisson.pmf(x, xg_A) * poisson.pmf(y, xg_B)
    if x == 0 and y == 0:
        return base_prob * (1 - xg_A * xg_B * rho)
    elif x == 0 and y == 1:
        return base_prob * (1 + xg_A * rho)
    elif x == 1 and y == 0:
        return base_prob * (1 + xg_B * rho)
    elif x == 1 and y == 1:
        return base_prob * (1 - rho)
    else:
        return base_prob

def simular_partido(equipo_A, equipo_B, contexto):
    xg_A = calcular_xg_v7(**equipo_A, **contexto)
    xg_B = calcular_xg_v7(**equipo_B, **contexto)
    
    max_goles = 7
    prob_A = prob_B = prob_Empate = 0.0
    
    for i in range(max_goles):
        for j in range(max_goles):
            p = dixon_coles_prob(i, j, xg_A, xg_B)
            if i > j: prob_A += p
            elif i < j: prob_B += p
            else: prob_Empate += p
            
    total = prob_A + prob_B + prob_Empate
    return (prob_A/total, prob_Empate/total, prob_B/total)
