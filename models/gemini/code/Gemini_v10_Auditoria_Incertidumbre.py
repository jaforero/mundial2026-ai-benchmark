import numpy as np

def auditar_incertidumbre_fase10(y_real_one_hot, probabilidades_v10):
    """Mide la fidelidad predictiva asegurando que no exista sobreestimación técnica."""
    brier_score = np.mean(np.sum((probabilidades_v10 - y_real_one_hot)**2, axis=1)) / 2
    sobreconfianza_penalizada = np.where((probabilidades_v10 > 0.90) & (y_real_one_hot == 0), 1, 0).sum()
    
    return {
        'Brier_Score_Auditado': brier_score,
        'Alertas_Sobreconfianza': sobreconfianza_penalizada
    }
