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
@font-face{font-family:'IgraSans';src:url('IgraSans.woff2') format('woff2'),url('https://javierforero.com/fonts/IgraSans.woff2') format('woff2');font-display:swap;}
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
/* ===== pie de página ===== */
.footer{background:var(--grad-hero);color:#fff;padding:28px 20px;text-align:center;font-size:13.5px;margin-top:40px;border-radius:28px 28px 0 0;}
.footer a{color:#ffd84d;text-decoration:none;font-weight:700;} .footer a:hover{text-decoration:underline;}
.footer .f-sub{opacity:.72;font-size:12px;margin-top:6px;}
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
body{margin:0;background:var(--bg);font-family:'IgraSans',Aptos,Helvetica,Arial,sans-serif;color:var(--text);line-height:1.5;
transition:background .3s,color .3s;}
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
box-shadow:0 12px 32px rgba(4,28,89,.06);margin:14px 0;transition:background .3s,border-color .3s,transform .2s,box-shadow .2s;}
.card:hover{transform:translateY(-2px);box-shadow:0 16px 40px rgba(4,28,89,.10);}
.card h3{margin:0 0 10px;color:var(--deep-blue);font-size:17px;font-weight:800;}
.insight{background:var(--soft-lilac);border:1px solid var(--border);border-left:5px solid var(--purple);
border-radius:16px;padding:16px 18px;margin:16px 0;transition:background .3s,border-color .3s;}
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
.gcard{background:#fff;border:1px solid var(--border);border-radius:16px;padding:14px 16px;margin:12px 0;box-shadow:0 10px 28px rgba(4,28,89,.05);transition:background .3s,border-color .3s,transform .2s,box-shadow .2s;}
.gcard:hover{transform:translateY(-2px);box-shadow:0 14px 34px rgba(4,28,89,.09);}
.gh{font-size:16px;font-weight:800;color:var(--deep-blue);margin-bottom:8px;}
.mtab td{font-size:12.5px;padding:5px 7px;border-bottom:1px solid #f0f3fa;}
.mtab tbody tr:nth-child(even) td{background:var(--soft-lilac);}
.mtab .ta{font-weight:700;color:var(--deep-blue);width:30%;} .mtab .tb{font-weight:700;color:var(--deep-blue);text-align:right;width:30%;}
.mtab .sc{text-align:center;font-weight:800;color:var(--purple);width:56px;}
.agree{display:inline-flex;gap:3px;}
.agree i{width:7px;height:7px;border-radius:50%;background:var(--range);display:inline-block;}
.agree i.on{background:var(--vibrant-blue);}
.wdltxt{font-size:10.5px;color:var(--muted);margin-left:7px;}
.note{font-size:13px;color:var(--muted);line-height:1.5;margin:-2px 0 12px;max-width:820px;}
/* jornada oficial (separador en tabla de partidos) */
.md-sep td{border:none!important;padding:6px 0 2px!important;}
.md-label{font-size:11px;font-weight:700;color:var(--muted);letter-spacing:.3px;text-transform:uppercase;}
/* colores de clasificación en la proyección de grupos */
.grp-q{background:var(--soft-lilac);}
.grp-3rd{background:#fff8e1;}
.grp-out{opacity:.55;}
/* ===== Bota de Oro · goleadores ===== */
.scorers{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px;}
.sk{display:grid;grid-template-columns:30px 1fr auto;align-items:center;gap:12px;padding:10px 14px;
border:1px solid var(--border);border-radius:14px;background:var(--card);transition:transform .15s,box-shadow .15s;}
.sk:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(78,0,255,.10);}
.sk-rank{font-weight:800;font-size:16px;color:var(--purple);text-align:center;}
.sk-rank.gold{color:#d4a017;}.sk-rank.sil{color:#9aa3b2;}.sk-rank.bro{color:#b06a3b;}
.sk-main{min-width:0;}
.sk-name{font-weight:700;color:var(--deep-blue);font-size:15px;}
.sk-team{font-size:12.5px;color:var(--muted);margin-left:2px;}
.sk-bar{height:7px;border-radius:5px;background:var(--soft-lilac);margin-top:6px;overflow:hidden;}
.sk-bar>span{display:block;height:100%;border-radius:5px;background:linear-gradient(90deg,#7c4dff,#0048ff);}
.sk-right{text-align:right;white-space:nowrap;}
.sk-prob{font-weight:800;color:var(--deep-blue);font-size:16px;}
.sk-chips{margin-top:3px;font-size:10.5px;color:var(--muted);}
.sk-chip{display:inline-block;padding:1px 6px;border-radius:7px;background:var(--soft-lilac);margin-left:4px;font-weight:700;}
.sk-agree{display:inline-block;font-size:10px;font-weight:800;padding:1px 7px;border-radius:8px;margin-left:6px;}
.sk-agree.three{background:#dcfce7;color:#15803d;}.sk-agree.two{background:#e6f7ee;color:#1a9e5c;}.sk-agree.one{background:#fff3da;color:#b58900;}
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
.reachscroll tbody tr:nth-child(even) td{background:var(--soft-lilac);}
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
.tip:hover::after,.tip:hover::before,.tip:focus::after,.tip:focus::before{opacity:1;visibility:visible;}
.tip{outline:none;}
/* Tecnicismo inline con explicación (hover en escritorio, tap/foco en móvil) */
.term{position:relative;border-bottom:1px dotted currentColor;cursor:help;outline:none;}
.term::after{content:attr(data-tip);position:absolute;bottom:150%;left:50%;transform:translateX(-50%);
width:250px;max-width:74vw;background:var(--tip-bg);color:#e8ecff;font-size:12px;font-weight:500;line-height:1.5;
padding:10px 12px;border-radius:10px;opacity:0;visibility:hidden;transition:opacity .15s;z-index:60;
box-shadow:0 10px 28px rgba(0,0,0,.28);text-align:left;white-space:normal;pointer-events:none;}
.term::before{content:"";position:absolute;bottom:150%;left:50%;transform:translate(-50%,98%);border:6px solid transparent;
border-top-color:var(--tip-bg);opacity:0;visibility:hidden;transition:opacity .15s;z-index:61;}
.term:hover::after,.term:hover::before,.term:focus::after,.term:focus::before{opacity:1;visibility:visible;}
/* ===== UX: banda de veredicto + podio ===== */
.verdict{background:var(--grad-hero);color:#fff;border-radius:24px;padding:26px 28px;margin:8px 0 6px;
box-shadow:0 18px 40px rgba(78,0,255,.18);}
.verdict .vlead{font-size:12px;letter-spacing:2px;text-transform:uppercase;opacity:.85;margin:0 0 6px;font-weight:700;}
.verdict .vmain{font-size:23px;font-weight:800;line-height:1.3;margin:0;}
.verdict .vmain b{color:#ffd84d;}
.podium{display:grid;grid-template-columns:1fr 1.18fr 1fr;gap:14px;align-items:end;margin-top:20px;}
.pod{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:15px 10px;text-align:center;}
.pod .rk{font-size:26px;line-height:1;}
.pod .tm{font-size:16px;font-weight:800;margin:3px 0 1px;}
.pod .pc{font-size:25px;font-weight:900;line-height:1;}
.pod .pl{font-size:11px;opacity:.8;}
.pod.p1{transform:translateY(-12px);background:rgba(255,216,77,.16);border-color:rgba(255,216,77,.55);padding-bottom:24px;}
.pod.p1 .pc{color:#ffd84d;font-size:30px;}
/* ===== UX: tarjetas de hallazgos clave ===== */
.takeaways{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0 6px;}
.tk{background:#fff;border:1px solid var(--border);border-radius:16px;padding:14px 15px;border-top:4px solid var(--purple);
box-shadow:0 10px 26px rgba(4,28,89,.05);transition:background .3s,border-color .3s,transform .2s;}
.tk:hover{transform:translateY(-2px);}
.tk .lab{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:800;}
.tk .big{font-size:18px;font-weight:900;color:var(--deep-blue);margin:5px 0 2px;line-height:1.15;}
.tk .sub{font-size:12px;color:var(--muted);}
.tk.green{border-top-color:#1a9e5c;} .tk.red{border-top-color:#c0392b;} .tk.blue{border-top-color:var(--vibrant-blue);}
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
  <p class="sub" data-en="Three artificial intelligences —<b>Claude</b>, <b>ChatGPT</b> and <b>Gemini</b>— forecast the 2026 World Cup: who will lift the trophy, how each group will end, the road to the final and who wins the Golden Boot. A fourth forecast, the <b>consensus</b>, combines all three. Each AI reaches its numbers in a different way; in every tab you can open its full explanation.">Tres inteligencias artificiales —<b>Claude</b>, <b>ChatGPT</b> y <b>Gemini</b>— pronostican el Mundial 2026:
  quién levantará la copa, cómo terminará cada grupo, el camino hasta la final y quién ganará la Bota de Oro. Un cuarto pronóstico, el <b>consenso</b>,
  combina los tres. Cada IA llega a sus números de una forma distinta; en cada pestaña puedes abrir su explicación completa.</p>
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

<div class="footer">
  <div data-en="Javier Forero · Statistician and AI & Analytics Consultant">Javier Forero · Estadístico y consultor en IA y Analítica</div>
  <div class="f-sub"><a href="https://www.javierforero.com">javierforero.com</a> · <a href="https://www.linkedin.com/in/jforero/">LinkedIn</a> · <a href="https://github.com/jaforero/mundial2026-ai-benchmark">GitHub</a> · <span data-en="June 2026">junio 2026</span></div>
  <div class="f-sub" style="margin-top:8px;opacity:.58" data-en="The probabilities are model estimates, not certainties. Consensus = combination of the three tools.">Las probabilidades son estimaciones de modelos, no certezas. Consenso = combinación de las tres herramientas.</div>
</div>

</div>

<script>
const DATA = __BLOB__;
const COL = {Claude:'#0048ff', ChatGPT:'#10a37f', Gemini:'#7c4dff', Consenso:'#4e00ff'};
const ELO = DATA.elo || {};
const fmt = x => (x==null?'—':(Math.round(x*10)/10).toFixed(1)+'%');

/* ============ i18n ============ */
let LANG='es';
const TEAM_EN={'Alemania':'Germany','Arabia Saudí':'Saudi Arabia','Argelia':'Algeria','Argentina':'Argentina','Australia':'Australia','Austria':'Austria','Bosnia':'Bosnia & H.','Brasil':'Brazil','Bélgica':'Belgium','Cabo Verde':'Cape Verde','Canadá':'Canada','Chequia':'Czechia','Colombia':'Colombia','Corea del Sur':'South Korea','Costa de Marfil':'Ivory Coast','Croacia':'Croatia','Curazao':'Curaçao','Ecuador':'Ecuador','Egipto':'Egypt','Escocia':'Scotland','España':'Spain','Estados Unidos':'United States','Francia':'France','Ghana':'Ghana','Haití':'Haiti','Inglaterra':'England','Iraq':'Iraq','Irán':'Iran','Japón':'Japan','Jordania':'Jordan','Marruecos':'Morocco','México':'Mexico','Noruega':'Norway','Nueva Zelanda':'New Zealand','Panamá':'Panama','Paraguay':'Paraguay','Países Bajos':'Netherlands','Portugal':'Portugal','Qatar':'Qatar','RD Congo':'DR Congo','Senegal':'Senegal','Sudáfrica':'South Africa','Suecia':'Sweden','Suiza':'Switzerland','Túnez':'Tunisia','Türkiye':'Turkey','Uruguay':'Uruguay','Uzbekistán':'Uzbekistan'};
function tx(es,en){return LANG==='en'?en:es;}          /* texto UI */
function term(label,tip){return `<span class="term" tabindex="0" role="note" aria-label="${tip}" data-tip="${tip}">${label}</span>`;}  /* tecnicismo con tooltip */
const TEAM_ES={'Türkiye':'Turquía'};
function tn(n){return LANG==='en'?(TEAM_EN[n]||n):(TEAM_ES[n]||n);}   /* nombre de selección (solo para mostrar) */const FLAG={'Alemania':'🇩🇪','Arabia Saudí':'🇸🇦','Argelia':'🇩🇿','Argentina':'🇦🇷','Australia':'🇦🇺','Austria':'🇦🇹','Bosnia':'🇧🇦','Brasil':'🇧🇷','Bélgica':'🇧🇪','Cabo Verde':'🇨🇻','Canadá':'🇨🇦','Chequia':'🇨🇿','Colombia':'🇨🇴','Corea del Sur':'🇰🇷','Costa de Marfil':'🇨🇮','Croacia':'🇭🇷','Curazao':'🇨🇼','Ecuador':'🇪🇨','Egipto':'🇪🇬','Escocia':'🇬🇧','España':'🇪🇸','Estados Unidos':'🇺🇸','Francia':'🇫🇷','Ghana':'🇬🇭','Haití':'🇭🇹','Inglaterra':'🇬🇧','Iraq':'🇮🇶','Irán':'🇮🇷','Japón':'🇯🇵','Jordania':'🇯🇴','Marruecos':'🇲🇦','México':'🇲🇽','Noruega':'🇳🇴','Nueva Zelanda':'🇳🇿','Panamá':'🇵🇦','Paraguay':'🇵🇾','Países Bajos':'🇳🇱','Portugal':'🇵🇹','Qatar':'🇶🇦','RD Congo':'🇨🇩','Senegal':'🇸🇳','Sudáfrica':'🇿🇦','Suecia':'🇸🇪','Suiza':'🇨🇭','Túnez':'🇹🇳','Türkiye':'🇹🇷','Uruguay':'🇺🇾','Uzbekistán':'🇺🇿'};
function tf(n){return (FLAG[n]||'')+'  '+tn(n);}  /* bandera + nombre (tablas/tarjetas) */

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
      <div class="chteam">${tf(t)}<br><span class="elo">${tx('nivel','strength')} ${ELO[t]||'—'}</span></div>
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

/* ---------- Bota de Oro: goleadores ---------- */
function medalCls(i){return i===0?'gold':(i===1?'sil':(i===2?'bro':''));}
function scorersConsensus(){
  const list=(DATA.consensus&&DATA.consensus.scorers)||[]; if(!list.length) return '';
  const MAX=Math.max.apply(null,list.map(s=>s.prob))*1.08;
  let h='<ol class="scorers">';
  list.forEach((s,i)=>{
    const chips=[s.cl!=null?`<span class="sk-chip">Claude ${s.cl}%</span>`:'',
                 s.cg!=null?`<span class="sk-chip">ChatGPT ${s.cg}%</span>`:'',
                 s.gm!=null?`<span class="sk-chip">Gemini ${s.gm}%</span>`:''].join('');
    const agcls=s.models>=3?'three':(s.models===2?'two':'one');
    const agtip=s.models>=3?tx('Las tres IAs lo incluyen en su Top 10','All three AIs list him in their Top 10')
              :(s.models===2?tx('Dos de las tres IAs lo incluyen','Two of the three AIs list him')
                            :tx('Solo una IA lo incluye','Only one AI lists him'));
    const agree=`<span class="sk-agree ${agcls}" tabindex="0" data-tip="${agtip}">${s.models} IA</span>`;
    h+=`<li class="sk"><span class="sk-rank ${medalCls(i)}">${i+1}</span>
      <div class="sk-main"><span class="sk-name">${s.player}</span> <span class="sk-team">${tf(s.team)}</span>${agree}
        <div class="sk-bar"><span style="width:${100*s.prob/MAX}%"></span></div></div>
      <div class="sk-right"><div class="sk-prob">${fmt(s.prob)}</div><div class="sk-chips">${chips}</div></div></li>`;
  });
  return h+'</ol>';
}
function scorersAI(aiKey){
  const list=(DATA[aiKey]&&DATA[aiKey].scorers)||[]; if(!list.length) return '';
  const MAX=Math.max.apply(null,list.map(s=>s.prob))*1.08;
  let h='<ol class="scorers">';
  list.forEach((s,i)=>{
    const note=s.note?` <span class="term" tabindex="0" role="note" aria-label="${s.note}" data-tip="${s.note}">ⓘ</span>`:'';
    const extra=(s.xg!=null)?`<div class="sk-chips">${tx('goles esperados','expected goals')} ${s.xg}</div>`:'';
    h+=`<li class="sk"><span class="sk-rank ${medalCls(i)}">${s.rank||i+1}</span>
      <div class="sk-main"><span class="sk-name">${s.player}</span> <span class="sk-team">${tf(s.team)}</span>${note}
        <div class="sk-bar"><span style="width:${100*s.prob/MAX}%"></span></div></div>
      <div class="sk-right"><div class="sk-prob">${fmt(s.prob)}</div>${extra}</div></li>`;
  });
  return h+'</ol>';
}

/* ---------- reach table ---------- */
function reachTable(reach, teams){
  let h = `<div class="reachscroll"><table><thead><tr><th>${tx('Selección','Team')}</th><th>R32</th><th>${tx('Octavos','R16')}</th><th>${tx('Cuartos','QF')}</th><th>${tx('Semis','SF')}</th><th>${tx('Final','Final')}</th><th>${tx('Campeón','Champion')}</th></tr></thead><tbody>`;
  for(const t of teams){
    const r = k => reach[k] && reach[k][t]!=null ? fmt(reach[k][t]) : '—';
    h += `<tr><td class="tm">${tf(t)}</td><td>${r('R32')}</td><td>${r('R16')}</td><td>${r('QF')}</td><td>${r('SF')}</td><td>${r('FINAL')}</td><td class="hl">${r('CAMPEON')}</td></tr>`;
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
function backtestPanel(aiKey){
  const b = (DATA.backtest||{})[aiKey]; if(!b) return '';
  return `<details class="meth"><summary>${tx('Ver backtesting y validación estadística','View backtesting and statistical validation')} · ${(LANG==='en'&&b.title_en)?b.title_en:b.title}</summary><div class="methbody">${(LANG==='en'&&b.html_en)?b.html_en:b.html}</div></details>`;
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
      <span style="width:118px;font-weight:700;color:var(--deep-blue);font-size:12.5px">${tf(t)}</span>
      ${bar(p,MAX,color)}<span style="font-weight:800;color:var(--deep-blue);font-size:12.5px">${fmt(p)}</span></div>`;
  }
  return h+`<div class="legend" style="margin:6px 2px 2px">${tx('Las 48 selecciones, ordenadas por probabilidad de campeón.','All 48 teams, ranked by title probability.')}</div></div>`;
}

/* ---------- group projection (consensus tab) ---------- */
function groupProjection(){
  const bt=DATA.best_thirds||[];
  let h='<div class="grid2">';
  for(const gl of Object.keys(DATA.groups)){
    const row = DATA.group_proj[gl];
    const cons = row.Consenso;
    h += `<div class="gcard"><div class="gh">${tx('Grupo','Group')} ${gl}</div>
      <table class="mtab"><thead><tr><th>#</th><th>${tx('Selección','Team')}</th><th>${tx('Pts esp. (cons.)','Exp. pts (cons.)')}</th><th></th></tr></thead><tbody>`;
    const w = {Claude:row.Claude[0][0],ChatGPT:row.ChatGPT[0][0],Gemini:row.Gemini[0][0]};
    cons.forEach((pair,i)=>{
      const [t,pts]=pair;
      const cls = i<2?'grp-q':(i===2&&bt.includes(gl)?'grp-3rd':'grp-out');
      const badge = i<2?'✓':(i===2&&bt.includes(gl)?'③':'');
      h+=`<tr class="${cls}"><td style="font-weight:800">${i+1}</td><td class="ta">${tf(t)}</td><td>${pts}</td><td style="font-size:12px">${badge}</td></tr>`;
    });
    const same = (w.Claude===w.ChatGPT)&&(w.ChatGPT===w.Gemini);
    h+=`</tbody></table><div class="legend">${same?(tx('✓ Las 3 IAs coinciden en el 1.º: ','✓ The 3 AIs agree on 1st: ')+'<b>'+tf(w.Claude)+'</b>'):(tx('⚠ Disputa por el 1.º — ','⚠ Dispute for 1st — ')+'Claude: '+tf(w.Claude)+' · ChatGPT: '+tf(w.ChatGPT)+' · Gemini: '+tf(w.Gemini))}</div></div>`;
  }
  h+=`</div><p class="note" style="margin-top:12px">${tx('🟣 Top 2 clasificados directamente · 🟡 ③ = mejor tercero (8 de 12 pasan) · Atenuado = no clasifica.','🟣 Top 2 qualify directly · 🟡 ③ = best third (8 of 12 advance) · Dimmed = does not qualify.')}</p>`;
  return h;
}

/* ---------- match table per AI ---------- */
function matchTableByAI(matches, showXg){
  // matches: array {a,b,pA,pD,pB,score,(xa,xb),md,date} ; agrupar por grupo, ordenar por jornada oficial
  let h='<div class="grid2">';
  for(const gl of Object.keys(DATA.groups)){
    const teams=DATA.groups[gl];
    const grp=matches.filter(m=>teams.includes(m.a)&&teams.includes(m.b)).sort((a,b)=>(a.md||0)-(b.md||0));
    h+=`<div class="gcard"><div class="gh">${tx('Grupo','Group')} ${gl}</div><table class="mtab"><tbody>`;
    let prevMd=0;
    for(const m of grp){
      if(m.md && m.md!==prevMd){ h+=`<tr class="md-sep"><td colspan="4"><span class="md-label">${tx('Jornada','Matchday')} ${m.md} · ${m.date||''}</span></td></tr>`; prevMd=m.md; }
      const xg = (showXg && m.xa!=null) ? `<span class="wdltxt" style="margin-left:0">xG ${m.xa}–${m.xb}</span>` : '';
      h+=`<tr><td class="ta">${tf(m.a)}</td><td class="sc">${m.score}</td><td class="tb">${tf(m.b)}</td>
        <td>${wdlBar(m.pA,m.pD,m.pB)}<span class="wdltxt">${Math.round(m.pA)}·${Math.round(m.pD)}·${Math.round(m.pB)}</span>${xg?'<br>'+xg:''}</td></tr>`;
    }
    h+='</tbody></table></div>';
  }
  return h+'</div>';
}

/* ---------- consensus match table with agreement ---------- */
function consensusMatchTable(){
  let h='<div class="grid2">';
  for(const gl of Object.keys(DATA.groups)){
    const teams=DATA.groups[gl];
    const grp=DATA.consensus.matches.filter(m=>teams.includes(m.a)&&teams.includes(m.b)).sort((a,b)=>(a.md||0)-(b.md||0));
    h+=`<div class="gcard"><div class="gh">${tx('Grupo','Group')} ${gl}</div><table class="mtab"><tbody>`;
    let prevMd=0;
    for(const m of grp){
      if(m.md && m.md!==prevMd){ h+=`<tr class="md-sep"><td colspan="4"><span class="md-label">${tx('Jornada','Matchday')} ${m.md} · ${m.date||''}</span></td></tr>`; prevMd=m.md; }
      const dots=`<span class="agree"><i class="${m.agree>=1?'on':''}"></i><i class="${m.agree>=2?'on':''}"></i><i class="${m.agree>=3?'on':''}"></i></span>`;
      const ci=m.conf_idx, ccol = ci>=75?'#1a9e5c':(ci>=55?'#0048ff':(ci>=45?'#b58900':'#c0392b'));
      const chip=`<span class="cchip" style="background:${ccol}" title="${tx('Confianza del pronóstico (0–100)','Forecast confidence (0–100)')}">${ci}</span>`;
      h+=`<tr><td class="ta">${tf(m.a)}</td><td class="sc">${m.score}</td><td class="tb">${tf(m.b)}</td>
        <td>${wdlBar(m.pA,m.pD,m.pB)} ${dots}${chip}</td></tr>`;
    }
    h+='</tbody></table></div>';
  }
  return h+'</div>';
}

/* ---------- HEAD TO HEAD ---------- */
function h2hOptions(){
  let opts=''; 
  DATA.consensus.matches.forEach((m,idx)=>{ opts+=`<option value="${idx}">${m.group} · ${tf(m.a)} vs ${tf(m.b)}</option>`; });
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
        <div class="m"><div class="v">${f.cs_a}%</div><div class="l">${tx('Sin gol en contra','Clean sheet')} · ${tf(f.a)}</div></div>
        <div class="m"><div class="v">${f.cs_b}%</div><div class="l">${tx('Sin gol en contra','Clean sheet')} · ${tf(f.b)}</div></div>
        <div class="m"><div class="v">${f.xpts_a}/${f.xpts_b}</div><div class="l">${tx('Puntos esperados','Expected points')}</div></div>
      </div></div>`;
  }
  // índice de consenso: cifra + veredicto en lenguaje claro; teoría en tooltip
  const ci=m.conf_idx, col = ci>=75?'#1a9e5c':(ci>=55?'#0048ff':(ci>=45?'#b58900':'#c0392b'));
  const verdict = ci>=75?tx('Favorito claro · las 3 IAs coinciden','Clear favorite · all 3 AIs agree'):(ci>=55?tx('Favorito moderado','Moderate favorite'):(ci>=45?tx('Partido igualado','Close match'):tx('Muy igualado · difícil de predecir','Very close · hard to call')));
  const favName = (m.pA>=m.pD&&m.pA>=m.pB)?m.a:((m.pB>=m.pD&&m.pB>=m.pA)?m.b:null);
  const favLine = favName?`${tx('Favorito del consenso','Consensus favorite')}: <b>${tf(favName)}</b> (${Math.round(Math.max(m.pA,m.pB))}%)`:tx('El empate es el resultado más probable','A draw is the most likely result');
  const tipTxt = tx(`Resume en una cifra cuán claro y consensuado es el resultado. Combina la fuerza del favorito con el acuerdo entre las 3 IAs — acuerdo ${m.agree_idx}/100; probabilidades combinadas (pool logarítmico) ${m.p_log[0]}% · ${m.p_log[1]}% · ${m.p_log[2]}%. Más alto = más claro y consensuado; más bajo = parejo o disputado.`,`A single figure for how clear and agreed the result is. It combines the favorite's strength with the agreement among the 3 AIs — agreement ${m.agree_idx}/100; combined probabilities (logarithmic pool) ${m.p_log[0]}% · ${m.p_log[1]}% · ${m.p_log[2]}%. Higher = clearer and more agreed; lower = close or disputed.`);
  const cidx=`<div class="cidx"><div class="ring" style="background:${col}">${ci}</div>
    <div class="meta">
      <div class="cidx-h">${tx('Confianza del pronóstico','Forecast confidence')}: <b style="margin-left:4px">${ci}/100</b><span class="tip" data-tip="${tipTxt}">i</span></div>
      <div class="cidx-v" style="color:${col}">${verdict}</div>
      <div class="legend" style="margin-top:2px">${favLine}</div>
    </div></div>`;
  document.getElementById('h2h-out').innerHTML =
    `<div class="h2h-big"><span class="h2h-team">${tf(m.a)}</span><span class="h2h-vs">vs</span><span class="h2h-team">${tf(m.b)}</span></div>
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
  const pod=(rk,t,cls)=>`<div class="pod ${cls}"><div class="rk">${rk}</div><div class="tm">${tf(t[0])}</div><div class="pc">${fmt(t[1])}</div><div class="pl">${tx('campeón','champion')}</div></div>`;
  return `<div class="verdict">
    <p class="vlead">${tx('El veredicto del consenso · Mundial 2026','The consensus verdict · World Cup 2026')}</p>
    <p class="vmain">${verdict}</p>
    <div class="podium">${pod('🥈',t2,'p2')}${pod('🥇',t1,'p1')}${pod('🥉',t3,'p3')}</div>
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
    <div class="tk blue"><div class="lab">${tx('Favorito del consenso','Consensus favorite')}</div><div class="big">${tf(fav[0])}</div><div class="sub">${fmt(fav[1])} ${tx('de probabilidad de título','title probability')}</div></div>
    <div class="tk"><div class="lab">${tx('Mayor desacuerdo entre IAs','Biggest disagreement between AIs')}</div><div class="big">${tf(dis.t)}</div><div class="sub">${tx('entre','between')} ${fmt(dis.min)} ${tx('y','and')} ${fmt(dis.max)} ${tx('según el modelo','depending on the model')}</div></div>
    <div class="tk green"><div class="lab">${tx('Pronóstico más seguro','Safest forecast')}</div><div class="big">${tf(safe.a)} vs ${tf(safe.b)}</div><div class="sub">${tx('confianza','confidence')} ${safe.conf_idx}/100 · ${tx('marcador','score')} ${safe.score}</div></div>
    <div class="tk red"><div class="lab">${tx('Moneda al aire','Coin flip')}</div><div class="big">${tf(coin.a)} vs ${tf(coin.b)}</div><div class="sub">${tx('confianza','confidence')} ${coin.conf_idx}/100 · ${tx('muy igualado','razor-thin')}</div></div>
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
      <span style="margin-left:14px">${term(tx('¿qué es el «nivel»?','what is «strength»?'), tx('Medida de fuerza de cada selección que se recalcula tras cada partido, parecida a un ranking dinámico. Técnicamente, un sistema Elo.','A strength measure for each team recomputed after every match, like a dynamic ranking. Technically, an Elo system.'))}</span>
    </div>
    ${champDivergence()}
  </div>
  <div class="insight"><p>${tx(`Por qué difieren: cada IA cree que un Mundial lo decide algo distinto. <b>Gemini</b> mira el ${term('estado físico actual','Minutos de alta exigencia jugados en clubes esta temporada (Champions, Libertadores) como señal de desgaste y rodaje de cada plantilla')} de los jugadores y penaliza al campeón vigente: baja a Argentina y sube a Francia. <b>ChatGPT</b> confía en la ${term('historia y los rankings','Posición en el ranking FIFA, valor de las plantillas y resultados de Mundiales anteriores')} y encabeza con España. <b>Claude</b> combina el ${term('rendimiento real de goles','Goles marcados y recibidos en partidos internacionales reales, analizados partido a partido')} con el ${term('nivel actualizado de cada equipo','Una medida de fuerza que se recalcula tras cada partido, parecida a un ranking dinámico. Técnicamente se llama sistema Elo.')}, y realza a Brasil, Inglaterra y Colombia. El <b>consenso</b> toma el punto medio de las tres y modera los extremos.`,`Why they differ: each AI believes a World Cup is decided by something different. <b>Gemini</b> looks at the players' ${term('current physical state','High-intensity minutes played at clubs this season (Champions League, Libertadores) as a sign of each squads wear and match sharpness')} and penalizes the reigning champion: Argentina drops, France rises. <b>ChatGPT</b> trusts ${term('history and the rankings','FIFA ranking position, squad market value and results from previous World Cups')} and leads with Spain. <b>Claude</b> combines ${term('real goal performance','Goals scored and conceded in real international matches, analyzed game by game')} with an ${term('up-to-date team strength','A strength measure recomputed after every match, like a dynamic ranking. Technically it is called an Elo system.')}, raising Brazil, England and Colombia. The <b>consensus</b> takes the middle ground of the three and tempers the extremes.`)}</p></div>

  <div class="section-title">🥇 ${tx('Bota de Oro — Top 10 goleadores (consenso)','Golden Boot — Top 10 scorers (consensus)')}</div>
  <p class="note">${tx('Una dimensión nueva: ya no solo qué selección gana, sino qué jugador marca más. Ahora las <b>tres IAs</b> pronostican goleadores —incluido el <b>nuevo modelo de jugador de Claude</b>, que parte de los goles que su modelo de selección proyecta para cada equipo—. El consenso promedia las probabilidades e indica en cuántas IAs coincide cada nombre.','A new dimension: not just which team wins, but which player scores most. Now <b>all three AIs</b> forecast scorers —including <b>the new Claude player-level model</b>, built on the goals its team model projects for each side—. The consensus averages the probabilities and shows how many AIs agree on each name.')}</p>
  <div class="card">${scorersConsensus()}</div>

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
  <p class="lead">${tx(`Combina las versiones más avanzadas de las tres IAs. Para el título usa la <b>${term('mediana','El valor del medio de las tres IAs: si un modelo se va a un extremo, no arrastra el resultado.')}</b> de las tres; para los grupos, los <b>${term('puntos esperados','Promedio de puntos que sumaría cada equipo en sus 3 partidos de grupo, según las probabilidades de cada resultado.')}</b> de los 72 partidos; y para cada partido, el promedio de probabilidades con el marcador más votado. El <b>índice de confianza</b> de cada partido aparece explicado al pasar el cursor sobre su cifra.`,`It combines the most advanced versions of the three AIs. For the title it uses the <b>${term('median','The middle value of the three AIs: if one model goes to an extreme, it does not drag the result.')}</b> of the three; for the groups, the <b>${term('expected points','Average points each team would earn in its 3 group matches, given the probability of each result.')}</b> from the 72 matches; and for each match, the average of the probabilities with the most-voted scoreline. The <b>confidence index</b> for each match is explained on hover over its figure.`)}</p>`;
  renderH2H(0);
}

function renderClaude(){
  const d=DATA.claude;
  const champTop=sortByTitle(d.title).slice(0,16).map(x=>x[0]);
  document.getElementById('claude').innerHTML = `
  <div class="insight"><p>${tx(`<b>Recalibración v7 (Fase 7).</b> Capa de calibración sobre v5/v6, sin reentrenar: corrige el <b>exceso de confianza</b> encogiendo las probabilidades hacia la tasa base de cada ronda (el campeón más probable baja de ${fmt(18.23)} a ${fmt(d.title[sortByTitle(d.title)[0][0]])} y sube la cola), <b>infla el empate</b> en partidos parejos, marca los <b>partidos de alta incertidumbre</b> y ajusta su marcador, y recalibra los goleadores con un desglose de riesgos. Todo se expresa como probabilidad, no como certeza.`,`<b>Recalibration v7 (Phase 7).</b> A calibration layer over v5/v6, without retraining: it corrects <b>overconfidence</b> by shrinking probabilities toward each round base rate (the most likely champion drops from ${fmt(18.23)} to ${fmt(d.title[sortByTitle(d.title)[0][0]])} and the tail rises), <b>inflates draws</b> in close matches, flags <b>high-uncertainty matches</b> and tempers their scoreline, and recalibrates scorers with a risk breakdown. Everything is expressed as probability, not certainty.`)}</p></div>
  <div class="section-title">${tx('Metodología','Methodology')} · Claude <span style="color:var(--c-claude)">v7</span></div>
  <div class="card methclassic">
    <p>${tx(`Motor de <b>ensamble</b> que promedia un <b>Dixon-Coles data-driven</b> (ataque/defensa por equipo estimados de miles de partidos reales) con un <b>modelo de Machine Learning</b> (gradient boosting con pérdida de Poisson) que integra <b>Elo actual a junio-2026, forma reciente e histórico de Mundiales</b>. El ensamble es el que mejor valida.`,`An <b>ensemble</b> engine that averages a <b>data-driven Dixon-Coles</b> model (per-team attack/defense estimated from thousands of real matches) with a <b>Machine Learning model</b> (gradient boosting with Poisson loss) integrating <b>current Elo as of June 2026, recent form and World Cup history</b>. The ensemble validates best.`)}</p>
    <p>${tx(`Desempeño medido fuera de muestra con código sobre <b>4 Mundiales reales (2010–2022, 192 partidos)</b>: ensamble RPS 0.2002 vs 0.2413 (azar), <b>mejora del 17.0%</b> — supera al ML solo (0.2012) y al Dixon-Coles solo (0.2016). Detalle en el panel de backtesting.`,`Out-of-sample performance measured with code over <b>4 real World Cups (2010–2022, 192 matches)</b>: ensemble RPS 0.2002 vs 0.2413 (chance), a <b>17.0% improvement</b> — beating ML alone (0.2012) and Dixon-Coles alone (0.2016). Detail in the backtesting panel.`)}</p>
    <div style="margin-top:8px">
      <span class="badge">${tx('Ensamble Dixon-Coles + Machine Learning','Dixon-Coles + Machine Learning ensemble')}</span><span class="badge">${tx('Elo · forma · histórico Mundiales','Elo · form · World Cup history')}</span>
      <span class="badge">${tx('Validado OOS 2010–2022 (192 partidos)','Validated OOS 2010–2022 (192 matches)')}</span><span class="badge">${tx('Bracket R32 corregido (v5)','R32 bracket fixed (v5)')}</span><span class="badge">${tx('Distribución completa por partido','Full per-match distribution')}</span>
    </div>
  </div>
  <div class="insight"><p>${tx(`Honestidad metodológica: sobre 4 Mundiales reales, el ML solo y el estadístico quedan <b>parejos</b>, pero el ensamble de ambos <b>supera a los dos</b>; "deep learning" no es automáticamente mejor con datos escasos. El resultado: España (${fmt(d.title['España'])}) y un top plano con <b>Brasil (${fmt(d.title['Brasil'])}), Inglaterra (${fmt(d.title['Inglaterra'])}) y Colombia (${fmt(d.title['Colombia'])})</b> realzados por datos.`,`Methodological honesty: across 4 real World Cups, ML alone and the statistical model are <b>roughly tied</b>, but the ensemble of the two <b>beats both</b>; "deep learning" is not automatically better with scarce data. The result: Spain (${fmt(d.title['España'])}) and a flat top tier with <b>Brazil (${fmt(d.title['Brasil'])}), England (${fmt(d.title['Inglaterra'])}) and Colombia (${fmt(d.title['Colombia'])})</b> lifted by the data.`)}</p></div>

  ${methPanel("claude")}
  ${backtestPanel("claude")}
  <div class="section-title">${tx('Probabilidad de campeón · Claude','Champion probability · Claude')}</div>
  <div class="card">${champBars(d.title, COL.Claude)}</div>

  <div class="section-title">${tx('Camino al título · Claude · las 48 selecciones','Road to the title · Claude · all 48 teams')}</div>
  <div class="card">${reachTable(d.reach, all48(d.title))}</div>

  <div class="section-title">${tx('Los 72 partidos · Claude v7 (recalibrado, distribución por partido)','The 72 matches · Claude v7 (recalibrated, per-match distribution)')}</div>
  <p class="note">${tx('El marcador y las probabilidades V/E/D salen de la <b>distribución de Poisson completa</b> del modelo, y se muestra además el <b>xG (goles esperados)</b> de cada selección por partido.','The scoreline and W/D/L probabilities come from the model <b>full Poisson distribution</b>, and the <b>xG (expected goals)</b> of each team per match is also shown.')}</p>
  ${matchTableByAI(d.fixtures.map(f=>({a:f.a,b:f.b,pA:f.pA,pD:f.pD,pB:f.pB,score:f.score,xa:f.eg_a,xb:f.eg_b,md:f.md,date:f.date,grp:f.grp})), true)}

  <div class="section-title">🥇 ${tx('Bota de Oro · Top 10 goleadores — Claude v7','Golden Boot · Top 10 scorers — Claude v7')}</div>
  <p class="note">${tx('Modelo nuevo de jugador montado sobre el de selección. Los goles esperados de cada jugador parten de los <b>goles que su equipo proyecta marcar en el torneo</b> (partidos esperados según su avance × goles por partido del modelo) y se reparten por <b>cuota de rol y penales</b>, ajustados por <b>titularidad</b>, <b>disponibilidad física</b> y <b>forma</b>. La Bota de Oro se estima por simulación. Pasa el cursor sobre la ⓘ para ver el detalle de cada jugador.','New player-level model built on top of the team model. Each player expected goals start from the <b>goals their team is projected to score in the tournament</b> (expected matches from its run × goals per match) and are split by <b>role share and penalties</b>, adjusted for <b>starting probability</b>, <b>physical availability</b> and <b>form</b>. The Golden Boot is estimated by simulation. Hover the ⓘ for the detail of each player.')}</p>
  <div class="insight"><p>${tx(`Por qué <b>riesgo físico</b> y <b>forma</b> son factores <b>separados</b>: el ${term('riesgo físico','Lesiones recientes, carga y edad: afecta cuántos minutos juega y si lo reservan para fases finales.')} ajusta los <b>minutos</b> (cuánto juega), mientras que la ${term('forma','Racha goleadora y afinación: afecta su eficacia por minuto cuando sí está en cancha.')} ajusta la <b>tasa</b> de gol por minuto. Un jugador puede estar fino pero con riesgo de rotación, o sano pero frío; mezclarlos en una sola variable perdería esa diferencia.`,`Why <b>physical risk</b> and <b>form</b> are <b>separate</b> factors: ${term('physical risk','Recent injuries, load and age: it affects how many minutes he plays and whether he is rested for later rounds.')} adjusts the <b>minutes</b> (how much he plays), while ${term('form','Scoring streak and sharpness: it affects his efficiency per minute when he is on the pitch.')} adjusts the <b>scoring rate</b> per minute. A player can be sharp but at rotation risk, or fit but cold; merging them into one variable would lose that distinction.`)}</p></div>
  <div class="card">${scorersAI("claude")}</div>`;
}

function renderChatGPT(){
  const d=DATA.chatgpt;
  const champTop=sortByTitle(d.title).slice(0,16).map(x=>x[0]);
  document.getElementById('chatgpt').innerHTML = `
  <div class="section-title">${tx('Metodología','Methodology')} · ChatGPT <span style="color:var(--c-chatgpt)">v7</span></div>
  <div class="card methclassic">
    <p>${tx(`Ensamble <b>calibrado histórico</b> con los ajustes del <b>Backtesting Nivel 2</b>: refuerza el núcleo <b>FIFA/Elo</b> (sube a 24%), reduce el clima a contextual (4%) y añade una <b>penalización de sesgo de mercado</b> para no sobrevalorar a las ligas europeas más líquidas. Plantilla, player-level, forma y experiencia entran como capas de ajuste, no como dominantes.`,`A <b>historically-calibrated</b> ensemble with the <b>Level 2 Backtesting</b> adjustments: it reinforces the <b>FIFA/Elo</b> core (up to 24%), reduces climate to contextual (4%) and adds a <b>market-bias penalty</b> so the most liquid European leagues are not overvalued. Squad, player-level, form and experience enter as adjustment layers, not as dominant ones.`)}</p>
    <div style="margin-top:8px"><span class="badge">${tx('Núcleo FIFA/Elo reforzado','Reinforced FIFA/Elo core')}</span><span class="badge">${tx('Anti-sesgo de mercado','Anti-market-bias')}</span><span class="badge">${tx('Calibración histórica','Historical calibration')}</span><span class="badge">${tx('Outsiders tácticos corregidos','Tactical outsiders corrected')}</span></div>
  </div>
  <div class="insight"><p>${tx(`Rasgo de la v6.2: la IA <b>más prudente y mejor calibrada</b>. Contiene a España (${fmt(d.title['España'])}) sin ventaja excesiva y forma un bloque de élite con Francia (${fmt(d.title['Francia'])}), Inglaterra (${fmt(d.title['Inglaterra'])}) y Argentina (${fmt(d.title['Argentina'])}). El Nivel 2 sube moderadamente a outsiders tácticos (Marruecos, Colombia, Senegal, Japón). El detalle está en el backtesting.`,`v6.2 trait: the <b>most prudent and best-calibrated</b> model. It caps Spain (${fmt(d.title['España'])}) without an excessive edge and forms an elite block with France (${fmt(d.title['Francia'])}), England (${fmt(d.title['Inglaterra'])}) and Argentina (${fmt(d.title['Argentina'])}). Level 2 moderately lifts tactical outsiders (Morocco, Colombia, Senegal, Japan). The detail is in the backtesting.`)}</p></div>

  ${methPanel("chatgpt")}
  ${backtestPanel("chatgpt")}
  <div class="section-title">${tx('Probabilidad de campeón · ChatGPT','Champion probability · ChatGPT')}</div>
  <div class="card">${champBars(d.title, COL.ChatGPT)}</div>

  <div class="section-title">${tx('Camino al título · ChatGPT · las 48 selecciones','Road to the title · ChatGPT · all 48 teams')}</div>
  <div class="card">${reachTable(d.reach, all48(d.title))}</div>

  <div class="section-title">${tx('Los 72 partidos · ChatGPT v7 (recalibrado Fase 7)','The 72 matches · ChatGPT v7 (Phase 7 recalibration)')}</div>
  ${matchTableByAI(d.matches)}

  <div class="section-title">🥇 ${tx('Bota de Oro · Top 10 goleadores — ChatGPT','Golden Boot · Top 10 scorers — ChatGPT')}</div>
  <p class="note">${tx('Probabilidad de ganar la Bota de Oro por jugador, con sus goles esperados. Pasa el cursor sobre la ⓘ para ver la justificación de cada caso.','Probability of winning the Golden Boot per player, with expected goals. Hover the ⓘ for the rationale of each pick.')}</p>
  <div class="card">${scorersAI("chatgpt")}</div>`;
}

function renderGemini(){
  const d=DATA.gemini;
  const champTop=sortByTitle(d.title).slice(0,16).map(x=>x[0]);
  document.getElementById('gemini').innerHTML = `
  <div class="section-title">${tx('Metodología','Methodology')} · Gemini <span style="color:var(--c-gemini)">v8</span></div>
  <div class="card methclassic">
    <p>${tx(`Ensamble físico-estadístico que <b>abandona la "memoria histórica de los escudos"</b> del v6. Mide la resiliencia por la <b>carga de estrés cognitivo actual</b> de las plantillas (minutos de eliminación directa en Champions/Libertadores = <b>Redes de Presión Local</b>), aplica un <b>Factor de Decaimiento</b> al campeón defensor y reconfigura el <b>Aura de Localía</b> de forma asimétrica, sobre el motor bio-termodinámico UTCI.`,`A physics-statistical ensemble that <b>abandons the v6 "crest historical memory"</b>. It measures resilience via each squad's <b>current cognitive stress load</b> (knockout minutes in the Champions League/Libertadores = <b>Local Pressure Networks</b>), applies a <b>Champion Decay Factor</b> to the defending champion and reshapes the <b>Home Aura</b> asymmetrically, on top of the UTCI bio-thermodynamic engine.`)}</p>
    <div style="margin-top:8px"><span class="badge">${tx('Redes de Presión Local','Local Pressure Networks')}</span><span class="badge">${tx('Decaimiento del campeón (−8%)','Champion decay (−8%)')}</span><span class="badge">${tx('Aura de localía asimétrica','Asymmetric home aura')}</span><span class="badge">${tx('Motor bio-termodinámico UTCI','UTCI bio-thermodynamic engine')}</span></div>
  </div>
  <div class="insight"><p>${tx(`Giro del v7: <b>castiga el dogma histórico</b>. <b>Francia toma el nº 1</b> (${fmt(d.title['Francia'])}) por el volumen de minutos de élite de su plantilla; <b>Argentina cae al 3º</b> (${fmt(d.title['Argentina'])}) por el decaimiento del campeón; y <b>Brasil baja</b> (${fmt(d.title['Brasil'])}) al neutralizar su "gravedad de escudo". España se sostiene 2ª (${fmt(d.title['España'])}). El detalle empírico está en el backtesting.`,`v7 shift: it <b>punishes historical dogma</b>. <b>France takes #1</b> (${fmt(d.title['Francia'])}) on its squad's elite-minutes volume; <b>Argentina drops to 3rd</b> (${fmt(d.title['Argentina'])}) from champion decay; and <b>Brazil falls</b> (${fmt(d.title['Brasil'])}) as its "crest gravity" is neutralized. Spain holds 2nd (${fmt(d.title['España'])}). The empirical detail is in the backtesting.`)}</p></div>

  ${methPanel("gemini")}
  ${backtestPanel("gemini")}
  <div class="section-title">${tx('Probabilidad de campeón · Gemini','Champion probability · Gemini')}</div>
  <div class="card">${champBars(d.title, COL.Gemini)}</div>

  <div class="section-title">${tx('Camino al título · Gemini · las 48 selecciones','Road to the title · Gemini · all 48 teams')}</div>
  <div class="card">${reachTable(d.reach, all48(d.title))}</div>

  <div class="section-title">${tx('Los 72 partidos · Gemini v8 (recalibrado Fase 8)','The 72 matches · Gemini v8 (Phase 8 recalibration)')}</div>
  ${matchTableByAI(d.matches)}

  <div class="section-title">🥇 ${tx('Bota de Oro · Top 10 goleadores — Gemini','Golden Boot · Top 10 scorers — Gemini')}</div>
  <p class="note">${tx('Probabilidad de Bota de Oro con ajuste por estado de forma y riesgo de titularidad. Pasa el cursor sobre la ⓘ para ver el análisis de cada jugador.','Golden Boot probability adjusted for form and starting-role risk. Hover the ⓘ for the analysis of each player.')}</p>
  <div class="card">${scorersAI("gemini")}</div>`;
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
