# -*- coding: utf-8 -*-
"""
AJUSTE v3 — Ataque/Defensa por equipo estimados por máxima verosimilitud
(Dixon-Coles / Maher) sobre resultados internacionales reales (martj42 dataset),
con decaimiento temporal y menor peso a amistosos.

Entrega:
  - validación FUERA DE MUESTRA contra los Mundiales 2018 y 2022 (RPS) vs línea base
  - parámetros finales (att, def por equipo, mu, home, rho) ajustados con datos
    hasta 2026-06-05, mapeados a los nombres en español de las 48 del Mundial 2026
Guarda strengths_v3.json
"""
import csv, json, math
import numpy as np
from scipy.optimize import minimize_scalar

DATA = "/home/claude/wc2026/intl_results.csv"

# 48 (español) -> nombre en el dataset (inglés)
NAME = {"México":"Mexico","Sudáfrica":"South Africa","Corea del Sur":"South Korea","Chequia":"Czech Republic",
"Canadá":"Canada","Bosnia":"Bosnia and Herzegovina","Qatar":"Qatar","Suiza":"Switzerland","Brasil":"Brazil",
"Marruecos":"Morocco","Haití":"Haiti","Escocia":"Scotland","Estados Unidos":"United States","Paraguay":"Paraguay",
"Australia":"Australia","Türkiye":"Turkey","Alemania":"Germany","Curazao":"Curaçao","Costa de Marfil":"Ivory Coast",
"Ecuador":"Ecuador","Países Bajos":"Netherlands","Japón":"Japan","Suecia":"Sweden","Túnez":"Tunisia",
"Bélgica":"Belgium","Egipto":"Egypt","Irán":"Iran","Nueva Zelanda":"New Zealand","España":"Spain",
"Cabo Verde":"Cape Verde","Arabia Saudí":"Saudi Arabia","Uruguay":"Uruguay","Francia":"France","Senegal":"Senegal",
"Noruega":"Norway","Iraq":"Iraq","Argentina":"Argentina","Argelia":"Algeria","Austria":"Austria","Jordania":"Jordan",
"Portugal":"Portugal","RD Congo":"DR Congo","Uzbekistán":"Uzbekistan","Colombia":"Colombia","Inglaterra":"England",
"Croacia":"Croatia","Ghana":"Ghana","Panamá":"Panama"}
INV = {v:k for k,v in NAME.items()}

# ---------- carga ----------
ALLROWS = []
with open(DATA, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["home_score"] in ("NA",""): continue
        ALLROWS.append((r["date"], r["home_team"], r["away_team"],
                        int(r["home_score"]), int(r["away_score"]),
                        r["tournament"], r["neutral"].strip().upper()=="TRUE"))
ALLROWS.sort(key=lambda x: x[0])

def days(d1, d0):
    from datetime import date
    a = date(*map(int,d1.split("-"))); b = date(*map(int,d0.split("-")))
    return (a-b).days

def fit(cutoff, window_years=6.0, half_life=730.0, friendly_w=0.55, ridge=0.08):
    """Ajusta att/def/mu/home con datos en [cutoff-window, cutoff). Devuelve dicts."""
    lo = f"{int(cutoff[:4])-int(window_years)}{cutoff[4:]}"
    rows = [r for r in ALLROWS if lo <= r[0] < cutoff]
    teams = sorted({t for r in rows for t in (r[1], r[2])})
    idx = {t:i for i,t in enumerate(teams)}; T = len(teams)
    hi = np.array([idx[r[1]] for r in rows]); ai = np.array([idx[r[2]] for r in rows])
    hs = np.array([r[3] for r in rows], float); as_ = np.array([r[4] for r in rows], float)
    hf = np.array([0.0 if r[6] else 1.0 for r in rows])         # localía solo si no neutral
    w  = np.array([(0.5**(days(cutoff,r[0])/half_life)) * (friendly_w if r[5]=="Friendly" else 1.0)
                   for r in rows])
    # vector de parámetros: [mu, home, att(T), def(T)]
    def unpack(p): return p[0], p[1], p[2:2+T], p[2+T:2+2*T]
    def negll(p):
        mu, h, att, dfn = unpack(p)
        lh = np.exp(mu + att[hi] - dfn[ai] + h*hf)
        la = np.exp(mu + att[ai] - dfn[hi])
        ll = np.sum(w*(hs*np.log(lh) - lh + as_*np.log(la) - la))
        ll -= 0.5*ridge*(np.sum(att**2)+np.sum(dfn**2))
        # gradiente
        rh = w*(hs-lh); ra = w*(as_-la)
        gmu = np.sum(rh)+np.sum(ra); gh = np.sum(rh*hf)
        gatt = np.zeros(T); gdef = np.zeros(T)
        np.add.at(gatt, hi, rh); np.add.at(gatt, ai, ra)
        np.add.at(gdef, ai, -rh); np.add.at(gdef, hi, -ra)
        gatt -= ridge*att; gdef -= ridge*dfn
        return -ll, -np.concatenate([[gmu,gh],gatt,gdef])
    from scipy.optimize import minimize
    p0 = np.zeros(2+2*T); p0[0] = math.log(1.3); p0[1] = 0.25
    res = minimize(negll, p0, jac=True, method="L-BFGS-B",
                   options={"maxiter":500,"ftol":1e-9})
    mu, h, att, dfn = unpack(res.x)
    att = att - att.mean(); dfn = dfn - dfn.mean()   # centrar (identificabilidad)
    ATT = {t: float(att[idx[t]]) for t in teams}; DEF = {t: float(dfn[idx[t]]) for t in teams}
    rho = fit_rho(rows, mu, h, ATT, DEF)
    return {"mu":float(mu), "home":float(h), "att":ATT, "def":DEF, "rho":rho, "n_matches":len(rows)}

def tau(i,j,la,lb,rho):
    if i==0 and j==0: return 1 - la*lb*rho
    if i==0 and j==1: return 1 + la*rho
    if i==1 and j==0: return 1 + lb*rho
    if i==1 and j==1: return 1 - rho
    return 1.0

def fit_rho(rows, mu, h, ATT, DEF):
    sub = [r for r in rows if r[1] in ATT and r[2] in ATT][-4000:]
    def nll(rho):
        s=0.0
        for d,ht,at_,hsc,asc,tn,neu in sub:
            la=math.exp(mu+ATT[ht]-DEF[at_]+(0 if neu else h)); lb=math.exp(mu+ATT[at_]-DEF[ht])
            if hsc<=1 and asc<=1:
                t=tau(hsc,asc,la,lb,rho)
                if t<=0: return 1e9
                s+=math.log(t)
        return -s
    r=minimize_scalar(nll, bounds=(-0.2,0.2), method="bounded")
    return float(r.x)

def outcome_probs(la, lb, rho, kmax=10):
    pa=np.exp(-la)*np.array([la**k/math.factorial(k) for k in range(kmax+1)])
    pb=np.exp(-lb)*np.array([lb**k/math.factorial(k) for k in range(kmax+1)])
    M=np.outer(pa,pb)
    for (i,j) in [(0,0),(0,1),(1,0),(1,1)]: M[i,j]*=tau(i,j,la,lb,rho)
    M/=M.sum()
    pH=np.tril(M,-1).sum(); pD=np.trace(M); pA=np.triu(M,1).sum()
    return pH,pD,pA

def rps(probs, outcome):  # probs=(pH,pD,pA), outcome in {0,1,2}
    o=[0,0,0]; o[outcome]=1
    c=0.0; cp=0.0; co=0.0
    for k in range(3):
        cp+=probs[k]; co+=o[k]; c+=(cp-co)**2
    return 0.5*c

def wc_group_matches(year, n=48):
    rs=[r for r in ALLROWS if r[5]=="FIFA World Cup" and r[0][:4]==year]
    return rs[:n]   # fase de grupos = primeros 48 cronológicamente

def validate(year, cutoff):
    f=fit(cutoff)
    ms=wc_group_matches(year)
    used=0; rps_model=0.0; rps_unif=0.0; hits=0
    for d,ht,at_,hsc,asc,tn,neu in ms:
        if ht not in f["att"] or at_ not in f["att"]: continue
        la=math.exp(f["mu"]+f["att"][ht]-f["def"][at_]+(0 if neu else f["home"]))
        lb=math.exp(f["mu"]+f["att"][at_]-f["def"][ht])
        pH,pD,pA=outcome_probs(la,lb,f["rho"])
        oc=0 if hsc>asc else (2 if asc>hsc else 1)
        rps_model+=rps((pH,pD,pA),oc); rps_unif+=rps((1/3,1/3,1/3),oc)
        pred=0 if pH>=pD and pH>=pA else (2 if pA>=pD else 1)
        hits+= (pred==oc); used+=1
    return used, rps_model/used, rps_unif/used, hits/used

if __name__=="__main__":
    print("=== VALIDACIÓN FUERA DE MUESTRA (ajuste solo con datos previos a cada Mundial) ===")
    tot_m=tot_u=0.0; tot_n=0
    for year,cut in [("2018","2018-06-10"),("2022","2022-11-19")]:
        n,rm,ru,acc=validate(year,cut)
        tot_m+=rm*n; tot_u+=ru*n; tot_n+=n
        print(f"  Mundial {year}: {n} partidos | RPS modelo {rm:.4f} | RPS uniforme {ru:.4f} | "
              f"mejora {100*(1-rm/ru):.1f}% | acierto 1X2 {100*acc:.1f}%")
    print(f"  GLOBAL 2018+2022: RPS modelo {tot_m/tot_n:.4f} vs uniforme {tot_u/tot_n:.4f} "
          f"-> mejora {100*(1-tot_m/tot_u):.1f}%  (v2 reportó RPS≈0.224, +9% sobre uniforme)")

    print("\n=== AJUSTE FINAL (datos hasta 2026-06-05) ===")
    F=fit("2026-06-05")
    print(f"  Partidos usados: {F['n_matches']}  | mu={F['mu']:.3f} home={F['home']:.3f} rho={F['rho']:.3f}")
    out={"mu":F["mu"],"home":F["home"],"rho":F["rho"],"n_matches":F["n_matches"],
         "att":{}, "def":{}}
    miss=[]
    for es,en in NAME.items():
        if en in F["att"]:
            out["att"][es]=F["att"][en]; out["def"][es]=F["def"][en]
        else: miss.append(es)
    out["missing"]=miss
    json.dump(out, open("/home/claude/wc2026/strengths_v3.json","w",encoding="utf-8"), ensure_ascii=False, indent=0)
    # top ataque y mejor defensa entre las 48
    aa=sorted(out["att"].items(),key=lambda x:-x[1])[:8]
    dd=sorted(out["def"].items(),key=lambda x:-x[1])[:8]
    print("  Mejor ATAQUE (log):", ", ".join(f"{k} {v:+.2f}" for k,v in aa))
    print("  Mejor DEFENSA (log):", ", ".join(f"{k} {v:+.2f}" for k,v in dd))
    print("  Sin datos:", miss)
    print("Guardado strengths_v3.json")
