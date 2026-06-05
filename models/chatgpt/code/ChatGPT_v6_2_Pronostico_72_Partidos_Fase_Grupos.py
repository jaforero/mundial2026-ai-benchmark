"""
ChatGPT_v6_2_Pronostico_72_Partidos_Fase_Grupos.py

Reproduce el pronóstico v6.2-M para los 72 partidos de fase de grupos.

Ejecución:
    python ChatGPT_v6_2_Pronostico_72_Partidos_Fase_Grupos.py

Salidas:
    outputs_chatgpt_v6_2/ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6_2.csv
    outputs_chatgpt_v6_2/ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6_2.md
"""

from pathlib import Path
import pandas as pd

OUTPUT_DIR = Path("outputs_chatgpt_v6_2")
OUTPUT_DIR.mkdir(exist_ok=True)

MATCH_ROWS = [
    [1,"A","Ciudad de México","Templado + altitud","México","2-0","Sudáfrica","76-17-7","México","24%","Alta","v6.2 mantiene alta localía mexicana; altitud y fuerza estructural favorecen control territorial."],
    [2,"A","Guadalajara","Calor + tormentas vespertinas","Corea del Sur","1-1","Chequia","39-29-32","Corea del Sur","61%","Baja","Partido de fuerzas cercanas; calor reduce ritmo y eleva empate."],
    [3,"B","Toronto","Templado","Canadá","1-0","Bosnia y Herzegovina","63-22-15","Canadá","37%","Media-Alta","Localía y clima templado elevan el edge canadiense."],
    [4,"D","Los Ángeles","Cálido moderado","Estados Unidos","1-0","Paraguay","53-26-21","Estados Unidos","47%","Media","EE. UU. conserva ventaja de localía; Paraguay mantiene resistencia competitiva."],
    [5,"C","Boston","Moderado","Haití","0-1","Escocia","15-23-62","Escocia","38%","Media","Escocia superior, aunque con margen moderado."],
    [6,"D","Vancouver","Templado","Australia","0-1","Türkiye","21-26-53","Türkiye","47%","Media","Türkiye mantiene mejor score v6.2; Australia conserva robustez física."],
    [7,"C","Nueva York / Nueva Jersey","Calor húmedo","Brasil","1-1","Marruecos","44-29-27","Brasil","56%","Baja","Brasil sube levemente en v6.2, pero Marruecos conserva perfil táctico de alto riesgo."],
    [8,"B","San Francisco / Bahía","Fresco","Qatar","0-2","Suiza","9-21-70","Suiza","30%","Alta","Clima fresco y estructura suiza sostienen ventaja amplia."],
    [9,"E","Filadelfia","Calor húmedo","Costa de Marfil","1-1","Ecuador","34-28-38","Ecuador","62%","Baja","Ecuador sube por v6.2, pero calor y físico de Costa de Marfil sostienen empate modal."],
    [10,"E","Houston","Calor húmedo + domo mitigado","Alemania","3-0","Curazao","81-16-3","Alemania","19%","Alta","Diferencia de plantilla domina y el domo reduce estrés térmico."],
    [11,"F","Dallas","Calor extremo mitigado","Países Bajos","1-0","Japón","56-25-19","Países Bajos","44%","Media","Japón sube en v6.2, reduciendo margen neerlandés."],
    [12,"F","Monterrey","Calor extremo","Suecia","1-1","Túnez","45-30-25","Suecia","55%","Baja","v6.2 reduce ventaja sueca; calor extremo favorece empate."],
    [13,"H","Miami","Calor + humedad extremos","Arabia Saudita","0-1","Uruguay","10-23-67","Uruguay","33%","Alta","Uruguay se mantiene fuerte, aunque humedad limita el margen."],
    [14,"H","Atlanta","Domo / calor mitigado","España","3-0","Cabo Verde","82-17-1","España","18%","Alta","España conserva dominio por fuerza v6.2 y condiciones mitigadas."],
    [15,"G","Los Ángeles","Cálido moderado","Irán","1-0","Nueva Zelanda","60-24-16","Irán","40%","Media","Irán conserva ventaja, aunque v6.2 no lo sobredimensiona."],
    [16,"G","Seattle","Templado/fresco","Bélgica","1-0","Egipto","61-24-15","Bélgica","39%","Media","Bélgica baja marginalmente en v6.2; Egipto queda algo más competitivo."],
    [17,"I","Nueva York / Nueva Jersey","Calor húmedo","Francia","1-0","Senegal","59-25-16","Francia","41%","Media","Francia sube por rating, Senegal sube por robustez/clima; resultado cerrado."],
    [18,"I","Boston","Moderado","Irak","0-2","Noruega","7-19-74","Noruega","26%","Alta","Noruega mejora por talento diferencial y player-level."],
    [19,"J","Kansas City","Calor continental","Argentina","2-1","Argelia","64-24-12","Argentina","36%","Media-Alta","Argentina se mantiene élite, pero v6.2 reconoce mayor robustez argelina."],
    [20,"J","San Francisco / Bahía","Fresco","Austria","2-0","Jordania","70-20-10","Austria","30%","Alta","Austria superior y condiciones frescas favorecen estructura europea."],
    [21,"L","Toronto","Templado","Ghana","1-1","Panamá","43-29-28","Ghana","57%","Baja","Ghana sube levemente por físico y player-level; empate sigue modal."],
    [22,"L","Dallas","Calor extremo mitigado","Inglaterra","1-0","Croacia","63-23-14","Inglaterra","37%","Media","Inglaterra baja marginalmente por regularización de knockout; Croacia gana experiencia."],
    [23,"K","Houston","Calor húmedo + domo mitigado","Portugal","2-0","RD Congo","77-18-5","Portugal","23%","Alta","Portugal conserva ventaja amplia, aunque v6.2 reduce techo por riesgo defensivo."],
    [24,"K","Ciudad de México","Templado + altitud","Uzbekistán","0-2","Colombia","9-21-70","Colombia","30%","Alta","Colombia sube por v6.2, altitud y adaptación regional."],
    [25,"A","Atlanta","Domo / calor mitigado","Chequia","1-0","Sudáfrica","50-28-22","Chequia","50%","Media","Chequia baja marginalmente; partido con incertidumbre moderada."],
    [26,"B","Los Ángeles","Cálido moderado","Suiza","1-0","Bosnia y Herzegovina","60-24-16","Suiza","40%","Media","Suiza se mantiene estable por estructura y ranking."],
    [27,"B","Vancouver","Templado","Canadá","2-0","Qatar","71-20-9","Canadá","29%","Alta","v6.2 fortalece localía canadiense ante Qatar."],
    [28,"A","Guadalajara","Calor + tormentas vespertinas","México","2-1","Corea del Sur","62-23-15","México","38%","Media-Alta","México conserva ventaja por localía y adaptación; Corea sigue competitivo."],
    [29,"C","Filadelfia","Calor húmedo","Brasil","3-0","Haití","85-13-2","Brasil","15%","Alta","Brasil sube levemente por ajuste v6.2 y adaptación climática."],
    [30,"C","Boston","Moderado","Escocia","0-1","Marruecos","13-23-64","Marruecos","36%","Media-Alta","Marruecos sube por robustez táctica y validación de outsiders."],
    [31,"D","San Francisco / Bahía","Fresco","Türkiye","1-0","Paraguay","56-25-19","Türkiye","44%","Media","Türkiye conserva ventaja estructural; Paraguay mantiene riesgo de empate."],
    [32,"D","Seattle","Templado/fresco","Estados Unidos","1-0","Australia","54-25-21","Estados Unidos","46%","Media","Localía de EE. UU. compensa la solidez australiana."],
    [33,"E","Toronto","Templado","Alemania","1-0","Costa de Marfil","58-25-17","Alemania","42%","Media","Costa de Marfil sube en v6.2; Alemania mantiene edge."],
    [34,"E","Kansas City","Calor continental","Ecuador","2-0","Curazao","81-15-4","Ecuador","19%","Alta","Ecuador sube por clima, físico y ajuste de outsider competitivo."],
    [35,"F","Houston","Calor húmedo + domo mitigado","Países Bajos","1-0","Suecia","59-24-17","Países Bajos","41%","Media","Suecia baja levemente; Países Bajos conserva control."],
    [36,"F","Monterrey","Calor extremo","Túnez","1-1","Japón","22-30-48","Japón","52%","Baja","Japón sube en v6.2, pero calor mantiene empate como resultado modal."],
    [37,"H","Miami","Calor + humedad extremos","Uruguay","1-0","Cabo Verde","69-21-10","Uruguay","31%","Alta","Uruguay mejora por experiencia y robustez competitiva."],
    [38,"H","Atlanta","Domo / calor mitigado","España","3-0","Arabia Saudita","81-17-2","España","19%","Alta","España domina; v6.2 no cambia la lectura."],
    [39,"G","Los Ángeles","Cálido moderado","Bélgica","1-0","Irán","61-25-14","Bélgica","39%","Media","Bélgica baja levemente por riesgo generacional; Irán gana algo de resistencia."],
    [40,"G","Vancouver","Templado","Nueva Zelanda","0-1","Egipto","17-24-59","Egipto","41%","Media","Egipto sube levemente por ajuste v6.2."],
    [41,"I","Nueva York / Nueva Jersey","Calor húmedo","Noruega","0-1","Senegal","29-28-43","Senegal","57%","Baja","Ambos suben en v6.2; clima y físico sostienen ventaja senegalesa."],
    [42,"I","Filadelfia","Calor húmedo","Francia","2-0","Irak","79-17-4","Francia","21%","Alta","Francia sube por profundidad y rating; Irak permanece muy limitado."],
    [43,"J","Dallas","Calor extremo mitigado","Argentina","2-0","Austria","66-23-11","Argentina","34%","Media-Alta","Argentina baja marginalmente por edad y defensa del título."],
    [44,"J","San Francisco / Bahía","Fresco","Jordania","0-1","Argelia","13-23-64","Argelia","36%","Media-Alta","Argelia mejora por v6.2 y robustez física."],
    [45,"L","Boston","Moderado","Inglaterra","2-0","Ghana","76-19-5","Inglaterra","24%","Alta","Inglaterra sigue muy superior, aunque v6.2 sube ligeramente a Ghana."],
    [46,"L","Toronto","Templado","Panamá","0-1","Croacia","14-24-62","Croacia","38%","Media-Alta","Croacia conserva control por experiencia y gestión de torneo."],
    [47,"K","Houston","Calor húmedo + domo mitigado","Portugal","2-0","Uzbekistán","78-18-4","Portugal","22%","Alta","Portugal conserva ventaja, pero sin expansión excesiva por plantilla."],
    [48,"K","Guadalajara","Calor + tormentas vespertinas","Colombia","2-0","RD Congo","68-21-11","Colombia","32%","Alta","Colombia sube por equilibrio competitivo y contexto regional."],
    [49,"C","Miami","Calor + humedad extremos","Escocia","0-3","Brasil","7-17-76","Brasil","24%","Alta","Brasil mejora por adaptación y brecha de talento; humedad perjudica a Escocia."],
    [50,"C","Atlanta","Domo / calor mitigado","Marruecos","2-0","Haití","82-15-3","Marruecos","18%","Alta","Marruecos sube por v6.2 y control táctico."],
    [51,"B","Vancouver","Templado","Suiza","1-1","Canadá","34-29-37","Canadá","63%","Baja","Canadá conserva leve ventaja por localía; empate sigue modal."],
    [52,"B","Seattle","Templado/fresco","Bosnia y Herzegovina","1-1","Qatar","48-27-25","Bosnia y Herzegovina","52%","Baja","Qatar baja por menor fit climático y fuerza estructural."],
    [53,"A","Ciudad de México","Templado + altitud","Chequia","0-2","México","12-22-66","México","34%","Media-Alta","México sube por altitud/localía y mejor ajuste v6.2."],
    [54,"A","Monterrey","Calor extremo","Sudáfrica","1-1","Corea del Sur","25-29-46","Corea del Sur","54%","Baja","Calor reduce ventaja coreana; empate modal."],
    [55,"E","Filadelfia","Calor húmedo","Curazao","0-2","Costa de Marfil","6-19-75","Costa de Marfil","25%","Alta","Costa de Marfil sube por player-level físico y adaptación."],
    [56,"E","Nueva York / Nueva Jersey","Calor húmedo","Ecuador","1-1","Alemania","29-29-42","Alemania","58%","Baja","Ecuador sube y Alemania baja levemente; empate gana plausibilidad."],
    [57,"F","Dallas","Calor extremo mitigado","Japón","1-1","Suecia","41-29-30","Japón","59%","Baja","Japón sube por disciplina y player-level táctico."],
    [58,"F","Kansas City","Calor continental","Túnez","0-1","Países Bajos","10-23-67","Países Bajos","33%","Media-Alta","Países Bajos mantiene ventaja; calor limita margen."],
    [59,"D","Los Ángeles","Cálido moderado","Türkiye","1-1","Estados Unidos","41-28-31","Türkiye","59%","Baja","v6.2 conserva equilibrio entre fuerza turca y localía estadounidense."],
    [60,"D","San Francisco / Bahía","Fresco","Paraguay","1-1","Australia","35-29-36","Australia","64%","Baja","Partido de alta paridad; empate modal robusto."],
    [61,"I","Boston","Moderado","Noruega","0-1","Francia","13-22-65","Francia","35%","Media-Alta","Francia fuerte; Noruega conserva amenaza individual."],
    [62,"I","Toronto","Templado","Senegal","2-0","Irak","79-16-5","Senegal","21%","Alta","Senegal mejora por v6.2 y fuerza física/estructural."],
    [63,"G","Seattle","Templado/fresco","Egipto","1-1","Irán","39-29-32","Egipto","61%","Baja","Egipto sube levemente; partido táctico cerrado."],
    [64,"G","Vancouver","Templado","Nueva Zelanda","0-2","Bélgica","4-18-78","Bélgica","22%","Alta","Bélgica sigue superior pese a ligera regularización."],
    [65,"H","Houston","Calor húmedo + domo mitigado","Cabo Verde","1-1","Arabia Saudita","35-29-36","Arabia Saudita","64%","Baja","Partido de baja diferencia; empate modal."],
    [66,"H","Guadalajara","Calor + tormentas vespertinas","Uruguay","0-1","España","18-25-57","España","43%","Media","Uruguay mejora ligeramente y reduce margen español."],
    [67,"L","Nueva York / Nueva Jersey","Calor húmedo","Panamá","0-2","Inglaterra","5-19-76","Inglaterra","24%","Alta","Inglaterra mantiene ventaja; regularización evita exceso."],
    [68,"L","Filadelfia","Calor húmedo","Croacia","1-1","Ghana","51-28-21","Croacia","49%","Baja","Croacia mantiene leve edge; Ghana gana por físico/calor."],
    [69,"J","Kansas City","Calor continental","Argelia","1-0","Austria","43-29-28","Argelia","57%","Baja","Argelia sube por v6.2 y adaptación al calor."],
    [70,"J","Dallas","Calor extremo mitigado","Jordania","0-3","Argentina","2-16-82","Argentina","18%","Alta","Brecha de talento muy amplia; marcador estable."],
    [71,"K","Miami","Calor + humedad extremos","Colombia","1-1","Portugal","27-29-44","Portugal","56%","Baja","Colombia sube por v6.2; humedad extrema reduce margen portugués."],
    [72,"K","Atlanta","Domo / calor mitigado","RD Congo","1-1","Uzbekistán","40-28-32","RD Congo","60%","Baja","RD Congo sube levemente por físico y player-level agregado."],
]

COLUMNS = ["M","Grupo","Sede","Riesgo climático","Equipo A","Marcador v6.2-M","Equipo B","Prob. A-E-B","Favorito","Riesgo sorpresa","Confianza","Nota técnica"]

def parse_prob_triplet(prob_string):
    """Convierte '76-17-7' en (0.76, 0.17, 0.07)."""
    a, draw, b = [float(x) / 100.0 for x in prob_string.split("-")]
    return a, draw, b

def add_numeric_probability_columns(df):
    probs = df["Prob. A-E-B"].apply(parse_prob_triplet)
    df["P_A"] = probs.apply(lambda x: x[0])
    df["P_Empate"] = probs.apply(lambda x: x[1])
    df["P_B"] = probs.apply(lambda x: x[2])
    return df

def validate_probabilities(df):
    """Verifica que cada fila sume 100%."""
    sums = df["Prob. A-E-B"].apply(lambda s: sum(int(x) for x in s.split("-")))
    invalid = df.loc[sums != 100]
    if not invalid.empty:
        raise ValueError(f"Hay probabilidades que no suman 100: {invalid[['M','Prob. A-E-B']]}")
    return True

def build_table():
    df = pd.DataFrame(MATCH_ROWS, columns=COLUMNS)
    validate_probabilities(df)
    df = add_numeric_probability_columns(df)
    return df

def write_outputs(df):
    csv_path = OUTPUT_DIR / "ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6_2.csv"
    md_path = OUTPUT_DIR / "ChatGPT_Pronostico_72_Partidos_Fase_Grupos_v6_2.md"

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    display_cols = COLUMNS
    md = "# ChatGPT Pronóstico 72 Partidos Fase de Grupos v6.2\n\n"
    md += "## Tabla completa\n\n"
    md += df[display_cols].to_markdown(index=False)
    md += "\n"
    md_path.write_text(md, encoding="utf-8")

    print(f"CSV generado: {csv_path}")
    print(f"Markdown generado: {md_path}")

if __name__ == "__main__":
    final_df = build_table()
    write_outputs(final_df)
