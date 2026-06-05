import numpy as np
import pandas as pd

class GeminiV7_TournamentSimulator:
    def __init__(self, df_equipos, iteraciones=10000):
        self.equipos = df_equipos
        self.iteraciones = iteraciones
        self.resultados_acumulados = {eq: {'R32':0, 'Oct':0, 'Cua':0, 'Sem':0, 'Fin':0, 'Camp':0} for eq in self.equipos['Nombre']}

    def simular_llave_eliminatoria(self, equipo_A, equipo_B):
        # Pseudo-implementacion para backtesting
        xg_A = np.random.normal(1.5, 0.5) 
        xg_B = np.random.normal(1.2, 0.5)
        
        goles_A = np.random.poisson(max(0, xg_A))
        goles_B = np.random.poisson(max(0, xg_B))
        
        if goles_A > goles_B: return equipo_A
        elif goles_B > goles_A: return equipo_B
        else:
            # Ensamble DRL: Resolución por penales
            prob_penales_A = 0.5 + (self.equipos.loc[equipo_A, 'lpn'] - self.equipos.loc[equipo_B, 'lpn'])
            return equipo_A if np.random.rand() < prob_penales_A else equipo_B

    def exportar_probabilidades(self):
        df_resultados = pd.DataFrame(self.resultados_acumulados).T / self.iteraciones
        return df_resultados.sort_values(by='Camp', ascending=False)
