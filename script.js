// A.O.W.I Pro v8.2 — offline minimal engine (deterministic, GitHub Pages safe)
const APP_VERSION = 'v8.2-pro-offline';

const el = q => document.querySelector(q);
const $cards = el('#cardsView');
const $table = el('#tableView');
const $logs = el('#logs');
const $snap = el('#snapshot');
const $view = el('#viewMode');
const $posture = el('#posture');
const $price = el('#price');
const $atr = el('#atr');
const $analyze = el('#analyze');
const $clear = el('#clear');

// Single source of truth
const state = {
  anchor: null,
  atr: null,
  posture: 'classic',
  schedule: null,
  lastSource: 'Manual',
};

function log(msg){ $logs.textContent += msg + '\n'; $logs.scrollTop = $logs.scrollHeight; }
function fmt(n){ return Number(n).toFixed(2); }

// Simple deterministic 24h template
const WINDOWS = [
  ['01:00','Asia Early','SELL','SHORT'],
  ['03:00','Asia Mid','SELL','SHORT'],
  ['05:00','Asia Late','SELL','SHORT'],
  ['07:50','Pre-London','BUY','LONG'],
  ['08:05','London Open','SELL','SHORT'],
  ['08:20','London Open','SELL','SHORT'],
  ['11:00','London Mid','SELL','SHORT'],
  ['12:50','EU Lunch','BUY','LONG'],
  ['14:00','US Pre-data','SELL','SHORT'],
  ['15:05','US Data','SELL','SHORT'],
  ['15:20','US Data','SELL','SHORT'],
  ['16:50','London Close','BUY','LONG'],
  ['18:00','US Mid','SELL','SHORT'],
  ['20:00','US Late','SELL','SHORT'],
  ['22:50','Asia Pre-open','BUY','LONG'],
  ['23:50','Roll','BUY','LONG'],
];

// Posture multipliers
const POSTURE = {
  classic: { tp1:0.6, tp2:1.2, tp3:1.8, sl:1.3, entryBand:0.30 },
  aggr:    { tp1:0.8, tp2:1.6, tp3:2.4, sl:1.1, entryBand:0.35 },
  cons:    { tp1:0.45,tp2:0.9, tp3:1.35,sl:1.6, entryBand:0.25 }
};

function computeSchedule(anchor, atr, postureKey){
  const P = POSTURE[postureKey] || POSTURE.classic;
  const rows = WINDOWS.map(([t,label,act,side], i)=>{
    // Entry band logic (absolute)
    const dir = (act === 'BUY') ? -1 : 1; // buy below anchor, sell above anchor
    const half = P.entryBand * atr;
    const center = anchor + dir * (0.55 * atr);
    const entryLow = center - half;
    const entryHigh = center + half;

    // Targets and Stop from entry center
    const tp1 = center + (act==='BUY' ? 1 : -1) * (P.tp1*atr);
    const tp2 = center + (act==='BUY' ? 1 : -1) * (P.tp2*atr);
    const tp3 = center + (act==='BUY' ? 1 : -1) * (P.tp3*atr);
    const sl  = center + (act==='BUY' ? -1 : 1) * (P.sl*atr);

    // Simple confidence score scaling with time buckets (make it deterministic)
    const baseScore = 55 + Math.round( (Math.sin(i*1.7)+1)*10 ); // 55..75
    const prob = 25 + Math.round((baseScore-55) * 0.5); // ~P%

    return {
      time:t, window:label, action:act, side:side,
      entry:[entryLow, entryHigh],
      tp1, tp2, tp3, sl,
      score: baseScore, prob
    };
  });
  return rows;
}

function renderCards(schedule){
  $cards.innerHTML = '';
  schedule.forEach(w=>{
    const card = document.createElement('div');
    card.className = 'card glow';
    card.innerHTML = `
      <div class="head">
        <div class="window">${w.time} → ${w.window}</div>
        <div class="badge">Score ${w.score} • P≈${w.prob}%</div>
      </div>
      <div class="rowKV">
        <div class="kv"><div class="label">Direction</div><div class="value ${w.action==='BUY'?'buy':'sell'}">${w.side} • ${w.action}</div></div>
        <div class="kv"><div class="label">Entry</div><div class="value">${fmt(w.entry[0])} – ${fmt(w.entry[1])}</div></div>
        <div class="kv"><div class="label">TP1</div><div class="value tp">${fmt(w.tp1)}</div></div>
        <div class="kv"><div class="label">TP2</div><div class="value tp">${fmt(w.tp2)}</div></div>
        <div class="kv"><div class="label">TP3</div><div class="value tp">${fmt(w.tp3)}</div></div>
        <div class="kv"><div class="label">Stop</div><div class="value stop">${fmt(w.sl)}</div></div>
      </div>
    `;
    $cards.appendChild(card);
  });
}

function renderTable(schedule){
  $table.innerHTML = '';
  const tbl = document.createElement('table');
  tbl.className = 'table';
  tbl.innerHTML = `
    <thead><tr>
      <th>Time</th><th>Window</th><th>Action</th>
      <th>Entry</th><th>Targets</th><th>Stop</th>
    </tr></thead>
    <tbody></tbody>`;
  const tb = tbl.querySelector('tbody');
  schedule.forEach(w=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${w.time}</td>
      <td>${w.window}</td>
      <td class="${w.action==='BUY'?'buy':'sell'}">${w.side} • ${w.action}</td>
      <td>${fmt(w.entry[0])} – ${fmt(w.entry[1])}</td>
      <td>TP1 ${fmt(w.tp1)} • TP2 ${fmt(w.tp2)} • TP3 ${fmt(w.tp3)}</td>
      <td class="sell">${fmt(w.sl)}</td>`;
    tb.appendChild(tr);
  });
  $table.appendChild(tbl);
}

function updateSnapshot(){
  const snap = [
    ['From', state.lastSource],
    ['Anchor', state.anchor!=null ? fmt(state.anchor) : '—'],
    ['ATR', state.atr!=null ? fmt(state.atr) : '—'],
    ['Posture', state.posture.toUpperCase()],
    ['Windows', state.schedule ? state.schedule.length : 0],
  ];
  $snap.innerHTML = snap.map(([k,v])=>`<div>${k}: <b>${v}</b></div>`).join('');
}

function recalcAndRender(){
  if(state.anchor==null || state.atr==null){ log('Provide Price + ATR first.'); return; }
  if(!state.schedule){
    state.schedule = computeSchedule(state.anchor, state.atr, state.posture);
  }
  // Toggle views without recomputing
  if($view.value === 'cards'){
    $table.classList.add('hidden'); $cards.classList.remove('hidden');
    renderCards(state.schedule);
  }else{
    $cards.classList.add('hidden'); $table.classList.remove('hidden');
    renderTable(state.schedule);
  }
  updateSnapshot();
}

$view.addEventListener('change', ()=>{
  // Only re-render existing schedule; do NOT recompute
  recalcAndRender();
});

$posture.addEventListener('change', ()=>{
  state.posture = $posture.value;
  // Recompute with posture change
  state.schedule = computeSchedule(state.anchor, state.atr, state.posture);
  recalcAndRender();
});

$analyze.addEventListener('click', ()=>{
  const p = parseFloat(($price.value || '').replace(',', '.'));
  const a = parseFloat(($atr.value || '').replace(',', '.'));
  if(!isFinite(p) || !isFinite(a)){ log('Invalid Price or ATR.'); return; }
  state.anchor = p; state.atr = a; state.posture = $posture.value;
  state.lastSource = 'Manual';
  state.schedule = computeSchedule(state.anchor, state.atr, state.posture);
  $logs.textContent = '';
  log(`Schedule ready. Source: ${state.lastSource}. Anchor=${fmt(p)} ATR=${fmt(a)} Posture=${state.posture}`);
  recalcAndRender();
});

$clear.addEventListener('click', ()=>{
  state.anchor = null; state.atr = null; state.schedule = null;
  $price.value=''; $atr.value=''; $logs.textContent=''; $snap.innerHTML='';
  $cards.innerHTML=''; $table.innerHTML='';
  log('Cleared.');
});

// Defaults
$view.value = 'cards';
$posture.value = 'classic';
