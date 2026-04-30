import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts';

/* ─── CSS ─────────────────────────────────────────────────────────────────── */
const css = `
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg:       #F7F6F3;
  --surface:  #FFFFFF;
  --surf2:    #EFEFEB;
  --border:   #E2E0DA;
  --text:     #1A1916;
  --muted:    #8C8880;
  --faint:    #C8C5BE;
  --accent:   #1A6B3C;
  --accent2:  #E8F5EE;
  --warn:     #B45309;
  --warn2:    #FEF3C7;
  --danger:   #B91C1C;
  --danger2:  #FEE2E2;
  --line1:    #1A6B3C;
  --line2:    #B45309;
  --sid:      #141210;
  --sid2:     #1C1A17;
  --r: 6px;
}

[data-theme=dark] {
  --bg:       #111110;
  --surface:  #1C1C1A;
  --surf2:    #242422;
  --border:   #2E2E2B;
  --text:     #F0EDE8;
  --muted:    #78756E;
  --faint:    #3A3835;
  --accent:   #34D170;
  --accent2:  #0D2B1A;
  --warn:     #F59E0B;
  --warn2:    #2D1F08;
  --danger:   #F87171;
  --danger2:  #2D1010;
  --line1:    #34D170;
  --line2:    #F59E0B;
  --sid:      #0D0C0A;
  --sid2:     #161410;
}

*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  background:var(--bg);color:var(--text);
  font-family:'DM Sans',sans-serif;font-size:14px;line-height:1.5;
  -webkit-font-smoothing:antialiased;min-height:100vh;
  transition:background .2s,color .2s;
}

/* ── SHELL ── */
.shell{display:flex;height:100vh;overflow:hidden}

/* ── SIDEBAR ── */
.sidebar{
  width:210px;flex-shrink:0;
  background:var(--sid);
  display:flex;flex-direction:column;
  border-right:1px solid rgba(255,255,255,.04);
  overflow:hidden;
  transition:width .25s cubic-bezier(.4,0,.2,1);
  z-index:200;
}
.sidebar.closed{width:0}

.sid-logo{
  padding:16px 14px 12px;
  border-bottom:1px solid rgba(255,255,255,.05);
  display:flex;align-items:center;gap:10px;flex-shrink:0;
}
.sid-mark{
  width:28px;height:28px;background:var(--accent);
  border-radius:6px;display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.sid-mark svg{width:13px;height:13px;stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round}
.sid-name{font-size:12px;font-weight:500;color:#EDE9E1;white-space:nowrap;letter-spacing:-.01em}
.sid-sub{font-size:9px;color:rgba(255,255,255,.25);text-transform:uppercase;letter-spacing:.06em;margin-top:1px}

.sid-sec{padding:12px 8px 4px}
.sid-sec-lbl{font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.18);padding:0 6px;margin-bottom:4px}

.nav-btn{
  display:flex;align-items:center;gap:9px;
  padding:7px 10px;border-radius:6px;
  color:rgba(255,255,255,.35);font-size:12px;
  cursor:pointer;transition:all .15s;
  margin-bottom:1px;white-space:nowrap;
  border:none;background:transparent;width:100%;font-family:inherit;text-align:left;
}
.nav-btn:hover{background:rgba(255,255,255,.06);color:rgba(255,255,255,.65)}
.nav-btn.active{background:rgba(26,107,60,.2);color:#5DD5A0}
.nav-ico{width:14px;height:14px;flex-shrink:0;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.nav-badge{
  margin-left:auto;background:var(--danger);color:#fff;
  font-size:9px;font-weight:600;padding:1px 5px;border-radius:99px;min-width:16px;text-align:center;
}

.sid-footer{
  margin-top:auto;padding:10px 8px;
  border-top:1px solid rgba(255,255,255,.05);flex-shrink:0;
}
.sid-status{
  display:flex;align-items:center;gap:8px;
  padding:7px 10px;background:rgba(255,255,255,.03);border-radius:6px;
}
.s-dot{width:6px;height:6px;border-radius:50%;background:#34D170;animation:blink 2.5s ease infinite;flex-shrink:0}
.s-dot.off{background:var(--danger);animation:none}
.s-txt{font-size:11px;color:rgba(255,255,255,.3);white-space:nowrap}
.s-val{font-size:10px;color:rgba(255,255,255,.45);margin-left:auto;font-family:'DM Mono',monospace}

/* ── MAIN COLUMN ── */
.main-col{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}

/* ── HEADER ── */
.hdr{
  background:var(--bg);border-bottom:1px solid var(--border);
  padding:0 24px;height:52px;flex-shrink:0;
  display:flex;align-items:center;justify-content:space-between;
  z-index:100;
}
.hdr-left{display:flex;align-items:center;gap:10px}
.menu-btn{
  width:28px;height:28px;border-radius:6px;
  border:1px solid var(--border);background:transparent;
  cursor:pointer;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:3.5px;flex-shrink:0;transition:background .15s;
}
.menu-btn:hover{background:var(--surf2)}
.menu-btn span{display:block;width:12px;height:1.5px;background:var(--text);border-radius:99px}
.hdr-title{font-size:13px;font-weight:500;letter-spacing:-.01em;color:var(--text)}
.hdr-sub{font-size:10px;color:var(--muted);margin-top:1px}
.hdr-right{display:flex;align-items:center;gap:8px}
.pill{
  display:flex;align-items:center;gap:5px;
  padding:4px 10px;border:1px solid var(--border);
  border-radius:99px;font-size:11px;color:var(--muted);
  background:var(--surface);font-family:'DM Mono',monospace;
}
.dot{width:5px;height:5px;border-radius:50%;background:var(--accent);animation:blink 2.5s ease infinite}
.dot.off{background:var(--danger);animation:none}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
.btn-sm{
  height:28px;padding:0 12px;border-radius:99px;
  border:1px solid var(--border);background:var(--surface);
  color:var(--muted);font-family:'DM Sans',sans-serif;
  font-size:11px;cursor:pointer;transition:all .15s;white-space:nowrap;
}
.btn-sm:hover{background:var(--surf2);color:var(--text)}
.badge-red{
  display:flex;align-items:center;gap:5px;
  padding:4px 10px;border-radius:99px;font-size:11px;font-weight:500;
  background:var(--danger2);color:var(--danger);
}

/* ── SCROLL AREA ── */
.scroll-area{flex:1;overflow-y:auto;scrollbar-width:thin;scrollbar-color:var(--faint) transparent}

/* ── HERO ── */
.hero{
  padding:32px 28px 20px;border-bottom:1px solid var(--border);
}
.hero-tag{
  display:inline-flex;align-items:center;gap:6px;
  font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--accent);font-weight:500;margin-bottom:10px;
}
.hero-tag span{width:16px;height:1px;background:var(--accent);display:inline-block}
.hero h1{font-size:26px;font-weight:300;letter-spacing:-.03em;line-height:1.1;margin-bottom:8px}
.hero h1 strong{font-weight:500}
.hero p{font-size:12px;color:var(--muted);max-width:460px;line-height:1.7}

/* ── TABS ── */
.tabs{
  padding:0 28px;border-bottom:1px solid var(--border);
  display:flex;gap:0;overflow-x:auto;scrollbar-width:none;flex-shrink:0;
}
.tabs::-webkit-scrollbar{display:none}
.tab-btn{
  padding:10px 14px;border:none;border-bottom:2px solid transparent;
  background:transparent;color:var(--muted);
  font-family:'DM Sans',sans-serif;font-size:12px;
  cursor:pointer;white-space:nowrap;transition:all .15s;
  display:flex;align-items:center;gap:6px;
}
.tab-btn:hover{color:var(--text)}
.tab-btn.active{color:var(--text);border-bottom-color:var(--accent);font-weight:500}
.tab-badge{width:5px;height:5px;border-radius:50%;background:var(--danger);display:inline-block}

/* ── CONTENT ── */
.content{padding:20px 28px 56px}

/* ── BANNER ── */
.banner{
  padding:11px 14px;border-radius:var(--r);border:1px solid;margin-bottom:14px;
  display:flex;align-items:flex-start;gap:10px;
}
.banner.danger{border-color:var(--danger);background:var(--danger2)}
.banner.warn{border-color:var(--warn);background:var(--warn2)}
.banner-ico{font-size:13px;margin-top:1px;flex-shrink:0}
.banner-ttl{font-size:12px;font-weight:500;margin-bottom:2px}
.banner.danger .banner-ttl{color:var(--danger)}
.banner.warn .banner-ttl{color:var(--warn)}
.banner-dsc{font-size:11px;color:var(--muted);line-height:1.5}

/* ── FILTRO ── */
.filtro-row{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.filtro-lbl{font-size:11px;color:var(--muted)}
.filtro-sel{
  background:var(--surface);border:1px solid var(--border);
  color:var(--text);padding:5px 12px;border-radius:99px;
  font-family:'DM Sans',sans-serif;font-size:11px;cursor:pointer;outline:none;
}

/* ── STATS ── */
.stats{
  display:grid;grid-template-columns:repeat(5,1fr);
  gap:1px;background:var(--border);
  border:1px solid var(--border);border-radius:var(--r);overflow:hidden;margin-bottom:16px;
}
.stat{background:var(--surface);padding:14px 16px}
.stat-lbl{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:7px;font-family:'DM Mono',monospace}
.stat-val{font-size:22px;font-weight:500;letter-spacing:-.03em;line-height:1}
.stat-val.g{color:var(--accent)}
.stat-val.w{color:var(--warn)}
.stat-val.d{color:var(--danger)}
.stat-unit{font-size:10px;color:var(--faint);margin-top:4px;font-family:'DM Mono',monospace}

/* ── CHART GRID ── */
.chart-grid{display:grid;grid-template-columns:1fr 240px;gap:14px;margin-bottom:14px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:16px 18px}
.card-hdr{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:3px}
.card-ttl{font-size:12px;font-weight:500}
.card-sub{font-size:11px;color:var(--muted);margin-bottom:14px}
.chart-wrap{height:200px}

/* ── NIVEL ── */
.nivel{display:flex;flex-direction:column;gap:16px;padding-top:4px}
.n-lbl{font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:4px;font-family:'DM Mono',monospace}
.n-val{font-size:18px;font-weight:500;letter-spacing:-.02em}
.n-bar{height:2px;background:var(--surf2);border-radius:99px;margin-top:7px;overflow:hidden}
.n-fill{height:100%;border-radius:99px;transition:width 1.2s cubic-bezier(.4,0,.2,1)}
.n-fill.g{background:var(--accent)}
.n-fill.w{background:var(--warn)}
.n-fill.d{background:var(--danger)}
.n-status{font-size:12px;font-weight:500;margin-top:3px}

/* ── MAPA ── */
.map-section{margin-top:20px;margin-bottom:8px}
.map-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;flex-wrap:wrap;gap:8px}
.map-header-left h3{font-size:13px;font-weight:500;margin-bottom:2px}
.map-header-left p{font-size:11px;color:var(--muted)}
.map-legend{display:flex;align-items:center;gap:14px}
.map-legend-item{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--muted)}
.map-dot-l{width:9px;height:9px;border-radius:50%}
.map-wrap{
  border:1px solid var(--border);border-radius:var(--r);
  overflow:hidden;height:420px;
}
#mapa-leaflet{width:100%;height:100%}

/* Leaflet popup */
.leaflet-popup-content-wrapper{
  font-family:'DM Sans',sans-serif !important;
  border-radius:10px !important;
  box-shadow:0 8px 32px rgba(0,0,0,.15) !important;
  padding:0 !important;overflow:hidden;
  border:1px solid #E2E0DA !important;
}
.leaflet-popup-tip-container{margin-top:-1px}
.leaflet-popup-content{margin:0 !important;min-width:230px}
.leaflet-popup-close-button{top:12px !important;right:12px !important;color:#8C8880 !important;font-size:18px !important;font-weight:300 !important;z-index:1}
.p-card{background:#fff;padding:16px 18px 18px}
.p-name{font-size:14px;font-weight:500;color:#1A1916;margin-bottom:4px;padding-right:20px}
.p-badge{display:inline-flex;align-items:center;gap:4px;font-size:10.5px;font-weight:500;padding:2px 8px;border-radius:99px;margin-bottom:10px}
.p-date{font-size:10px;color:#8C8880;font-family:'DM Mono',monospace;margin-bottom:10px;margin-top:-6px}
.p-metrics{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:10px}
.p-metric{background:#EFEFEB;border-radius:5px;padding:8px 10px}
.p-metric-lbl{font-size:9px;text-transform:uppercase;letter-spacing:.07em;color:#8C8880;margin-bottom:3px}
.p-metric-val{font-size:16px;font-weight:500;color:#1A1916;letter-spacing:-.02em}
.p-metric-unit{font-size:10px;color:#8C8880;font-weight:400}
.p-bar-labels{display:flex;justify-content:space-between;font-size:10px;color:#8C8880;margin-bottom:4px}
.p-bar-track{height:3px;border-radius:99px;background:#EFEFEB;overflow:hidden;margin-bottom:10px}
.p-bar-fill{height:100%;border-radius:99px}
.p-btn{display:block;width:100%;padding:8px 0;border-radius:5px;border:1px solid #E2E0DA;background:transparent;color:#1A6B3C;font-family:'DM Sans',sans-serif;font-size:11.5px;font-weight:500;cursor:pointer;text-align:center;transition:background .15s}
.p-btn:hover{background:#E8F5EE}

/* ── ALERTAS PAGE ── */
.al-cards{display:flex;flex-direction:column;gap:8px;margin-bottom:20px}
.al-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:12px 16px;display:flex;align-items:center;gap:12px;cursor:pointer;transition:background .15s;
}
.al-card:hover{background:var(--surf2)}
.al-card-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.al-card-name{font-size:12.5px;font-weight:500}
.al-card-desc{font-size:11px;color:var(--muted);margin-top:1px}
.al-card-cota{font-family:'DM Mono',monospace;font-size:14px;text-align:right;flex-shrink:0}

/* ── TABELA ── */
.tbl{width:100%;border-collapse:collapse}
.tbl th{font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding:7px 10px;text-align:left;border-bottom:1px solid var(--border);font-family:'DM Mono',monospace;font-weight:400}
.tbl td{padding:9px 10px;border-bottom:1px solid var(--border);font-size:12px;vertical-align:middle}
.tbl tr:last-child td{border-bottom:none}
.tbl tbody tr:hover td{background:var(--surf2);cursor:pointer}
.tbl-dot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:7px;vertical-align:middle}

/* ── SEC TITLE ── */
.sec-ttl{font-size:15px;font-weight:500;letter-spacing:-.02em;margin-bottom:4px}
.sec-sub{font-size:12px;color:var(--muted);margin-bottom:18px}

/* ── STATE ── */
.state{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:280px;gap:12px;color:var(--muted)}
.spinner{width:20px;height:20px;border-radius:50%;border:2px solid var(--border);border-top-color:var(--accent);animation:spin .6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes mapPulse{0%,100%{transform:scale(1);opacity:.4}50%{transform:scale(2.2);opacity:0}}

/* ── FOOTER ── */
.footer{border-top:1px solid var(--border);padding:12px 28px;text-align:center;font-size:10px;color:var(--faint);font-family:'DM Mono',monospace;flex-shrink:0}

@media(max-width:900px){
  .stats{grid-template-columns:repeat(3,1fr)}
  .chart-grid{grid-template-columns:1fr}
  .sidebar{position:fixed;top:0;bottom:0;left:0;z-index:300}
}
@media(max-width:600px){
  .hero{padding:20px 16px 16px}
  .tabs{padding:0 16px}
  .content{padding:14px 16px 48px}
  .stats{grid-template-columns:1fr 1fr}
  .hdr{padding:0 16px}
  .map-legend{display:none}
}
`;

/* ─── Config ──────────────────────────────────────────────────────────────── */
const ALERTAS = {
  "Manaus": { tipo: "danger", titulo: "Alerta de enchente — Manaus", desc: "Zona Sul com risco elevado. Nível acima da cota de atenção desde 24/04/2026." }
};

const CONFIG_ESTACOES = {
  "Manaus":      { lat: -3.10, lon: -60.02, rio: "Rio Negro",    cota_alerta: 29.00, cota_max: 29.97, estado: "AM" },
  "Itacoatiara": { lat: -3.14, lon: -58.44, rio: "Rio Amazonas", cota_alerta: 14.00, cota_max: 16.83, estado: "AM" },
  "Manacapuru":  { lat: -3.31, lon: -60.61, rio: "Rio Solimões", cota_alerta: 21.00, cota_max: 23.50, estado: "AM" },
  "Parintins":   { lat: -2.63, lon: -56.74, rio: "Rio Amazonas", cota_alerta: 11.50, cota_max: 13.80, estado: "AM" },
  "Óbidos":      { lat: -1.92, lon: -55.52, rio: "Rio Amazonas", cota_alerta:  9.00, cota_max: 11.20, estado: "PA" },
  "Tefé":        { lat: -3.37, lon: -64.72, rio: "Rio Solimões", cota_alerta: 14.50, cota_max: 17.50, estado: "AM" },
  "Santarém":    { lat: -2.44, lon: -54.70, rio: "Rio Amazonas", cota_alerta:  8.50, cota_max: 10.50, estado: "PA" },
  "Tabatinga":   { lat: -4.25, lon: -69.94, rio: "Rio Solimões", cota_alerta: 11.00, cota_max: 13.50, estado: "AM" },
};

const PERIODOS = [
  { label: 'Todos os dados', value: 0 },
  { label: 'Últimos 30 dias', value: 30 },
  { label: 'Últimos 60 dias', value: 60 },
  { label: 'Últimos 90 dias', value: 90 },
];

const BACIAS = {
  'Todas': null,
  'Alto Solimões': ['Tabatinga', 'Tefé'],
  'Médio Amazonas': ['Manaus', 'Manacapuru', 'Itacoatiara', 'Parintins'],
  'Baixo Amazonas': ['Óbidos', 'Santarém'],
};

const MAP_LAYERS = {
  'Padrão':  'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
  'Satélite':'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
  'Escuro':  'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
};

const NAV = [
  { id: 'dashboard', label: 'Dashboard',  d: 'M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z M9 22V12h6v10' },
  { id: 'alertas',   label: 'Alertas',    d: 'M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z M12 9v4 M12 17h.01', badge: true },
  { id: 'estacoes',  label: 'Estações',   d: 'M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z M12 10a2 2 0 100-4 2 2 0 000 4' },
];

const COR = { g: '#1A6B3C', w: '#F59E0B', d: '#DC2626' };
const fmtData = s => { if (!s) return ''; const [,m,d] = s.split('-'); return `${d}/${m}`; };

function classificar(cota, cfg) {
  if (!cfg) return { cls: 'g', txt: 'Normal', pct: 0 };
  const pct = Math.min((cota / cfg.cota_max) * 100, 100);
  if (cota >= cfg.cota_alerta * 1.2) return { cls: 'd', txt: 'Emergência', pct };
  if (cota >= cfg.cota_alerta)       return { cls: 'd', txt: 'Alerta',     pct };
  if (cota >= cfg.cota_alerta * 0.7) return { cls: 'w', txt: 'Atenção',    pct };
  return { cls: 'g', txt: 'Normal', pct };
}

function estimarPico(lista) {
  if (!lista || lista.length < 7) return null;
  const recente = lista.slice(-14);
  const diffs = recente.slice(1).map((d, i) => (d.cota_m ?? 0) - (recente[i].cota_m ?? 0));
  const tendencia = diffs.reduce((a, b) => a + b, 0) / diffs.length;
  const cotaAtual = lista[lista.length - 1]?.cota_m ?? 0;
  if (tendencia <= 0) return { data: 'Estável', cota: cotaAtual.toFixed(2), desc: 'Rio em queda ou estável' };
  const dataPico = new Date();
  dataPico.setDate(dataPico.getDate() + 30);
  return {
    data: dataPico.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' }),
    cota: Math.min(cotaAtual + tendencia * 30, 35).toFixed(2),
    desc: `+${tendencia.toFixed(3)} m/dia tendência`,
  };
}

function loadLeaflet(cb) {
  if (window.L) { cb(); return; }
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
  document.head.appendChild(link);
  const script = document.createElement('script');
  script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
  script.onload = cb;
  document.head.appendChild(script);
}

const Tip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:6, padding:'8px 12px', fontSize:11, boxShadow:'0 4px 20px rgba(0,0,0,.12)' }}>
      <p style={{ color:'var(--muted)', marginBottom:4, fontFamily:'DM Mono,monospace' }}>{label}</p>
      {payload.map((p, i) => <p key={i} style={{ color:p.color, fontWeight:500 }}>{p.name}: {(+p.value).toFixed(2)}</p>)}
    </div>
  );
};

const NavIco = ({ d }) => (
  <svg width="14" height="14" viewBox="0 0 24 24" className="nav-ico"><path d={d}/></svg>
);

/* ══════════════════════════════════════════════════════════════════════════ */
export default function App() {
  const [dados, setDados]       = useState({});
  const [estacoes, setEstacoes] = useState([]);
  const [cidade, setCidade]     = useState('');
  const [periodo, setPeriodo]   = useState(0);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState(null);
  const [tema, setTema]         = useState(() => localStorage.getItem('tema') || 'light');
  const [pagina, setPagina]     = useState('dashboard');
  const [sideOpen, setSideOpen] = useState(true);
  const [bacia, setBacia]       = useState('Todas');
  const [mapLayer, setMapLayer] = useState('Padrão');
  const [filterStatus, setFilterStatus] = useState('Todos');

  const mapaRef    = useRef(null);
  const mapaInst   = useRef(null);
  const markersRef = useRef([]);
  const tileRef    = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', tema);
    localStorage.setItem('tema', tema);
  }, [tema]);

  useEffect(() => {
    window.__selecionarEstacao = (nome) => {
      setCidade(nome);
      setPagina('dashboard');
      setTimeout(() => {
        document.getElementById('secao-dados')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 150);
    };
    return () => { delete window.__selecionarEstacao; };
  }, []);

  const carregar = async (est = cidade, dias = periodo) => {
    try {
      setLoading(true); setError(null);
      const [rE, rD] = await Promise.all([
        axios.get('/api/estacoes'),
        axios.get('/api/dados', { params: { ...(est && { estacao: est }), ...(dias > 0 && { dias }) } })
      ]);
      const lista = rE.data?.estacoes || [];
      setEstacoes(lista);
      setDados(rD.data);
      if (!est && lista.length) setCidade(lista[0]);
    } catch (e) { setError(e.message); }
    finally { setLoading(false); }
  };

  useEffect(() => { carregar('', 0); }, []);
  useEffect(() => { if (cidade) carregar(cidade, periodo); }, [cidade, periodo]);

  /* ── Inicializar mapa uma vez ── */
  useEffect(() => {
    loadLeaflet(() => {
      if (mapaInst.current || !mapaRef.current) return;
      const L = window.L;
      const map = L.map('mapa-leaflet', { zoomControl: true, scrollWheelZoom: false })
        .setView([-3.0, -60.5], 6);
      const tile = L.tileLayer(MAP_LAYERS['Padrão'], { attribution:'© OSM © CARTO', maxZoom:18 }).addTo(map);
      tileRef.current = tile;
      mapaInst.current = map;
      setDados(d => ({ ...d }));
    });
  }, []);

  /* ── Trocar camada ── */
  useEffect(() => {
    if (!window.L || !mapaInst.current || !tileRef.current) return;
    mapaInst.current.removeLayer(tileRef.current);
    tileRef.current = window.L.tileLayer(MAP_LAYERS[mapLayer], { attribution:'© OSM', maxZoom:18 }).addTo(mapaInst.current);
  }, [mapLayer]);

  /* ── Atualizar marcadores ── */
  useEffect(() => {
    if (!window.L || !mapaInst.current) return;
    const L = window.L;
    const map = mapaInst.current;
    markersRef.current.forEach(m => map.removeLayer(m));
    markersRef.current = [];

    const nomes = (estacoes.length ? estacoes : Object.keys(CONFIG_ESTACOES)).filter(nome => {
      if (bacia !== 'Todas' && BACIAS[bacia] && !BACIAS[bacia].includes(nome)) return false;
      if (filterStatus !== 'Todos') {
        const cfg2 = CONFIG_ESTACOES[nome];
        const lista2 = dados[nome]?.dados || [];
        const cota2 = lista2[lista2.length-1]?.cota_m ?? 0;
        const { cls: cls2 } = classificar(cota2, cfg2);
        const statusMap = { 'Alerta':'d', 'Atenção':'w', 'Normal':'g' };
        if (cls2 !== statusMap[filterStatus]) return false;
      }
      return true;
    });

    nomes.forEach(nome => {
      const cfg = CONFIG_ESTACOES[nome];
      if (!cfg) return;
      const info  = dados[nome] || {};
      const lista = info.dados  || [];
      const ult   = lista[lista.length - 1] || {};
      const cota  = ult.cota_m ?? 0;
      const vazao = ult.vazao  ?? 0;
      const { cls, txt: stTxt, pct } = classificar(cota, cfg);

      const COR_MAP  = { g: '#1A6B3C', w: '#F59E0B', d: '#DC2626' };
      const COR_BD   = { g: '#0f4023', w: '#92400e', d: '#7f1d1d' };
      const STBG     = { g: '#E8F5EE', w: '#FEF3C7', d: '#FEE2E2' };
      const STCLR    = { g: '#1A6B3C', w: '#B45309', d: '#B91C1C' };
      const cor = COR_MAP[cls];

      const pulso = cls !== 'g' ? `<div style="position:absolute;top:-5px;left:-5px;width:24px;height:24px;border-radius:50%;background:${cor};animation:mapPulse 1.8s ease-out infinite;"></div>` : '';

      const icon = L.divIcon({
        className: '',
        html: `<div style="position:relative;width:14px;height:14px;">${pulso}<div style="width:14px;height:14px;border-radius:50%;background:${cor};border:2.5px solid ${COR_BD[cls]};box-shadow:0 2px 8px rgba(0,0,0,.35);position:relative;z-index:1;"></div></div>`,
        iconSize: [14,14], iconAnchor: [7,7], popupAnchor: [0,-14],
      });

      const popupHTML = `
        <div class="p-card">
          <div class="p-name">${nome}</div>
          <div><span class="p-badge" style="background:${STBG[cls]};color:${STCLR[cls]}">● ${stTxt}</span></div>
          <div class="p-date">${ult.data || '—'} · ${cfg.estado}</div>
          <div class="p-metrics">
            <div class="p-metric"><div class="p-metric-lbl">Cota atual</div><div class="p-metric-val">${cota.toFixed(2)}<span class="p-metric-unit"> m</span></div></div>
            <div class="p-metric"><div class="p-metric-lbl">Cota alerta</div><div class="p-metric-val">${cfg.cota_alerta.toFixed(2)}<span class="p-metric-unit"> m</span></div></div>
            <div class="p-metric"><div class="p-metric-lbl">Vazão</div><div class="p-metric-val">${vazao > 1000 ? (vazao/1000).toFixed(1)+'k' : vazao > 0 ? vazao.toFixed(0) : '—'}<span class="p-metric-unit"> m³/s</span></div></div>
            <div class="p-metric"><div class="p-metric-lbl">Nível</div><div class="p-metric-val">${pct.toFixed(0)}<span class="p-metric-unit">%</span></div></div>
          </div>
          <div class="p-bar-labels"><span>0%</span><span>${pct.toFixed(0)}% do máximo</span></div>
          <div class="p-bar-track"><div class="p-bar-fill" style="width:${Math.min(pct,100).toFixed(1)}%;background:${cor}"></div></div>
          <button class="p-btn" onclick="window.__selecionarEstacao('${nome}')">Ver série histórica completa →</button>
        </div>
      `;

      const marker = L.marker([cfg.lat, cfg.lon], { icon })
        .bindPopup(popupHTML, { maxWidth:270, closeButton:true })
        .addTo(map);
      markersRef.current.push(marker);
    });
  }, [dados, estacoes, bacia, filterStatus]);

  /* ── Derivados ── */
  const info  = dados[cidade] || {};
  const lista = info.dados    || [];
  const ult   = lista[lista.length - 1] || {};
  const cota  = ult.cota_m ?? 0;
  const cfg   = CONFIG_ESTACOES[cidade];
  const { cls, txt: stTxt, pct } = classificar(cota, cfg);
  const stColor = cls === 'g' ? 'var(--accent)' : cls === 'w' ? 'var(--warn)' : 'var(--danger)';
  const al      = ALERTAS[cidade];
  const pico    = estimarPico(lista);
  const fonteLabel = { sace:'SACE/SGB', 'open-meteo':'Open-Meteo', fallback:'Cache local' }[info.fonte] || info.fonte || '—';

  const todasAlertas = estacoes.map(nome => {
    const d = dados[nome] || {};
    const l = d.dados || [];
    const co = l[l.length-1]?.cota_m ?? 0;
    const { cls: c, txt: t } = classificar(co, CONFIG_ESTACOES[nome]);
    return { nome, cota: co, status: t, cls: c };
  }).filter(e => e.cls !== 'g');

  const alertCount = todasAlertas.length;

  /* ── Loading/Error inicial ── */
  if (loading && !estacoes.length) return (
    <><style>{css}</style>
    <div className="state" style={{ minHeight:'100vh' }}>
      <div className="spinner"/><span style={{ fontSize:12 }}>Carregando…</span>
    </div></>
  );

  if (error && !estacoes.length) return (
    <><style>{css}</style>
    <div className="state" style={{ minHeight:'100vh' }}>
      <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:8, padding:24, maxWidth:380 }}>
        <p style={{ fontWeight:500, color:'var(--danger)', marginBottom:8 }}>Backend offline</p>
        <p style={{ fontSize:12, color:'var(--muted)', lineHeight:1.7 }}>
          Rode o servidor:<br/>
          <code style={{ display:'block', marginTop:8, fontSize:11, fontFamily:'DM Mono,monospace', background:'var(--surf2)', padding:'6px 10px', borderRadius:4 }}>
            python -m uvicorn backend.server:app --port 5000 --reload
          </code>
        </p>
        <button className="btn-sm" style={{ marginTop:14 }} onClick={() => carregar('', 0)}>Tentar novamente</button>
      </div>
    </div></>
  );

  /* ─────────────────────── PÁGINAS ─────────────────────── */

  /* DASHBOARD */
  const renderDashboard = () => (
    <>
      {/* Hero */}
      <div className="hero">
        <div className="hero-tag"><span/>Monitoramento · Amazonas · 2026</div>
        <h1>Nível do<br/><strong>Rio Amazonas</strong></h1>
        <p>Cotas em {estacoes.length} estações fluviométricas. Clique em um ponto no mapa para ver os dados.</p>
      </div>

      {/* Tabs de estação */}
      <nav className="tabs">
        {estacoes.map(c => (
          <button key={c} className={`tab-btn${c === cidade ? ' active' : ''}`} onClick={() => setCidade(c)}>
            {c}{ALERTAS[c] && <span className="tab-badge"/>}
          </button>
        ))}
      </nav>

      <div className="content">
        <div className="filtro-row">
          <span className="filtro-lbl">Período:</span>
          <select className="filtro-sel" value={periodo} onChange={e => setPeriodo(Number(e.target.value))}>
            {PERIODOS.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
          </select>
          {loading && <div className="spinner" style={{ width:16, height:16 }}/>}
        </div>

        {al && (
          <div className={`banner ${al.tipo}`}>
            <div className="banner-ico">⚠</div>
            <div>
              <div className="banner-ttl">{al.titulo}</div>
              <div className="banner-dsc">{al.desc}</div>
            </div>
          </div>
        )}

        {lista.length > 0 && (
          <div id="secao-dados">
            <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:14 }}>
              <div>
                <div style={{ fontSize:15, fontWeight:500, letterSpacing:'-.02em' }}>{cidade}</div>
                <div style={{ fontSize:11, color:'var(--muted)', marginTop:2 }}>
                  {cfg?.estado} · {cfg?.rio} · {ult.data || '—'} · <span style={{ color:stColor }}>{stTxt}</span>
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="stats">
              <div className="stat">
                <div className="stat-lbl">Cota Atual</div>
                <div className={`stat-val ${cls}`}>{cota.toFixed(2)}</div>
                <div className="stat-unit">metros</div>
              </div>
              <div className="stat">
                <div className="stat-lbl">Cota de Alerta</div>
                <div className="stat-val">{cfg?.cota_alerta?.toFixed(2) ?? '—'}</div>
                <div className="stat-unit">metros</div>
              </div>
              <div className="stat">
                <div className="stat-lbl">% do Máximo</div>
                <div className={`stat-val ${cls}`}>{pct.toFixed(0)}%</div>
                <div className="stat-unit">histórico</div>
              </div>
              <div className="stat">
                <div className="stat-lbl">Registros</div>
                <div className="stat-val">{lista.length}</div>
                <div className="stat-unit">dias</div>
              </div>
              <div className="stat">
                <div className="stat-lbl">Fonte</div>
                <div className="stat-val" style={{ fontSize:13, paddingTop:4 }}>{fonteLabel}</div>
                <div className="stat-unit">{info.fonte === 'sace' ? 'dados reais' : 'estimativa'}</div>
              </div>
            </div>

            {/* Painel visual */}
            <VisualPanel cota={cota} cfg={cfg} cls={cls} stTxt={stTxt} pct={pct} pico={pico} lista={lista} cidade={cidade}/>

            {/* Gráfico + painel */}
            <div className="chart-grid">
              <div className="card">
                <div className="card-hdr"><div className="card-ttl">Cota hídrica</div></div>
                <div className="card-sub">metros — {cidade}</div>
                <div className="chart-wrap">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={lista} margin={{ top:4, right:8, left:0, bottom:0 }}>
                      <CartesianGrid strokeDasharray="2 4" stroke="var(--border)" vertical={false}/>
                      <XAxis dataKey="data" tickFormatter={fmtData} tick={{ fontSize:10, fill:'var(--muted)', fontFamily:'DM Mono,monospace' }} axisLine={false} tickLine={false} interval="preserveStartEnd"/>
                      <YAxis tick={{ fontSize:10, fill:'var(--muted)', fontFamily:'DM Mono,monospace' }} axisLine={false} tickLine={false} width={38} domain={['auto','auto']}/>
                      <Tooltip content={<Tip/>}/>
                      {cfg && <ReferenceLine y={cfg.cota_alerta} stroke="var(--warn)" strokeDasharray="3 3" strokeWidth={1.5} label={{ value:'Alerta', position:'insideTopRight', fontSize:9, fill:'var(--warn)' }}/>}
                      {cfg && <ReferenceLine y={cfg.cota_max} stroke="var(--danger)" strokeDasharray="3 3" strokeWidth={1} label={{ value:'Máx hist.', position:'insideTopRight', fontSize:9, fill:'var(--danger)' }}/>}
                      <Line type="monotone" dataKey="cota_m" name="Cota (m)" stroke="var(--line1)" strokeWidth={1.5} dot={false} activeDot={{ r:4, strokeWidth:0 }}/>
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div style={{ display:'flex', flexDirection:'column', gap:14 }}>
                <div className="card" style={{ flex:1 }}>
                  <div className="card-ttl">Nível hídrico</div>
                  <div className="card-sub">status atual</div>
                  <div className="nivel">
                    <div>
                      <div className="n-lbl">Cota</div>
                      <div className="n-val">{cota.toFixed(2)} m</div>
                      <div className="n-bar"><div className={`n-fill ${cls}`} style={{ width:`${pct.toFixed(1)}%` }}/></div>
                    </div>
                    <div>
                      <div className="n-lbl">Margem p/ alerta</div>
                      <div className="n-val">{cfg ? Math.max(cfg.cota_alerta - cota, 0).toFixed(2) : '—'} m</div>
                      <div className="n-bar">
                        <div className="n-fill g" style={{ width:`${Math.min(((cota / (cfg?.cota_alerta || 1)) * 100), 100).toFixed(1)}%` }}/>
                      </div>
                    </div>
                    <div>
                      <div className="n-lbl">Status</div>
                      <div className="n-status" style={{ color:stColor }}>{stTxt}</div>
                    </div>
                  </div>
                </div>
                {pico && (
                  <div className="card">
                    <div className="card-ttl">Previsão de pico</div>
                    <div className="card-sub">estimativa por tendência</div>
                    <div style={{ display:'flex', flexDirection:'column', gap:10 }}>
                      <div><div className="n-lbl">Data estimada</div><div className="n-val" style={{ fontSize:16 }}>{pico.data}</div></div>
                      <div><div className="n-lbl">Cota estimada</div><div className="n-val" style={{ fontSize:16 }}>{pico.cota} m</div></div>
                      <div className="n-lbl" style={{ marginTop:2 }}>{pico.desc}</div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {!loading && lista.length === 0 && (
          <div className="state">
            <span style={{ fontSize:13 }}>Selecione uma estação nas abas acima.</span>
          </div>
        )}

        {/* ─── MAPA (sempre visível no dashboard, abaixo dos dados) ─── */}
        <div className="map-section">
          <div className="map-header">
            <div className="map-header-left">
              <h3>Estações fluviométricas — Bacia Amazônica</h3>
              <p>Clique em um ponto para ver os dados da estação</p>
            </div>
            <div style={{ display:'flex', alignItems:'center', gap:8, flexWrap:'wrap' }}>
              <select className="filtro-sel" value={bacia} onChange={e => setBacia(e.target.value)} style={{ fontSize:11 }}>
                {Object.keys(BACIAS).map(b => <option key={b} value={b}>{b}</option>)}
              </select>
              <select className="filtro-sel" value={filterStatus} onChange={e => setFilterStatus(e.target.value)} style={{ fontSize:11 }}>
                {['Todos','Normal','Atenção','Alerta'].map(s => <option key={s} value={s}>{s}</option>)}
              </select>
              <div style={{ display:'flex', gap:4 }}>
                {Object.keys(MAP_LAYERS).map(lbl => (
                  <button key={lbl} className="btn-sm"
                    style={{ background: mapLayer===lbl?'var(--accent)':'var(--surface)', color:mapLayer===lbl?'#fff':'var(--muted)', borderColor:mapLayer===lbl?'var(--accent)':'var(--border)', fontSize:10.5, padding:'0 9px' }}
                    onClick={() => setMapLayer(lbl)}
                  >{lbl}</button>
                ))}
              </div>
              <div className="map-legend">
                {[['#1A6B3C','Normal'],['#F59E0B','Atenção'],['#DC2626','Alerta']].map(([cor,lbl]) => (
                  <div key={lbl} className="map-legend-item">
                    <div className="map-dot-l" style={{ background:cor }}/>{lbl}
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="map-wrap">
            <div id="mapa-leaflet" ref={mapaRef}/>
          </div>
        </div>

      </div>
    </>
  );

  /* ALERTAS */
  const renderAlertas = () => (
    <div className="content">
      <div className="sec-ttl">Alertas ativos</div>
      <div className="sec-sub">Estações acima da cota de atenção</div>
      {todasAlertas.length === 0
        ? <div className="state"><span>✓ Nenhuma estação em alerta no momento.</span></div>
        : <div className="al-cards">
            {todasAlertas.map(e => (
              <div key={e.nome} className="al-card" onClick={() => { setCidade(e.nome); setPagina('dashboard'); }}>
                <div className="al-card-dot" style={{ background:COR[e.cls] }}/>
                <div style={{ flex:1, minWidth:0 }}>
                  <div className="al-card-name">{e.nome}</div>
                  <div className="al-card-desc">{CONFIG_ESTACOES[e.nome]?.rio} · {e.status}</div>
                </div>
                <div className="al-card-cota" style={{ color:COR[e.cls] }}>{e.cota.toFixed(2)} m</div>
              </div>
            ))}
          </div>
      }
      <div style={{ marginTop:20 }}>
        <div className="card-ttl" style={{ marginBottom:12 }}>Resumo todas as estações</div>
        <div className="card">
          <table className="tbl">
            <thead>
              <tr><th>Estação</th><th>Rio</th><th style={{ textAlign:'right' }}>Cota (m)</th><th style={{ textAlign:'right' }}>Alerta (m)</th><th style={{ textAlign:'right' }}>Status</th></tr>
            </thead>
            <tbody>
              {estacoes.map(nome => {
                const d = dados[nome] || {};
                const l = d.dados || [];
                const co = l[l.length-1]?.cota_m ?? 0;
                const { cls: c, txt: t } = classificar(co, CONFIG_ESTACOES[nome]);
                return (
                  <tr key={nome} onClick={() => { setCidade(nome); setPagina('dashboard'); }}>
                    <td style={{ fontWeight:500 }}><span className="tbl-dot" style={{ background:COR[c] }}/>{nome}</td>
                    <td style={{ color:'var(--muted)', fontSize:11 }}>{CONFIG_ESTACOES[nome]?.rio || '—'}</td>
                    <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace' }}>{co.toFixed(2)}</td>
                    <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', color:'var(--muted)' }}>{CONFIG_ESTACOES[nome]?.cota_alerta?.toFixed(2) || '—'}</td>
                    <td style={{ textAlign:'right', color:COR[c], fontWeight:500 }}>{t}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  /* ESTAÇÕES */
  const renderEstacoes = () => (
    <div className="content">
      <div className="sec-ttl">Estações fluviométricas</div>
      <div className="sec-sub">Rede de monitoramento · Bacia Amazônica</div>
      <div className="card">
        <table className="tbl">
          <thead>
            <tr>
              <th>Estação</th><th>Rio</th>
              <th style={{ textAlign:'right' }}>Lat</th>
              <th style={{ textAlign:'right' }}>Lon</th>
              <th style={{ textAlign:'right' }}>Alerta (m)</th>
              <th style={{ textAlign:'right' }}>Máx hist.</th>
              <th>Fonte</th>
              <th style={{ textAlign:'right' }}>Registros</th>
            </tr>
          </thead>
          <tbody>
            {estacoes.map(nome => {
              const d = dados[nome] || {};
              const cfg2 = CONFIG_ESTACOES[nome] || {};
              const co = d.dados?.[d.dados.length-1]?.cota_m ?? 0;
              const { cls: c } = classificar(co, cfg2);
              return (
                <tr key={nome} onClick={() => { setCidade(nome); setPagina('dashboard'); }}>
                  <td style={{ fontWeight:500 }}><span className="tbl-dot" style={{ background:COR[c] }}/>{nome}</td>
                  <td style={{ color:'var(--muted)', fontSize:11 }}>{cfg2.rio || '—'}</td>
                  <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', fontSize:11, color:'var(--muted)' }}>{cfg2.lat?.toFixed(2)}</td>
                  <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', fontSize:11, color:'var(--muted)' }}>{cfg2.lon?.toFixed(2)}</td>
                  <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace' }}>{cfg2.cota_alerta?.toFixed(2) || '—'}</td>
                  <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace' }}>{cfg2.cota_max?.toFixed(2) || '—'}</td>
                  <td><span style={{ fontSize:10, padding:'2px 7px', borderRadius:99, background:'var(--accent2)', color:'var(--accent)' }}>{{ sace:'SACE', 'open-meteo':'Open-Meteo', fallback:'Cache' }[d.fonte] || d.fonte || '—'}</span></td>
                  <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', color:'var(--muted)' }}>{d.dados?.length || 0}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );

  const pageLabels = {
    dashboard: `Dashboard · ${cidade}`,
    alertas:   'Alertas',
    estacoes:  'Estações',
  };

  return (
    <>
      <style>{css}</style>
      <div className="shell">

        {/* SIDEBAR */}
        <aside className={`sidebar${sideOpen ? '' : ' closed'}`}>
          <div className="sid-logo">
            <div className="sid-mark">
              <svg viewBox="0 0 14 14"><path d="M1 8 Q3.5 4 7 8 Q10.5 12 13 8"/></svg>
            </div>
            <div>
              <div className="sid-name">Rio Amazonas</div>
              <div className="sid-sub">Monitor</div>
            </div>
          </div>

          <div className="sid-sec">
            <div className="sid-sec-lbl">Navegação</div>
            {NAV.map(n => (
              <button key={n.id} className={`nav-btn${pagina === n.id ? ' active' : ''}`} onClick={() => setPagina(n.id)}>
                <NavIco d={n.d}/>
                {n.label}
                {n.badge && alertCount > 0 && <span className="nav-badge">{alertCount}</span>}
              </button>
            ))}
          </div>

          <div className="sid-footer">
            <div className="sid-status">
              <span className={`s-dot${error ? ' off' : ''}`}/>
              <span className="s-txt">{error ? 'Offline' : 'Ao vivo'}</span>
              <span className="s-val">SACE/SGB</span>
            </div>
          </div>
        </aside>

        {/* MAIN */}
        <div className="main-col">

          {/* Header */}
          <header className="hdr">
            <div className="hdr-left">
              <button className="menu-btn" onClick={() => setSideOpen(o => !o)}>
                <span/><span/><span/>
              </button>
              <div>
                <div className="hdr-title">{pageLabels[pagina]}</div>
                <div className="hdr-sub">{estacoes.length} estações · {new Date().toLocaleDateString('pt-BR', { day:'2-digit', month:'long', year:'numeric' })}</div>
              </div>
            </div>
            <div className="hdr-right">
              {alertCount > 0 && <span className="badge-red">⚠ {alertCount} alerta{alertCount > 1 ? 's' : ''}</span>}
              {loading && <div className="spinner" style={{ width:16, height:16 }}/>}
              <button className="btn-sm" onClick={() => carregar(cidade, periodo)}>↻ Atualizar</button>
              <button className="btn-sm" onClick={() => setTema(t => t === 'dark' ? 'light' : 'dark')}>
                {tema === 'dark' ? '☀ Claro' : '◐ Escuro'}
              </button>
            </div>
          </header>

          {/* Scroll area */}
          <div className="scroll-area">
            {pagina === 'dashboard' && renderDashboard()}
            {pagina === 'alertas'   && renderAlertas()}
            {pagina === 'estacoes'  && renderEstacoes()}
            <footer className="footer">
              Rio Amazonas · Dados via SACE/SGB · {new Date().toLocaleDateString('pt-BR', { day:'2-digit', month:'long', year:'numeric' })}
            </footer>
          </div>

        </div>
      </div>
    </>
  );
}

/* ─── VisualPanel ────────────────────────────────────────────────────────── */
function VisualPanel({ cota, cfg, cls, stTxt, pct, pico, lista, cidade }) {
  if (!cfg) return null;
  const margem = Math.max(cfg.cota_alerta - cota, 0);
  const tendencia = (() => {
    if (lista.length < 4) return 0;
    const r = lista.slice(-7);
    const d = r.slice(1).map((x, i) => (x.cota_m ?? 0) - (r[i].cota_m ?? 0));
    return d.reduce((a, b) => a + b, 0) / d.length;
  })();
  const tendTxt = tendencia > 0.05 ? '↑ Subindo' : tendencia < -0.05 ? '↓ Descendo' : '→ Estável';
  const tendClr = tendencia > 0.05 ? 'var(--danger)' : tendencia < -0.05 ? 'var(--accent)' : 'var(--muted)';
  const semaforo = { g:{ cor:'#16a34a', emoji:'🟢', msg:'Situação Normal' }, w:{ cor:'#d97706', emoji:'🟡', msg:'Requer Atenção' }, d:{ cor:'#dc2626', emoji:'🔴', msg:'Alerta — Risco Elevado' } }[cls];
  const altPct = Math.min(pct, 100);
  const altClr = cls==='g' ? '#3b82f6' : cls==='w' ? '#f59e0b' : '#ef4444';
  const alertaPct = Math.min((cfg.cota_alerta / cfg.cota_max) * 100, 100);
  const spark = lista.slice(-14).map(d => ({ v: d.cota_m ?? 0 }));

  return (
    <div style={{ marginBottom:14 }}>
      <div style={{ display:'flex', alignItems:'center', gap:8, marginBottom:10 }}>
        <div style={{ width:3, height:14, borderRadius:2, background:'var(--accent)' }}/>
        <span style={{ fontSize:11, fontWeight:500, color:'var(--muted)', textTransform:'uppercase', letterSpacing:'.06em' }}>
          Resumo Visual — {cidade}
        </span>
      </div>
      <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr 1fr 170px', gap:10 }}>

        {/* Semáforo */}
        <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:'var(--r)', padding:'16px 18px', display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', gap:8 }}>
          <div style={{ fontSize:44, lineHeight:1 }}>{semaforo.emoji}</div>
          <div style={{ fontSize:12, fontWeight:600, color:semaforo.cor, textAlign:'center' }}>{semaforo.msg}</div>
          <div style={{ fontSize:11, color:'var(--muted)', textAlign:'center', lineHeight:1.5 }}>
            {cls==='g' && 'Rio dentro do nível esperado para esta época.'}
            {cls==='w' && `Faltam apenas ${margem.toFixed(2)}m para o nível de alerta.`}
            {cls==='d' && 'Cota de alerta ultrapassada. Risco de inundação.'}
          </div>
        </div>

        {/* Régua */}
        <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:'var(--r)', padding:'16px 18px' }}>
          <div style={{ fontSize:10, fontWeight:500, marginBottom:10, color:'var(--muted)', textTransform:'uppercase', letterSpacing:'.06em' }}>Altura do Rio</div>
          <div style={{ display:'flex', gap:12, alignItems:'flex-end' }}>
            <div style={{ position:'relative', width:28, height:110, background:'var(--surf2)', borderRadius:5, overflow:'hidden', flexShrink:0 }}>
              <div style={{ position:'absolute', bottom:0, left:0, right:0, background:altClr, height:`${altPct}%`, borderRadius:'0 0 5px 5px', transition:'height 1.5s cubic-bezier(.4,0,.2,1)', opacity:.85 }}/>
              <div style={{ position:'absolute', left:0, right:0, bottom:`${alertaPct}%`, height:'1.5px', background:'var(--warn)', zIndex:2 }}/>
              <div style={{ position:'absolute', left:0, right:0, bottom:`${alertaPct}%`, fontSize:7, color:'var(--warn)', paddingLeft:2, lineHeight:1, zIndex:2, whiteSpace:'nowrap', transform:'translateY(-2px)' }}>alerta</div>
            </div>
            <div>
              <div style={{ fontSize:26, fontWeight:500, letterSpacing:'-.03em', color:altClr, lineHeight:1 }}>{cota.toFixed(2)}</div>
              <div style={{ fontSize:11, color:'var(--muted)', marginTop:3 }}>metros</div>
              <div style={{ marginTop:8, fontSize:11, color:'var(--muted)' }}>Máx: <strong>{cfg.cota_max.toFixed(2)}m</strong></div>
              <div style={{ fontSize:11, color:'var(--muted)' }}>Alerta: <strong style={{ color:'var(--warn)' }}>{cfg.cota_alerta.toFixed(2)}m</strong></div>
            </div>
          </div>
        </div>

        {/* Tendência */}
        <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:'var(--r)', padding:'16px 18px', display:'flex', flexDirection:'column', gap:14 }}>
          <div>
            <div style={{ fontSize:10, color:'var(--muted)', textTransform:'uppercase', letterSpacing:'.06em', marginBottom:5 }}>Tendência (7 dias)</div>
            <div style={{ fontSize:20, fontWeight:500, color:tendClr }}>{tendTxt}</div>
            <div style={{ fontSize:11, color:'var(--muted)', marginTop:3 }}>{Math.abs(tendencia).toFixed(3)} m/dia</div>
          </div>
          <div>
            <div style={{ fontSize:10, color:'var(--muted)', textTransform:'uppercase', letterSpacing:'.06em', marginBottom:5 }}>Margem p/ Alerta</div>
            <div style={{ fontSize:20, fontWeight:500, color: margem < 1 ? 'var(--danger)' : margem < 3 ? 'var(--warn)' : 'var(--accent)' }}>{margem.toFixed(2)} m</div>
            <div style={{ fontSize:11, color:'var(--muted)', marginTop:3 }}>{margem < 0.5 ? '⚠ Crítico' : margem < 2 ? 'Monitorar' : 'Seguro'}</div>
          </div>
        </div>

        {/* Spark + pico */}
        <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:'var(--r)', padding:'16px 18px', display:'flex', flexDirection:'column', gap:12 }}>
          <div>
            <div style={{ fontSize:10, color:'var(--muted)', textTransform:'uppercase', letterSpacing:'.06em', marginBottom:7 }}>Últimos 14 dias</div>
            <div style={{ height:48 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={spark} margin={{ top:2, right:2, left:2, bottom:2 }}>
                  <Line type="monotone" dataKey="v" stroke={altClr} strokeWidth={1.5} dot={false}/>
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
          {pico && (
            <div>
              <div style={{ fontSize:10, color:'var(--muted)', textTransform:'uppercase', letterSpacing:'.06em', marginBottom:5 }}>Pico estimado</div>
              <div style={{ fontSize:14, fontWeight:500 }}>{pico.data}</div>
              <div style={{ fontSize:12, color: cls==='g' ? 'var(--accent)' : 'var(--warn)', marginTop:2 }}>{pico.cota} m</div>
              <div style={{ fontSize:10, color:'var(--muted)', marginTop:2 }}>{pico.desc}</div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
