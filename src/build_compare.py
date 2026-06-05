# -*- coding: utf-8 -*-
"""Genera la página web comparativa (Claude vs ChatGPT vs Gemini + Consenso)."""
import json

DATA = json.load(open("/home/claude/wc2026/consolidated.json", encoding="utf-8"))
BLOB = json.dumps(DATA, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Benchmark IA · Pronósticos Mundial FIFA 2026 — Claude · ChatGPT · Gemini</title>

<!-- ============ SEO ============ -->
<meta name="description" content="Claude, ChatGPT y Gemini pronostican el Mundial FIFA 2026 y un consenso las combina: 48 selecciones, 72 partidos y modelos de ciencia de datos comparados.">
<meta name="author" content="Javier Forero">
<meta name="keywords" content="Mundial 2026, pronóstico Mundial 2026, IA fútbol, Claude ChatGPT Gemini, ciencia de datos deportiva, Dixon-Coles, machine learning fútbol, Javier Forero">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#4e00ff">
<link rel="canonical" href="https://mundial.javierforero.co/">
<link rel="icon" type="image/svg+xml" href="favicon.svg">

<!-- ============ Open Graph (LinkedIn, Facebook, WhatsApp) ============ -->
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="Javier Forero">
<meta property="og:url" content="https://mundial.javierforero.co/">
<meta property="og:title" content="Benchmark IA · Mundial 2026 — Claude vs ChatGPT vs Gemini">
<meta property="og:description" content="Tres IAs pronostican la Copa Mundial 2026 y un consenso las combina. Compara 48 selecciones y 72 partidos con modelos estadísticos y de machine learning.">
<meta property="og:image" content="https://mundial.javierforero.co/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Benchmark IA · Mundial 2026 — Claude, ChatGPT y Gemini">

<!-- ============ Twitter / X ============ -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Benchmark IA · Mundial 2026 — Claude vs ChatGPT vs Gemini">
<meta name="twitter:description" content="Tres IAs pronostican la Copa Mundial 2026 y un consenso las combina. 48 selecciones, 72 partidos, ciencia de datos.">
<meta name="twitter:image" content="https://mundial.javierforero.co/og-image.png">

<!-- ============ Datos estructurados (GEO / motores de IA) ============ -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Benchmark IA · Mundial 2026 — Claude vs ChatGPT vs Gemini",
  "url": "https://mundial.javierforero.co/",
  "inLanguage": "es",
  "description": "Comparación de los pronósticos de Claude, ChatGPT y Gemini para la Copa Mundial de la FIFA 2026, con un consenso construido sobre los tres modelos.",
  "author": {"@type": "Person", "name": "Javier Forero", "url": "https://www.javierforero.com"},
  "creator": {"@type": "Person", "name": "Javier Forero", "url": "https://www.linkedin.com/in/jforero/"},
  "about": ["Copa Mundial de la FIFA 2026", "Inteligencia Artificial", "Ciencia de datos deportiva"]
}
</script>
<style>
@font-face{font-family:'IgraSans';src:url('https://javierforero.com/fonts/IgraSans.woff2') format('woff2');font-display:swap;}
:root{--purple:#4e00ff;--purple-light:#7c4dff;--deep-blue:#041c59;--vibrant-blue:#0048ff;
--bg:#f5f7fb;--white:#fff;--border:#e3e8f5;--soft-lilac:#f6f3ff;--text:#1f2937;--muted:#5f6b7a;
--grad-hero:linear-gradient(135deg,#041c59 0%,#4e00ff 68%,#7c4dff 100%);
--c-claude:#0048ff;--c-chatgpt:#10a37f;--c-gemini:#7c4dff;--c-cons:#4e00ff;
--tip-bg:#0e1430;--track:#f1f3fa;--range:#d8def0;--bartrack:#eef1f8;}
/* ===== tema oscuro ===== */
[data-theme="dark"]{--deep-blue:#cfd9f7;--bg:#0a1020;--white:#121b33;--border:#26324d;
--soft-lilac:#1b2138;--text:#e8edf9;--muted:#9fabc4;--vibrant-blue:#7aa2ff;
--tip-bg:#1b2440;--track:#161d33;--range:#2a3656;--bartrack:#1b2440;}
[data-theme="dark"] .tab,[data-theme="dark"] .card,[data-theme="dark"] .gcard,
[data-theme="dark"] .h2h-sel,[data-theme="dark"] .reachscroll thead th,
[data-theme="dark"] .tk{background:var(--white);}
[data-theme="dark"] .tab{color:var(--deep-blue);}
[data-theme="dark"] .dot{border-color:var(--white);}
[data-theme="dark"] .cidx{background:linear-gradient(135deg,#1a2138,#16203a);}
[data-theme="dark"] .scorechips .s{background:var(--soft-lilac);}
[data-theme="dark"] .mtab td{border-bottom-color:#222c46;}
[data-theme="dark"] .tabs{background:rgba(10,16,32,.92);}
/* ===== barra de controles (idioma + tema) ===== */
.topbar{display:flex;justify-content:flex-end;align-items:center;gap:10px;margin:0 0 14px;}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:999px;overflow:hidden;background:var(--white);}
.seg-btn{border:0;background:transparent;color:var(--muted);font-family:inherit;font-weight:800;
font-size:13px;padding:7px 14px;cursor:pointer;transition:.15s;}
.seg-btn.active{background:var(--purple);color:#fff;}
.icon-btn{border:1px solid var(--border);background:var(--white);border-radius:999px;width:38px;height:34px;
cursor:pointer;font-size:16px;line-height:1;display:inline-flex;align-items:center;justify-content:center;}
.icon-btn:hover{border-color:var(--purple-light);}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);font-family:'IgraSans',Aptos,Helvetica,Arial,sans-serif;color:var(--text);line-height:1.5;}
.wrap{max-width:1120px;margin:0 auto;padding:24px 20px 70px;}
.hero{background:var(--grad-hero);color:#fff;border-radius:28px;padding:38px 42px;}
.hero .eyebrow{font-size:12.5px;letter-spacing:2px;text-transform:uppercase;opacity:.88;margin:0 0 12px;}
.hero h1{margin:0;font-size:36px;line-height:1.1;font-weight:800;}
.hero .sub{margin:14px 0 0;font-size:16.5px;line-height:1.5;opacity:.94;max-width:820px;}
.hero .meta{margin:18px 0 0;font-size:13px;opacity:.9;}
/* tabs */
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 8px;}
.tab{border:1px solid var(--border);background:#fff;color:var(--deep-blue);font-family:inherit;
font-size:14.5px;font-weight:800;padding:11px 20px;border-radius:999px;cursor:pointer;transition:.15s;}
.tab:hover{border-color:var(--purple-light);}
.tab.active{background:var(--purple);color:#fff;border-color:var(--purple);}
.tab .dotc{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px;vertical-align:middle;}
.panel{display:none;} .panel.active{display:block;}
.section-title{color:var(--deep-blue);text-transform:uppercase;letter-spacing:.12em;font-weight:800;
font-size:14px;border-left:4px solid var(--purple);padding-left:12px;margin:34px 0 16px;}
.card{background:#fff;border:1px solid var(--border);border-radius:18px;padding:20px 22px;
box-shadow:0 12px 32px rgba(4,28,89,.06);margin:14px 0;}
.card h3{margin:0 0 10px;color:var(--deep-blue);font-size:17px;font-weight:800;}
.insight{background:var(--soft-lilac);border:1px solid var(--border);border-left:5px solid var(--purple);
border-radius:16px;padding:16px 18px;margin:16px 0;}
.insight p{margin:0;color:var(--deep-blue);font-weight:600;font-size:15px;}
.lead{font-size:16px;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
table{width:100%;border-collapse:collapse;font-size:13px;}
th{text-align:left;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.4px;
padding:8px 7px;border-bottom:2px solid var(--border);font-weight:700;}
td{padding:6px 7px;border-bottom:1px solid var(--border);}
td.tm{font-weight:700;color:var(--deep-blue);} td.hl{font-weight:800;color:var(--purple);}
.barwrap{display:inline-block;height:9px;background:var(--bartrack);border-radius:999px;vertical-align:middle;overflow:hidden;}
.barfill{display:block;height:100%;border-radius:999px;}
.wdl{display:inline-flex;width:118px;height:9px;border-radius:999px;overflow:hidden;vertical-align:middle;}
.wdl span{display:block;height:100%;}
.legend{font-size:11.5px;color:var(--muted);margin:8px 0 0;}
.badge{display:inline-block;background:var(--soft-lilac);color:var(--deep-blue);border:1px solid var(--border);
border-radius:999px;padding:3px 10px;font-size:11px;font-weight:700;margin:2px 4px 2px 0;}
/* champion divergence rows */
.chrow{display:grid;grid-template-columns:130px 1fr 150px;align-items:center;gap:12px;margin:8px 0;}
.chteam{font-weight:700;color:var(--deep-blue);font-size:13.5px;}
.chteam .elo{font-size:10.5px;color:var(--muted);font-weight:600;}
.track{position:relative;height:26px;background:var(--track);border-radius:8px;}
.range{position:absolute;height:6px;top:10px;background:var(--range);border-radius:999px;}
.dot{position:absolute;width:13px;height:13px;border-radius:50%;top:6px;transform:translateX(-50%);border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.2);}
.medmark{position:absolute;width:3px;height:26px;background:var(--purple);top:0;transform:translateX(-50%);border-radius:2px;}
.chnums{font-size:12.5px;text-align:right;}
.chnums .med{font-size:17px;font-weight:800;color:var(--purple);}
.chnums .mn{color:var(--muted);font-size:11px;}
.gcard{background:#fff;border:1px solid var(--border);border-radius:16px;padding:14px 16px;margin:12px 0;box-shadow:0 10px 28px rgba(4,28,89,.05);}
.gh{font-size:16px;font-weight:800;color:var(--deep-blue);margin-bottom:8px;}
.mtab td{font-size:12.5px;padding:5px 7px;border-bottom:1px solid #f0f3fa;}
.mtab .ta{font-weight:700;color:var(--deep-blue);width:30%;} .mtab .tb{font-weight:700;color:var(--deep-blue);text-align:right;width:30%;}
.mtab .sc{text-align:center;font-weight:800;color:var(--purple);width:56px;}
.agree{display:inline-flex;gap:3px;}
.agree i{width:7px;height:7px;border-radius:50%;background:var(--range);display:inline-block;}
.agree i.on{background:var(--vibrant-blue);}
.wdltxt{font-size:10.5px;color:var(--muted);margin-left:7px;}
.dotleg{display:inline-block;width:10px;height:10px;border-radius:50%;margin:0 4px 0 10px;vertical-align:middle;}
/* head to head */
.h2h-sel{width:100%;max-width:480px;padding:11px 14px;border:1px solid var(--border);border-radius:12px;
font-family:inherit;font-size:14.5px;color:var(--deep-blue);font-weight:700;background:#fff;}
.h2h-row{display:grid;grid-template-columns:96px 1fr 64px;align-items:center;gap:12px;margin:10px 0;}
.h2h-row .nm{font-weight:800;font-size:13px;}
.h2h-big{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:6px 0 14px;border-bottom:1px solid var(--border);margin-bottom:14px;}
.h2h-team{font-size:20px;font-weight:800;color:var(--deep-blue);}
.h2h-vs{color:var(--muted);font-weight:700;}
.rich{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px;}
.rich .m{background:var(--soft-lilac);border:1px solid var(--border);border-radius:12px;padding:10px 12px;}
.rich .m .v{font-size:18px;font-weight:800;color:var(--purple);} .rich .m .l{font-size:10.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;margin-top:3px;}
.scorechips{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;}
.scorechips .s{background:#fff;border:1px solid var(--border);border-radius:8px;padding:4px 9px;font-size:12px;font-weight:700;color:var(--deep-blue);}
.scorechips .s em{font-style:normal;color:var(--muted);font-weight:600;margin-left:4px;}
.foot{text-align:center;margin-top:46px;padding-top:18px;border-top:1px solid var(--border);font-size:12.5px;color:var(--muted);}
.foot a{color:var(--vibrant-blue);text-decoration:none;} .foot .dot{color:var(--purple);}
.methclassic{font-size:14px;color:var(--text);} .methclassic b{color:var(--deep-blue);}
.reachscroll{max-height:560px;overflow-y:auto;border:1px solid var(--border);border-radius:12px;}
.reachscroll table{font-size:12.5px;} .reachscroll thead th{position:sticky;top:0;background:#fff;z-index:2;box-shadow:0 1px 0 var(--border);}
.reachscroll tbody tr:nth-child(-n+3) td.tm{color:var(--purple);}
details.meth{margin:10px 0 0;border:1px solid var(--border);border-radius:12px;background:#fbfcff;}
details.meth>summary{cursor:pointer;padding:11px 16px;font-weight:800;color:var(--deep-blue);font-size:13.5px;list-style:none;}
details.meth>summary::-webkit-details-marker{display:none;}
details.meth>summary::before{content:"▸ ";color:var(--purple);}
details.meth[open]>summary::before{content:"▾ ";}
details.meth .methbody{padding:4px 18px 16px;font-size:13.5px;color:var(--text);}
details.meth .methbody p{margin:8px 0;} details.meth .methbody b{color:var(--deep-blue);}
details.meth .methbody pre{background:#0e1430;color:#cdd6f4;border-radius:10px;padding:11px 13px;font-size:11.5px;
overflow-x:auto;line-height:1.45;white-space:pre-wrap;}
details.meth .methbody .methlim{background:var(--soft-lilac);border-left:3px solid var(--purple-light);
border-radius:8px;padding:8px 11px;color:var(--deep-blue);}
.cidx{display:flex;gap:16px;align-items:center;margin-top:14px;background:linear-gradient(135deg,#f3efff,#eef3ff);
border:1px solid var(--border);border-radius:14px;padding:14px 16px;}
.cidx .ring{width:74px;height:74px;border-radius:50%;flex:0 0 auto;display:flex;align-items:center;justify-content:center;
font-weight:900;font-size:22px;color:#fff;}
.cidx .meta{font-size:13px;color:var(--text);} .cidx .meta b{color:var(--deep-blue);}
.cidx .meta .legend{margin-top:5px;}
.cchip{display:inline-block;min-width:30px;text-align:center;border-radius:7px;padding:1px 6px;font-weight:800;
font-size:11px;color:#fff;margin-left:6px;}
.cidx-h{font-size:14px;color:var(--deep-blue);display:flex;align-items:center;}
.cidx-v{font-weight:800;font-size:15px;margin-top:1px;}
.tip{position:relative;display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;
border-radius:50%;background:var(--purple-light);color:#fff;font-size:10px;font-weight:800;font-style:normal;
cursor:help;margin-left:7px;user-select:none;}
.tip::after{content:attr(data-tip);position:absolute;bottom:150%;left:50%;transform:translateX(-50%);
width:265px;max-width:72vw;background:var(--tip-bg);color:#e8ecff;font-size:12px;font-weight:500;line-height:1.5;
padding:10px 12px;border-radius:10px;opacity:0;visibility:hidden;transition:opacity .15s;z-index:60;
box-shadow:0 10px 28px rgba(0,0,0,.28);text-align:left;white-space:normal;pointer-events:none;}
.tip::before{content:"";position:absolute;bottom:150%;left:50%;transform:translate(-50%,98%);border:6px solid transparent;
border-top-color:var(--tip-bg);opacity:0;visibility:hidden;transition:opacity .15s;z-index:61;}
.tip:hover::after,.tip:hover::before{opacity:1;visibility:visible;}
/* ===== UX: banda de veredicto + podio ===== */
.verdict{background:var(--grad-hero);color:#fff;border-radius:24px;padding:26px 28px;margin:8px 0 6px;
box-shadow:0 18px 40px rgba(78,0,255,.18);}
.verdict .vlead{font-size:12px;letter-spacing:2px;text-transform:uppercase;opacity:.85;margin:0 0 6px;font-weight:700;}
.verdict .vmain{font-size:23px;font-weight:800;line-height:1.3;margin:0;}
.verdict .vmain b{color:#ffd84d;}
.podium{display:grid;grid-template-columns:1fr 1.18fr 1fr;gap:14px;align-items:end;margin-top:20px;}
.pod{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:15px 10px;text-align:center;}
.pod .rk{font-size:18px;}
.pod .tm{font-size:16px;font-weight:800;margin:3px 0 1px;}
.pod .pc{font-size:25px;font-weight:900;line-height:1;}
.pod .pl{font-size:11px;opacity:.8;}
.pod.p1{transform:translateY(-12px);background:rgba(255,216,77,.16);border-color:rgba(255,216,77,.55);padding-bottom:24px;}
.pod.p1 .pc{color:#ffd84d;font-size:30px;}
/* ===== UX: tarjetas de hallazgos clave ===== */
.takeaways{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0 6px;}
.tk{background:#fff;border:1px solid var(--border);border-radius:16px;padding:14px 15px;border-top:4px solid var(--purple);
box-shadow:0 10px 26px rgba(4,28,89,.05);}
.tk .lab{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:800;}
.tk .big{font-size:18px;font-weight:900;color:var(--deep-blue);margin:5px 0 2px;line-height:1.15;}
.tk .sub{font-size:12px;color:var(--muted);}
.tk.green{border-top-color:#1a9e5c;} .tk.red{border-top-color:#c0392b;} .tk.blue{border-top-color:var(--bright-blue);}
/* ===== UX: tabs fijas al hacer scroll ===== */
.tabs{position:sticky;top:0;z-index:45;background:rgba(247,248,252,.92);backdrop-filter:blur(8px);
padding:10px 0;border-bottom:1px solid var(--border);}
@media(max-width:760px){.grid2,.grid3,.rich{grid-template-columns:1fr;}.hero h1{font-size:27px;}
.hero{padding:26px 22px;border-radius:22px;} .wrap{padding:14px 13px 60px;}
.chrow{grid-template-columns:96px 1fr 92px;}.h2h-row{grid-template-columns:74px 1fr 56px;}
.takeaways{grid-template-columns:1fr 1fr;} .verdict .vmain{font-size:18px;} .verdict{padding:20px 18px;}
.pod .pc{font-size:21px;} .pod.p1 .pc{font-size:25px;} .pod .tm{font-size:14px;}
.section-title{font-size:12.5px;margin:26px 0 12px;} .card{padding:15px 15px;border-radius:15px;}
.mtab{font-size:11.5px;} .tab{padding:9px 14px;font-size:13px;}
table{font-size:12px;} .reachscroll{max-height:440px;}}
@media(max-width:430px){.takeaways{grid-template-columns:1fr;} .podium{gap:8px;} .pod{padding:11px 6px;}}
</style></head>
<body><div class="wrap">

<div class="topbar">
  <div class="seg" id="langSeg" role="group" aria-label="Idioma / Language">
    <button class="seg-btn active" data-lang="es">ES</button>
    <button class="seg-btn" data-lang="en">EN</button>
  </div>
  <button class="icon-btn" id="themeBtn" aria-label="Cambiar tema claro/oscuro" title="Tema claro/oscuro">🌙</button>
</div>

<div class="hero">
  <p class="eyebrow" data-en="Artificial Intelligence Benchmark · Sports Analytics">Benchmark de Inteligencia Artificial · Sports Analytics</p>
  <h1 data-en="FIFA World Cup 2026 — Three AIs, one consensus">Mundial FIFA 2026 — Tres IAs, un consenso</h1>
  <p class="sub" data-en="A comparison of the <b>v6</b> forecasts from <b>Claude</b> (v4: Dixon-Coles + Machine Learning ensemble, validated on 2018+2022), <b>ChatGPT</b> (v6, historically-calibrated ensemble + weather) and <b>Gemini</b> (v6 Heritage AI: Bayesian + thermodynamic + pedigree) for the 48 teams, the 72 group-stage matches and the road to the title — plus a fourth <b>consensus</b> forecast. Each tab includes the model's full methodology in an expandable panel.">Comparativa de los pronósticos <b>v6</b> de <b>Claude</b> (v4: ensamble Dixon-Coles + Machine Learning, validado 2018+2022),
  <b>ChatGPT</b> (v6, ensamble calibrado histórico + clima) y <b>Gemini</b> (v6 Heritage AI: bayesiano + termodinámico + pedigrí)
  para las 48 selecciones, los 72 partidos de grupos y el camino al título — con un cuarto pronóstico de <b>consenso</b>.
  Cada pestaña incluye la metodología completa del modelo desplegable.</p>
  <p class="meta" data-en="Quantitative analysis · June 2026 · full data from the three tools">Análisis cuantitativo · junio de 2026 · datos completos de las tres herramientas</p>
</div>

<div class="tabs" id="tabs">
  <button class="tab active" data-t="consenso"><span class="dotc" style="background:var(--c-cons)"></span><span data-en="Consensus">Consenso</span></button>
  <button class="tab" data-t="claude"><span class="dotc" style="background:var(--c-claude)"></span>Claude</button>
  <button class="tab" data-t="chatgpt"><span class="dotc" style="background:var(--c-chatgpt)"></span>ChatGPT</button>
  <button class="tab" data-t="gemini"><span class="dotc" style="background:var(--c-gemini)"></span>Gemini</button>
</div>

<div id="consenso" class="panel active"></div>
<div id="claude" class="panel"></div>
<div id="chatgpt" class="panel"></div>
<div id="gemini" class="panel"></div>

<div class="foot">Javier Forero <span class="dot">·</span> <a href="https://javierforero.co">javierforero.co</a><br>
<span style="font-size:11px">Benchmark metodológico de tres IAs. Las probabilidades son estimaciones de modelos, no certezas. Consenso = combinación de las tres herramientas (mediana como cifra principal, media como referencia).</span></div>
</div>

<script>
const DATA = __BLOB__;
const COL = {Claude:'#0048ff', ChatGPT:'#10a37f', Gemini:'#7c4dff', Consenso:'#4e00ff'};
const ELO = DATA.elo || {};
const fmt = x => (x==null?'—':(Math.round(x*10)/10).toFixed(1)+'%');

/* ============ i18n ============ */
let LANG='es';
const TEAM_EN={'Alemania':'Germany','Arabia Saudí':'Saudi Arabia','Argelia':'Algeria','Argentina':'Argentina','Australia':'Australia','Austria':'Austria','Bosnia':'Bosnia & H.','Brasil':'Brazil','Bélgica':'Belgium','Cabo Verde':'Cape Verde','Canadá':'Canada','Chequia':'Czechia','Colombia':'Colombia','Corea del Sur':'South Korea','Costa de Marfil':'Ivory Coast','Croacia':'Croatia','Curazao':'Curaçao','Ecuador':'Ecuador','Egipto':'Egypt','Escocia':'Scotland','España':'Spain','Estados Unidos':'United States','Francia':'France','Ghana':'Ghana','Haití':'Haiti','Inglaterra':'England','Iraq':'Iraq','Irán':'Iran','Japón':'Japan','Jordania':'Jordan','Marruecos':'Morocco','México':'Mexico','Noruega':'Norway','Nueva Zelanda':'New Zealand','Panamá':'Panama','Paraguay':'Paraguay','Países Bajos':'Netherlands','Portugal':'Portugal','Qatar':'Qatar','RD Congo':'DR Congo','Senegal':'Senegal','Sudáfrica':'South Africa','Suecia':'Sweden','Suiza':'Switzerland','Túnez':'Tunisia','Türkiye':'Türkiye','Uruguay':'Uruguay','Uzbekistán':'Uzbekistan'};
function tx(es,en){return LANG==='en'?en:es;}          /* texto UI */
function tn(n){return LANG==='en'?(TEAM_EN[n]||n):n;}   /* nombre de selección (solo para mostrar) */

function bar(p, max, color){
  const w = Math.max(0, Math.min(100, 100*p/max));
  return `<span class="barwrap" style="width:150px"><span class="barfill" style="width:${w.toFixed(1)}%;background:${color}"></span></span>`;
}
function wdlBar(pA,pD,pB){
  return `<span class="wdl"><span style="width:${pA}%;background:#0048ff"></span>`+
         `<span style="width:${pD}%;background:#b9c2d6"></span>`+
         `<span style="width:${pB}%;background:#4e00ff"></span></span>`;
}
function sortByTitle(obj){ return Object.entries(obj).sort((a,b)=>b[1]-a[1]); }

/* ---------- CHAMPION divergence chart (consensus) ---------- */
function champDivergence(){
  const st = DATA.consensus.title_stat;
  const med = DATA.consensus.title_median, mean = DATA.consensus.title;
  const top = Object.entries(med).sort((a,b)=>b[1]-a[1]).slice(0,16);
  const MAX = 24;
  let h = '';
  for(const [t,m] of top){
    const s = st[t]; const cl=DATA.claude.title[t], ch=DATA.chatgpt.title[t], gm=DATA.gemini.title[t];
    const pos = v => (100*v/MAX);
    h += `<div class="chrow">
      <div class="chteam">${tn(t)}<br><span class="elo">Elo ${ELO[t]||'—'}</span></div>
      <div class="track">
        <div class="range" style="left:${pos(s.min)}%;width:${pos(s.max-s.min)}%"></div>
        <div class="medmark" style="left:${pos(m)}%"></div>
        <div class="dot" style="left:${pos(cl)}%;background:${COL.Claude}" title="Claude ${fmt(cl)}"></div>
        <div class="dot" style="left:${pos(ch)}%;background:${COL.ChatGPT}" title="ChatGPT ${fmt(ch)}"></div>
        <div class="dot" style="left:${pos(gm)}%;background:${COL.Gemini}" title="Gemini ${fmt(gm)}"></div>
      </div>
      <div class="chnums"><span class="med">${fmt(m)}</span><br><span class="mn">${tx('media','avg')} ${fmt(mean[t])} · ${s.min}–${s.max}</span></div>
    </div>`;
  }
  return h;
}

/* ---------- reach table ---------- */
function reachTable(reach, teams){
  let h = `<div class="reachscroll"><table><thead><tr><th>${tx('Selección','Team')}</th><th>R32</th><th>${tx('Octavos','R16')}</th><th>${tx('Cuartos','QF')}</th><th>${tx('Semis','SF')}</th><th>${tx('Final','Final')}</th><th>${tx('Campeón','Champion')}</th></tr></thead><tbody>`;
  for(const t of teams){
    const r = k => reach[k] && reach[k][t]!=null ? fmt(reach[k][t]) : '—';
    h += `<tr><td class="tm">${tn(t)}</td><td>${r('R32')}</td><td>${r('R16')}</td><td>${r('QF')}</td><td>${r('SF')}</td><td>${r('FINAL')}</td><td class="hl">${r('CAMPEON')}</td></tr>`;
  }
  return h+'</tbody></table></div>';
}
// las 48 selecciones ordenadas por una tabla de campeón dada
function all48(titleObj){ return Object.entries(titleObj).sort((a,b)=>b[1]-a[1]).map(x=>x[0]); }
// panel desplegable con la metodología completa de una IA
function methPanel(aiKey){
  const m = DATA.meth[aiKey]; if(!m) return '';
  return `<details class="meth"><summary>${tx('Ver metodología y algoritmo completos','View full methodology and algorithm')} · ${(LANG==='en'&&m.title_en)?m.title_en:m.title}</summary><div class="methbody">${(LANG==='en'&&m.html_en)?m.html_en:m.html}</div></details>`;
}

/* ---------- champion bars (per AI) ---------- */
function champBars(title, color){
  const all = sortByTitle(title); const MAX=Math.max(...all.map(x=>x[1]));
  let h='<div class="reachscroll" style="padding:6px 12px">';
  let r=0;
  for(const [t,p] of all){
    r++;
    h += `<div style="display:flex;align-items:center;gap:10px;margin:5px 0">
      <span style="width:26px;color:var(--muted);font-size:11px;text-align:right">${r}</span>
      <span style="width:118px;font-weight:700;color:var(--deep-blue);font-size:12.5px">${tn(t)}</span>
      ${bar(p,MAX,color)}<span style="font-weight:800;color:var(--deep-blue);font-size:12.5px">${fmt(p)}</span></div>`;
  }
  return h+`<div class="legend" style="margin:6px 2px 2px">${tx('Las 48 selecciones, ordenadas por probabilidad de campeón.','All 48 teams, ranked by title probability.')}</div></div>`;
}

/* ---------- group projection (consensus tab) ---------- */
function groupProjection(){
  let h='<div class="grid2">';
  for(const gl of Object.keys(DATA.groups)){
    const row = DATA.group_proj[gl];
    const cons = row.Consenso;
    h += `<div class="gcard"><div class="gh">${tx('Grupo','Group')} ${gl}</div>
      <table class="mtab"><thead><tr><th>#</th><th>${tx('Selección','Team')}</th><th>${tx('Pts esp. (cons.)','Exp. pts (cons.)')}</th><th></th></tr></thead><tbody>`;
    const w = {Claude:row.Claude[0][0],ChatGPT:row.ChatGPT[0][0],Gemini:row.Gemini[0][0]};
    cons.forEach((pair,i)=>{
      const [t,pts]=pair;
      const cls = i<2?'style="background:var(--soft-lilac)"':'';
      h+=`<tr ${cls}><td style="color:var(--muted);font-weight:800">${i+1}</td><td class="ta">${tn(t)}</td><td>${pts}</td><td></td></tr>`;
    });
    const same = (w.Claude===w.ChatGPT)&&(w.ChatGPT===w.Gemini);
    h+=`</tbody></table><div class="legend">${same?(tx('✓ Las 3 IAs coinciden en el 1.º: ','✓ The 3 AIs agree on 1st: ')+'<b>'+tn(w.Claude)+'</b>'):(tx('⚠ Disputa por el 1.º — ','⚠ Dispute for 1st — ')+'Claude: '+tn(w.Claude)+' · ChatGPT: '+tn(w.ChatGPT)+' · Gemini: '+tn(w.Gemini))}</div></div>`;
  }
  return h+'</div>';
}

/* ---------- match table per AI ---------- */
function matchTableByAI(matches, showXg){
  // matches: array {a,b,pA,pD,pB,score,(xa,xb)} ; agrupar por DATA.groups
  const byKey={}; matches.forEach(m=>byKey[[m.a,m.b].sort().join('|')]=m);
  let h='<div class="grid2">';
  for(const gl of Object.keys(DATA.groups)){
    const teams=DATA.groups[gl]; h+=`<div class="gcard"><div class="gh">${tx('Grupo','Group')} ${gl}</div><table class="mtab"><tbody>`;
    for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
      const key=[teams[i],teams[j]].sort().join('|'); const m=byKey[key]; if(!m)continue;
      const xg = (showXg && m.xa!=null) ? `<span class="wdltxt" style="margin-left:0">xG ${m.xa}–${m.xb}</span>` : '';
      h+=`<tr><td class="ta">${tn(m.a)}</td><td class="sc">${m.score}</td><td class="tb">${tn(m.b)}</td>
        <td>${wdlBar(m.pA,m.pD,m.pB)}<span class="wdltxt">${Math.round(m.pA)}·${Math.round(m.pD)}·${Math.round(m.pB)}</span>${xg?'<br>'+xg:''}</td></tr>`;
    }
    h+='</tbody></table></div>';
  }
  return h+'</div>';
}

/* ---------- consensus match table with agreement ---------- */
function consensusMatchTable(){
  const byKey={}; DATA.consensus.matches.forEach(m=>byKey[[m.a,m.b].sort().join('|')]=m);
  let h='<div class="grid2">';
  for(const gl of Object.keys(DATA.groups)){
    const teams=DATA.groups[gl]; h+=`<div class="gcard"><div class="gh">${tx('Grupo','Group')} ${gl}</div><table class="mtab"><tbody>`;
    for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
      const key=[teams[i],teams[j]].sort().join('|'); const m=byKey[key]; if(!m)continue;
      const dots=`<span class="agree"><i class="${m.agree>=1?'on':''}"></i><i class="${m.agree>=2?'on':''}"></i><i class="${m.agree>=3?'on':''}"></i></span>`;
      const ci=m.conf_idx, ccol = ci>=75?'#1a9e5c':(ci>=55?'#0048ff':(ci>=45?'#b58900':'#c0392b'));
      const chip=`<span class="cchip" style="background:${ccol}" title="${tx('Confianza del pronóstico (0–100)','Forecast confidence (0–100)')}">${ci}</span>`;
      h+=`<tr><td class="ta">${tn(m.a)}</td><td class="sc">${m.score}</td><td class="tb">${tn(m.b)}</td>
        <td>${wdlBar(m.pA,m.pD,m.pB)} ${dots}${chip}</td></tr>`;
    }
    h+='</tbody></table></div>';
  }
  return h+'</div>';
}

/* ---------- HEAD TO HEAD ---------- */
function h2hOptions(){
  let opts=''; 
  DATA.consensus.matches.forEach((m,idx)=>{ opts+=`<option value="${idx}">${m.group} · ${tn(m.a)} vs ${tn(m.b)}</option>`; });
  return opts;
}
function renderH2H(idx){
  const m = DATA.consensus.matches[idx];
  const claudeRich = DATA.claude.fixtures.find(f=>(f.a===m.a&&f.b===m.b)||(f.a===m.b&&f.b===m.a));
  let rows='';
  for(const ai of ['Claude','ChatGPT','Gemini']){
    const r=m.by[ai];
    rows+=`<div class="h2h-row"><span class="nm" style="color:${COL[ai]}">${ai}</span>
      <span>${wdlBar(r.pA,r.pD,r.pB)}<span class="wdltxt">${r.pA}% · ${r.pD}% · ${r.pB}%</span></span>
      <span style="font-weight:800;color:var(--purple);text-align:right">${r.score}</span></div>`;
  }
  rows+=`<div class="h2h-row" style="border-top:1px solid var(--border);padding-top:10px;margin-top:6px">
    <span class="nm" style="color:var(--c-cons)">${tx('Consenso','Consensus')}</span>
    <span>${wdlBar(m.pA,m.pD,m.pB)}<span class="wdltxt">${m.pA}% · ${m.pD}% · ${m.pB}%</span></span>
    <span style="font-weight:800;color:var(--purple);text-align:right">${m.score}</span></div>`;
  const agreeTxt = m.agree===3?tx('Las 3 IAs coinciden en el favorito','All 3 AIs agree on the favorite'):(m.agree===2?tx('2 de 3 coinciden en el favorito','2 of 3 agree on the favorite'):tx('Las 3 difieren en el favorito','The 3 AIs differ on the favorite'));
  // nota si el marcador de consenso es empate pero la barra inclina a un equipo
  const hg=parseInt(m.score.split('-')[0]), ag=parseInt(m.score.split('-')[1]);
  const favWin = (m.pA>m.pD && m.pA>=m.pB) || (m.pB>m.pD && m.pB>=m.pA);
  const drawNote = (hg===ag && favWin) ? tx(` El marcador de consenso (${m.score}) es el resultado exacto más probable (voto mayoritario de las 3 IAs); la barra muestra que un equipo es ligero favorito a ganar — son métricas distintas.`,` The consensus scoreline (${m.score}) is the single most likely exact result (majority vote of the 3 AIs); the bar shows one team is a slight favorite to win — these are different metrics.`) : '';
  // goles esperados por IA (Claude y Gemini v2 los publican)
  let xgline='';
  if(m.xg && m.xg.Claude){
    xgline=`<div class="legend" style="margin-top:10px">${tx('Goles esperados (xG)','Expected goals (xG)')} — <b style="color:${COL.Claude}">Claude</b> ${m.xg.Claude[0]}–${m.xg.Claude[1]} &nbsp;·&nbsp; <span style="color:var(--muted)">${tx('ChatGPT v5 y Gemini v5 publican marcador modal y 1·X·2, sin xG','ChatGPT v5 and Gemini v5 publish modal scoreline and 1·X·2, no xG')}</span></div>`;
  }
  let rich='';
  if(claudeRich){
    const f=claudeRich;
    const chips = f.top_scores.map(s=>`<span class="s">${s[0]}<em>${s[1]}%</em></span>`).join('');
    rich = `<div style="margin-top:14px"><div class="legend" style="margin-bottom:6px"><b>${tx('Detalle distribucional de Claude','Claude distributional detail')}</b> ${tx('(motor Dixon-Coles): marcadores más probables','(Dixon-Coles engine): most likely scorelines')}</div>
      <div class="scorechips">${chips}</div>
      <div class="rich">
        <div class="m"><div class="v">${f.over25}%</div><div class="l">${tx('+2.5 goles','Over 2.5 goals')}</div></div>
        <div class="m"><div class="v">${f.btts}%</div><div class="l">${tx('Ambos marcan','Both teams score')}</div></div>
        <div class="m"><div class="v">${f.conf}%</div><div class="l">${tx('Confianza (entropía)','Confidence (entropy)')}</div></div>
        <div class="m"><div class="v">${f.cs_a}%</div><div class="l">${tx('Portería 0','Clean sheet')} · ${tn(f.a)}</div></div>
        <div class="m"><div class="v">${f.cs_b}%</div><div class="l">${tx('Portería 0','Clean sheet')} · ${tn(f.b)}</div></div>
        <div class="m"><div class="v">${f.xpts_a}/${f.xpts_b}</div><div class="l">${tx('Puntos esperados','Expected points')}</div></div>
      </div></div>`;
  }
  // índice de consenso: cifra + veredicto en lenguaje claro; teoría en tooltip
  const ci=m.conf_idx, col = ci>=75?'#1a9e5c':(ci>=55?'#0048ff':(ci>=45?'#b58900':'#c0392b'));
  const verdict = ci>=75?tx('Favorito claro · las 3 IAs coinciden','Clear favorite · all 3 AIs agree'):(ci>=55?tx('Favorito moderado','Moderate favorite'):(ci>=45?tx('Partido parejo','Close match'):tx('Muy parejo · difícil de predecir','Very close · hard to call')));
  const favName = (m.pA>=m.pD&&m.pA>=m.pB)?m.a:((m.pB>=m.pD&&m.pB>=m.pA)?m.b:null);
  const favLine = favName?`${tx('Favorito del consenso','Consensus favorite')}: <b>${tn(favName)}</b> (${Math.round(Math.max(m.pA,m.pB))}%)`:tx('El empate es el resultado más probable','A draw is the most likely result');
  const tipTxt = tx(`Resume en una cifra cuán claro y consensuado es el resultado. Combina la fuerza del favorito con el acuerdo entre las 3 IAs — acuerdo ${m.agree_idx}/100; probabilidades combinadas (pool logarítmico) ${m.p_log[0]}% · ${m.p_log[1]}% · ${m.p_log[2]}%. Más alto = más claro y consensuado; más bajo = parejo o disputado.`,`A single figure for how clear and agreed the result is. It combines the favorite's strength with the agreement among the 3 AIs — agreement ${m.agree_idx}/100; combined probabilities (logarithmic pool) ${m.p_log[0]}% · ${m.p_log[1]}% · ${m.p_log[2]}%. Higher = clearer and more agreed; lower = close or disputed.`);
  const cidx=`<div class="cidx"><div class="ring" style="background:${col}">${ci}</div>
    <div class="meta">
      <div class="cidx-h">${tx('Confianza del pronóstico','Forecast confidence')}: <b style="margin-left:4px">${ci}/100</b><span class="tip" data-tip="${tipTxt}">i</span></div>
      <div class="cidx-v" style="color:${col}">${verdict}</div>
      <div class="legend" style="margin-top:2px">${favLine}</div>
    </div></div>`;
  document.getElementById('h2h-out').innerHTML =
    `<div class="h2h-big"><span class="h2h-team">${tn(m.a)}</span><span class="h2h-vs">vs</span><span class="h2h-team">${tn(m.b)}</span></div>
     ${rows}<div class="insight" style="margin-top:14px"><p>${agreeTxt}. ${tx(`Barra: azul gana ${tn(m.a)} · gris empate · morado gana ${tn(m.b)}.`,`Bar: blue = ${tn(m.a)} wins · grey = draw · purple = ${tn(m.b)} wins.`)}${drawNote}</p></div>${cidx}${xgline}${rich}`;
}

/* ============ RENDER PANELS ============ */
function consensusVerdict(){
  const c=DATA.consensus;
  const top=Object.entries(c.title_median).sort((a,b)=>b[1]-a[1]).slice(0,3);
  const t1=top[0],t2=top[1],t3=top[2];
  // ¿cuán abierto? nº de selecciones con ≥5% de título
  const contenders=Object.values(c.title_median).filter(v=>v>=5).length;
  const verdict=tx(`Las tres IAs coinciden: <b>${tn(t1[0])}</b> es la favorita al título (${fmt(t1[1])}), por delante de ${tn(t2[0])} y ${tn(t3[0])} — pero es un Mundial <b>muy abierto</b>, con ${contenders} selecciones en pelea real por la copa.`,`The three AIs agree: <b>${tn(t1[0])}</b> is the title favorite (${fmt(t1[1])}), ahead of ${tn(t2[0])} and ${tn(t3[0])} — but it is a <b>wide-open</b> World Cup, with ${contenders} teams in genuine contention for the trophy.`);
  const pod=(rk,t,cls)=>`<div class="pod ${cls}"><div class="rk">${rk}</div><div class="tm">${tn(t[0])}</div><div class="pc">${fmt(t[1])}</div><div class="pl">${tx('campeón','champion')}</div></div>`;
  return `<div class="verdict">
    <p class="vlead">${tx('El veredicto del consenso · Mundial 2026','The consensus verdict · World Cup 2026')}</p>
    <p class="vmain">${verdict}</p>
    <div class="podium">${pod(tx('2.º','2nd'),t2,'p2')}${pod(tx('1.º','1st'),t1,'p1')}${pod(tx('3.º','3rd'),t3,'p3')}</div>
  </div>`;
}
function keyTakeaways(){
  const c=DATA.consensus;
  const fav=Object.entries(c.title_median).sort((a,b)=>b[1]-a[1])[0];
  let dis=null;
  for(const t in c.title_stat){ const s=c.title_stat[t];
    if(s.median<3) continue; const sp=s.max-s.min;
    if(!dis||sp>dis.sp) dis={t,sp,min:s.min,max:s.max};
  }
  let safe=null,coin=null;
  for(const m of c.matches){
    if(!safe||m.conf_idx>safe.conf_idx) safe=m;
    if(!coin||m.conf_idx<coin.conf_idx) coin=m;
  }
  return `<div class="takeaways">
    <div class="tk blue"><div class="lab">${tx('Favorito del consenso','Consensus favorite')}</div><div class="big">${tn(fav[0])}</div><div class="sub">${fmt(fav[1])} ${tx('de probabilidad de título','title probability')}</div></div>
    <div class="tk"><div class="lab">${tx('Mayor desacuerdo entre IAs','Biggest disagreement between AIs')}</div><div class="big">${tn(dis.t)}</div><div class="sub">${tx('entre','between')} ${fmt(dis.min)} ${tx('y','and')} ${fmt(dis.max)} ${tx('según el modelo','depending on the model')}</div></div>
    <div class="tk green"><div class="lab">${tx('Pronóstico más seguro','Safest forecast')}</div><div class="big">${tn(safe.a)} vs ${tn(safe.b)}</div><div class="sub">${tx('confianza','confidence')} ${safe.conf_idx}/100 · ${tx('marcador','score')} ${safe.score}</div></div>
    <div class="tk red"><div class="lab">${tx('El gran volado','The big coin-flip')}</div><div class="big">${tn(coin.a)} vs ${tn(coin.b)}</div><div class="sub">${tx('confianza','confidence')} ${coin.conf_idx}/100 · ${tx('parejísimo','razor-thin')}</div></div>
  </div>`;
}
function renderConsenso(){
  const c=DATA.consensus;
  const champTop = Object.entries(c.title_median).sort((a,b)=>b[1]-a[1]).slice(0,12).map(x=>x[0]);
  const el=document.getElementById('consenso');
  el.innerHTML = `
  ${consensusVerdict()}
  ${keyTakeaways()}

  <div class="section-title">${tx('Probabilidad de campeón — las 3 IAs y el consenso','Champion probability — the 3 AIs and the consensus')}</div>
  <div class="card">
    <div class="legend" style="margin-bottom:10px">
      <span class="dotleg" style="background:var(--c-claude)"></span>Claude
      <span class="dotleg" style="background:var(--c-chatgpt)"></span>ChatGPT
      <span class="dotleg" style="background:var(--c-gemini)"></span>Gemini
      <span style="margin-left:14px">${tx('línea morada vertical = <b>mediana de consenso</b> · barra gris = rango entre IAs','purple vertical line = <b>consensus median</b> · grey bar = range across AIs')}</span>
    </div>
    ${champDivergence()}
  </div>
  <div class="insight"><p>${tx(`Por qué difieren: las filosofías se equilibran. <b>Gemini</b> premia el <b>pedigrí histórico</b> (sube a Argentina, Francia y Brasil); <b>ChatGPT</b> aplica <b>calibración histórica</b> y encabeza con España; y <b>Claude</b> —ensamble estadístico + machine learning, el único <b>validado contra Mundiales reales</b>— combina ataque/defensa con Elo, forma e histórico, realzando a Brasil, Inglaterra y Colombia. La mediana sintetiza las tres y modera los extremos.`,`Why they differ: the philosophies balance out. <b>Gemini</b> rewards <b>historical pedigree</b> (lifting Argentina, France and Brazil); <b>ChatGPT</b> applies <b>historical calibration</b> and leads with Spain; and <b>Claude</b> —a statistical + machine-learning ensemble, the only one <b>validated against real World Cups</b>— combines attack/defense with Elo, form and history, raising Brazil, England and Colombia. The median synthesizes all three and tempers the extremes.`)}</p></div>

  <div class="section-title">${tx('Comparador cara a cara — partido por partido','Head-to-head comparator — match by match')}</div>
  <div class="card">
    <p class="legend" style="margin-bottom:10px">${tx('Elige cualquiera de los 72 partidos y compara cómo lo ve cada IA y el consenso. Cada partido trae su <b>confianza del pronóstico</b> en lenguaje claro.','Pick any of the 72 matches and compare how each AI and the consensus see it. Every match shows its <b>forecast confidence</b> in plain language.')}</p>
    <select class="h2h-sel" id="h2h-sel" onchange="renderH2H(this.value)">${h2hOptions()}</select>
    <div id="h2h-out" style="margin-top:18px"></div>
  </div>

  <div class="section-title">${tx('Los 72 partidos — consenso y confianza','The 72 matches — consensus and confidence')}</div>
  <p class="legend" style="margin-bottom:6px">${tx(`El <b>chip de color</b> resume la confianza del pronóstico: verde = favorito claro y las IAs de acuerdo · azul = favorito moderado · ámbar = parejo · rojo = muy parejo. Los tres puntos: en cuántas IAs coincide el favorito. En partidos muy parejos el marcador de consenso puede ser 1-1 aunque la barra incline a un equipo (la barra es quién gana; el marcador es el resultado exacto más probable).`,`The <b>colored chip</b> sums up forecast confidence: green = clear favorite and AIs agree · blue = moderate favorite · amber = close · red = very close. The three dots: how many AIs agree on the favorite. In very tight matches the consensus score can be 1-1 even if the bar leans to one team (the bar is who wins; the score is the single most likely exact result).`)}</p>
  ${consensusMatchTable()}

  <div class="section-title">${tx('Proyección de grupos — quién pasa','Group projection — who advances')}</div>
  ${groupProjection()}

  <div class="section-title">${tx('Camino al título — las 48 selecciones','Road to the title — all 48 teams')}</div>
  <div class="card">${reachTable(c.reach, all48(c.title_median))}
  <p class="legend">${tx('Probabilidad media de las tres IAs de alcanzar cada ronda, de Treintaidosavos a Campeón.','Average probability across the three AIs of reaching each round, from the Round of 32 to Champion.')}</p></div>

  <div class="section-title">${tx('Cómo se construye el consenso','How the consensus is built')}</div>
  <p class="lead">${tx(`Combina las versiones más avanzadas de las tres IAs. Para el título usa la <b>mediana</b> de las tres (robusta a un modelo atípico); para los grupos, puntos esperados de los 72 partidos; y para cada partido, el promedio de probabilidades con el marcador por mayoría. El <b>índice de confianza</b> de cada partido aparece explicado al pasar el cursor sobre su cifra.`,`It combines the most advanced versions of the three AIs. For the title it uses the <b>median</b> of the three (robust to an outlier model); for the groups, expected points from the 72 matches; and for each match, the average of the probabilities with a majority-vote scoreline. The <b>confidence index</b> for each match is explained on hover over its figure.`)}</p>`;
  renderH2H(0);
}

function renderClaude(){
  const d=DATA.claude;
  const champTop=sortByTitle(d.title).slice(0,16).map(x=>x[0]);
  document.getElementById('claude').innerHTML = `
  <div class="section-title">${tx('Metodología','Methodology')} · Claude <span style="color:var(--c-claude)">v4</span></div>
  <div class="card methclassic">
    <p>${tx(`Motor de <b>ensamble</b> que promedia un <b>Dixon-Coles data-driven</b> (ataque/defensa por equipo estimados de miles de partidos reales) con un <b>modelo de Machine Learning</b> (gradient boosting con pérdida de Poisson) que integra <b>Elo actual a junio-2026, forma reciente e histórico de Mundiales</b>. El ensamble es el que mejor valida.`,`An <b>ensemble</b> engine that averages a <b>data-driven Dixon-Coles</b> model (per-team attack/defense estimated from thousands of real matches) with a <b>Machine Learning model</b> (gradient boosting with Poisson loss) integrating <b>current Elo as of June 2026, recent form and World Cup history</b>. The ensemble validates best.`)}</p>
    <p>${tx(`Es la <b>única de las cuatro IAs con desempeño medido fuera de muestra contra los Mundiales 2018 y 2022 reales</b>: RPS 0.2122 vs 0.245 (azar), <b>mejora del 13.3%</b> — superior al ML solo (12.7%) y al Dixon-Coles solo (13.1%).`,`It is the <b>only one of the four AIs with out-of-sample performance measured against the real 2018 and 2022 World Cups</b>: RPS 0.2122 vs 0.245 (chance), a <b>13.3% improvement</b> — better than ML alone (12.7%) and Dixon-Coles alone (13.1%).`)}</p>
    <div style="margin-top:8px">
      <span class="badge">${tx('Ensamble Dixon-Coles + Machine Learning','Dixon-Coles + Machine Learning ensemble')}</span><span class="badge">${tx('Elo · forma · histórico Mundiales','Elo · form · World Cup history')}</span>
      <span class="badge">${tx('Validado OOS 2018+2022','Validated OOS 2018+2022')}</span><span class="badge">${tx('Distribución completa por partido','Full per-match distribution')}</span>
    </div>
  </div>
  <div class="insight"><p>${tx(`Honestidad metodológica: probé el ML solo y resultó <b>algo peor</b> que el modelo estadístico; "deep learning" no es automáticamente mejor con datos escasos. El ensamble de ambos sí gana. El resultado: España (${fmt(d.title['España'])}) y un top plano con <b>Brasil (${fmt(d.title['Brasil'])}), Inglaterra (${fmt(d.title['Inglaterra'])}) y Colombia (${fmt(d.title['Colombia'])})</b> realzados por datos. Además es la única IA que reporta la distribución completa por partido.`,`Methodological honesty: I tested ML alone and it came out <b>slightly worse</b> than the statistical model; "deep learning" is not automatically better with scarce data. The ensemble of the two does win. The result: Spain (${fmt(d.title['España'])}) and a flat top tier with <b>Brazil (${fmt(d.title['Brasil'])}), England (${fmt(d.title['Inglaterra'])}) and Colombia (${fmt(d.title['Colombia'])})</b> lifted by the data. It is also the only AI that reports the full per-match distribution.`)}</p></div>

  ${methPanel("claude")}
  <div class="section-title">${tx('Probabilidad de campeón · Claude','Champion probability · Claude')}</div>
  <div class="card">${champBars(d.title, COL.Claude)}</div>

  <div class="section-title">${tx('Camino al título · Claude · las 48 selecciones','Road to the title · Claude · all 48 teams')}</div>
  <div class="card">${reachTable(d.reach, all48(d.title))}</div>

  <div class="section-title">${tx('Los 72 partidos · Claude v4 (distribución completa por partido)','The 72 matches · Claude v4 (full per-match distribution)')}</div>
  ${matchTableByAI(d.fixtures.map(f=>({a:f.a,b:f.b,pA:f.pA,pD:f.pD,pB:f.pB,score:f.score})))}`;
}

function renderChatGPT(){
  const d=DATA.chatgpt;
  const champTop=sortByTitle(d.title).slice(0,16).map(x=>x[0]);
  document.getElementById('chatgpt').innerHTML = `
  <div class="section-title">${tx('Metodología','Methodology')} · ChatGPT <span style="color:var(--c-chatgpt)">v6</span></div>
  <div class="card methclassic">
    <p>${tx(`Ensamble <b>calibrado histórico + team-level + player-level + climate-aware</b>. Sobre la fuerza estructural (FIFA-Elo, World Football Elo, talento de plantilla, lectura player-level, forma, clima/altitud, ruta y localía) añade una capa de <b>calibración histórica</b> que aplica <b>shrinkage de favoritos</b>, penaliza rutas difíciles y regulariza el título para que ningún equipo reciba una probabilidad irreal. 60.000–80.000 corridas Monte Carlo.`,`A <b>historically-calibrated + team-level + player-level + climate-aware</b> ensemble. On top of structural strength (FIFA-Elo, World Football Elo, squad talent, player-level reading, form, climate/altitude, route and home advantage) it adds a <b>historical-calibration</b> layer that applies <b>favorite shrinkage</b>, penalizes hard routes and regularizes the title so no team gets an unrealistic probability. 60,000–80,000 Monte Carlo runs.`)}</p>
    <div style="margin-top:8px"><span class="badge">${tx('Calibración histórica','Historical calibration')}</span><span class="badge">${tx('Shrinkage de favoritos','Favorite shrinkage')}</span><span class="badge">${tx('Ajuste climático por sede','Per-venue climate adjustment')}</span><span class="badge">60k–80k Monte Carlo</span></div>
  </div>
  <div class="insight"><p>${tx(`Rasgo de la v6: es la IA <b>mejor calibrada y más prudente en la cúspide</b> — contiene a España en ${fmt(d.title['España'])} y reparte hacia el bloque perseguidor (Francia ${fmt(d.title['Francia'])}, Inglaterra ${fmt(d.title['Inglaterra'])}, Argentina ${fmt(d.title['Argentina'])}). Encabeza con España, muy cerca de Claude.`,`v6 trait: the <b>best-calibrated and most prudent at the top</b> — it caps Spain at ${fmt(d.title['España'])} and spreads probability to the chasing pack (France ${fmt(d.title['Francia'])}, England ${fmt(d.title['Inglaterra'])}, Argentina ${fmt(d.title['Argentina'])}). It leads with Spain, very close to Claude.`)}</p></div>

  ${methPanel("chatgpt")}
  <div class="section-title">${tx('Probabilidad de campeón · ChatGPT','Champion probability · ChatGPT')}</div>
  <div class="card">${champBars(d.title, COL.ChatGPT)}</div>

  <div class="section-title">${tx('Camino al título · ChatGPT · las 48 selecciones','Road to the title · ChatGPT · all 48 teams')}</div>
  <div class="card">${reachTable(d.reach, all48(d.title))}</div>

  <div class="section-title">${tx('Los 72 partidos · ChatGPT v6 (con ajuste climático)','The 72 matches · ChatGPT v6 (with climate adjustment)')}</div>
  ${matchTableByAI(d.matches)}`;
}

function renderGemini(){
  const d=DATA.gemini;
  const champTop=sortByTitle(d.title).slice(0,16).map(x=>x[0]);
  document.getElementById('gemini').innerHTML = `
  <div class="section-title">${tx('Metodología','Methodology')} · Gemini <span style="color:var(--c-gemini)">v6 · Heritage AI</span></div>
  <div class="card methclassic">
    <p>${tx(`Ensamble híbrido (<b>redes bayesianas + termodinámica + motor DRL</b>) más tres capas <b>psico-históricas</b>: Prior Bayesiano de Pedigrí Mundialista, Índice de Elasticidad Cognitiva bajo presión y Efecto de Gravedad Táctica. Las ecuaciones inyectan un multiplicador de <b>resiliencia histórica</b> (γ_heritage) sobre el xG térmico antes del motor de Poisson. Publica tabla completa de ronda por ronda.`,`A hybrid ensemble (<b>Bayesian networks + thermodynamics + DRL engine</b>) plus three <b>psycho-historical</b> layers: a Bayesian World Cup Pedigree Prior, a Cognitive Elasticity Index under pressure and a Tactical Gravity Effect. The equations inject a <b>historical-resilience</b> multiplier (γ_heritage) onto the thermal xG before the Poisson engine. It publishes a full round-by-round table.`)}</p>
    <div style="margin-top:8px"><span class="badge">${tx('Heritage AI (pedigrí histórico)','Heritage AI (historical pedigree)')}</span><span class="badge">${tx('Redes bayesianas + DRL','Bayesian networks + DRL')}</span><span class="badge">${tx('Motor bio-termodinámico UTCI','UTCI bio-thermodynamic engine')}</span><span class="badge">${tx('Elasticidad cognitiva','Cognitive elasticity')}</span></div>
  </div>
  <div class="insight"><p>${tx(`Rasgo distintivo de la v6: el <b>prior histórico premia a las potencias tradicionales</b>. Corona a Argentina (${fmt(d.title['Argentina'])}) y Francia (${fmt(d.title['Francia'])}) y <b>sube a Brasil al podio</b> (${fmt(d.title['Brasil'])}) por su pedigrí, dejando a España cuarta (${fmt(d.title['España'])}). La propia Gemini advierte que esto puede ser "regresión al romanticismo" e infravalorar a emergentes tecnificados.`,`v6 hallmark: the <b>historical prior rewards the traditional powers</b>. It crowns Argentina (${fmt(d.title['Argentina'])}) and France (${fmt(d.title['Francia'])}) and <b>lifts Brazil onto the podium</b> (${fmt(d.title['Brasil'])}) for its pedigree, leaving Spain fourth (${fmt(d.title['España'])}). Gemini itself warns this may be a "regression to romanticism" that undervalues technically strong emerging sides.`)}</p></div>

  ${methPanel("gemini")}
  <div class="section-title">${tx('Probabilidad de campeón · Gemini','Champion probability · Gemini')}</div>
  <div class="card">${champBars(d.title, COL.Gemini)}</div>

  <div class="section-title">${tx('Camino al título · Gemini · las 48 selecciones','Road to the title · Gemini · all 48 teams')}</div>
  <div class="card">${reachTable(d.reach, all48(d.title))}</div>

  <div class="section-title">${tx('Los 72 partidos · Gemini v6 (Heritage AI + bio-termodinámico)','The 72 matches · Gemini v6 (Heritage AI + bio-thermodynamic)')}</div>
  ${matchTableByAI(d.matches)}`;
}

/* ============ TABS ============ */
document.getElementById('tabs').addEventListener('click', e=>{
  const b=e.target.closest('.tab'); if(!b)return;
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(x=>x.classList.remove('active'));
  b.classList.add('active'); document.getElementById(b.dataset.t).classList.add('active');
});

/* ============ IDIOMA + TEMA ============ */
function applyLang(lang){
  LANG=lang; document.documentElement.lang=lang;
  document.querySelectorAll('[data-en]').forEach(el=>{
    if(el._es===undefined) el._es=el.innerHTML;
    el.innerHTML = lang==='en' ? el.getAttribute('data-en') : el._es;
  });
  document.querySelectorAll('#langSeg .seg-btn').forEach(b=>b.classList.toggle('active', b.dataset.lang===lang));
  renderConsenso(); renderClaude(); renderChatGPT(); renderGemini();
  try{localStorage.setItem('jf_lang',lang)}catch(e){}
}
document.querySelectorAll('#langSeg .seg-btn').forEach(b=>b.addEventListener('click',()=>applyLang(b.dataset.lang)));

function applyTheme(t){
  document.documentElement.setAttribute('data-theme',t);
  const btn=document.getElementById('themeBtn');
  btn.textContent = t==='dark'?'☀️':'🌙'; btn.setAttribute('aria-pressed', t==='dark');
  try{localStorage.setItem('jf_theme',t)}catch(e){}
}
const savedTheme=(function(){try{return localStorage.getItem('jf_theme')}catch(e){return null}})()||((window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light');
applyTheme(savedTheme);
document.getElementById('themeBtn').addEventListener('click',()=>{applyTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark');});

const savedLang=(function(){try{return localStorage.getItem('jf_lang')}catch(e){return null}})()||'es';
applyLang(savedLang);
</script>
</body></html>"""

HTML = HTML.replace("__BLOB__", BLOB)
open("/home/claude/wc2026/Benchmark_IA_Mundial2026.html","w",encoding="utf-8").write(HTML)
print("Generado:", len(HTML), "bytes")
