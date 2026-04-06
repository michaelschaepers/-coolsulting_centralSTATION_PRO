# °coolWIRE – Systemkontext für neuen Chat
> Stand: 06.04.2026 – Diese Datei zu Beginn eines neuen Chats hochladen

## Projekt
Streamlit-Kälteplanungstool | coolsulting e.U. | Michael Schäpers | Linz AT
Port 8580 | START_coolWIRE.bat | Python 3.14 | Streamlit 1.30+
CI: #36A9E1 Blau, #3C3C3B Dunkelgrau, DM Sans

## Dateistruktur
```
coolWIRE\
├── coolWIRE_main.py          (2101 Zeilen)
├── modules\
│   ├── auth.py
│   ├── calculation_kabel.py  (13 Cluster, 99 Typen)
│   ├── datenbank.py
│   ├── kabelliste.py
│   ├── ki_import.py          (Claude API Datenblatt-Import)
│   ├── kuehlstellen.py       (18 Komponenten)
│   └── rohrnetz.py           (NEU – coolROHR Physik)
├── .streamlit\secrets.toml   (NICHT committen!)
└── LAWOG_Waizenkirchen_2024.json
```

## Tabs
📁 1·Projekt | ❄️ 2·Kühlstellen | 🧮 3·Steuerung | 🧵 4·Kabelplanung | ╔ 5·Rohrnetz | 📄 6·Doku | 🔑 7·Admin

## Kritischer Bug (Python 3.14 / Streamlit 1.30+)
value= in st.text_input nach st.rerun() wird ignoriert.
Lösung: KEIN st.rerun() nach JSON-Laden. st.query_params["loaded"] = timestamp.

## 18 Komponenten (kuehlstellen.py)
Pflicht: verdampfer_luefter, temperaturfuehler_innen, temperaturfuehler_abtau,
tuer_kontakt, innenbeleuchtung, bewegungsmelder, schaltkasten, haccp_aufzeichnung
Optional: abtauheizung, ablaufheizung, gehaeuse_heizung, tuer_heizung,
eev (4 Typen, Schrittmotor MAX 8m!), magnetventil, druckfuehler,
personennotruf, gaswarnanlage, monitoring_kiconex

## rohrnetz.py (coolROHR Integration)
Kältemittel: R513A, R449A, R744, R455A, R452A, R1234yf
Hauptfunktion: berechne_leitung(ref_key, t0_C, tc_C, Q_kW, L_h_m, L_v_m, ...)
CU_PIPES: 13 Dim. 10×1,0 bis 108×2,5
Physik: Darcy-Weisbach/Blasius, Clausius-Clapeyron, Äquivalentlängen, Isolierung

## LAWOG Waizenkirchen – Finaler Projektstand
15 Kühlstellen | 3 Kreise | Angebot Intarcon 26PRE4291

### Kreis 1 – MDV-SY-50582 #2 (R513A, 400V 3N, Dach) – 8 KS
E-14/Pos.159/GK.02.02.F – KZ MoPro – 1,5kW – 14m – MJB-NY-3325 – MTM-N-01161/230V
E-13/Pos.161/GK.02.02.G – KZ Fleisch – 1,7kW – 13m – MJB-NY-3325 – MTM-N-01161/230V
E-11/Pos.170/GK.02.02.H – KZ O&G – 2,1kW – 11m – MJB-NY-4430 – MTM-N-01161/230V
E-07/Pos.173/GK.02.02.I – Lager Trocken – 1,2kW – 18m – AJB-NY-2220 – ATM-N-01031/230V (Umluft!)
E-08/Pos.174/GK.02.02.J – Lager Konserven – 1,2kW – 18m – AJB-NY-2220 – ATM-N-01031/230V (Umluft!)
E-?/Pos.69 – Kühltisch – 0,3kW – 5m – Fremd
E-?/Pos.111 – Kühlschrank – 0,48kW – 3m – Fremd
E-?/Pos.112 – Kühlwanne – 0,48kW – 3m – Fremd

### Kreis 2 – Sigilus BDF-NG-1075 (R449A, 230V 1-ph, Dach) – 1 KS (TK)
E-12/Pos.166/GK.03.03.A – Tiefkühlzelle – 1,94kW – 30m – BJC-NG-1225 – MTM-N-13161/400V 3N
Abtau: Elektro 2×700W=1400W + Ablaufheizung

### Kreis 3 – MDV-SY-50582 #1 (R513A, 400V 3N, Dach) – 6 KS
E-64/Pos.116/GK.02.02.A – KZ Fleisch – 3,27kW – 64m – MJB-NY-3325 – MTM-N-01161/230V
E-65/Pos.119/GK.02.02.B – KZ Rohrbahn – 2,7kW – 65m – MJB-NY-4430 – MTM-N-01161/230V
E-58/Pos.121/GK.02.02.C – Kühlzelle – 1,7kW – 58m – MJB-NY-3325 – MTM-N-01161/230V
E-57/Pos.124/GK.02.02.D – Kühlzelle – 1,7kW – 57m – MJB-NY-3325 – MTM-N-01161/230V
E-90/Pos.126/GK.02.02.E – Kühlzelle – 2,1kW – 90m – MJB-NY-4430 – MTM-N-01161/230V
E-79/Pos.79/NEU – KZ Blumen – 1,2kW – 79m – MJB-NY-3325 – MTM-N-01161/230V (5°C, Elektro-Abtau 800W)

### Verdampfer-Specs:
MJB-NY-3325: 3×Ø254mm, 210W, Elektro 2×800W=1600W
MJB-NY-4430: 4×Ø300mm, 480W, Elektro 3×1000W=3000W
AJB-NY-2220: 2×Ø200mm, 140W, UMLUFT (kein Heizstab!)
BJC-NG-1225: 2×Ø254mm, 140W, Elektro 2×700W=1400W

### Monitoring:
Kiconex KI16BAS (kibox2), 2×RS485, 4G Router, Zentralschrank EG
Bus-Kabel: KI-CAB-04-001 (2x2x0,25mm²)

## GitHub
Repo: michaelschaepers/-coolsulting_centralSTATION_PRO
Branch: main | Committed: 15 Dateien
Push via Claude Code in Centralstation ausstehend

## Offene TODOs
1. GitHub Push via Centralstation
2. Tab 1 Projektfelder nach JSON-Laden (teilweise gelöst)
3. DSR-Auslegung in Tab 5
4. Excel-Export Tab 5 Rohrnetz
5. Passwort-Ändern-Funktion
6. SQL-Backend
7. PDF-Bericht

## Coding-Regeln
- Vollständige Dateien, nie Snippets
- Kein print() in Streamlit
- CSS f-strings: {} → {{}}
- ast.parse() vor Ausgabe
- Export: /mnt/user-data/outputs/coolwire/
- Sprache: Deutsch

*Stand: 06.04.2026 | °coolsulting e.U. | Michael Schäpers*
