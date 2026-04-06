# °coolWIRE – CLAUDE.md für Claude Code
# Stand: 06.04.2026

## Projekt
Streamlit-Kälteplanungstool von coolsulting e.U. (Michael Schäpers, Linz AT)
Port: 8580 | Starter: START_coolWIRE.bat
Pfad: C:\Users\MichaelSchäpers\Documents\Python_Projekte\coolWIRE\

## Dateistruktur
```
coolWIRE\
├── coolWIRE_main.py          (2101 Zeilen – Hauptapp)
├── coolwire_datenbank.json   (auto-generiert, NICHT committen)
├── LAWOG_Waizenkirchen_2024.json (Beispielprojekt, NICHT committen)
├── START_coolWIRE.bat
├── requirements.txt
├── README.md
├── CLAUDE.md                 (diese Datei)
├── .streamlit\
│   ├── config.toml
│   └── secrets.toml          (NIEMALS committen!)
└── modules\
    ├── __init__.py
    ├── auth.py
    ├── calculation_kabel.py  (13 Cluster, 99 Kabeltypen)
    ├── datenbank.py          (JSON-DB, Geräte-DB, Theme-System)
    ├── kabelliste.py         (Kabelliste-Berechnung)
    ├── ki_import.py          (Claude API: PDF/Bild/Excel/Text Import)
    ├── kuehlstellen.py       (18 Komponenten, Datenmodell)
    └── rohrnetz.py           (coolROHR Physik: Darcy-Weisbach, 6 Kältemittel)
```

## Tab-Struktur (7 Tabs)
| Tab | Icon | Inhalt |
|-----|------|--------|
| 1 · Projekt | 📁 | Projektdaten (st.form), Maschinenstandorte |
| 2 · Kühlstellen | ❄️ | KI-Import, Datenblatt-Import, Gerätedatenbank |
| 3 · Steuerung | 🧮 | Kreiszuordnung, Schaltschrank |
| 4 · Kabelplanung | 🧵 | Kabelliste, HACCP, Excel/CSV Export |
| 5 · Rohrnetz | ╔ | coolROHR Integration – Rohrdimensionierung |
| 6 · Doku | 📄 | Projektübersicht, JSON/CSV Export |
| 7 · Admin | 🔑 | Regler-DB, Geräte-DB, Theme |

## Kritischer Streamlit-Bug (Python 3.14 / Streamlit 1.30+)
value= in st.text_input wird ignoriert wenn Widget bereits existiert.
Lösung: KEIN st.rerun() nach JSON-Laden. st.query_params["loaded"] = timestamp gesetzt.
Tab 1 Formular: kein key=, kein value= zusammen verwenden.

## Authentifizierung
secrets.toml → [users], [roles], [display_names]
E-Mail als Keys (MIT Anführungszeichen!)
Rollen: admin / partner | Standard-PW: Fernseher24!
API-Key: st.secrets["anthropic"]["api_key"]

## rohrnetz.py – coolROHR Physik
Kältemittel: R513A, R449A, R744, R455A, R452A, R1234yf
Hauptfunktion: berechne_leitung(ref_key, t0_C, tc_C, Q_kW, L_h_m, L_v_m, ...)
Gibt dict zurück mit SL/DL/FL: pipe, v, dp_K, dp_bar, insul_mm, warns
CU_PIPES: 13 Rohrdimensionen 10×1,0 bis 108×2,5

## LAWOG Waizenkirchen – Referenzprojekt
15 Kühlstellen | 3 Kreise | Angebot Intarcon 26PRE4291

Kreis 1: MDV-SY-50582 #2 · R513A · 400V 3N · 8 KS · 8,354kW
Kreis 2: Sigilus BDF-NG-1075 · R449A · 230V 1-ph · 1 KS (TK) · 1,586kW
Kreis 3: MDV-SY-50582 #1 · R513A · 400V 3N · 6 KS · 8,354kW
Monitoring: Kiconex KI16BAS, Zentralschrank EG

## GitHub
Repo: michaelschaepers/-coolsulting_centralSTATION_PRO
Branch: main
.gitignore: secrets.toml, *.json (außer beispiel_projekt.json), venv/, __pycache__/

## Coding-Regeln
- Vollständige Dateien liefern, nie Snippets
- Kein print() im Streamlit-Code
- CSS f-strings: {} → {{}}
- Syntax mit ast.parse() prüfen vor Ausgabe
- Kommunikation: Deutsch

## Offene TODOs
1. GitHub Push via Centralstation abschließen
2. Tab 1 Projektfelder-Bug (value= nach JSON-Laden) – teilweise gelöst
3. Passwort-Ändern-Funktion
4. SQL-Backend
5. PDF-Bericht für Kunden
6. DSR-Auslegung in Tab 5 (Doppelsteigrohr)
7. Excel-Export Tab 5 Rohrnetz
