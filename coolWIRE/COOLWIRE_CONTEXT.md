# °coolWIRE – Systemkontext für Claude

> Diese Datei am Anfang eines neuen Chats hochladen damit Claude sofort weiß was °coolWIRE ist.
> Stand: April 2026

---

## Was ist °coolWIRE?

Streamlit-basiertes Kälteplanungstool von coolsulting e.U. (Michael Schäpers, Linz, AT).
Dient zur strukturierten Erfassung von Kühlstellen, automatischer Kabelplanung, HACCP-Dokumentation und Projektexport.

- **Port:** 8580
- **Starter:** `START_coolWIRE.bat`
- **Pfad:** `C:\Users\MichaelSchäpers\Documents\Python_Projekte\coolWIRE\`
- **CI:** #36A9E1 Blau, #3C3C3B Dunkelgrau, Font DM Sans

---

## Dateistruktur

```
coolWIRE\
├── coolWIRE_main.py          (~1921 Zeilen)
├── coolwire_datenbank.json   (auto-generiert)
├── LAWOG_Waizenkirchen_2024.json  (Beispielprojekt)
├── START_coolWIRE.bat
├── .streamlit\
│   ├── config.toml
│   └── secrets.toml
└── modules\
    ├── auth.py
    ├── calculation_kabel.py  (13 Cluster, 99 Typen)
    ├── datenbank.py          (JSON-DB, Geräte-DB, Theme)
    ├── kabelliste.py         (Kabelliste pro Verbraucher)
    ├── ki_import.py          (Claude API: PDF/DXF/Excel/Bild/Text + Datenblatt-Analyse)
    └── kuehlstellen.py       (18 Komponenten, Datenmodell)
```

---

## App-Struktur (6 Tabs)

| Tab | Inhalt |
|-----|--------|
| 📁 1 · Projekt | Projektdaten (st.form), Kälteanlagen/Maschinenstandorte, SK-Konfiguration |
| ❄️ 2 · Kühlstellen | KI-Import, Datenblatt-Import, Gerätedatenbank, Kühlstellenliste + Formular |
| 🎛️ 3 · Steuerung | Steuerungssysteme, Kreiszuordnung |
| 🔌 4 · Kabelplanung | Kabelliste pro Verbraucher, HACCP-Module, Excel/CSV Export |
| 📄 5 · Doku | Kühlstellenübersicht, Export JSON/CSV |
| 🔑 6 · Admin | Nutzerverwaltung, Regler-DB, Geräte-DB, Theme |

---

## Kritischer Streamlit-Bug (Python 3.14 / Streamlit 1.30+)

`value=` in `st.text_input` wird ignoriert wenn Widget-ID bereits existiert.
**Lösung:** Projektdaten-Formular in `st.form("projekt_form")` gewrappt.
Nach JSON-Laden: `st.query_params["loaded"] = timestamp` + `st.rerun()`.

---

## Authentifizierung

- `secrets.toml` → `[users]`, `[roles]`, `[display_names]`
- E-Mail-Adressen als Keys (MIT Anführungszeichen!)
- Rollen: `admin` / `partner`
- Standard-PW: `Fernseher24!`
- API-Key: `st.secrets["anthropic"]["api_key"]`

---

## 18 Komponenten (kuehlstellen.py)

### Pflicht:
- `verdampfer_luefter` – anzahl_verdampfer, spannung, anzahl_luefter, leistung_w
- `temperaturfuehler_innen` – typ_fuehler, anzahl
- `temperaturfuehler_abtau` – typ_fuehler
- `tuer_kontakt` – anzahl_tueren, typ, tuerlicht_schaltung
- `innenbeleuchtung` – licht_typ, spannung, schaltung, leistung_w
- `bewegungsmelder` – typ_melder, funktion, spannung
- `schaltkasten` – steuerung_typ, regler_typ, bus_protokoll, montageort, versorgung
- `haccp_aufzeichnung` – anzahl_fuehler, fuehler_typ, aufzeichnung_system, alarm_grenzwert_oben/unten, alarm_verzoegerung_min

### Optional:
- `abtauheizung` – auto bei < -1°C | Typen: Elektro-Abtau / Umluft-Abtau / Heißgas / Kein Heizstab
- `ablaufheizung` – auto bei < -1°C
- `gehaeuse_heizung`, `tuer_heizung`
- `eev` – 4 Typen: Schrittmotor+Treiber (MAX 8m!), EVD ice, PWM AKV, Treiber im Regler
- `magnetventil`, `druckfuehler`, `personennotruf`, `gaswarnanlage`, `monitoring_kiconex`

### EEV-Kabellogik (kritisch!):
- Schrittmotor: LIYY 6x0,5mm² MAX 8m Ventil→Treiber + YMM-J 230V + LIYCY Steuerleitung
- EVD ice: YMM-J 3x1,5mm² 230V + J-Y(ST)Y RS485 Bus
- PWM AKV: LIYY 2x0,5mm²
- App-Warnung: >5m gelb, >8m rot

---

## Kabelmatrix – 13 Cluster, 99 Typen

**Bus DEFAULT:** J-Y(ST)Y 2x2x0,8mm² (BUS-RS485-2x2x08)

EEV-Cluster (9): EEV-MOT, EEV-TREIBER-STEUER, EEV-TREIBER-VER, EEV-EVD-ICE, EEV-EVD-BUS, EEV-PWM-AKV, EEV-TF-SAUG, EEV-TF-AUS, EEV-DRUCK

MSR/GWA-Cluster (12): inkl. MSR-XWEB-BUS (Dixell XWEB), MSR-BEWEGUNG (Bewegungsmelder→Regler), MSR-UNTERFRIER (SIHF 3x1,5mm²)

---

## Gerätedatenbank (datenbank.py)

- `get_geraete(db, typ)`, `add_geraet()`, `delete_geraet()`, `geraet_zu_kuehlstelle()`
- `GERAET_TYPEN`: Verdampfer / Außenunit / Verflüssiger / Kompaktaggregat / Verbundanlage
- Datenblatt-Import: `analysiere_datenblatt_pdf()`, `analysiere_datenblatt_bild()`, `analysiere_datenblatt_excel()`

---

## LAWOG Waizenkirchen – Finaler Projektstand (04.04.2026)

**Angebot Intarcon 26PRE4291** | 15 Kühlstellen | 3 Kreise

### Kreis 1 – MDV-SY-50582 #2 (400V 3N, Dach) – 8 KS
| E-Nr | Pos | GK | Name | kW | m | Verdampfer | Regler/Spannung |
|------|-----|----|------|----|---|-----------|----------------|
| E-14 | 159 | GK.02.02.F | KZ MoPro | 1,5 | 14 | MJB-NY-3325 | MTM-N-01161 / 230V |
| E-13 | 161 | GK.02.02.G | KZ Fleisch | 1,7 | 13 | MJB-NY-3325 | MTM-N-01161 / 230V |
| E-11 | 170 | GK.02.02.H | KZ O&G | 2,1 | 11 | MJB-NY-4430 | MTM-N-01161 / 230V |
| E-07 | 173 | GK.02.02.I | Lager Trocken | 1,2 | 18 | AJB-NY-2220 | ATM-N-01031 / 230V |
| E-08 | 174 | GK.02.02.J | Lager Konserven | 1,2 | 18 | AJB-NY-2220 | ATM-N-01031 / 230V |
| E-? | 69 | – | Kühltisch | 0,3 | 5 | Fremd | Fremd |
| E-? | 111 | – | Kühlschrank | 0,48 | 3 | Fremd | Fremd |
| E-? | 112 | – | Kühlwanne | 0,48 | 3 | Fremd | Fremd |

**E-07/E-08:** Umluft-Abtau, KEIN Heizstab!

### Kreis 2 – Sigilus BDF-NG-1075 (230V 1-ph, Dach) – 1 KS
| E-Nr | Pos | GK | Name | kW | m | Verdampfer | Regler/Spannung |
|------|-----|----|------|----|---|-----------|----------------|
| E-12 | 166 | GK.03.03.A | Tiefkühlzelle | 1,94 | 30 | BJC-NG-1225 | MTM-N-13161 / **400V 3N** |

TK: Elektro-Abtau 2×700W=1400W (OPT.ODE.14) + Ablaufheizung aktiv

### Kreis 3 – MDV-SY-50582 #1 (400V 3N, Dach) – 6 KS
| E-Nr | Pos | GK | Name | kW | m | Verdampfer | Regler/Spannung |
|------|-----|----|------|----|---|-----------|----------------|
| E-64 | 116 | GK.02.02.A | KZ Fleisch | 3,27 | 64 | MJB-NY-3325 | MTM-N-01161 / 230V |
| E-65 | 119 | GK.02.02.B | KZ Rohrbahn | 2,7 | 65 | MJB-NY-4430 | MTM-N-01161 / 230V |
| E-58 | 121 | GK.02.02.C | Kühlzelle | 1,7 | 58 | MJB-NY-3325 | MTM-N-01161 / 230V |
| E-57 | 124 | GK.02.02.D | Kühlzelle | 1,7 | 57 | MJB-NY-3325 | MTM-N-01161 / 230V |
| E-90 | 126 | GK.02.02.E | Kühlzelle | 2,1 | 90 | MJB-NY-4430 | MTM-N-01161 / 230V |
| E-79 | 79 | NEU | KZ Blumen | 1,2 | 79 | MJB-NY-3325 | MTM-N-01161 / 230V |

Blumen: 5°C, Elektro-Abtau 800W

### Maschinenstandorte:
- ms1: MDV-SY-50582 #2, Dach, Kreis 1
- ms2: Sigilus BDF-NG-1075, Dach, Kreis 2
- ms3: MDV-SY-50582 #1, Dach, Kreis 3
- ms4: Kiconex KI16BAS (kibox2), Maschinenraum EG, Kreis 1+2+3

### Außenunit-Daten MDV-SY-50582:
R513A, 400V 3N 50Hz, 8,354kW @-8°C/37°C, 8,7A Nenn / 22A Max, 2× Scroll ZB29, 1195×740×1534mm, 182kg, 28dB(A)

### Verdampfer-Specs:
| Modell | Lüfter | W | Abtau | Für |
|--------|--------|---|-------|-----|
| MJB-NY-3325 | 3× Ø254 | 210 | Elektro 2×800W | Pos.01,03,04,06,07,11,79 |
| MJB-NY-4430 | 4× Ø300 | 480 | Elektro 3×1000W | Pos.02,05,08 |
| AJB-NY-2220 | 2× Ø200 | 140 | **Umluft** (kein Heizstab!) | Pos.09,10 |
| BJC-NG-1225 | 2× Ø254 | 140 | Elektro 2×700W | Pos.12 TK |

---

## Coding-Regeln

- Vollständige Dateien immer liefern, nie Snippets
- Kein `print()` im Streamlit-Code
- CSS f-strings: `{}` → `{{}}`
- Streamlit 1.30+: `st.form()` für Formulare verwenden
- Syntax immer mit `ast.parse()` prüfen
- Export: `/mnt/user-data/outputs/coolwire/`
- Kommunikation: Deutsch

## Offene TODOs

1. Passwort-Ändern-Funktion
2. SQL-Backend
3. Türanzahl nur pro Kühlstelle
4. PDF-Bericht für Kunden
5. Login-Fix (leere Labels in auth.py)

---

*Stand: 04.04.2026 | °coolsulting e.U. | Michael Schäpers | Linz, Austria*
