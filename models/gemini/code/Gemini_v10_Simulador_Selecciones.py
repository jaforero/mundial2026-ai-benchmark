import numpy as np
import pandas as pd

class SimuladorFase10_Equipos:
    def __init__(self, df_equipos, iteraciones=10000, temperatura=1.12):
        self.equipos = df_equipos
        self.iteraciones = iteraciones
        self.temp = temperatura
        self.resultados = {eq: {'R32':0, 'Oct':0, 'Cua':0, 'Sem':0, 'Fin':0, 'Camp':0} for eq in self.equipos['index']}

    def _ajuste_softmax_temperatura(self, prob_A, prob_B):
        """Distribuye la probabilidad mitigando afirmaciones estocásticas absolutas."""
        logits = np.log([prob_A + 1e-9, prob_B + 1e-9]) / self.temp
        exp_logits = np.exp(logits)
        return exp_logits / np.sum(exp_logits)

    def simular_cruce_eliminatorio(self, eq_A, eq_B):
        fuerza_A = self.equipos.loc[eq_A, 'lpn_calibrado'] - self.equipos.loc[eq_A, 'decaimiento_campeon']
        fuerza_B = self.equipos.loc[eq_B, 'lpn_calibrado'] - self.equipos.loc[eq_B, 'decaimiento_campeon']
        
        prob_base_A = 1 / (1 + np.exp(-(fuerza_A - fuerza_B)))
        prob_calibrada_A, _ = self._ajuste_softmax_temperatura(prob_base_A, 1 - prob_base_A)
        
        return eq_A if np.random.rand() < prob_calibrada_A else eq_B
        
    def exportar_probabilidades_calibradas(self):
        return pd.DataFrame(self.resultados).T / self.iteraciones

# Anexo Técnico y Conclusiones: Fase 10 (Auditoría de Muestreo)
