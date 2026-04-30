import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts';

/* ─── CSS ─────────────────────────────────────────────────────────────────── */
const css = `
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg:      #F5F3EF;
  --surface: #FFFFFF;
  --surf2:   #EEEBE4;
  --border:  rgba(26,23,20,0.08);
  --bordm:   rgba(26,23,20,0.14);
  --text:    #1A1714;
  --muted:   #8A8278;
  --faint:   #C2BCB2;
  --teal:    #1B7C6C;
  --tealL:   #E3F2EF;
  --amber:   #C47A1E;
  --amberL:  #FBF0DF;
  --red:     #C0392B;
  --redL:    #FCEAE8;
  --green:   #2A7A3A;
  --sid:     #141210;
  --sid2:    #1C1A17;
  --r: 8px;
}
[data-theme=dark]{
  --bg:      #0F0E0C;
  --surface: #1A1916;
  --surf2:   #232018;
  --border:  rgba(255,255,255,0.07);
  --bordm:   rgba(255,255,255,0.13);
  --text:    #EDE9E1;
  --muted:   #7A7268;
  --faint:   #4A4438;
  --teal:    #3DB89A;
  --tealL:   rgba(27,124,108,0.15);
  --amber:   #D4921E;
  --amberL:  rgba(196,122,30,0.15);
  --red:     #D94F3D;
  --redL:    rgba(192,57,43,0.12);
  --green:   #3A9A4A;
  --sid:     #0D0C0A;
  --sid2:    #161410;
}

*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  font-family:'DM Sans',system-ui,sans-serif;
  font-size:13px;line-height:1.5;
  background:var(--bg);color:var(--text);
  -webkit-font-smoothing:antialiased;
  transition:background .2s,color .2s;
}

/* SHELL */
.shell{display:flex;height:100vh;overflow:hidden}

/* SIDEBAR */
.sidebar{
  width:210px;flex-shrink:0;
  background:var(--sid);
  display:flex;flex-direction:column;
  border-right:1px solid rgba(255,255,255,.04);
  overflow:hidden;
  transition:width .25s cubic-bezier(.4,0,.2,1);
}
.sidebar.closed{width:0}

.sid-logo{
  padding:18px 16px 14px;
  border-bottom:1px solid rgba(255,255,255,.05);
  display:flex;align-items:center;gap:10px;
  flex-shrink:0;
}
.sid-mark{
  width:30px;height:30px;background:var(--teal);
  border-radius:7px;display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.sid-mark svg{width:14px;height:14px;stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round}
.sid-name{font-size:12.5px;font-weight:500;color:#EDE9E1;white-space:nowrap;letter-spacing:-.01em}
.sid-sub{font-size:9px;color:rgba(255,255,255,.25);text-transform:uppercase;letter-spacing:.06em;margin-top:1px}

.sid-sec{padding:14px 10px 4px}
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
.nav-btn.active{background:rgba(61,184,154,.12);color:#5DD5C4}
.nav-ico{width:15px;height:15px;flex-shrink:0;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.nav-badge{
  margin-left:auto;background:var(--red);color:#fff;
  font-size:9px;font-weight:600;padding:1px 5px;border-radius:99px;min-width:16px;text-align:center;
}

.sid-footer{
  margin-top:auto;padding:12px 10px;
  border-top:1px solid rgba(255,255,255,.05);flex-shrink:0;
}
.sid-status{
  display:flex;align-items:center;gap:8px;
  padding:7px 10px;background:rgba(255,255,255,.03);border-radius:6px;
}
.s-dot{width:6px;height:6px;border-radius:50%;background:#3DB87C;animation:blink 2.5s ease infinite;flex-shrink:0}
.s-dot.off{background:var(--red);animation:none}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
.s-txt{font-size:11px;color:rgba(255,255,255,.3);white-space:nowrap}
.s-val{font-size:10px;color:rgba(255,255,255,.45);margin-left:auto;font-family:'DM Mono',monospace}

/* MAIN */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}

/* TOPBAR */
.topbar{
  background:var(--surface);border-bottom:1px solid var(--border);
  padding:10px 20px;display:flex;align-items:center;gap:12px;flex-shrink:0;
}
.menu-btn{
  width:30px;height:30px;border-radius:6px;
  border:1px solid var(--bordm);background:transparent;
  cursor:pointer;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:4px;flex-shrink:0;transition:background .15s;
}
.menu-btn:hover{background:var(--surf2)}
.menu-btn span{display:block;width:13px;height:1.5px;background:var(--text);border-radius:99px}
.topbar-info{flex:1;min-width:0}
.topbar-ttl{font-size:14px;font-weight:500;letter-spacing:-.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.topbar-sub{font-size:11px;color:var(--muted);margin-top:1px}
.topbar-right{display:flex;align-items:center;gap:8px;flex-shrink:0}

.badge{font-size:11px;font-weight:500;padding:3px 9px;border-radius:99px;white-space:nowrap}
.b-red  {background:var(--redL);color:var(--red)}
.b-teal {background:var(--tealL);color:var(--teal)}
.b-amb  {background:var(--amberL);color:var(--amber)}

.btn-sm{
  padding:5px 12px;border-radius:99px;
  border:1px solid var(--bordm);background:var(--surface);
  color:var(--muted);font-family:inherit;font-size:11px;
  cursor:pointer;transition:all .15s;white-space:nowrap;
}
.btn-sm:hover{background:var(--surf2);color:var(--text)}

.filtro-sel{
  background:var(--surface);border:1px solid var(--bordm);
  color:var(--text);padding:5px 11px;border-radius:99px;
  font-family:inherit;font-size:11px;cursor:pointer;outline:none;
}

/* SCROLL */
.scroll{flex:1;overflow-y:auto;padding:18px 22px 56px;scrollbar-width:thin;scrollbar-color:var(--faint) transparent}

/* CITY TABS — aba inferior */
.city-tabs{
  display:flex;gap:0;overflow-x:auto;scrollbar-width:none;
  border-bottom:1px solid var(--border);margin-bottom:18px;
}
.city-tabs::-webkit-scrollbar{display:none}
.c-tab{
  padding:9px 14px;border:none;border-bottom:2px solid transparent;
  background:transparent;font-family:inherit;font-size:12px;
  color:var(--muted);cursor:pointer;white-space:nowrap;
  transition:all .15s;display:flex;align-items:center;gap:5px;flex-shrink:0;
}
.c-tab:hover{color:var(--text)}
.c-tab.active{color:var(--text);border-bottom-color:var(--teal);font-weight:500}
.c-tab .cdot{width:5px;height:5px;border-radius:50%;background:var(--red);display:inline-block}

/* ALERTA BAR */
.al-bar{
  display:flex;align-items:flex-start;gap:10px;
  padding:10px 14px;border-radius:var(--r);
  border-left:3px solid var(--red);background:var(--redL);
  margin-bottom:16px;
}
.al-bar.warn{border-left-color:var(--amber);background:var(--amberL)}
.al-ico{font-size:13px;flex-shrink:0;margin-top:1px}
.al-ttl{font-size:12px;font-weight:500;color:var(--red);margin-bottom:2px}
.al-bar.warn .al-ttl{color:var(--amber)}
.al-dsc{font-size:11px;color:var(--muted);line-height:1.5}

/* FILTRO */
.filtro-row{display:flex;align-items:center;gap:10px;margin-bottom:16px}
.filtro-lbl{font-size:11px;color:var(--muted)}

/* KPI GRID */
.kpi-grid{
  display:grid;grid-template-columns:repeat(4,1fr);
  background:var(--border);gap:1px;
  border:1px solid var(--border);border-radius:var(--r);
  overflow:hidden;margin-bottom:16px;
}
.kpi{background:var(--surface);padding:14px 16px}
.kpi-lbl{font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:7px;font-family:'DM Mono',monospace}
.kpi-val{font-size:22px;font-weight:500;letter-spacing:-.03em;line-height:1;color:var(--text)}
.kpi-val.g{color:var(--teal)}
.kpi-val.w{color:var(--amber)}
.kpi-val.d{color:var(--red)}
.kpi-unit{font-size:10px;color:var(--faint);margin-top:4px;font-family:'DM Mono',monospace}
.kpi-change{font-size:10px;margin-top:4px;display:flex;align-items:center;gap:3px}
.ku{color:var(--red)}.kd{color:var(--green)}.kn{color:var(--muted)}

/* CHART GRID */
.chart-grid{display:grid;grid-template-columns:1fr 230px;gap:12px;margin-bottom:12px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:15px 17px}
.card-hdr{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px}
.card-ttl{font-size:12.5px;font-weight:500}
.card-sub{font-size:11px;color:var(--muted);margin-top:2px}
.chart-box{height:190px}

/* NIVEL */
.nivel{display:flex;flex-direction:column;gap:15px}
.n-lbl{font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:4px;font-family:'DM Mono',monospace}
.n-val{font-size:17px;font-weight:500;letter-spacing:-.02em}
.n-bar{height:3px;background:var(--surf2);border-radius:99px;margin-top:7px;overflow:hidden}
.n-fill{height:100%;border-radius:99px;transition:width 1.3s cubic-bezier(.4,0,.2,1)}
.n-fill.g{background:var(--teal)}.n-fill.w{background:var(--amber)}.n-fill.d{background:var(--red)}
.n-status{font-size:12px;font-weight:500;margin-top:3px}

/* PICO */
.pico{display:flex;flex-direction:column;gap:11px}

/* TABELA ESTAÇÕES */
.est-tbl{width:100%;border-collapse:collapse}
.est-tbl th{font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding:7px 10px;text-align:left;border-bottom:1px solid var(--border);font-family:'DM Mono',monospace;font-weight:400}
.est-tbl td{padding:9px 10px;border-bottom:1px solid var(--border);font-size:12px;vertical-align:middle}
.est-tbl tr:last-child td{border-bottom:none}
.est-tbl tbody tr:hover td{background:var(--surf2);cursor:pointer}
.tbl-dot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:7px;vertical-align:middle}

/* MAPA */
.map-hdr{display:flex;align-items:baseline;gap:10px;margin-bottom:12px}
.map-ttl{font-size:13px;font-weight:500}
.map-sub{font-size:11px;color:var(--muted)}
.map-wrap{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;height:360px}
#mapa-leaflet{width:100%;height:100%}

/* Leaflet label personalizado */
.leaflet-tooltip.city-lbl{
  background:rgba(255,255,255,.9)!important;
  border:none!important;box-shadow:none!important;
  color:#1A1714;font-size:10px;font-weight:500;
  padding:2px 6px;border-radius:4px;
  font-family:'DM Sans',sans-serif;
}
.leaflet-tooltip.city-lbl::before{display:none!important}

/* ALERTAS PAGE */
.al-cards{display:flex;flex-direction:column;gap:8px;margin-bottom:20px}
.al-card{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--r);
  padding:12px 16px;display:flex;align-items:center;gap:12px;cursor:pointer;transition:background .15s;
}
.al-card:hover{background:var(--surf2)}
.al-card-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.al-card-name{font-size:12.5px;font-weight:500}
.al-card-desc{font-size:11px;color:var(--muted);margin-top:1px}
.al-card-cota{font-family:'DM Mono',monospace;font-size:13px;text-align:right;flex-shrink:0}

/* SEC TITLE */
.sec-ttl{font-size:15px;font-weight:500;letter-spacing:-.02em;margin-bottom:4px}
.sec-sub{font-size:12px;color:var(--muted);margin-bottom:18px}

/* ESTADO */
.state{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:300px;gap:12px;color:var(--muted);text-align:center}
.spinner{width:22px;height:22px;border-radius:50%;border:2px solid var(--border);border-top-color:var(--teal);animation:spin .6s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* FOOTER */
.footer{border-top:1px solid var(--border);padding:11px 22px;text-align:center;font-size:10px;color:var(--faint);font-family:'DM Mono',monospace;flex-shrink:0}

@media(max-width:900px){
  .kpi-grid{grid-template-columns:repeat(2,1fr)}
  .chart-grid{grid-template-columns:1fr}
}
@media(max-width:600px){
  .scroll{padding:12px 14px 48px}
  .topbar{padding:8px 14px}
  .kpi-grid{grid-template-columns:1fr 1fr}
}
`;

/* ─── Config ──────────────────────────────────────────────────────────────── */
const ALERTAS_FIXOS = {
  "Manaus": { tipo:"danger", titulo:"Alerta de enchente — Manaus", desc:"Zona Sul com risco elevado. Nível acima da cota de atenção desde 24/04/2026." }
};

const CFG = {
  "Manaus":      { lat:-3.10, lon:-60.02, rio:"Rio Negro",    cota_alerta:29.00, cota_max:29.97 },
  "Itacoatiara": { lat:-3.14, lon:-58.44, rio:"Rio Amazonas", cota_alerta:14.00, cota_max:16.83 },
  "Manacapuru":  { lat:-3.31, lon:-60.61, rio:"Rio Solimões", cota_alerta:21.00, cota_max:23.50 },
  "Parintins":   { lat:-2.63, lon:-56.74, rio:"Rio Amazonas", cota_alerta:11.50, cota_max:13.80 },
  "Óbidos":      { lat:-1.92, lon:-55.52, rio:"Rio Amazonas", cota_alerta: 9.00, cota_max:11.20 },
  "Tefé":        { lat:-3.37, lon:-64.72, rio:"Rio Solimões", cota_alerta:14.50, cota_max:17.50 },
  "Santarém":    { lat:-2.44, lon:-54.70, rio:"Rio Amazonas", cota_alerta: 8.50, cota_max:10.50 },
  "Tabatinga":   { lat:-4.25, lon:-69.94, rio:"Rio Solimões", cota_alerta:11.00, cota_max:13.50 },
};

const PERIODOS = [
  { label:'Todos os dados', value:0 },
  { label:'Últimos 30 dias', value:30 },
  { label:'Últimos 60 dias', value:60 },
  { label:'Últimos 90 dias', value:90 },
];

const NAV = [
  { id:'dashboard', label:'Dashboard',
    d:'M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z M9 22V12h6v10' },
  { id:'alertas',   label:'Alertas',
    d:'M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z M12 9v4 M12 17h.01', badge:true },
  { id:'estacoes',  label:'Estações',
    d:'M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z M12 10a2 2 0 100-4 2 2 0 000 4' },
  { id:'mapa',      label:'Mapa',
    d:'M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3V6z M9 3v15 M15 6v15' },
];

const COR = { g:'#1B7C6C', w:'#C47A1E', d:'#C0392B' };
const fmtD = s => { if (!s) return ''; const [,m,d] = s.split('-'); return `${d}/${m}`; };

function classificar(cota, cfg) {
  if (!cfg) return { c:'g', t:'Normal', pct:0 };
  const pct = Math.min((cota / cfg.cota_max) * 100, 100);
  if (cota >= cfg.cota_alerta * 1.2) return { c:'d', t:'Emergência', pct };
  if (cota >= cfg.cota_alerta)       return { c:'d', t:'Alerta',     pct };
  if (cota >= cfg.cota_alerta * 0.7) return { c:'w', t:'Atenção',    pct };
  return { c:'g', t:'Normal', pct };
}

function estimarPico(lista) {
  if (!lista || lista.length < 7) return null;
  const rec = lista.slice(-14);
  const diffs = rec.slice(1).map((d,i) => (d.cota_m??0) - (rec[i].cota_m??0));
  const tend = diffs.reduce((a,b) => a+b, 0) / diffs.length;
  const cotaAtual = lista[lista.length-1]?.cota_m ?? 0;
  if (tend <= 0) return { data:'Estável', cota:cotaAtual.toFixed(2), desc:'Rio em queda ou estável' };
  const dias = Math.min(30, Math.round(14 + Math.abs(cotaAtual / (tend||0.001))));
  const cotaPico = Math.min(cotaAtual + tend * dias, 38);
  const dt = new Date(); dt.setDate(dt.getDate() + dias);
  return {
    data: dt.toLocaleDateString('pt-BR', { day:'2-digit', month:'short' }),
    cota: cotaPico.toFixed(2),
    desc: `${tend > 0 ? '+' : ''}${tend.toFixed(3)} m/dia`
  };
}

/* ─── Tooltip ─────────────────────────────────────────────────────────────── */
const Tip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background:'var(--surface)', border:'1px solid var(--bordm)', borderRadius:6, padding:'8px 12px', fontSize:11, boxShadow:'0 4px 16px rgba(0,0,0,.08)' }}>
      <p style={{ color:'var(--muted)', marginBottom:4, fontFamily:'DM Mono,monospace' }}>{label}</p>
      {payload.map((p,i) => <p key={i} style={{ color:p.color, fontWeight:500 }}>{p.name}: {(+p.value).toFixed(2)}</p>)}
    </div>
  );
};

const Ico = ({ d }) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="nav-ico">
    <path d={d}/>
  </svg>
);

/* ══════════════════════════════════════════════════════════════════════════ */
export default function App() {
  const [dados,    setDados]    = useState({});
  const [estacoes, setEstacoes] = useState([]);
  const [cidade,   setCidade]   = useState('');
  const [periodo,  setPeriodo]  = useState(0);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState(null);
  const [tema,     setTema]     = useState(() => localStorage.getItem('tema') || 'light');
  const [pagina,   setPagina]   = useState('dashboard');
  const [sideOpen, setSideOpen] = useState(true);

  const mapaRef  = useRef(null);
  const mapaInst = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', tema);
    localStorage.setItem('tema', tema);
  }, [tema]);

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

  /* ── Mapa ── */
  const buildMap = (dadosAtual) => {
    const L = window.L;
    const el = document.getElementById('mapa-leaflet');
    if (!L || !el) return;
    if (mapaInst.current) { mapaInst.current.remove(); mapaInst.current = null; }

    const map = L.map('mapa-leaflet', { zoomControl:true, scrollWheelZoom:false }).setView([-3.5, -62], 5);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution:'© CartoDB', maxZoom:14
    }).addTo(map);

    Object.entries(CFG).forEach(([nome, cfg]) => {
      const info  = dadosAtual[nome] || {};
      const lista = info.dados || [];
      const cota  = lista[lista.length-1]?.cota_m ?? 0;
      const { c } = classificar(cota, cfg);
      const cor   = COR[c];

      const icon = L.divIcon({
        className: '',
        html: `<div style="width:12px;height:12px;border-radius:50%;background:${cor};border:2.5px solid #fff;box-shadow:0 1px 5px rgba(0,0,0,.3)"></div>`,
        iconSize: [12,12], iconAnchor: [6,6]
      });

      const marker = L.marker([cfg.lat, cfg.lon], { icon }).addTo(map);

      /* Popup ao hover */
      marker.bindTooltip(
        `<b>${nome}</b> — ${cota.toFixed(2)} m<br/><span style="color:${cor}">${c==='g'?'Normal':c==='w'?'Atenção':'Alerta'}</span>`,
        { direction:'top', offset:[0,-6] }
      );

      /* Label permanente com o nome da cidade */
      L.tooltip({ permanent:true, direction:'right', offset:[8,0], className:'city-lbl' })
        .setLatLng([cfg.lat, cfg.lon])
        .setContent(nome)
        .addTo(map);

      marker.on('click', () => { setCidade(nome); setPagina('dashboard'); });
    });

    mapaInst.current = map;
  };

  useEffect(() => {
    if (pagina !== 'mapa' && pagina !== 'dashboard') return;
    const timer = setTimeout(() => {
      if (!document.getElementById('mapa-leaflet')) return;
      if (window.L) { buildMap(dados); return; }
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      document.head.appendChild(link);
      const sc = document.createElement('script');
      sc.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      sc.onload = () => buildMap(dados);
      document.head.appendChild(sc);
    }, 150);
    return () => clearTimeout(timer);
  }, [pagina, JSON.stringify(Object.keys(dados))]);

  /* ── Derivados ── */
  const info    = dados[cidade] || {};
  const lista   = info.dados    || [];
  const ult     = lista[lista.length-1] || {};
  const cota    = ult.cota_m ?? 0;
  const cfgC    = CFG[cidade];
  const { c:cl, t:stTxt, pct } = classificar(cota, cfgC);
  const stColor = cl==='g' ? 'var(--teal)' : cl==='w' ? 'var(--amber)' : 'var(--red)';
  const al      = ALERTAS_FIXOS[cidade];
  const pico    = estimarPico(lista);
  const fonteLabel = { sace:'SACE/SGB', 'open-meteo':'Open-Meteo', fallback:'Cache' }[info.fonte] || info.fonte || '—';

  const todasAlertas = estacoes.map(nome => {
    const d = dados[nome] || {};
    const l = d.dados || [];
    const u = l[l.length-1] || {};
    const co = u.cota_m ?? 0;
    const { c, t } = classificar(co, CFG[nome]);
    return { nome, cota:co, status:t, cls:c };
  }).filter(e => e.cls !== 'g');

  const alertCount = todasAlertas.length;

  /* ── Loading / Error ── */
  if (loading && !estacoes.length) return (
    <><style>{css}</style>
    <div className="state" style={{ minHeight:'100vh' }}>
      <div className="spinner"/><span style={{ fontSize:12 }}>Carregando…</span>
    </div></>
  );

  if (error && !estacoes.length) return (
    <><style>{css}</style>
    <div className="state" style={{ minHeight:'100vh' }}>
      <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:10, padding:24, maxWidth:380 }}>
        <p style={{ fontWeight:500, color:'var(--red)', marginBottom:8 }}>Backend offline</p>
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

  /* ── Páginas ── */
  const renderPage = () => {

    /* DASHBOARD */
    if (pagina === 'dashboard') return (
      <>
        {/* City tabs */}
        <nav className="city-tabs">
          {estacoes.map(c => (
            <button key={c} className={`c-tab${c === cidade ? ' active' : ''}`} onClick={() => setCidade(c)}>
              {c}
              {ALERTAS_FIXOS[c] && <span className="cdot"/>}
            </button>
          ))}
        </nav>

        {/* Filtro */}
        <div className="filtro-row">
          <span className="filtro-lbl">Período:</span>
          <select className="filtro-sel" value={periodo} onChange={e => setPeriodo(Number(e.target.value))}>
            {PERIODOS.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
          </select>
          {loading && <div className="spinner" style={{ width:15, height:15 }}/>}
        </div>

        {/* Alerta */}
        {al && (
          <div className={`al-bar${al.tipo === 'warn' ? ' warn' : ''}`}>
            <div className="al-ico">⚠</div>
            <div>
              <div className="al-ttl">{al.titulo}</div>
              <div className="al-dsc">{al.desc}</div>
            </div>
          </div>
        )}

        {!loading && lista.length === 0
          ? <div className="state"><span>Sem dados para <strong>{cidade}</strong>.</span></div>
          : <>
            {/* KPIs */}
            <div className="kpi-grid">
              <div className="kpi">
                <div className="kpi-lbl">Cota Atual</div>
                <div className={`kpi-val ${cl}`}>{cota.toFixed(2)}</div>
                <div className="kpi-unit">metros</div>
              </div>
              <div className="kpi">
                <div className="kpi-lbl">Cota de Alerta</div>
                <div className="kpi-val">{cfgC?.cota_alerta?.toFixed(2) ?? '—'}</div>
                <div className="kpi-unit">metros</div>
              </div>
              <div className="kpi">
                <div className="kpi-lbl">% do Máximo</div>
                <div className={`kpi-val ${cl}`}>{pct.toFixed(0)}%</div>
                <div className="kpi-unit">histórico</div>
              </div>
              <div className="kpi">
                <div className="kpi-lbl">Fonte de dados</div>
                <div className="kpi-val" style={{ fontSize:12, paddingTop:4 }}>{fonteLabel}</div>
                <div className="kpi-unit">{info.fonte === 'sace' ? 'dados reais' : 'estimativa'}</div>
              </div>
            </div>

            {/* Gráfico + Painel lateral */}
            <div className="chart-grid">
              <div className="card">
                <div className="card-hdr">
                  <div>
                    <div className="card-ttl">Cota hídrica — histórico</div>
                    <div className="card-sub">metros · {cidade} · {cfgC?.rio}</div>
                  </div>
                  <span className="badge b-teal" style={{ fontSize:10 }}>{lista.length} dias</span>
                </div>
                <div className="chart-box">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={lista} margin={{ top:4, right:8, left:0, bottom:0 }}>
                      <CartesianGrid strokeDasharray="2 4" stroke="var(--border)" vertical={false}/>
                      <XAxis dataKey="data" tickFormatter={fmtD} tick={{ fontSize:10, fill:'var(--muted)', fontFamily:'DM Mono,monospace' }} axisLine={false} tickLine={false} interval="preserveStartEnd"/>
                      <YAxis tick={{ fontSize:10, fill:'var(--muted)', fontFamily:'DM Mono,monospace' }} axisLine={false} tickLine={false} width={34} domain={['auto','auto']}/>
                      <Tooltip content={<Tip/>}/>
                      {cfgC && <ReferenceLine y={cfgC.cota_alerta} stroke="var(--amber)" strokeDasharray="3 3" strokeWidth={1.5} label={{ value:'Alerta', position:'insideTopRight', fontSize:9, fill:'var(--amber)' }}/>}
                      {cfgC && <ReferenceLine y={cfgC.cota_max} stroke="var(--red)" strokeDasharray="2 4" strokeWidth={1} label={{ value:'Máx.', position:'insideTopRight', fontSize:9, fill:'var(--red)' }}/>}
                      <Line type="monotone" dataKey="cota_m" name="Cota (m)" stroke="var(--teal)" strokeWidth={1.8} dot={false} activeDot={{ r:4, strokeWidth:0 }}/>
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Painel direito */}
              <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
                <div className="card" style={{ flex:1 }}>
                  <div className="card-hdr" style={{ marginBottom:14 }}>
                    <div>
                      <div className="card-ttl">Nível hídrico</div>
                      <div className="card-sub">status atual</div>
                    </div>
                  </div>
                  <div className="nivel">
                    <div>
                      <div className="n-lbl">Cota</div>
                      <div className="n-val">{cota.toFixed(2)} m</div>
                      <div className="n-bar"><div className={`n-fill ${cl}`} style={{ width:`${pct.toFixed(1)}%` }}/></div>
                    </div>
                    <div>
                      <div className="n-lbl">Margem p/ alerta</div>
                      <div className="n-val">{cfgC ? (cfgC.cota_alerta - cota).toFixed(2) : '—'} m</div>
                      <div className="n-bar">
                        <div className="n-fill g" style={{ width:`${Math.min((cota/(cfgC?.cota_alerta||1))*100, 100).toFixed(1)}%` }}/>
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
                    <div className="card-sub" style={{ marginBottom:12 }}>estimativa por tendência</div>
                    <div className="pico">
                      <div>
                        <div className="n-lbl">Data estimada</div>
                        <div className="n-val" style={{ fontSize:15 }}>{pico.data}</div>
                      </div>
                      <div>
                        <div className="n-lbl">Cota estimada</div>
                        <div className="n-val" style={{ fontSize:15 }}>{pico.cota} m</div>
                      </div>
                      <div className="n-lbl" style={{ marginTop:2 }}>{pico.desc}</div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Tabela todas estações */}
            <div className="card" style={{ marginBottom:14 }}>
              <div className="card-hdr">
                <div>
                  <div className="card-ttl">Todas as estações</div>
                  <div className="card-sub">leitura mais recente</div>
                </div>
              </div>
              <table className="est-tbl">
                <thead>
                  <tr>
                    <th>Estação</th><th>Rio</th>
                    <th style={{ textAlign:'right' }}>Cota (m)</th>
                    <th style={{ textAlign:'right' }}>Alerta (m)</th>
                    <th style={{ textAlign:'right' }}>Var. dia</th>
                    <th style={{ textAlign:'right' }}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {estacoes.map(nome => {
                    const d = dados[nome] || {};
                    const l = d.dados || [];
                    const u = l[l.length-1] || {};
                    const co = u.cota_m ?? 0;
                    const prev = l.length > 1 ? (l[l.length-2]?.cota_m ?? co) : co;
                    const diff = co - prev;
                    const { c, t } = classificar(co, CFG[nome]);
                    return (
                      <tr key={nome} onClick={() => setCidade(nome)}>
                        <td style={{ fontWeight:500 }}>
                          <span className="tbl-dot" style={{ background:COR[c] }}/>
                          {nome}
                        </td>
                        <td style={{ color:'var(--muted)', fontSize:11 }}>{CFG[nome]?.rio || '—'}</td>
                        <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace' }}>{co.toFixed(2)}</td>
                        <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', color:'var(--muted)' }}>{CFG[nome]?.cota_alerta?.toFixed(2) || '—'}</td>
                        <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', color: diff > 0 ? 'var(--red)' : diff < 0 ? 'var(--green)' : 'var(--muted)' }}>
                          {diff > 0 ? '+' : ''}{diff.toFixed(2)}
                        </td>
                        <td style={{ textAlign:'right', color:COR[c], fontWeight:500 }}>{t}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Mapa */}
            <div>
              <div className="map-hdr">
                <div className="map-ttl">Estações monitoradas</div>
                <div className="map-sub">Clique para selecionar · cores indicam status</div>
              </div>
              <div className="map-wrap">
                <div id="mapa-leaflet" ref={mapaRef}/>
              </div>
            </div>
          </>
        }
      </>
    );

    /* ALERTAS */
    if (pagina === 'alertas') return (
      <>
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
                    <div className="al-card-desc">{CFG[e.nome]?.rio} · {e.status}</div>
                  </div>
                  <div className="al-card-cota" style={{ color:COR[e.cls] }}>{e.cota.toFixed(2)} m</div>
                </div>
              ))}
            </div>
        }

        <div style={{ marginTop:20 }}>
          <div className="card-ttl" style={{ marginBottom:12 }}>Resumo geral</div>
          <div className="card">
            <table className="est-tbl">
              <thead>
                <tr><th>Estação</th><th>Rio</th><th style={{ textAlign:'right' }}>Cota (m)</th><th style={{ textAlign:'right' }}>Alerta (m)</th><th style={{ textAlign:'right' }}>Status</th></tr>
              </thead>
              <tbody>
                {estacoes.map(nome => {
                  const d = dados[nome] || {};
                  const l = d.dados || [];
                  const co = l[l.length-1]?.cota_m ?? 0;
                  const { c, t } = classificar(co, CFG[nome]);
                  return (
                    <tr key={nome} onClick={() => { setCidade(nome); setPagina('dashboard'); }}>
                      <td style={{ fontWeight:500 }}><span className="tbl-dot" style={{ background:COR[c] }}/>{nome}</td>
                      <td style={{ color:'var(--muted)', fontSize:11 }}>{CFG[nome]?.rio || '—'}</td>
                      <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace' }}>{co.toFixed(2)}</td>
                      <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', color:'var(--muted)' }}>{CFG[nome]?.cota_alerta?.toFixed(2) || '—'}</td>
                      <td style={{ textAlign:'right', color:COR[c], fontWeight:500 }}>{t}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </>
    );

    /* ESTAÇÕES */
    if (pagina === 'estacoes') return (
      <>
        <div className="sec-ttl">Estações fluviométricas</div>
        <div className="sec-sub">Rede de monitoramento · Bacia Amazônica</div>
        <div className="card">
          <table className="est-tbl">
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
                const cfg2 = CFG[nome] || {};
                const { c } = classificar(d.dados?.[d.dados.length-1]?.cota_m ?? 0, cfg2);
                return (
                  <tr key={nome} onClick={() => { setCidade(nome); setPagina('dashboard'); }}>
                    <td style={{ fontWeight:500 }}><span className="tbl-dot" style={{ background:COR[c] }}/>{nome}</td>
                    <td style={{ color:'var(--muted)', fontSize:11 }}>{cfg2.rio || '—'}</td>
                    <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', fontSize:11, color:'var(--muted)' }}>{cfg2.lat?.toFixed(2)}</td>
                    <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', fontSize:11, color:'var(--muted)' }}>{cfg2.lon?.toFixed(2)}</td>
                    <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace' }}>{cfg2.cota_alerta?.toFixed(2) || '—'}</td>
                    <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace' }}>{cfg2.cota_max?.toFixed(2) || '—'}</td>
                    <td>
                      <span style={{ fontSize:10, padding:'2px 7px', borderRadius:99, background:'var(--tealL)', color:'var(--teal)' }}>
                        {{ sace:'SACE', 'open-meteo':'Open-Meteo', fallback:'Cache' }[d.fonte] || d.fonte || '—'}
                      </span>
                    </td>
                    <td style={{ textAlign:'right', fontFamily:'DM Mono,monospace', color:'var(--muted)' }}>{d.dados?.length || 0}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </>
    );

    /* MAPA */
    if (pagina === 'mapa') return (
      <>
        <div className="sec-ttl">Mapa de estações</div>
        <div className="sec-sub">Clique em uma estação para abrir no Dashboard · verde = normal · laranja = atenção · vermelho = alerta</div>
        <div className="map-wrap" style={{ height:520 }}>
          <div id="mapa-leaflet" ref={mapaRef}/>
        </div>
      </>
    );
  };

  const pageTitle = { dashboard:`Dashboard · ${cidade}`, alertas:'Alertas', estacoes:'Estações', mapa:'Mapa' }[pagina];

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
                <Ico d={n.d}/>
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
        <div className="main">
          <div className="topbar">
            <button className="menu-btn" onClick={() => setSideOpen(o => !o)}>
              <span/><span/><span/>
            </button>
            <div className="topbar-info">
              <div className="topbar-ttl">{pageTitle}</div>
              <div className="topbar-sub">
                {estacoes.length} estações · {new Date().toLocaleDateString('pt-BR', { day:'2-digit', month:'long', year:'numeric' })}
              </div>
            </div>
            <div className="topbar-right">
              {alertCount > 0 && <span className="badge b-red">⚠ {alertCount} alerta{alertCount > 1 ? 's' : ''}</span>}
              {loading && <div className="spinner" style={{ width:16, height:16 }}/>}
              <button className="btn-sm" onClick={() => setTema(t => t === 'dark' ? 'light' : 'dark')}>
                {tema === 'dark' ? '☀ Claro' : '◐ Escuro'}
              </button>
            </div>
          </div>

          <div className="scroll">
            {renderPage()}
          </div>

          <div className="footer">
            Rio Amazonas · Dados via SACE/SGB · 2026
          </div>
        </div>
      </div>
    </>
  );
}
