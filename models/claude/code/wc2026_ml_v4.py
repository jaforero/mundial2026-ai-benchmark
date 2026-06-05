# -*- coding: utf-8 -*-
"""
v4 — Modelo de MACHINE LEARNING (gradient boosting con pérdida de Poisson) que integra:
  - Elo actual (World Football Elo calculado de resultados reales, a junio 2026)
  - Forma reciente (goles a favor/en contra, últimos partidos)
  - Histórico de Mundiales (partidos y % de victoria en Copas del Mundo)
  - Localía / sede neutral
Predice los goles esperados de cada lado -> matriz Poisson(+Dixon-Coles) -> distribución.
Se VALIDA FUERA DE MUESTRA contra los Mundiales 2018 y 2022 y se compara, cabeza a cabeza,
contra el motor Dixon-Coles data-driven v3. Decide la evidencia, no la etiqueta.
"""
import csv, math, json
import numpy as np
from collections import defaultdict, deque
from sklearn.ensemble import HistGradientBoostingRegressor

DATA="/home/claude/wc2026/intl_results.csv"
NAME = json.load(open("/home/claude/wc2026/strengths_v3.json",encoding="utf-8"))  # solo para nombres ES
# (reusamos el mapa ES->EN del fit v3)
ES2EN = {"México":"Mexico","Sudáfrica":"South Africa","Corea del Sur":"South Korea","Chequia":"Czech Republic",
"Canadá":"Canada","Bosnia":"Bosnia and Herzegovina","Qatar":"Qatar","Suiza":"Switzerland","Brasil":"Brazil",
"Marruecos":"Morocco","Haití":"Haiti","Escocia":"Scotland","Estados Unidos":"United States","Paraguay":"Paraguay",
"Australia":"Australia","Türkiye":"Turkey","Alemania":"Germany","Curazao":"Curaçao","Costa de Marfil":"Ivory Coast",
"Ecuador":"Ecuador","Países Bajos":"Netherlands","Japón":"Japan","Suecia":"Sweden","Túnez":"Tunisia",
"Bélgica":"Belgium","Egipto":"Egypt","Irán":"Iran","Nueva Zelanda":"New Zealand","España":"Spain",
"Cabo Verde":"Cape Verde","Arabia Saudí":"Saudi Arabia","Uruguay":"Uruguay","Francia":"France","Senegal":"Senegal",
"Noruega":"Norway","Iraq":"Iraq","Argentina":"Argentina","Argelia":"Algeria","Austria":"Austria","Jordania":"Jordan",
"Portugal":"Portugal","RD Congo":"DR Congo","Uzbekistán":"Uzbekistan","Colombia":"Colombia","Inglaterra":"England",
"Croacia":"Croatia","Ghana":"Ghana","Panamá":"Panama"}

rows=[]
with open(DATA,encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["home_score"] in ("NA",""): continue
        rows.append((r["date"],r["home_team"],r["away_team"],int(r["home_score"]),int(r["away_score"]),
                     r["tournament"],r["neutral"].strip().upper()=="TRUE"))
rows.sort(key=lambda x:x[0])

IMP={"FIFA World Cup":60,"FIFA World Cup qualification":40,"UEFA Euro":50,"Copa América":50,
     "African Cup of Nations":40,"AFC Asian Cup":40,"UEFA Nations League":35,"Confederations Cup":40,
     "CONCACAF Championship":35,"Gold Cup":35,"Friendly":20}
def kfac(t): return IMP.get(t,30)

def build_features(upto):
    """Recorre la historia hasta 'upto' y devuelve, por partido en [2004,upto),
    las features pre-partido + objetivo (goles). También deja el estado final por equipo."""
    elo=defaultdict(lambda:1500.0)
    formGF=defaultdict(lambda:deque(maxlen=10)); formGA=defaultdict(lambda:deque(maxlen=10))
    wcM=defaultdict(int); wcW=defaultdict(int)
    X=[]; y=[]; rowsout=[]
    for d,h,a,hs,as_,tn,neu in rows:
        if d>=upto: break
        eh,ea=elo[h],elo[a]
        # features pre-partido (perspectiva equipo->rival), dos filas por partido
        def feat(team,opp,is_home):
            gf=np.mean(formGF[team]) if formGF[team] else 1.2
            ga=np.mean(formGA[team]) if formGA[team] else 1.2
            ogf=np.mean(formGF[opp]) if formGF[opp] else 1.2
            oga=np.mean(formGA[opp]) if formGA[opp] else 1.2
            wr=(wcW[team]/wcM[team]) if wcM[team]>0 else 0.0
            owr=(wcW[opp]/wcM[opp]) if wcM[opp]>0 else 0.0
            return [elo[team],elo[opp],elo[team]-elo[opp],gf,ga,ogf,oga,
                    wcM[team],wr,owr,1.0 if is_home else 0.0]
        if d>="2004-01-01":
            X.append(feat(h,a,not neu)); y.append(hs)
            X.append(feat(a,h,False));   y.append(as_)
        # actualizar Elo (con escala por diferencia de goles)
        exp_h=1/(1+10**((ea-eh)/400)); res_h=1.0 if hs>as_ else (0.5 if hs==as_ else 0.0)
        gd=abs(hs-as_); mult=1.0 if gd<=1 else (1.5 if gd==2 else (1.75+(gd-3)/8))
        K=kfac(tn)
        delta=K*mult*(res_h-exp_h); elo[h]+=delta; elo[a]-=delta
        # forma
        formGF[h].append(hs);formGA[h].append(as_);formGF[a].append(as_);formGA[a].append(hs)
        # histórico mundiales
        if tn=="FIFA World Cup":
            wcM[h]+=1;wcM[a]+=1
            if hs>as_: wcW[h]+=1
            elif as_>hs: wcW[a]+=1
            else: wcW[h]+=0  # empate no suma victoria
    state={"elo":dict(elo),
           "formGF":{k:(np.mean(v) if v else 1.2) for k,v in formGF.items()},
           "formGA":{k:(np.mean(v) if v else 1.2) for k,v in formGA.items()},
           "wcM":dict(wcM),"wcW":dict(wcW)}
    return np.array(X),np.array(y),state

def featvec(state,team,opp,is_home):
    e=state["elo"]; gf=state["formGF"]; ga=state["formGA"]; wcM=state["wcM"]; wcW=state["wcW"]
    et=e.get(team,1500.0); eo=e.get(opp,1500.0)
    wr=(wcW.get(team,0)/wcM[team]) if wcM.get(team,0)>0 else 0.0
    owr=(wcW.get(opp,0)/wcM[opp]) if wcM.get(opp,0)>0 else 0.0
    return [et,eo,et-eo,gf.get(team,1.2),ga.get(team,1.2),gf.get(opp,1.2),ga.get(opp,1.2),
            wcM.get(team,0),wr,owr,1.0 if is_home else 0.0]

def train(upto):
    X,y,state=build_features(upto)
    m=HistGradientBoostingRegressor(loss="poisson",max_iter=400,learning_rate=0.05,
        max_depth=4,min_samples_leaf=60,l2_regularization=1.0,random_state=7)
    m.fit(X,y)
    return m,state

def tau(i,j,la,lb,rho):
    return {(0,0):1-la*lb*rho,(0,1):1+la*rho,(1,0):1+lb*rho,(1,1):1-rho}.get((i,j),1.0)
def probs(la,lb,rho=-0.05,k=10):
    pa=np.exp(-la)*np.array([la**i/math.factorial(i) for i in range(k+1)])
    pb=np.exp(-lb)*np.array([lb**i/math.factorial(i) for i in range(k+1)])
    M=np.outer(pa,pb)
    for ij in [(0,0),(0,1),(1,0),(1,1)]: M[ij]*=tau(ij[0],ij[1],la,lb,rho)
    M/=M.sum(); return np.tril(M,-1).sum(),np.trace(M),np.triu(M,1).sum()
def rps(p,o):
    oo=[0,0,0]; oo[o]=1; c=cp=co=0.0
    for k in range(3): cp+=p[k];co+=oo[k];c+=(cp-co)**2
    return 0.5*c

def wc_group(year,n=48):
    rs=[r for r in rows if r[5]=="FIFA World Cup" and r[0][:4]==year]; return rs[:n]

def validate(year,cutoff):
    m,state=train(cutoff)
    ms=wc_group(year); n=0; rm=0.0; ru=0.0; hit=0
    for d,h,a,hs,as_,tn,neu in ms:
        lh=float(m.predict([featvec(state,h,a,not neu)])[0])
        la=float(m.predict([featvec(state,a,h,False)])[0])
        pH,pD,pA=probs(lh,la)
        oc=0 if hs>as_ else (2 if as_>hs else 1)
        rm+=rps((pH,pD,pA),oc); ru+=rps((1/3,1/3,1/3),oc)
        pred=0 if pH>=pD and pH>=pA else (2 if pA>=pD else 1); hit+=(pred==oc); n+=1
    return n,rm/n,ru/n,hit/n

if __name__=="__main__":
    print("=== ML v4 — VALIDACIÓN FUERA DE MUESTRA (gradient boosting Poisson) ===")
    tm=tu=0.0; tn=0
    for year,cut in [("2018","2018-06-10"),("2022","2022-11-19")]:
        n,rm,ru,acc=validate(year,cut)
        tm+=rm*n;tu+=ru*n;tn+=n
        print(f"  Mundial {year}: RPS ML {rm:.4f} | uniforme {ru:.4f} | mejora {100*(1-rm/ru):.1f}% | acierto {100*acc:.1f}%")
    print(f"  GLOBAL ML 2018+2022: RPS {tm/tn:.4f} -> mejora {100*(1-tm/tu):.1f}%")
    print(f"  --- Referencia Dixon-Coles v3 (mismo test): RPS 0.2127, mejora 13.1% ---")
