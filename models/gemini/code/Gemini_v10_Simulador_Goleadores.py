import numpy as np
import pandas as pd

def proyeccion_goleadores_fase10(df_jugadores):
    """
    Integra auditoría clínica. Jugadores con estado crítico (<0.3 en viabilidad)
    son excluidos para evitar proyecciones irreales de Goles Esperados.
    """
    proyecciones = []
    
    for _, jg in df_jugadores.iterrows():
        # Filtro estricto de viabilidad clínica contemporánea
        if jg['viabilidad_clinica_actual'] < 0.3:
            continue 
            
        xg_bruto = (jg['xg_equipo'] * jg['cuota_remate']) + (1.5 * jg['penalista'])
        modificador_minutos = 1.0 - jg['riesgo_rotacion']
        minutos_estimados = min(680, 720 * modificador_minutos)
        
        xg_ajustado = xg_bruto * (minutos_estimados / 720)
        proyecciones.append({'Jugador': jg['nombre'], 'xG_Fase10': xg_ajustado, 'Minutos': minutos_estimados})
        
    df_res = pd.DataFrame(proyecciones).sort_values(by='xG_Fase10', ascending=False)
    exp_vals = np.exp(df_res['xG_Fase10'])
    df_res['Prob_Bota_Oro'] = exp_vals / exp_vals.sum()
    
    return df_res
