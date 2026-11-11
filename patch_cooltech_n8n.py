#!/usr/bin/env python3
"""
Patch-Script: Erweitert coolTECH HTML um n8n-API-Artikelsuche.

Fügt ein:
1. Umschalter "Lokal / n8n-API" in der Artikelsuche
2. API-Suchfunktion die POST /cooltech-artikel aufruft
3. Ergebnis-Darstellung mit Preisvergleich REISS vs Beijer

Anwendung:
  python3 patch_cooltech_n8n.py coolTECH_v0.19.html coolTECH_v0.20.html

Die bestehende lokale Suche bleibt erhalten. Der Umschalter lässt den
Benutzer wählen ob er lokal (schnell, offline) oder über n8n (immer aktuell)
suchen möchte.
"""
import sys
import re

API_URL = "https://coolsulting.app.n8n.cloud/webhook/cooltech-artikel"

# CSS das eingefügt wird
PATCH_CSS = """
/* n8n-API-Suche */
.n8n-toggle{display:flex;gap:6px;align-items:center;margin:8px 0;font-size:13px}
.n8n-toggle label{display:inline-flex;align-items:center;gap:4px;cursor:pointer;font-weight:normal}
.n8n-toggle input[type=radio]{accent-color:#36A9E1;width:14px;height:14px}
.n8n-api-status{font-size:12px;color:#888;margin-left:8px}
.n8n-api-status.ok{color:#27ae60}
.n8n-api-status.err{color:#e74c3c}
.n8n-treffer{border:1px solid #e0e0e0;border-radius:8px;overflow:hidden;margin-top:8px}
.n8n-treffer table{width:100%;border-collapse:collapse;font-size:12px}
.n8n-treffer th{background:#36A9E1;color:#fff;padding:6px 8px;text-align:left;font-size:11px;position:sticky;top:0}
.n8n-treffer td{padding:5px 8px;border-bottom:1px solid #f0f0f0}
.n8n-treffer tr:hover td{background:#f0f8ff}
.n8n-treffer .guenstiger-r{color:#e74c3c;font-weight:600}
.n8n-treffer .guenstiger-b{color:#36A9E1;font-weight:600}
.n8n-treffer .guenstiger-g{color:#888}
.n8n-api-box{background:#fff;border-radius:10px;padding:16px;margin-top:10px;border-left:4px solid #36A9E1;box-shadow:0 2px 8px rgba(0,0,0,0.06)}
.n8n-api-box h4{margin:0 0 8px;font-size:14px;color:#3C3C3B}
.n8n-such-zeile{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.n8n-such-zeile input[type=text]{flex:1;min-width:200px;padding:8px 12px;border:2px solid #d0d0d0;border-radius:8px;font-size:14px;font-weight:bold;color:#36A9E1}
.n8n-such-zeile input:focus{border-color:#36A9E1;outline:none}
.n8n-such-zeile button{background:#3C3C3B;color:#fff;border:none;border-radius:8px;padding:8px 20px;font-weight:bold;cursor:pointer;font-size:13px}
.n8n-such-zeile button:hover{background:#555}
.n8n-info{font-size:12px;color:#888;margin-top:6px}
"""

# JavaScript das eingefügt wird
PATCH_JS = """
// === n8n-API-Artikelsuche ===
(function() {
  const N8N_API = '""" + API_URL + """';
  let n8nModus = 'lokal'; // 'lokal' oder 'api'

  // UI einfügen nach der bestehenden Artikelsuche
  function initN8nSuche() {
    // Finde den Artikel-Tab oder die Suchleiste
    const artikelTab = document.querySelector('[data-tab="artikel"], #artikelSuche, .artikel-suche, [id*="artikel"]');
    if (!artikelTab) {
      // Fallback: am Ende des body einfügen
      const box = document.createElement('div');
      box.id = 'n8nSucheBox';
      box.className = 'n8n-api-box';
      box.style.margin = '16px';
      box.innerHTML = buildN8nUI();
      document.body.appendChild(box);
    } else {
      // Vor der bestehenden Suche einfügen
      const box = document.createElement('div');
      box.id = 'n8nSucheBox';
      box.className = 'n8n-api-box';
      box.innerHTML = buildN8nUI();
      artikelTab.parentNode.insertBefore(box, artikelTab);
    }
    bindN8nEvents();
  }

  function buildN8nUI() {
    return '<h4>Artikelsuche (n8n-API)</h4>' +
      '<div class="n8n-such-zeile">' +
        '<input type="text" id="n8nSuchText" placeholder="Artikelnr., Bezeichnung, Hersteller oder Matchcode ..." autocomplete="off">' +
        '<button onclick="n8nSuchen()">Suchen</button>' +
        '<span class="n8n-api-status" id="n8nStatus"></span>' +
      '</div>' +
      '<div class="n8n-info" id="n8nInfo">Suche über n8n-API: 23.235 Artikel · REISS + Beijer Ref · Preisvergleich</div>' +
      '<div id="n8nErgebnis"></div>';
  }

  function bindN8nEvents() {
    const input = document.getElementById('n8nSuchText');
    if (input) {
      input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') n8nSuchen();
      });
    }
  }

  window.n8nSuchen = async function() {
    const text = (document.getElementById('n8nSuchText') || {}).value || '';
    if (!text.trim()) return;
    const status = document.getElementById('n8nStatus');
    const ergebnis = document.getElementById('n8nErgebnis');
    const info = document.getElementById('n8nInfo');
    status.textContent = 'suche ...';
    status.className = 'n8n-api-status';
    ergebnis.innerHTML = '';

    try {
      const res = await fetch(N8N_API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'suche', text: text.trim(), limit: 50 })
      });
      const data = await res.json();

      if (!data.ok) {
        status.textContent = data.error || 'Fehler';
        status.className = 'n8n-api-status err';
        return;
      }

      status.textContent = data.anzahl + ' Treffer';
      status.className = 'n8n-api-status ok';
      info.textContent = 'Gesucht: "' + data.gesucht + '" · ' + data.anzahl + ' von ' + (data.gesamt || '?') + ' Artikeln';

      if (!data.treffer || !data.treffer.length) {
        ergebnis.innerHTML = '<div style="padding:12px;color:#888;font-size:13px">Keine Artikel gefunden.</div>';
        return;
      }

      let html = '<div class="n8n-treffer" style="max-height:500px;overflow:auto"><table>';
      html += '<thead><tr><th>Art.-Nr.</th><th>Bezeichnung</th><th>Hersteller</th><th>BLP</th><th>EK REISS</th><th>Rab.</th><th>EK Beijer</th><th>Rab.</th><th>VK</th><th>Günstiger</th></tr></thead>';
      html += '<tbody>';
      data.treffer.forEach(function(a) {
        const cls = a.guenstiger === 'Beijer' ? 'guenstiger-b' : a.guenstiger === 'REISS' ? 'guenstiger-r' : 'guenstiger-g';
        html += '<tr>';
        html += '<td><b>' + esc(a.nr) + '</b></td>';
        html += '<td>' + esc(a.bezeichnung) + '</td>';
        html += '<td>' + esc(a.hersteller) + '</td>';
        html += '<td style="text-align:right">' + fmt(a.blp) + '</td>';
        html += '<td style="text-align:right">' + fmt(a.ek_reiss) + '</td>';
        html += '<td style="text-align:right">' + (a.rabatt_reiss || '') + '%</td>';
        html += '<td style="text-align:right">' + fmt(a.ek_beijer) + '</td>';
        html += '<td style="text-align:right">' + (a.rabatt_beijer || '') + '%</td>';
        html += '<td style="text-align:right"><b>' + fmt(a.vk) + '</b></td>';
        html += '<td class="' + cls + '">' + (a.guenstiger || '-') + '</td>';
        html += '</tr>';
      });
      html += '</tbody></table></div>';
      ergebnis.innerHTML = html;

    } catch (e) {
      status.textContent = 'API nicht erreichbar: ' + e.message;
      status.className = 'n8n-api-status err';
    }
  };

  function esc(s) { return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function fmt(v) { if (!v || v === '0' || v === '') return '-'; return parseFloat(v).toLocaleString('de-AT', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }

  // Init wenn DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initN8nSuche);
  } else {
    setTimeout(initN8nSuche, 500);
  }
})();
"""

def patch(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. CSS einfügen vor </style> oder </head>
    if '</style>' in html:
        html = html.replace('</style>', PATCH_CSS + '\n</style>', 1)
    elif '</head>' in html:
        html = html.replace('</head>', '<style>' + PATCH_CSS + '</style>\n</head>', 1)

    # 2. JavaScript einfügen vor </body>
    js_block = '<script>\n' + PATCH_JS + '\n</script>'
    if '</body>' in html:
        html = html.replace('</body>', js_block + '\n</body>', 1)
    else:
        html += '\n' + js_block

    # 3. Version in der Titelzeile hochsetzen
    html = re.sub(r'(Version\s+)v?0\.19', r'\g<1>v0.20', html)
    html = re.sub(r'(version\s+)v?0\.19', r'\g<1>v0.20', html, flags=re.IGNORECASE)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Patched: {input_path} -> {output_path}")
    print(f"  CSS: {len(PATCH_CSS)} chars added")
    print(f"  JS:  {len(PATCH_JS)} chars added")
    print(f"  API: {API_URL}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 patch_cooltech_n8n.py INPUT.html OUTPUT.html")
        sys.exit(1)
    patch(sys.argv[1], sys.argv[2])
