from flask import Flask, render_template_string

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Matrix Addition Calculator</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@500;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f7f7f5;
    --surface: #ffffff;
    --border: #e2e2dc;
    --border-strong: #c8c8c0;
    --accent-a: #185FA5;
    --accent-b: #3B6D11;
    --accent-r: #A32D2D;
    --text: #1a1a1a;
    --muted: #6b6b66;
    --cell-bg: #f0f4fb;
    --cell-focus-border: #378ADD;
    --cell-focus-bg: #ffffff;
    --result-bg: #fdf0f0;
    --result-border: #f0c0c0;
    --result-text: #A32D2D;
    --pill-bg: #f0f0ea;
    --sidebar-w: 260px;
    --sidebar-collapsed: 56px;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --transition: 0.28s cubic-bezier(.4,0,.2,1);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: "Space Mono", monospace;
    min-height: 100vh;
    display: flex;
  }

  .sidebar {
    width: var(--sidebar-w);
    min-height: 100vh;
    background: var(--surface);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    position: fixed;
    top: 0; left: 0; bottom: 0;
    overflow: hidden;
    transition: width var(--transition);
    z-index: 100;
  }
  .sidebar.collapsed { width: var(--sidebar-collapsed); }

  .sidebar-toggle {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 14px 14px 10px;
    border-bottom: 1px solid var(--border);
    flex-shrink: 0;
  }
  .sidebar.collapsed .sidebar-toggle { justify-content: center; }
  .toggle-btn {
    background: none;
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-sm);
    width: 30px; height: 30px;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    color: var(--muted);
    transition: border-color 0.15s, color 0.15s;
    flex-shrink: 0;
  }
  .toggle-btn:hover { border-color: var(--accent-a); color: var(--accent-a); }
  .toggle-btn svg { width: 16px; height: 16px; transition: transform var(--transition); }
  .sidebar.collapsed .toggle-btn svg { transform: rotate(180deg); }

  .sidebar-nav {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 10px 8px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .sidebar-nav::-webkit-scrollbar { width: 3px; }
  .sidebar-nav::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }

  .nav-section-label {
    font-size: 0.58rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    padding: 10px 10px 4px;
    white-space: nowrap;
    overflow: hidden;
    opacity: 1;
    transition: opacity var(--transition);
  }
  .sidebar.collapsed .nav-section-label { opacity: 0; pointer-events: none; }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 10px;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    white-space: nowrap;
    overflow: hidden;
    color: var(--text);
    border: none;
    background: none;
    width: 100%;
    text-align: left;
    font-family: "Space Mono", monospace;
    font-size: 0.75rem;
  }
  .nav-item:hover { background: var(--bg); }
  .nav-item.active { background: #e8f0fb; color: var(--accent-a); }
  .nav-item.danger { color: var(--accent-r); }
  .nav-item.danger:hover { background: #fdf0f0; }
  .nav-icon {
    flex-shrink: 0;
    width: 20px; height: 20px;
    display: flex; align-items: center; justify-content: center;
  }
  .nav-icon svg { width: 18px; height: 18px; }
  .nav-label {
    opacity: 1;
    transition: opacity var(--transition);
    font-size: 0.75rem;
  }
  .sidebar.collapsed .nav-label { opacity: 0; pointer-events: none; }

  .nav-divider {
    height: 1px;
    background: var(--border);
    margin: 6px 4px;
  }

  .profile-section {
    display: none;
    flex-direction: column;
    gap: 0;
    padding: 0 8px 8px;
    overflow: hidden;
  }
  .profile-section.open { display: flex; }
  .sidebar.collapsed .profile-section { display: none !important; }
  .profile-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .profile-avatar {
    width: 48px; height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #e8f0fb, #d0e4f7);
    border: 2px solid var(--border-strong);
    display: flex; align-items: center; justify-content: center;
    font-family: "Syne", sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--accent-a);
  }
  .profile-info { display: flex; flex-direction: column; gap: 2px; }
  .profile-name { font-size: 0.8rem; font-weight: 700; color: var(--text); }
  .profile-email { font-size: 0.65rem; color: var(--muted); }
  .profile-badge {
    display: inline-block;
    background: #e8f0fb;
    color: var(--accent-a);
    font-size: 0.58rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 999px;
    border: 1px solid #c5d8f0;
    width: fit-content;
  }

  .history-section {
    display: none;
    flex-direction: column;
    gap: 6px;
    padding: 0 8px 8px;
    max-height: 340px;
    overflow-y: auto;
  }
  .history-section.open { display: flex; }
  .sidebar.collapsed .history-section { display: none !important; }
  .history-section::-webkit-scrollbar { width: 3px; }
  .history-section::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
  .history-empty {
    text-align: center;
    color: var(--muted);
    font-size: 0.63rem;
    padding: 20px 10px;
    line-height: 1.8;
    opacity: 0.7;
  }
  .history-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 10px 12px;
    cursor: pointer;
    transition: border-color 0.15s, transform 0.15s;
    animation: slideIn 0.2s ease;
  }
  @keyframes slideIn {
    from { opacity: 0; transform: translateX(-10px); }
    to   { opacity: 1; transform: translateX(0); }
  }
  .history-card:hover { border-color: var(--accent-a); transform: translateX(2px); }
  .history-card-top {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 6px;
  }
  .history-card-index { font-size: 0.58rem; letter-spacing: 1px; text-transform: uppercase; color: var(--muted); }
  .history-card-time  { font-size: 0.56rem; color: var(--muted); opacity: 0.8; }
  .history-card-eq    { font-size: 0.62rem; color: var(--text); line-height: 1.8; word-break: break-all; }
  .history-card-eq .ha { color: var(--accent-a); font-weight: 700; }
  .history-card-eq .hb { color: var(--accent-b); font-weight: 700; }
  .history-card-eq .hr { color: var(--accent-r); font-weight: 700; }
  .history-card-eq .op { color: var(--muted); margin: 0 2px; }
  .btn-clear-sm {
    background: transparent;
    border: 1px solid var(--border-strong);
    color: var(--muted);
    font-family: "Space Mono", monospace;
    font-size: 0.6rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 6px 12px;
    border-radius: 999px;
    cursor: pointer;
    transition: border-color 0.15s, color 0.15s;
    width: 100%;
  }
  .btn-clear-sm:hover { border-color: var(--accent-r); color: var(--accent-r); }

  .settings-section {
    display: none;
    flex-direction: column;
    gap: 0;
    padding: 0 8px 8px;
  }
  .settings-section.open { display: flex; }
  .sidebar.collapsed .settings-section { display: none !important; }
  .settings-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .setting-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .setting-label { font-size: 0.7rem; color: var(--text); }
  .setting-sub { font-size: 0.6rem; color: var(--muted); margin-top: 1px; }
  .toggle-switch {
    width: 36px; height: 20px;
    background: var(--border-strong);
    border-radius: 999px;
    position: relative;
    cursor: pointer;
    transition: background 0.2s;
    flex-shrink: 0;
    border: none;
  }
  .toggle-switch.on { background: var(--accent-a); }
  .toggle-switch::after {
    content: '';
    position: absolute;
    width: 14px; height: 14px;
    background: #fff;
    border-radius: 50%;
    top: 3px; left: 3px;
    transition: transform 0.2s;
  }
  .toggle-switch.on::after { transform: translateX(16px); }

  .sidebar-bottom {
    padding: 8px;
    border-top: 1px solid var(--border);
    flex-shrink: 0;
  }

  .main {
    margin-left: var(--sidebar-w);
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 48px 24px 80px;
    transition: margin-left var(--transition);
  }
  .main.collapsed { margin-left: var(--sidebar-collapsed); }

  .header { text-align: center; margin-bottom: 36px; }
  .header h1 {
    font-family: "Syne", sans-serif;
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
  }
  .header h1 span.a { color: var(--accent-a); }
  .header h1 span.b { color: var(--accent-b); }
  .header h1 span.r { color: var(--accent-r); }
  .header p { font-size: 0.72rem; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; }

  .size-card {
    display: flex; align-items: center; gap: 14px;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-lg); padding: 14px 24px;
    margin-bottom: 28px; flex-wrap: wrap; justify-content: center;
  }
  .size-card label { font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); }
  .size-card input[type=number] {
    width: 56px; height: 36px;
    border: 1px solid var(--border-strong); border-radius: var(--radius-sm);
    font-family: "Space Mono", monospace; font-size: 0.95rem;
    text-align: center; background: var(--cell-bg); color: var(--text); outline: none;
    transition: border-color 0.15s;
  }
  .size-card input[type=number]:focus { border-color: var(--cell-focus-border); }
  .size-sep { color: var(--muted); font-size: 1rem; }
  .size-hint { font-size: 0.65rem; color: var(--muted); letter-spacing: 1px; }

  .action-row {
    display: flex; gap: 10px; margin-bottom: 32px;
    flex-wrap: wrap; justify-content: center;
  }
  .btn-primary {
    background: var(--accent-a); color: #fff; border: none;
    font-family: "Space Mono", monospace; font-size: 0.8rem;
    font-weight: 700; letter-spacing: 0.5px; padding: 11px 28px;
    border-radius: 999px; cursor: pointer; transition: opacity 0.15s, transform 0.1s;
  }
  .btn-primary:hover { opacity: 0.88; transform: translateY(-1px); }
  .btn-primary:active { transform: translateY(0); }
  .btn-secondary {
    background: transparent; color: var(--muted);
    border: 1px solid var(--border-strong);
    font-family: "Space Mono", monospace; font-size: 0.75rem;
    letter-spacing: 0.5px; padding: 11px 20px; border-radius: 999px;
    cursor: pointer; transition: border-color 0.15s, color 0.15s, transform 0.1s;
  }
  .btn-secondary:hover { border-color: var(--text); color: var(--text); transform: translateY(-1px); }
  .btn-secondary:active { transform: translateY(0); }

  .matrices-area {
    display: flex; align-items: flex-start; gap: 18px;
    flex-wrap: wrap; justify-content: center; margin-bottom: 28px;
  }
  .mat-block { display: flex; flex-direction: column; align-items: center; gap: 10px; }
  .mat-label {
    font-family: "Syne", sans-serif; font-size: 0.85rem;
    font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
  }
  .mat-label.a { color: var(--accent-a); }
  .mat-label.b { color: var(--accent-b); }
  .mat-label.r { color: var(--accent-r); }
  .mat-op { font-size: 2rem; font-weight: 700; color: var(--muted); padding-top: 34px; line-height: 1; user-select: none; }
  .bracket-wrap { display: flex; align-items: center; gap: 2px; }
  .bracket { font-size: 2.8rem; font-weight: 200; color: var(--border-strong); line-height: 1; user-select: none; }
  .mat-table { border-collapse: collapse; }
  .mat-table th { font-size: 0.6rem; color: var(--muted); text-align: center; padding: 2px 4px 6px; font-weight: 400; letter-spacing: 1px; }
  .mat-table td { padding: 3px; }
  .mat-table input {
    width: 56px; height: 42px;
    border: 1px solid var(--border-strong); border-radius: var(--radius-sm);
    background: var(--cell-bg); color: var(--text);
    font-family: "Space Mono", monospace; font-size: 0.9rem;
    text-align: center; outline: none;
    transition: border-color 0.15s, background 0.15s, box-shadow 0.15s;
  }
  .mat-table input:hover { border-color: var(--cell-focus-border); background: var(--cell-focus-bg); }
  .mat-table input:focus {
    border-color: var(--cell-focus-border);
    box-shadow: 0 0 0 3px rgba(55,138,221,0.12);
    background: var(--cell-focus-bg);
  }
  .mat-table input.result-inp {
    background: var(--result-bg); border-color: var(--result-border);
    color: var(--result-text); font-weight: 700; pointer-events: none;
  }
  .info-row { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
  .info-pill {
    background: var(--pill-bg); border: 1px solid var(--border);
    border-radius: 999px; padding: 5px 14px;
    font-size: 0.68rem; color: var(--muted); letter-spacing: 0.5px;
  }
</style>
</head>
<body>

<aside class="sidebar" id="sidebar">

  <div class="sidebar-toggle">
    <button class="toggle-btn" onclick="toggleSidebar()" title="Toggle sidebar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="6"/><line x1="18" y1="12" x2="6" y2="12"/><line x1="18" y1="18" x2="6" y2="18"/>
      </svg>
    </button>
  </div>

  <div class="sidebar-nav" id="sidebar-nav">

    <div class="nav-section-label">Account</div>
    <button class="nav-item active" onclick="toggleSection('profile')">
      <span class="nav-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
        </svg>
      </span>
      <span class="nav-label">Profile</span>
    </button>
    <div class="profile-section open" id="section-profile">
      <div class="profile-card">
        <div class="profile-avatar">JD</div>
        <div class="profile-info">
          <div class="profile-name">John Doe</div>
          <div class="profile-email">john.doe@email.com</div>
        </div>
        <span class="profile-badge">Pro Plan</span>
      </div>
    </div>

    <div class="nav-divider"></div>

    <div class="nav-section-label">Data</div>
    <button class="nav-item" onclick="toggleSection('history')">
      <span class="nav-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 15"/>
        </svg>
      </span>
      <span class="nav-label">History</span>
    </button>
    <div class="history-section" id="section-history">
      <div class="history-empty" id="history-empty">No calculations yet.<br>Results will appear here.</div>
      <button class="btn-clear-sm" onclick="clearHistory()">Clear History</button>
    </div>

    <div class="nav-divider"></div>

    <div class="nav-section-label">Preferences</div>
    <button class="nav-item" onclick="toggleSection('settings')">
      <span class="nav-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="3"/>
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
        </svg>
      </span>
      <span class="nav-label">Settings</span>
    </button>
    <div class="settings-section" id="section-settings">
      <div class="settings-card">
        <div class="setting-row">
          <div>
            <div class="setting-label">Auto-calculate</div>
            <div class="setting-sub">Calculate on input change</div>
          </div>
          <button class="toggle-switch" id="toggle-auto" onclick="this.classList.toggle('on')"></button>
        </div>
        <div class="nav-divider"></div>
        <div class="setting-row">
          <div>
            <div class="setting-label">Show headers</div>
            <div class="setting-sub">Row &amp; column labels</div>
          </div>
          <button class="toggle-switch on" id="toggle-headers" onclick="this.classList.toggle('on')"></button>
        </div>
        <div class="nav-divider"></div>
        <div class="setting-row">
          <div>
            <div class="setting-label">Save history</div>
            <div class="setting-sub">Keep past calculations</div>
          </div>
          <button class="toggle-switch on" id="toggle-history" onclick="this.classList.toggle('on')"></button>
        </div>
      </div>
    </div>

  </div>

  <div class="sidebar-bottom">
    <button class="nav-item danger" onclick="alert('Logged out!')">
      <span class="nav-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
      </span>
      <span class="nav-label">Log Out</span>
    </button>
  </div>

</aside>

<main class="main" id="main">

  <div class="header">
    <h1><span class="a">Addition</span> Matrix <span class="b">Calculator</span><span class="r"></span></h1>
    <p>Matrix Addition Calculator</p>
  </div>

  <div class="size-card">
    <label>Rows</label>
    <input type="number" id="inp-rows" value="3" min="1" max="8" onchange="onSizeChange()" />
    <span class="size-sep">&times;</span>
    <label>Cols</label>
    <input type="number" id="inp-cols" value="3" min="1" max="8" onchange="onSizeChange()" />
    <span class="size-hint">max 8 &times; 8</span>
  </div>

  <div class="action-row">
    <button class="btn-primary" onclick="calculate()">Calculate A + B</button>
    <button class="btn-secondary" onclick="resetAll()">Reset</button>
  </div>

  <div class="matrices-area" id="matrices-area"></div>

  <div class="info-row">
    <span class="info-pill" id="info-size">3 &times; 3</span>
    <span class="info-pill">Both matrices must match in size</span>
  </div>

</main>

<script>
  let rows = 3, cols = 3;
  let dataA, dataB, dataR;
  let history = [];

  // ── SIDEBAR ──
  function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('collapsed');
    document.getElementById('main').classList.toggle('collapsed');
  }

  function toggleSection(name) {
    const sec = document.getElementById('section-' + name);
    sec.classList.toggle('open');
    // update active state on nav items
    const items = document.querySelectorAll('.nav-item');
    items.forEach(item => {
      if (item.getAttribute('onclick') === "toggleSection('" + name + "')") {
        item.classList.toggle('active', sec.classList.contains('open'));
      }
    });
  }

  //Logic
  function empty(r, c) { return Array.from({length: r}, () => Array(c).fill(0)); }
  function clamp(v, lo, hi) { return Math.min(hi, Math.max(lo, v)); }

  function syncMatrix(prefix, data) {
    for (let r = 0; r < rows; r++)
      for (let c = 0; c < cols; c++) {
        const el = document.getElementById(prefix + '-' + r + '-' + c);
        if (el) { const v = parseFloat(el.value); data[r][c] = isNaN(v) ? 0 : v; }
      }
  }

  function buildTable(prefix, data, readOnly) {
    const tbl = document.createElement('table');
    tbl.className = 'mat-table';
    const hrow = document.createElement('tr');
    hrow.innerHTML = '<th></th>';
    for (let c = 0; c < cols; c++) hrow.innerHTML += '<th>C' + (c+1) + '</th>';
    tbl.appendChild(hrow);
    for (let r = 0; r < rows; r++) {
      const tr = document.createElement('tr');
      const th = document.createElement('th');
      th.textContent = 'R' + (r+1);
      tr.appendChild(th);
      for (let c = 0; c < cols; c++) {
        const td = document.createElement('td');
        const inp = document.createElement('input');
        inp.type = 'text';
        inp.id = prefix + '-' + r + '-' + c;
        inp.value = data[r][c];
        if (readOnly) { inp.readOnly = true; inp.tabIndex = -1; inp.className = 'result-inp'; }
        td.appendChild(inp); tr.appendChild(td);
      }
      tbl.appendChild(tr);
    }
    return tbl;
  }

  function render() {
    const area = document.getElementById('matrices-area');
    area.innerHTML = '';
    const parts = [
      {prefix:'a', label:'Matrix A', cls:'a', data:dataA, readOnly:false},
      {sym:'+'},
      {prefix:'b', label:'Matrix B', cls:'b', data:dataB, readOnly:false},
      {sym:'='},
      {prefix:'r', label:'Result R', cls:'r', data:dataR, readOnly:true},
    ];
    parts.forEach(p => {
      if (p.sym) {
        const d = document.createElement('div');
        d.className = 'mat-op'; d.textContent = p.sym;
        area.appendChild(d); return;
      }
      const block = document.createElement('div'); block.className = 'mat-block';
      const lbl = document.createElement('div'); lbl.className = 'mat-label ' + p.cls; lbl.textContent = p.label;
      const bwrap = document.createElement('div'); bwrap.className = 'bracket-wrap';
      const bl = document.createElement('span'); bl.className = 'bracket'; bl.textContent = '[';
      const br = document.createElement('span'); br.className = 'bracket'; br.textContent = ']';
      bwrap.appendChild(bl); bwrap.appendChild(buildTable(p.prefix, p.data, p.readOnly)); bwrap.appendChild(br);
      block.appendChild(lbl); block.appendChild(bwrap);
      area.appendChild(block);
    });
    document.getElementById('info-size').textContent = rows + ' \xd7 ' + cols;
  }

  function matStr(m) {
    return '[' + m.map(row => '[' + row.map(v => { const n = parseFloat(v); return isNaN(n) ? 0 : n; }).join(',') + ']').join(', ') + ']';
  }
  function nowStr() {
    return new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', second:'2-digit'});
  }

  function renderHistory() {
    const list = document.getElementById('section-history');
    const emptyEl = document.getElementById('history-empty');
    const clearBtn = list.querySelector('.btn-clear-sm');
    list.querySelectorAll('.history-card').forEach(c => c.remove());
    if (history.length === 0) { emptyEl.style.display = ''; return; }
    emptyEl.style.display = 'none';
    history.forEach((entry, idx) => {
      const card = document.createElement('div');
      card.className = 'history-card';
      card.title = 'Click to reload';
      card.innerHTML =
        '<div class="history-card-top">' +
          '<span class="history-card-index">#' + (history.length - idx) + ' &middot; ' + entry.size + '</span>' +
          '<span class="history-card-time">' + entry.time + '</span>' +
        '</div>' +
        '<div class="history-card-eq">' +
          '<span class="ha">A</span><span class="op">=</span>' + matStr(entry.a) + '<br>' +
          '<span class="hb">B</span><span class="op">=</span>' + matStr(entry.b) + '<br>' +
          '<span class="hr">R</span><span class="op">=</span>' + matStr(entry.r) +
        '</div>';
      card.onclick = () => loadEntry(entry);
      list.insertBefore(card, clearBtn);
    });
  }

  function loadEntry(entry) {
    rows = entry.a.length; cols = entry.a[0].length;
    dataA = JSON.parse(JSON.stringify(entry.a));
    dataB = JSON.parse(JSON.stringify(entry.b));
    dataR = JSON.parse(JSON.stringify(entry.r));
    document.getElementById('inp-rows').value = rows;
    document.getElementById('inp-cols').value = cols;
    render();
  }

  function clearHistory() { history = []; renderHistory(); }

  function init() {
    dataA = empty(rows, cols); dataB = empty(rows, cols); dataR = empty(rows, cols);
    render();
  }

  function calculate() {
    syncMatrix('a', dataA); syncMatrix('b', dataB);
    dataR = Array.from({length: rows}, (_, r) =>
      Array.from({length: cols}, (_, c) => dataA[r][c] + dataB[r][c])
    );
    history.unshift({
      a: JSON.parse(JSON.stringify(dataA)),
      b: JSON.parse(JSON.stringify(dataB)),
      r: JSON.parse(JSON.stringify(dataR)),
      time: nowStr(), size: rows + 'x' + cols
    });
    render();
    renderHistory();
    // auto-open history section when a new calc is added
    const sec = document.getElementById('section-history');
    if (!sec.classList.contains('open')) toggleSection('history');
  }

  function resetAll() {
    dataA = empty(rows, cols); dataB = empty(rows, cols); dataR = empty(rows, cols);
    render();
  }

  function onSizeChange() {
    const nr = clamp(parseInt(document.getElementById('inp-rows').value) || 1, 1, 8);
    const nc = clamp(parseInt(document.getElementById('inp-cols').value) || 1, 1, 8);
    rows = nr; cols = nc;
    document.getElementById('inp-rows').value = rows;
    document.getElementById('inp-cols').value = cols;
    dataA = empty(rows, cols); dataB = empty(rows, cols); dataR = empty(rows, cols);
    render();
  }

  init();
</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
