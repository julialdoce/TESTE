import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine,
  BarChart, Bar
} from 'recharts';

/* ─── CSS ─────────────────────────────────────────────────────────────────── */
const css = `
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg:        #F4F2EE;
  --surface:   #FFFFFF;
  --surf2:     #ECEAE4;
  --border:    #E0DDD6;
  --text:      #18170F;
  --muted:     #7A7870;
  --faint:     #B8B4AB;
  --accent:    #1B7C6C;
  --accent2:   #E0F2EE;
  --warn:      #C07A20;
  --warn2:     #FBF0DF;
  --danger:    #C03030;
  --danger2:   #FCEAE8;
  --line1:     #1B7C6C;
  --line2:     #C07A20;
  --sidebar-w: 224px;
  --r: 8px;
}

[data-theme=dark] {
  --bg:      #0E0D0B;
  --surface: #181714;
  --surf2:   #201F1C;
  --border:  #2A2926;
  --text:    #EDE9E1;
  --muted:   #706C64;
  --faint:   #3A3832;
  --accent:  #3DB898;
  --accent2: #0D2B24;
  --warn:    #D4921E;
  --warn2:   #2A1E08;
  --danger:  #D94040;
  --danger2: #2A1010;
  --line1:   #3DB898;
  --line2:   #D4921E;
}

*,*::before,*::after { margin:0; padding:0; box-sizing:border-box }
html { scroll-behavior:smooth }
body {
  background:var(--bg); color:var(--text);
  font-family:'DM Sans',sans-serif; font-size:13.5px; line-height:1.5;
  -webkit-font-smoothing:antialiased;
  transition:background .2s,color .2s;
}

/* ── SHELL ── */
.shell { display:flex; height:100vh; overflow:hidden }

/* ── SIDEBAR ── */
.sidebar {
  width:var(--sidebar-w); flex-shrink:0;
  background:#111110;
  display:flex; flex-direction:column;
  overflow:hidden;
  transition:width .3s cubic-bezier(.4,0,.2,1);
  z-index:200;
}
.sidebar.collapsed { width:0 }

.sb-logo {
  padding:18px 16px 14px;
  border-bottom:1px solid rgba(255,255,255,.06);
  display:flex; align-items:center; gap:10px;
  flex-shrink:0;
}
.sb-mark {
  width:30px; height:30px; border-radius:8px;
  background:var(--accent); flex-shrink:0;
  display:flex; align-items:center; justify-content:center;
}
.sb-mark svg { width:14px; height:14px; stroke:#fff; fill:none; stroke-width:2; stroke-linecap:round }
.sb-name { font-size:13px; font-weight:600; color:#EDE9E1; white-space:nowrap }
.sb-sub  { font-size:9.5px; color:rgba(255,255,255,.28); letter-spacing:.06em; text-transform:uppercase; margin-top:1px }

.sb-section { padding:14px 10px 6px; flex-shrink:0 }
.sb-section-lbl {
  font-size:9px; letter-spacing:.12em; text-transform:uppercase;
  color:rgba(255,255,255,.22); padding:0 8px; margin-bottom:4px;
}

.nav-item {
  display:flex; align-items:center; gap:9px;
  padding:8px 10px; border-radius:7px;
  color:rgba(255,255,255,.38); font-size:12.5px;
  cursor:pointer; transition:all .15s; margin-bottom:1px;
  white-space:nowrap; user-select:none; position:relative;
}
.nav-item:hover { background:rgba(255,255,255,.05); color:rgba(255,255,255,.65) }
.nav-item.active { background:rgba(61,184,152,.18); color:#6DDDC8 }
.nav-item .nav-badge {
  position:absolute; right:10px; top:50%; transform:translateY(-50%);
  width:5px; height:5px; border-radius:50%; background:var(--danger);
}
.nav-icon { width:15px; height:15px; flex-shrink:0; fill:none; stroke:currentColor; stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round; opacity:.7 }
.nav-item.active .nav-icon { opacity:1 }

.sb-footer {
  margin-top:auto; padding:12px 10px;
  border-top:1px solid rgba(255,255,255,.06);
}
.sb-live {
  display:flex; align-items:center; gap:8px;
  padding:7px 10px; background:rgba(255,255,255,.04); border-radius:7px;
}
.sb-dot { width:6px; height:6px; border-radius:50%; background:#3DB87C; animation:pulse 2.5s ease infinite; flex-shrink:0 }
.sb-dot.off { background:var(--danger); animation:none }
@keyframes pulse { 0%,100%{opacity:1}50%{opacity:.25} }
.sb-live-txt { font-size:11px; color:rgba(255,255,255,.32) }
.sb-live-val { font-size:11px; color:rgba(255,255,255,.5); margin-left:auto }

/* ── MAIN ── */
.main { flex:1; display:flex; flex-direction:column; overflow:hidden; min-width:0 }

/* ── TOPBAR ── */
.topbar {
  background:var(--surface); border-bottom:1px solid var(--border);
  padding:10px 20px; display:flex; align-items:center; gap:12px;
  flex-shrink:0; height:48px;
}
.toggle-btn {
  width:32px; height:32px; border-radius:7px;
  border:1px solid var(--border); background:transparent;
  cursor:pointer; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:4px; flex-shrink:0;
  transition:background .15s;
}
.toggle-btn:hover { background:var(--surf2) }
.toggle-btn span {
  display:block; width:14px; height:1.5px; background:var(--text);
  border-radius:99px; transition:transform .25s, opacity .25s, width .25s; transform-origin:center;
}
.toggle-btn.open span:nth-child(1) { transform:translateY(5.5px) rotate(45deg) }
.toggle-btn.open span:nth-child(2) { opacity:0; width:0 }
.toggle-btn.open span:nth-child(3) { transform:translateY(-5.5px) rotate(-45deg) }

.topbar-title h1 { font-size:14px; font-weight:600; letter-spacing:-.01em }
.topbar-title p  { font-size:11px; color:var(--muted); margin-top:1px }

.topbar-right { display:flex; align-items:center; gap:8px; margin-left:auto }

.pill-btn {
  height:28px; padding:0 12px; border-radius:99px;
  border:1px solid var(--border); background:var(--surface);
  color:var(--muted); font-family:'DM Sans',sans-serif;
  font-size:11px; cursor:pointer; transition:all .15s; white-space:nowrap;
}
.pill-btn:hover { background:var(--surf2); color:var(--text) }

.page-badge {
  font-size:11px; font-weight:500; padding:3px 10px;
  border-radius:99px; white-space:nowrap;
}
.badge-danger { background:var(--danger2); color:var(--danger) }
.badge-ok     { background:var(--accent2); color:var(--accent) }
.badge-warn   { background:var(--warn2); color:var(--warn) }

/* ── SCROLL AREA ── */
.scroll-area { flex:1; overflow-y:auto; padding:20px 24px 56px; scrollbar-width:thin; scrollbar-color:var(--faint) transparent }

/* ── PAGE HEADER ── */
.page-hdr { margin-bottom:20px }
.page-tag {
  display:inline-flex; align-items:center; gap:5px;
  font-size:9.5px; letter-spacing:.1em; text-transform:uppercase;
  color:var(--accent); font-weight:600; margin-bottom:6px;
}
.page-tag span { width:14px; height:1px; background:var(--accent); display:inline-block }
.page-hdr h2 { font-size:22px; font-weight:300; letter-spacing:-.03em; line-height:1.1 }
.page-hdr h2 strong { font-weight:600 }
.page-hdr p { font-size:12px; color:var(--muted); margin-top:4px }

/* ── FILTRO ── */
.filtro-row { display:flex; align-items:center; gap:10px; margin-bottom:16px; flex-wrap:wrap }
.filtro-lbl { font-size:11px; color:var(--muted) }
.filtro-sel {
  background:var(--surface); border:1px solid var(--border);
  color:var(--text); padding:5px 12px; border-radius:99px;
  font-family:'DM Sans',sans-serif; font-size:11px;
  cursor:pointer; outline:none; transition:border-color .15s;
}
.filtro-sel:focus { border-color:var(--accent) }

/* ── STATION TABS ── */
.station-tabs {
  display:flex; gap:4px; margin-bottom:16px;
  overflow-x:auto; scrollbar-width:none; flex-wrap:wrap;
}
.station-tabs::-webkit-scrollbar { display:none }
.st-tab {
  padding:5px 13px; border-radius:99px;
  border:1px solid var(--border); background:transparent;
  font-family:'DM Sans',sans-serif; font-size:11.5px;
  cursor:pointer; color:var(--muted); white-space:nowrap;
  transition:all .15s; display:flex; align-items:center; gap:5px;
}
.st-tab:hover { color:var(--text); border-color:var(--faint) }
.st-tab.active {
  background:var(--text); color:#fff; border-color:var(--text);
}
[data-theme=dark] .st-tab.active { background:var(--accent); border-color:var(--accent); color:#fff }
.st-tab .rdot { width:5px; height:5px; border-radius:50%; background:var(--danger); display:inline-block }

/* ── BANNER ── */
.banner {
  padding:10px 14px; border-radius:var(--r); border-left:3px solid; margin-bottom:16px;
  display:flex; align-items:flex-start; gap:10px;
}
.banner.danger { border-color:var(--danger); background:var(--danger2) }
.banner.warn   { border-color:var(--warn);   background:var(--warn2) }
.banner-ico    { font-size:14px; margin-top:1px; flex-shrink:0 }
.banner-ttl    { font-size:12px; font-weight:600; margin-bottom:2px }
.banner.danger .banner-ttl { color:var(--danger) }
.banner.warn   .banner-ttl { color:var(--warn) }
.banner-dsc    { font-size:11px; color:var(--muted); line-height:1.6 }

/* ── STATS ── */
.stats { display:grid; grid-template-columns:repeat(5,1fr); gap:1px; background:var(--border); border:1px solid var(--border); border-radius:var(--r); overflow:hidden; margin-bottom:16px }
.stat { background:var(--surface); padding:14px 16px }
.stat-lbl { font-size:10px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin-bottom:6px; font-family:'DM Mono',monospace }
.stat-val { font-size:22px; font-weight:600; letter-spacing:-.03em; line-height:1 }
.stat-val.g { color:var(--accent) }
.stat-val.w { color:var(--warn) }
.stat-val.d { color:var(--danger) }
.stat-unit { font-size:10px; color:var(--faint); margin-top:3px; font-family:'DM Mono',monospace }

/* ── CHART GRID ── */
.chart-grid { display:grid; grid-template-columns:1fr 250px; gap:14px; margin-bottom:14px }
.card { background:var(--surface); border:1px solid var(--border); border-radius:var(--r); padding:16px 18px }
.card-hdr { display:flex; align-items:baseline; justify-content:space-between; margin-bottom:2px }
.card-ttl { font-size:12.5px; font-weight:600 }
.card-sub { font-size:11px; color:var(--muted); margin-bottom:14px }
.chart-wrap { height:190px }

/* ── NIVEL ── */
.nivel { display:flex; flex-direction:column; gap:16px }
.n-lbl { font-size:9.5px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); margin-bottom:4px; font-family:'DM Mono',monospace }
.n-val { font-size:18px; font-weight:600; letter-spacing:-.02em }
.n-bar { height:3px; background:var(--surf2); border-radius:99px; margin-top:6px; overflow:hidden }
.n-fill { height:100%; border-radius:99px; transition:width 1.2s cubic-bezier(.4,0,.2,1) }
.n-fill.g { background:var(--accent) }
.n-fill.w { background:var(--warn) }
.n-fill.d { background:var(--danger) }
.n-status { font-size:12px; font-weight:600; margin-top:3px }

/* ── MAP ── */
.map-wrap { background:var(--surface); border:1px solid var(--border); border-radius:var(--r); overflow:hidden; height:360px; position:relative }
#mapa-leaflet { width:100%; height:100% }
.map-legend {
  position:absolute; bottom:12px; left:12px; z-index:1000;
  background:var(--surface); border:1px solid var(--border); border-radius:6px;
  padding:8px 12px; font-size:10.5px;
  display:flex; flex-direction:column; gap:5px; pointer-events:none;
}
.legend-item { display:flex; align-items:center; gap:6px; color:var(--muted) }
.legend-dot { width:8px; height:8px; border-radius:50% }

/* ── ALERTAS PAGE ── */
.alertas-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:14px; margin-bottom:20px }
.alerta-card {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--r); padding:16px 18px;
  border-left:3px solid var(--border);
  transition:border-color .2s;
}
.alerta-card.danger { border-left-color:var(--danger) }
.alerta-card.warn   { border-left-color:var(--warn) }
.alerta-card.ok     { border-left-color:var(--accent) }
.ac-header { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:10px }
.ac-city { font-size:13px; font-weight:600 }
.ac-sub  { font-size:11px; color:var(--muted) }
.ac-badge { font-size:10px; font-weight:600; padding:2px 8px; border-radius:99px; white-space:nowrap; flex-shrink:0 }
.ac-badge.danger { background:var(--danger2); color:var(--danger) }
.ac-badge.warn   { background:var(--warn2);   color:var(--warn) }
.ac-badge.ok     { background:var(--accent2); color:var(--accent) }
.ac-row { display:flex; gap:20px; margin-top:10px }
.ac-stat { }
.ac-stat-lbl { font-size:9.5px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); font-family:'DM Mono',monospace }
.ac-stat-val { font-size:15px; font-weight:600; letter-spacing:-.02em }
.ac-bar { height:2px; background:var(--surf2); border-radius:99px; margin-top:8px; overflow:hidden }
.ac-fill { height:100%; border-radius:99px }

/* ── ESTAÇÕES TABLE ── */
.table-wrap { background:var(--surface); border:1px solid var(--border); border-radius:var(--r); overflow:hidden }
.trow {
  display:grid; grid-template-columns:1fr 90px 90px 90px 80px 80px;
  align-items:center; padding:10px 16px; gap:8px;
  border-bottom:1px solid var(--border);
}
.trow:last-child { border-bottom:none }
.trow.thead { background:var(--surf2); padding:8px 16px }
.trow.thead span { font-size:9.5px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); font-family:'DM Mono',monospace }
.trow:not(.thead):hover { background:var(--surf2); cursor:pointer }
.trow:not(.thead).sel { background:var(--accent2) }
.t-name { font-size:12.5px; font-weight:600 }
.t-sub  { font-size:10.5px; color:var(--muted) }
.t-num  { font-size:13px; font-family:'DM Mono',monospace; text-align:right }
.t-status { display:flex; justify-content:flex-end }
.status-chip {
  font-size:10px; font-weight:600; padding:2px 8px;
  border-radius:99px; white-space:nowrap;
}
.chip-ok   { background:var(--accent2); color:var(--accent) }
.chip-warn { background:var(--warn2);   color:var(--warn) }
.chip-dang { background:var(--danger2); color:var(--danger) }

/* ── STATE ── */
.state { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:300px; gap:12px; color:var(--muted) }
.spinner { width:22px; height:22px; border-radius:50%; border:2px solid var(--border); border-top-color:var(--accent); animation:spin .6s linear infinite }
@keyframes spin { to{transform:rotate(360deg)} }

/* ── FOOTER ── */
.footer { border-top:1px solid var(--border); padding:12px 24px; text-align:center; font-size:11px; color:var(--faint); font-family:'DM Mono',monospace; flex-shrink:0 }

@media(max-width:900px){
  .stats { grid-template-columns:repeat(3,1fr) }
  .chart-grid { grid-template-columns:1fr }
  .trow { grid-template-columns:1fr 80px 70px 70px }
  .trow > *:nth-child(5), .trow > *:nth-child(6) { display:none }
}
@media(max-width:600px){
  .scroll-area { padding:14px 16px 48px }
  .stats { grid-template-columns:1fr 1fr }
  :root { --sidebar-w:200px }
}
`;

/* ─── Constantes ──────────────────────────────────────────────────────────── */
const ALERTAS = {
  "Manaus": { tipo: "danger", titulo: "Alerta de enchente — Manaus", desc: "Zona Sul com risco elevado. Nível acima da cota de atenção desde 24/04/2026." }
};

const CONFIG_ESTACOES = {
  "Manaus":      { lat: -3.10, lon: -60.02, cota_alerta: 29.00, cota_max: 29.97, rio: "Rio Negro" },
  "Itacoatiara": { lat: -3.14, lon: -58.44, cota_alerta: 14.00, cota_max: 16.83, rio: "Rio Amazonas" },
  "Manacapuru":  { lat: -3.31, lon: -60.61, cota_alerta: 21.00, cota_max: 23.50, rio: "Rio Solimões" },
  "Parintins":   { lat: -2.63, lon: -56.74, cota_alerta: 11.50, cota_max: 13.80, rio: "Rio Amazonas" },
  "Óbidos":      { lat: -1.92, lon: -55.52, cota_alerta:  9.00, cota_max: 11.20, rio: "Rio Amazonas" },
  "Tefé":        { lat: -3.37, lon: -64.72, cota_alerta: 14.50, cota_max: 17.50, rio: "Rio Solimões" },
  "Santarém":    { lat: -2.44, lon: -54.70, cota_alerta:  8.50, cota_max: 10.50, rio: "Rio Amazonas" },
  "Tabatinga":   { lat: -4.25, lon: -69.94, cota_alerta: 11.00, cota_max: 13.50, rio: "Rio Solimões" },
};

const PERIODOS = [
  { label: 'Todos os dados', value: 0 },
  { label: 'Últimos 30 dias', value: 30 },
  { label: 'Últimos 60 dias', value: 60 },
  { label: 'Últimos 90 dias', value: 90 },
];

const PAGES = [
  { id: 'dashboard', label: 'Dashboard', icon: 'chart' },
  { id: 'alertas',   label: 'Alertas',   icon: 'alert', badge: true },
  { id: 'estacoes',  label: 'Estações',  icon: 'map' },
  { id: 'previsao',  label: 'Previsão',  icon: 'trend' },
];

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
  const ult = lista[lista.length - 1];
  const cotaAtual = ult?.cota_m ?? 0;
  if (tendencia <= 0) return { data: 'Estável', cota: cotaAtual.toFixed(2), desc: 'Rio em queda ou estável', tendencia };
  const dataPico = new Date();
  dataPico.setDate(dataPico.getDate() + Math.min(30, Math.round(14)));
  const cotaPico = Math.min(cotaAtual + tendencia * 30, 35);
  return {
    data: dataPico.toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' }),
    cota: cotaPico.toFixed(2),
    desc: `+${tendencia.toFixed(3)}m/dia tendência`,
    tendencia
  };
}

/* ─── Icons ── */
const Icon = ({ type, size = 15 }) => {
  const s = { width: size, height: size, fill: 'none', stroke: 'currentColor', strokeWidth: 1.6, strokeLinecap: 'round', strokeLinejoin: 'round' };
  if (type === 'chart')  return <svg style={s} viewBox="0 0 16 16"><polyline points="1,12 5,7 8,10 12,4 15,7"/><line x1="1" y1="15" x2="15" y2="15"/></svg>;
  if (type === 'alert')  return <svg style={s} viewBox="0 0 16 16"><path d="M8 2L14 13H2L8 2z"/><line x1="8" y1="7" x2="8" y2="10"/><circle cx="8" cy="12" r=".6" fill="currentColor"/></svg>;
  if (type === 'map')    return <svg style={s} viewBox="0 0 16 16"><polygon points="1,3 5,1 11,3 15,1 15,13 11,15 5,13 1,15"/><line x1="5" y1="1" x2="5" y2="13"/><line x1="11" y1="3" x2="11" y2="15"/></svg>;
  if (type === 'trend')  return <svg style={s} viewBox="0 0 16 16"><polyline points="1,13 6,7 10,10 15,3"/><polyline points="11,3 15,3 15,7"/></svg>;
  if (type === 'wave')   return <svg style={s} viewBox="0 0 14 14"><path d="M1 8 Q3.5 4 7 8 Q10.5 12 13 8"/></svg>;
  return null;
};

/* ─── Tooltip ── */
const Tip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background:'var(--surface)', border:'1px solid var(--border)', borderRadius:6, padding:'8px 12px', fontSize:11 }}>
      <p style={{ color:'var(--muted)', marginBottom:4, fontFamily:'DM Mono,monospace' }}>{label}</p>
      {payload.map((p,i) => <p key={i} style={{ color:p.color, fontWeight:600 }}>{p.name}: {(+p.value).toFixed(2)}</p>)}
    </div>
  );
};

/* ─── App ── */
export default function App() {
  const [dados, setDados]       = useState({});
  const [estacoes, setEstacoes] = useState([]);
  const [cidade, setCidade]     = useState('');
  const [periodo, setPeriodo]   = useState(0);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState(null);
  const [tema, setTema]         = useState(() => localStorage.getItem('tema') || 'light');
  const [sidebar, setSidebar]   = useState(true);
  const [page, setPage]         = useState('dashboard');

  const mapaRef  = useRef(null);
  const mapaInst = useRef(null);
  const markersRef = useRef({});

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

  /* Destaca marcador no mapa ao mudar cidade */
  useEffect(() => {
    if (!mapaInst.current || !window.L) return;
    Object.entries(markersRef.current).forEach(([nome, marker]) => {
      const cfg = CONFIG_ESTACOES[nome];
      const info2 = dados[nome] || {};
      const lista2 = info2.dados || [];
      const ult2 = lista2[lista2.length - 1] || {};
      const cota2 = ult2.cota_m ?? 0;
      const { cls: cls2 } = classificar(cota2, cfg);
      const cor = cls2 === 'g' ? '#1B7C6C' : cls2 === 'w' ? '#C07A20' : '#C03030';
      const isActive = nome === cidade;
      const icon = window.L.divIcon({
        className: '',
        html: `<div style="
          width:${isActive?16:10}px;height:${isActive?16:10}px;border-radius:50%;
          background:${cor};
          border:${isActive?'3px solid white':'2px solid rgba(255,255,255,.7)'};
          box-shadow:${isActive?`0 0 0 3px ${cor}55, 0 2px 8px rgba(0,0,0,.3)`:'0 1px 4px rgba(0,0,0,.25)'};
          transition:all .2s;
        "></div>`,
        iconSize: [isActive?16:10, isActive?16:10],
        iconAnchor: [isActive?8:5, isActive?8:5]
      });
      marker.setIcon(icon);
      if (isActive) marker.openPopup();
    });
  }, [cidade, dados]);

  /* Mapa Leaflet */
  useEffect(() => {
    if (!mapaRef.current || mapaInst.current) return;
    const initMap = () => {
      const L = window.L;
      if (!L) return;
      const map = L.map('mapa-leaflet', { zoomControl: true, scrollWheelZoom: false })
        .setView([-3.5, -62], 5);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', {
        attribution: '© CartoDB', maxZoom: 12
      }).addTo(map);

      Object.entries(CONFIG_ESTACOES).forEach(([nome, cfg]) => {
        const info2 = dados[nome] || {};
        const lista2 = info2.dados || [];
        const ult2 = lista2[lista2.length - 1] || {};
        const cota2 = ult2.cota_m ?? 0;
        const { cls: cls2 } = classificar(cota2, cfg);
        const cor = cls2 === 'g' ? '#1B7C6C' : cls2 === 'w' ? '#C07A20' : '#C03030';
        const isActive = nome === cidade;

        const icon = L.divIcon({
          className: '',
          html: `<div style="
            width:${isActive?16:10}px;height:${isActive?16:10}px;border-radius:50%;
            background:${cor};
            border:${isActive?'3px solid white':'2px solid rgba(255,255,255,.7)'};
            box-shadow:${isActive?`0 0 0 3px ${cor}55, 0 2px 8px rgba(0,0,0,.3)`:'0 1px 4px rgba(0,0,0,.25)'};
          "></div>`,
          iconSize: [isActive?16:10, isActive?16:10],
          iconAnchor: [isActive?8:5, isActive?8:5]
        });

        const marker = L.marker([cfg.lat, cfg.lon], { icon })
          .addTo(map)
          .bindPopup(
            `<div style="font-family:DM Sans,sans-serif;min-width:120px">
              <b style="font-size:13px">${nome}</b>
              <div style="font-size:11px;color:#666;margin-top:2px">${cfg.rio}</div>
              <div style="font-size:12px;margin-top:6px">Cota: <b>${cota2.toFixed(2)}m</b></div>
              <div style="font-size:11px;color:${cor};font-weight:600;margin-top:2px">${cls2 === 'g' ? 'Normal' : cls2 === 'w' ? 'Atenção' : 'Alerta'}</div>
            </div>`,
            { maxWidth: 180 }
          )
          .on('click', () => { setCidade(nome); if (page !== 'dashboard') setPage('dashboard'); });

        markersRef.current[nome] = marker;
        if (isActive) marker.openPopup();
      });

      mapaInst.current = map;
    };

    if (window.L) { initMap(); return; }
    const link = document.createElement('link');
    link.rel = 'stylesheet'; link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.onload = initMap;
    document.head.appendChild(script);
  }, [mapaRef.current, Object.keys(dados).length]);

  /* Dados derivados */
  const info   = dados[cidade] || {};
  const lista  = info.dados    || [];
  const ult    = lista[lista.length - 1] || {};
  const cota   = ult.cota_m ?? 0;
  const cfg    = CONFIG_ESTACOES[cidade];
  const { cls, txt: stTxt, pct } = classificar(cota, cfg);
  const stColor = cls === 'g' ? 'var(--accent)' : cls === 'w' ? 'var(--warn)' : 'var(--danger)';
  const al     = ALERTAS[cidade];
  const pico   = estimarPico(lista);
  const fonteLabel = { 'sace': 'SACE/SGB', 'open-meteo': 'Open-Meteo', 'fallback': 'Cache local' }[info.fonte] || info.fonte || '—';
  const hasAlerts = Object.keys(ALERTAS).some(k => estacoes.includes(k));

  /* Dados para página Estações */
  const allStationsData = estacoes.map(nome => {
    const inf = dados[nome] || {};
    const lst = inf.dados || [];
    const u = lst[lst.length - 1] || {};
    const co = u.cota_m ?? 0;
    const cfgg = CONFIG_ESTACOES[nome];
    const { cls: cl, txt } = classificar(co, cfgg);
    return { nome, cota: co, cfg: cfgg, cls: cl, txt, fonte: inf.fonte };
  });

  if (loading && !estacoes.length) return (
    <><style>{css}</style>
    <div className="state" style={{ minHeight:'100vh' }}>
      <div className="spinner"/>
      <span style={{ fontSize:12 }}>Carregando…</span>
    </div></>
  );

  /* ── PAGES ── */
  const renderDashboard = () => (
    <>
      {/* Station tabs */}
      <div className="station-tabs">
        {estacoes.map(c => (
          <button key={c} className={`st-tab${c === cidade ? ' active' : ''}`} onClick={() => setCidade(c)}>
            {c}
            {ALERTAS[c] && <span className="rdot"/>}
          </button>
        ))}
      </div>

      {/* Filtro */}
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

      {lista.length === 0
        ? <div className="state"><span>Sem dados para <b>{cidade}</b>.</span></div>
        : <>
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
              <div className="stat-val" style={{ fontSize:12, paddingTop:4 }}>{fonteLabel}</div>
              <div className="stat-unit">{info.fonte === 'sace' ? 'dados reais' : 'estimativa'}</div>
            </div>
          </div>

          <div className="chart-grid">
            <div className="card">
              <div className="card-hdr"><div className="card-ttl">Cota hídrica</div></div>
              <div className="card-sub">metros — {cidade}</div>
              <div className="chart-wrap">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={lista} margin={{ top:4, right:8, left:0, bottom:0 }}>
                    <CartesianGrid strokeDasharray="2 4" stroke="var(--border)" vertical={false}/>
                    <XAxis dataKey="data" tickFormatter={fmtData} tick={{ fontSize:10, fill:'var(--muted)', fontFamily:'DM Mono,monospace' }} axisLine={false} tickLine={false} interval="preserveStartEnd"/>
                    <YAxis tick={{ fontSize:10, fill:'var(--muted)', fontFamily:'DM Mono,monospace' }} axisLine={false} tickLine={false} width={36} domain={['auto','auto']}/>
                    <Tooltip content={<Tip/>}/>
                    {cfg && <ReferenceLine y={cfg.cota_alerta} stroke="var(--warn)" strokeDasharray="3 3" strokeWidth={1.5} label={{ value:'Alerta', position:'insideTopRight', fontSize:9, fill:'var(--warn)' }}/>}
                    {cfg && <ReferenceLine y={cfg.cota_max}    stroke="var(--danger)" strokeDasharray="3 3" strokeWidth={1} label={{ value:'Máx', position:'insideTopRight', fontSize:9, fill:'var(--danger)' }}/>}
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
                    <div className="n-lbl">Cota atual</div>
                    <div className="n-val">{cota.toFixed(2)} m</div>
                    <div className="n-bar"><div className={`n-fill ${cls}`} style={{ width:`${pct.toFixed(1)}%` }}/></div>
                  </div>
                  <div>
                    <div className="n-lbl">Margem até alerta</div>
                    <div className="n-val">{cfg ? (cfg.cota_alerta - cota).toFixed(2) : '—'} m</div>
                    <div className="n-bar">
                      <div className="n-fill g" style={{ width:`${Math.min(((cota/(cfg?.cota_alerta||1))*100),100).toFixed(1)}%` }}/>
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
                  <div className="card-ttl">Previsão</div>
                  <div className="card-sub">estimativa tendência</div>
                  <div style={{ display:'flex', flexDirection:'column', gap:8 }}>
                    <div><div className="n-lbl">Data estimada</div><div className="n-val" style={{ fontSize:15 }}>{pico.data}</div></div>
                    <div><div className="n-lbl">Cota estimada</div><div className="n-val" style={{ fontSize:15 }}>{pico.cota} m</div></div>
                    <div className="n-lbl" style={{ marginTop:2 }}>{pico.desc}</div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Mapa no dashboard */}
          <div className="card" style={{ marginBottom:0, padding:0, overflow:'hidden', position:'relative' }}>
            <div style={{ padding:'14px 16px 10px', borderBottom:'1px solid var(--border)', display:'flex', alignItems:'center', justifyContent:'space-between' }}>
              <div>
                <div className="card-ttl">Estações monitoradas</div>
                <div className="card-sub" style={{ margin:0 }}>Clique em um ponto para selecionar a estação</div>
              </div>
              <div style={{ display:'flex', gap:10 }}>
                {[['ok','#1B7C6C','Normal'],['warn','#C07A20','Atenção'],['dang','#C03030','Alerta']].map(([k,c,l]) => (
                  <div key={k} style={{ display:'flex', alignItems:'center', gap:5, fontSize:10.5, color:'var(--muted)' }}>
                    <div style={{ width:8, height:8, borderRadius:'50%', background:c }}/>
                    {l}
                  </div>
                ))}
              </div>
            </div>
            <div style={{ height:320 }}><div id="mapa-leaflet" ref={mapaRef} style={{ width:'100%', height:'100%' }}/></div>
          </div>
        </>
      }
    </>
  );

  const renderAlertas = () => {
    const todas = allStationsData;
    const criticas = todas.filter(s => s.cls === 'd');
    const atencao  = todas.filter(s => s.cls === 'w');
    const normais  = todas.filter(s => s.cls === 'g');

    return (
      <>
        <div style={{ display:'grid', gridTemplateColumns:'repeat(3,1fr)', gap:10, marginBottom:20 }}>
          {[
            { label:'Emergência / Alerta', val:criticas.length, cls:'danger' },
            { label:'Atenção',             val:atencao.length,  cls:'warn' },
            { label:'Normal',              val:normais.length,  cls:'ok' },
          ].map(s => (
            <div key={s.cls} className="card" style={{ textAlign:'center' }}>
              <div className="stat-lbl">{s.label}</div>
              <div className={`stat-val ${s.cls === 'ok' ? 'g' : s.cls === 'warn' ? 'w' : 'd'}`} style={{ fontSize:28, marginTop:6 }}>{s.val}</div>
              <div className="stat-unit">estações</div>
            </div>
          ))}
        </div>

        {criticas.length > 0 && (
          <>
            <div style={{ fontSize:11, fontWeight:600, textTransform:'uppercase', letterSpacing:'.08em', color:'var(--danger)', marginBottom:10, fontFamily:'DM Mono,monospace' }}>Situação crítica</div>
            <div className="alertas-grid" style={{ marginBottom:20 }}>
              {criticas.map(s => (
                <div key={s.nome} className="alerta-card danger" onClick={() => { setCidade(s.nome); setPage('dashboard'); }} style={{ cursor:'pointer' }}>
                  <div className="ac-header">
                    <div><div className="ac-city">{s.nome}</div><div className="ac-sub">{s.cfg?.rio}</div></div>
                    <div className="ac-badge danger">{s.txt}</div>
                  </div>
                  {ALERTAS[s.nome] && <div style={{ fontSize:11, color:'var(--muted)', lineHeight:1.6, marginBottom:8 }}>{ALERTAS[s.nome].desc}</div>}
                  <div className="ac-row">
                    <div className="ac-stat"><div className="ac-stat-lbl">Cota atual</div><div className="ac-stat-val" style={{ color:'var(--danger)' }}>{s.cota.toFixed(2)}m</div></div>
                    <div className="ac-stat"><div className="ac-stat-lbl">Cota alerta</div><div className="ac-stat-val">{s.cfg?.cota_alerta.toFixed(2)}m</div></div>
                    <div className="ac-stat"><div className="ac-stat-lbl">% máximo</div><div className="ac-stat-val">{((s.cota/s.cfg?.cota_max)*100).toFixed(0)}%</div></div>
                  </div>
                  <div className="ac-bar" style={{ marginTop:10 }}>
                    <div className="ac-fill" style={{ width:`${Math.min((s.cota/s.cfg?.cota_max)*100,100).toFixed(1)}%`, background:'var(--danger)', height:'100%', borderRadius:99, transition:'width 1s' }}/>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {atencao.length > 0 && (
          <>
            <div style={{ fontSize:11, fontWeight:600, textTransform:'uppercase', letterSpacing:'.08em', color:'var(--warn)', marginBottom:10, fontFamily:'DM Mono,monospace' }}>Atenção</div>
            <div className="alertas-grid" style={{ marginBottom:20 }}>
              {atencao.map(s => (
                <div key={s.nome} className="alerta-card warn" onClick={() => { setCidade(s.nome); setPage('dashboard'); }} style={{ cursor:'pointer' }}>
                  <div className="ac-header">
                    <div><div className="ac-city">{s.nome}</div><div className="ac-sub">{s.cfg?.rio}</div></div>
                    <div className="ac-badge warn">{s.txt}</div>
                  </div>
                  <div className="ac-row">
                    <div className="ac-stat"><div className="ac-stat-lbl">Cota atual</div><div className="ac-stat-val" style={{ color:'var(--warn)' }}>{s.cota.toFixed(2)}m</div></div>
                    <div className="ac-stat"><div className="ac-stat-lbl">Cota alerta</div><div className="ac-stat-val">{s.cfg?.cota_alerta.toFixed(2)}m</div></div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        {normais.length > 0 && (
          <>
            <div style={{ fontSize:11, fontWeight:600, textTransform:'uppercase', letterSpacing:'.08em', color:'var(--accent)', marginBottom:10, fontFamily:'DM Mono,monospace' }}>Situação normal</div>
            <div className="alertas-grid">
              {normais.map(s => (
                <div key={s.nome} className="alerta-card ok" onClick={() => { setCidade(s.nome); setPage('dashboard'); }} style={{ cursor:'pointer' }}>
                  <div className="ac-header">
                    <div><div className="ac-city">{s.nome}</div><div className="ac-sub">{s.cfg?.rio}</div></div>
                    <div className="ac-badge ok">Normal</div>
                  </div>
                  <div className="ac-row">
                    <div className="ac-stat"><div className="ac-stat-lbl">Cota atual</div><div className="ac-stat-val" style={{ color:'var(--accent)' }}>{s.cota.toFixed(2)}m</div></div>
                    <div className="ac-stat"><div className="ac-stat-lbl">Cota alerta</div><div className="ac-stat-val">{s.cfg?.cota_alerta.toFixed(2)}m</div></div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </>
    );
  };

  const renderEstacoes = () => (
    <>
      {/* Mapa grande */}
      <div className="card" style={{ marginBottom:16, padding:0, overflow:'hidden' }}>
        <div style={{ padding:'14px 16px 10px', borderBottom:'1px solid var(--border)', display:'flex', alignItems:'center', justifyContent:'space-between' }}>
          <div>
            <div className="card-ttl">Mapa de estações</div>
            <div className="card-sub" style={{ margin:0 }}>Clique para selecionar e ver dados no Dashboard</div>
          </div>
          <div style={{ display:'flex', gap:12 }}>
            {[['#1B7C6C','Normal'],['#C07A20','Atenção'],['#C03030','Alerta']].map(([c,l]) => (
              <div key={l} style={{ display:'flex', alignItems:'center', gap:5, fontSize:10.5, color:'var(--muted)' }}>
                <div style={{ width:8, height:8, borderRadius:'50%', background:c }}/>
                {l}
              </div>
            ))}
          </div>
        </div>
        <div style={{ height:380 }}><div id="mapa-leaflet" ref={mapaRef} style={{ width:'100%', height:'100%' }}/></div>
      </div>

      {/* Tabela */}
      <div className="table-wrap">
        <div className="trow thead">
          <span>Estação</span>
          <span style={{ textAlign:'right' }}>Cota (m)</span>
          <span style={{ textAlign:'right' }}>Alerta (m)</span>
          <span style={{ textAlign:'right' }}>% Máx</span>
          <span style={{ textAlign:'right' }}>Fonte</span>
          <span style={{ textAlign:'right' }}>Status</span>
        </div>
        {allStationsData.map(s => {
          const pct2 = s.cfg ? Math.min((s.cota/s.cfg.cota_max)*100,100) : 0;
          const chipCls = s.cls === 'g' ? 'chip-ok' : s.cls === 'w' ? 'chip-warn' : 'chip-dang';
          const isSelected = s.nome === cidade;
          return (
            <div key={s.nome} className={`trow${isSelected?' sel':''}`} onClick={() => { setCidade(s.nome); setPage('dashboard'); }}>
              <div>
                <div className="t-name">{s.nome}</div>
                <div className="t-sub">{s.cfg?.rio || ''}</div>
              </div>
              <div className="t-num" style={{ color: s.cls==='g'?'var(--accent)':s.cls==='w'?'var(--warn)':'var(--danger)' }}>
                {s.cota.toFixed(2)}
              </div>
              <div className="t-num">{s.cfg?.cota_alerta.toFixed(2) || '—'}</div>
              <div className="t-num">{pct2.toFixed(0)}%</div>
              <div className="t-num" style={{ fontSize:11, color:'var(--muted)' }}>
                {s.fonte === 'sace' ? 'SACE' : s.fonte === 'open-meteo' ? 'Open-Meteo' : s.fonte || '—'}
              </div>
              <div className="t-status">
                <span className={`status-chip ${chipCls}`}>{s.txt}</span>
              </div>
            </div>
          );
        })}
      </div>
    </>
  );

  const renderPrevisao = () => (
    <>
      <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(300px,1fr))', gap:14 }}>
        {estacoes.map(nome => {
          const inf = dados[nome] || {};
          const lst = inf.dados || [];
          const cfgg = CONFIG_ESTACOES[nome];
          const pico2 = estimarPico(lst);
          const { cls: cl2 } = classificar(lst[lst.length-1]?.cota_m ?? 0, cfgg);
          if (!pico2) return null;
          return (
            <div key={nome} className="card" onClick={() => { setCidade(nome); setPage('dashboard'); }} style={{ cursor:'pointer' }}>
              <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start', marginBottom:10 }}>
                <div>
                  <div className="card-ttl">{nome}</div>
                  <div className="card-sub" style={{ margin:0 }}>{cfgg?.rio}</div>
                </div>
                <span className={`page-badge ${cl2==='g'?'badge-ok':cl2==='w'?'badge-warn':'badge-danger'}`}>
                  {pico2.tendencia > 0 ? `+${pico2.tendencia.toFixed(3)}m/dia` : 'Estável'}
                </span>
              </div>
              <div style={{ display:'flex', gap:20 }}>
                <div><div className="n-lbl">Pico estimado</div><div className="n-val" style={{ fontSize:15 }}>{pico2.data}</div></div>
                <div><div className="n-lbl">Cota estimada</div><div className="n-val" style={{ fontSize:15 }}>{pico2.cota}m</div></div>
              </div>
              {lst.length > 0 && (
                <div style={{ height:60, marginTop:12 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={lst.slice(-30)} margin={{ top:0, right:0, left:0, bottom:0 }}>
                      <Line type="monotone" dataKey="cota_m" stroke={cl2==='g'?'var(--accent)':cl2==='w'?'var(--warn)':'var(--danger)'} strokeWidth={1.5} dot={false}/>
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </>
  );

  const pageConfig = {
    dashboard: { title: 'Dashboard', sub: `${cidade} — monitoramento em tempo real` },
    alertas:   { title: 'Alertas',   sub: 'Situação atual em todas as estações' },
    estacoes:  { title: 'Estações',  sub: `${estacoes.length} estações fluviométricas monitoradas` },
    previsao:  { title: 'Previsão',  sub: 'Estimativas de tendência por estação' },
  };
  const pc = pageConfig[page];

  return (
    <>
      <style>{css}</style>
      <div className="shell">

        {/* SIDEBAR */}
        <aside className={`sidebar${sidebar ? '' : ' collapsed'}`}>
          <div className="sb-logo">
            <div className="sb-mark"><Icon type="wave"/></div>
            <div>
              <div className="sb-name">Rio Amazonas</div>
              <div className="sb-sub">Monitor Fluviométrico</div>
            </div>
          </div>

          <div className="sb-section">
            <div className="sb-section-lbl">Navegação</div>
            {PAGES.map(p => (
              <div key={p.id} className={`nav-item${page === p.id ? ' active' : ''}`} onClick={() => setPage(p.id)}>
                <Icon type={p.icon} size={15}/>
                {p.label}
                {p.badge && hasAlerts && <span className="nav-badge"/>}
              </div>
            ))}
          </div>

          <div className="sb-section" style={{ marginTop:'auto', paddingTop:8 }}>
            <div className="sb-section-lbl">Estações</div>
            {estacoes.map(c => {
              const inf = dados[c] || {};
              const lst = inf.dados || [];
              const u = lst[lst.length-1] || {};
              const co = u.cota_m ?? 0;
              const { cls: cl } = classificar(co, CONFIG_ESTACOES[c]);
              const dotColor = cl==='g'?'var(--accent)':cl==='w'?'var(--warn)':'var(--danger)';
              return (
                <div key={c} className={`nav-item${c===cidade&&page==='dashboard'?' active':''}`}
                  onClick={() => { setCidade(c); setPage('dashboard'); }}>
                  <div style={{ width:7, height:7, borderRadius:'50%', background:dotColor, flexShrink:0 }}/>
                  <span style={{ flex:1 }}>{c}</span>
                  <span style={{ fontSize:11, fontFamily:'DM Mono,monospace', opacity:.6 }}>{co.toFixed(1)}m</span>
                </div>
              );
            })}
          </div>

          <div className="sb-footer">
            <div className="sb-live">
              <div className={`sb-dot${error?' off':''}`}/>
              <span className="sb-live-txt">{error ? 'Offline' : 'Ao vivo'}</span>
              <span className="sb-live-val">{new Date().toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'})}</span>
            </div>
          </div>
        </aside>

        {/* MAIN */}
        <div className="main">
          <header className="topbar">
            <button className={`toggle-btn${sidebar?' open':''}`} onClick={() => setSidebar(s => !s)}>
              <span/><span/><span/>
            </button>
            <div className="topbar-title">
              <h1>{pc.title}</h1>
              <p>{pc.sub}</p>
            </div>
            <div className="topbar-right">
              {page === 'alertas' && <span className={`page-badge ${hasAlerts?'badge-danger':'badge-ok'}`}>{hasAlerts?'Alertas ativos':'Tudo normal'}</span>}
              <button className="pill-btn" onClick={() => carregar(cidade, periodo)} disabled={loading}>↺ Atualizar</button>
              <button className="pill-btn" onClick={() => setTema(t => t==='dark'?'light':'dark')}>
                {tema==='dark'?'☀ Claro':'◐ Escuro'}
              </button>
            </div>
          </header>

          <div className="scroll-area">
            {loading && estacoes.length === 0
              ? <div className="state"><div className="spinner"/><span>Carregando…</span></div>
              : page === 'dashboard' ? renderDashboard()
              : page === 'alertas'   ? renderAlertas()
              : page === 'estacoes'  ? renderEstacoes()
              : page === 'previsao'  ? renderPrevisao()
              : null
            }
          </div>

          <footer className="footer">
            Rio Amazonas · SACE/SGB · {new Date().toLocaleDateString('pt-BR',{day:'2-digit',month:'long',year:'numeric'})}
          </footer>
        </div>
      </div>
    </>
  );
}
