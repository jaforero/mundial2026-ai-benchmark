import numpy as np
import pandas as pd

class SimuladorFase8_Equipos:
    def __init__(self, df_equipos, iteraciones=10000, temperatura=1.15):
        self.equipos = df_equipos
        self.iteraciones = iteraciones
        self.temp = temperatura
        self.resultados = {eq: {'R32':0, 'Oct':0, 'Cua':0, 'Sem':0, 'Fin':0, 'Camp':0} for eq in self.equipos['index']}

    def _ajuste_softmax_temperatura(self, prob_A, prob_B):
        """Aplica calibración de temperatura para evitar certezas absolutas."""
        logits = np.log([prob_A + 1e-9, prob_B + 1e-9]) / self.temp
        exp_logits = np.exp(logits)
        return exp_logits / np.sum(exp_logits)

    def simular_cruce_eliminatorio(self, eq_A, eq_B):
        """Simulación estocástica penalizando historial inactivo (LPN)."""
        fuerza_A = self.equipos.loc[eq_A, 'lpn_calibrado'] - self.equipos.loc[eq_A, 'decaimiento_campeon']
        fuerza_B = self.equipos.loc[eq_B, 'lpn_calibrado'] - self.equipos.loc[eq_B, 'decaimiento_campeon']
        
        prob_base_A = 1 / (1 + np.exp(-(fuerza_A - fuerza_B)))
        prob_calibrada_A, _ = self._ajuste_softmax_temperatura(prob_base_A, 1 - prob_base_A)
        
        return eq_A if np.random.rand() < prob_calibrada_A else eq_B
        
    def exportar_probabilidades_calibradas(self):
        return pd.DataFrame(self.resultados).T / self.iteraciones

# Bloque 2: Simulación de Partidos (Dixon-Coles Dinámico)
import numpy as np
from scipy.stats import poisson

def calcular_rho_dinamico(elo_A, elo_B, utci_impact):
    """Calcula la dependencia de empates basado en fricción y clima."""
    diff = abs(elo_A - elo_B)
    base_rho = -0.05
    ajuste_friccion = max(0, (100 - diff) * 0.001)
    ajuste_clima = utci_impact * 0.02
    return base_rho + ajuste_friccion + ajuste_clima

def prob_dixon_coles_fase8(x, y, xg_A, xg_B, elo_A, elo_B, utci):
    """Distribución bivariada con Rho dinámico."""
    rho = calcular_rho_dinamico(elo_A, elo_B, utci)
    prob_independiente = poisson.pmf(x, xg_A) * poisson.pmf(y, xg_B)
    
    if x == 0 and y == 0: return prob_independiente * (1 - xg_A * xg_B * rho)
    elif x == 0 and y == 1: return prob_independiente * (1 + xg_A * rho)
    elif x == 1 and y == 0: return prob_independiente * (1 + xg_B * rho)
    elif x == 1 and y == 1: return prob_independiente * (1 - rho)
    return prob_independiente

# Bloque 3: Top Goleadores (Ajuste de Forma Clínica)
import numpy as np
import pandas as pd

def proyeccion_goleadores_fase8(df_jugadores):
    """
    Integra la inactividad clínica y el riesgo de rotación.
    """
    proyecciones = []
    
    for _, jg in df_jugadores.iterrows():
        xg_bruto = (jg['xg_equipo'] * jg['cuota_remate']) + (1.5 * jg['penalista'])
        
        # Penalización Bayesiana por inactividad clínica
        modificador_minutos = 1.0 - jg['riesgo_clinico']
        minutos_estimados = min(680, 720 * modificador_minutos)
        
        xg_ajustado = xg_bruto * (minutos_estimados / 720)
        proyecciones.append({'Jugador': jg['nombre'], 'xG_Fase8': xg_ajustado, 'Minutos': minutos_estimados})
        
    df_res = pd.DataFrame(proyecciones).sort_values(by='xG_Fase8', ascending=False)
    
    exp_vals = np.exp(df_res['xG_Fase8'])
    df_res['Prob_Bota_Oro'] = exp_vals / exp_vals.sum()
    
    return df_res

# Bloque 4: Análisis de Calibración de Incertidumbre
import numpy as np
from sklearn.metrics import brier_score_loss

def auditar_incertidumbre_fase8(y_real_one_hot, probabilidades_v8):
    """
    Evalúa la robustez del modelo verificando que el exceso de confianza
    haya sido penalizado correctamente a través del Brier Score.
    """
    brier_score = np.mean(np.sum((probabilidades_v8 - y_real_one_hot)**2, axis=1)) / 2
    
    # Check de sobreconfianza: detecta escenarios de falla en proyecciones altas
    sobreconfianza_penalizada = np.where((probabilidades_v8 > 0.90) & (y_real_one_hot == 0), 1, 0).sum()
    
    return {
        'Brier_Score_Calibrado': brier_score,
        'Alertas_Sobreconfianza': sobreconfianza_penalizada
    }
