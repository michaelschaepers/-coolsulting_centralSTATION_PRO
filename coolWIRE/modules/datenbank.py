# modules/datenbank.py
# °coolWIRE v2.2 – Lernende lokale Datenbank (JSON-basiert)
# (c) coolsulting e.U. | Michael Schäpers

import json
import os
from datetime import datetime

DB_PFAD = os.path.join(os.path.dirname(os.path.dirname(__file__)), "coolwire_datenbank.json")

DEFAULT_DB = {
    "version": "1.0",
    "erstellt": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "zuletzt_geaendert": datetime.now().strftime("%d.%m.%Y %H:%M"),
    "regler": [
        {"id": "r001", "hersteller": "Intarcon / Dixell", "modell": "MTM-N-11161 / XM670", "typ": "Kühlstellenregler", "spannung": "230V 1-phasig", "bus": "RS485 Modbus", "display": "LCD 4-stellig", "relais_ausgaenge": 4, "fuehler_eingaenge": 3, "besonderheiten": "coolsulting Standard, OEM-Gerät, günstig, bewährt", "einsatzgebiet": ["NK", "TK", "NK+"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
        {"id": "r002", "hersteller": "Danfoss", "modell": "EKC 202 / AK-CC 210", "typ": "Kühlstellenregler", "spannung": "230V 1-phasig", "bus": "RS485 Modbus / LON", "display": "LCD", "relais_ausgaenge": 4, "fuehler_eingaenge": 3, "besonderheiten": "Supermarkt-Standard, ADAP-KOOL kompatibel", "einsatzgebiet": ["NK", "TK", "HNK"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
        {"id": "r003", "hersteller": "Danfoss", "modell": "EKC 301 / AK-CC 550", "typ": "Verbundregler / Rack Controller", "spannung": "230V 1-phasig", "bus": "RS485 / LON / TCP/IP", "display": "Grafik-LCD", "relais_ausgaenge": 8, "fuehler_eingaenge": 6, "besonderheiten": "Verdichterverbund, Verflüssiger, Abtaukoordination", "einsatzgebiet": ["Verbund", "NK", "TK"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
        {"id": "r004", "hersteller": "Wurm", "modell": "UDO-4", "typ": "Kühlstellenregler", "spannung": "230V 1-phasig", "bus": "CAN-Bus (Frigolink)", "display": "LED 4-stellig", "relais_ausgaenge": 4, "fuehler_eingaenge": 2, "besonderheiten": "Frigolink-kompatibel, CAN-Bus Feldmodul", "einsatzgebiet": ["NK", "TK", "HNK"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
        {"id": "r005", "hersteller": "Wurm", "modell": "UNO-4", "typ": "Kühlstellenregler", "spannung": "230V 1-phasig", "bus": "CAN-Bus (Frigolink)", "display": "LED 4-stellig", "relais_ausgaenge": 3, "fuehler_eingaenge": 2, "besonderheiten": "Kompaktversion UDO-4", "einsatzgebiet": ["NK", "HNK"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
        {"id": "r006", "hersteller": "Pego", "modell": "Nector", "typ": "Kühlstellenregler", "spannung": "230V 1-phasig", "bus": "RS485 Modbus", "display": "LCD", "relais_ausgaenge": 4, "fuehler_eingaenge": 3, "besonderheiten": "Modular aufbaubar, I/O-Erweiterung möglich", "einsatzgebiet": ["NK", "TK", "NK+"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
        {"id": "r007", "hersteller": "Carel", "modell": "Ultracella UCO*H", "typ": "Kühlstellenregler", "spannung": "230V 1-phasig", "bus": "RS485 Modbus / pLAN", "display": "LCD Grafik", "relais_ausgaenge": 5, "fuehler_eingaenge": 4, "besonderheiten": "Supermarkt/Verbund, HACCP-Logging, boss-kompatibel", "einsatzgebiet": ["NK", "TK", "HNK"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
        {"id": "r008", "hersteller": "Carel", "modell": "IR33", "typ": "Kühlstellenregler", "spannung": "230V 1-phasig", "bus": "RS485 Modbus (mit Adapter IROPZ48500)", "display": "LED 4-stellig", "relais_ausgaenge": 3, "fuehler_eingaenge": 2, "besonderheiten": "Klassiker, günstig, weit verbreitet", "einsatzgebiet": ["NK", "HNK"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
        {"id": "r009", "hersteller": "Eliwell", "modell": "ID974", "typ": "Kühlstellenregler", "spannung": "230V 1-phasig", "bus": "RS485 Modbus", "display": "LED 4-stellig", "relais_ausgaenge": 3, "fuehler_eingaenge": 2, "besonderheiten": "Günstig, einfach, Gastro", "einsatzgebiet": ["NK", "HNK"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
        {"id": "r010", "hersteller": "Dixell", "modell": "XR75CX", "typ": "Kühlstellenregler TK", "spannung": "230V 1-phasig", "bus": "RS485 Modbus", "display": "LED", "relais_ausgaenge": 4, "fuehler_eingaenge": 3, "besonderheiten": "TK-optimiert, Heißgasabtau, EEV-Ansteuerung", "einsatzgebiet": ["TK", "TK+"], "angelegt_am": "01.01.2025", "angelegt_von": "Michael Schäpers"},
    ],
    "kabeltypen_custom": [],
    "geraete_custom": [],
    "theme": {
        "primary_color": "#36A9E1", "dark_color": "#3C3C3B", "light_bg": "#F4F8FC",
        "border_color": "#D0E8F5", "accent_color": "#0078B8", "success_color": "#27AE60",
        "warning_color": "#E67E22", "error_color": "#E74C3C", "font_family": "DM Sans",
        "font_size_base": "14px", "border_radius": "10px",
        "card_shadow": "0 2px 8px rgba(0,0,0,0.06)",
        "header_gradient_start": "#1a6fa8", "header_gradient_end": "#5bc4f5",
        "sidebar_bg": "#F4F8FC", "input_bg": "transparent", "name": "°coolsulting Standard"
    },
    "theme_presets": {
        "coolsulting_standard": {"name": "°coolsulting Standard (Blau)", "primary_color": "#36A9E1", "dark_color": "#3C3C3B", "light_bg": "#F4F8FC", "border_color": "#D0E8F5", "accent_color": "#0078B8", "header_gradient_start": "#1a6fa8", "header_gradient_end": "#5bc4f5", "font_family": "DM Sans"},
        "dunkel": {"name": "Dark Mode (Dunkel)", "primary_color": "#36A9E1", "dark_color": "#E8E8E8", "light_bg": "#1E2A38", "border_color": "#2D3F52", "accent_color": "#5BC4F5", "header_gradient_start": "#0D1B2A", "header_gradient_end": "#1a6fa8", "font_family": "DM Sans"},
        "gruen": {"name": "Grün (Natur/Energie)", "primary_color": "#27AE60", "dark_color": "#1A3A2A", "light_bg": "#F0FAF4", "border_color": "#A8DFB8", "accent_color": "#1E8449", "header_gradient_start": "#145A32", "header_gradient_end": "#58D68D", "font_family": "DM Sans"},
        "anthrazit": {"name": "Anthrazit (Industrie)", "primary_color": "#7F8C8D", "dark_color": "#2C3E50", "light_bg": "#F2F3F4", "border_color": "#D5D8DC", "accent_color": "#566573", "header_gradient_start": "#1C2833", "header_gradient_end": "#566573", "font_family": "DM Sans"},
    }
}

def lade_datenbank() -> dict:
    if not os.path.exists(DB_PFAD):
        speichere_datenbank(DEFAULT_DB)
        return DEFAULT_DB.copy()
    try:
        with open(DB_PFAD, "r", encoding="utf-8") as f:
            db = json.load(f)
        for key, val in DEFAULT_DB.items():
            if key not in db:
                db[key] = val
        return db
    except Exception:
        return DEFAULT_DB.copy()

def speichere_datenbank(db: dict) -> bool:
    try:
        db["zuletzt_geaendert"] = datetime.now().strftime("%d.%m.%Y %H:%M")
        os.makedirs(os.path.dirname(DB_PFAD) if os.path.dirname(DB_PFAD) else ".", exist_ok=True)
        with open(DB_PFAD, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def get_regler_liste(db: dict) -> list:
    return db.get("regler", [])

def get_regler_optionen(db: dict) -> list:
    return [f"{r['hersteller']} {r['modell']}" for r in get_regler_liste(db)]

def add_regler(db, hersteller, modell, typ, spannung, bus, display, relais, fuehler, besonderheiten, einsatzgebiet, bearbeiter):
    existing_ids = [r.get("id","r000") for r in db.get("regler",[])]
    nr = len(existing_ids) + 1
    new_id = f"r{nr:03d}"
    while new_id in existing_ids:
        nr += 1
        new_id = f"r{nr:03d}"
    db.setdefault("regler", []).append({
        "id": new_id, "hersteller": hersteller, "modell": modell, "typ": typ,
        "spannung": spannung, "bus": bus, "display": display, "relais_ausgaenge": relais,
        "fuehler_eingaenge": fuehler, "besonderheiten": besonderheiten,
        "einsatzgebiet": einsatzgebiet,
        "angelegt_am": datetime.now().strftime("%d.%m.%Y %H:%M"), "angelegt_von": bearbeiter
    })
    return db

def delete_regler(db: dict, regler_id: str) -> dict:
    db["regler"] = [r for r in db.get("regler", []) if r.get("id") != regler_id]
    return db

GERAET_TYPEN = ["Verdampfer", "Außenunit / Verflüssigungseinheit", "Verflüssiger (getrennt)", "Kompaktaggregat", "Verbundanlage", "Sonstiges"]

DEFAULT_GERAET = {
    "id": "", "typ": "Verdampfer", "hersteller": "", "modell": "",
    "kaelteleistung_kw": None, "kaeltemittel": "", "temp_bereich": "NK",
    "raum_temp_c": None, "verdampfung_c": None, "anzahl_luefter": 1,
    "leistung_luefter_w": 150, "spannung_luefter": "230V 1-phasig",
    "abtau_typ": "Elektro-Abtau", "abtau_leistung_w": 800, "ablauf_heizung": False,
    "anschluss_spannung": "230V 1-phasig", "anschluss_strom_a": None,
    "freigabe_kontakt": True, "stoermeldung_kontakt": True, "betrieb_kontakt": True,
    "bus_schnittstelle": "", "steuerung_kabel_typ": "AU-7x1-STEUER",
    "notizen": "", "datenblatt_gelesen": False, "angelegt_am": "", "angelegt_von": "",
}

def get_geraete(db, typ=None):
    alle = db.get("geraete_custom", [])
    return [g for g in alle if g.get("typ") == typ] if typ else alle

def get_geraet_optionen(db, typ=None):
    return [f"{g['hersteller']} {g['modell']} ({g.get('kaelteleistung_kw','?')} kW)" for g in get_geraete(db, typ)]

def add_geraet(db, geraet, bearbeiter):
    existing_ids = [g.get("id","") for g in db.get("geraete_custom",[])]
    nr = len(existing_ids) + 1
    new_id = f"G{nr:04d}"
    while new_id in existing_ids:
        nr += 1
        new_id = f"G{nr:04d}"
    geraet["id"] = new_id
    geraet["angelegt_am"] = datetime.now().strftime("%d.%m.%Y %H:%M")
    geraet["angelegt_von"] = bearbeiter
    db.setdefault("geraete_custom", []).append(geraet)
    return db

def delete_geraet(db, geraet_id):
    db["geraete_custom"] = [g for g in db.get("geraete_custom",[]) if g.get("id") != geraet_id]
    return db

def geraet_zu_kuehlstelle(geraet, ks):
    typ = geraet.get("typ","")
    komp = ks.get("komponenten", {})
    if typ == "Verdampfer":
        if "verdampfer_luefter" not in komp:
            komp["verdampfer_luefter"] = {"aktiv": True, "parameter": {}, "ki_erkannt": False}
        komp["verdampfer_luefter"]["aktiv"] = True
        komp["verdampfer_luefter"]["parameter"].update({
            "anzahl_verdampfer": 1, "anzahl_luefter": geraet.get("anzahl_luefter", 1),
            "leistung_w": geraet.get("leistung_luefter_w", 150),
            "spannung": geraet.get("spannung_luefter", "230V 1-phasig"),
        })
        if "abtauheizung" not in komp:
            komp["abtauheizung"] = {"aktiv": False, "parameter": {}, "ki_erkannt": False}
        abtau_typ = geraet.get("abtau_typ", "Elektro-Abtau")
        komp["abtauheizung"]["aktiv"] = "Elektro" in abtau_typ or "Heißgas" in abtau_typ
        komp["abtauheizung"]["parameter"].update({"typ_abtau": abtau_typ, "leistung_w": geraet.get("abtau_leistung_w", 800), "spannung": "230V 1-phasig"})
        if geraet.get("ablauf_heizung"):
            komp.setdefault("ablaufheizung", {"aktiv": False, "parameter": {}, "ki_erkannt": False})["aktiv"] = True
        if geraet.get("raum_temp_c") is not None: ks["raum_temp_soll_c"] = geraet["raum_temp_c"]
        if geraet.get("verdampfung_c") is not None: ks["verdampfung_custom_c"] = geraet["verdampfung_c"]
        if geraet.get("kaelteleistung_kw") is not None: ks["kaelteleistung_kw"] = geraet["kaelteleistung_kw"]
        if geraet.get("temp_bereich"): ks["temp_bereich"] = geraet["temp_bereich"]
        ks["geraet_verdampfer_id"] = geraet.get("id","")
        ks["geraet_verdampfer_modell"] = f"{geraet.get('hersteller','')} {geraet.get('modell','')}".strip()
    elif "Außenunit" in typ or "Verflüssiger" in typ or "Kompakt" in typ:
        ks["geraet_aussenunit_id"] = geraet.get("id","")
        ks["geraet_aussenunit_modell"] = f"{geraet.get('hersteller','')} {geraet.get('modell','')}".strip()
        ks["geraet_aussenunit_spannung"] = geraet.get("anschluss_spannung","230V 1-phasig")
        ks["geraet_aussenunit_strom_a"] = geraet.get("anschluss_strom_a")
        ks["geraet_aussenunit_bus"] = geraet.get("bus_schnittstelle","")
        ks["geraet_aussenunit_steuerkabel"] = geraet.get("steuerung_kabel_typ","AU-7x1-STEUER")
    ks["komponenten"] = komp
    return ks

def get_theme(db): return db.get("theme", DEFAULT_DB["theme"])
def speichere_theme(db, theme): db["theme"] = theme; return db
def get_theme_presets(db): return db.get("theme_presets", DEFAULT_DB["theme_presets"])

def schreibe_config_toml(theme, config_pfad=None):
    if config_pfad is None:
        basis = os.path.dirname(os.path.dirname(__file__))
        config_pfad = os.path.join(basis, ".streamlit", "config.toml")
    base = "dark" if _ist_dunkel(theme) else "light"
    primary = theme.get("primary_color", "#36A9E1")
    bg = "#FFFFFF" if base == "light" else "#0E1117"
    sbg = theme.get("light_bg", "#F4F8FC") if base == "light" else "#262730"
    text = theme.get("dark_color", "#31333F") if base == "light" else "#FAFAFA"
    font = theme.get("font_family", "sans serif")
    zeilen = ["[server]","port = 8580","headless = true","enableCORS = false","enableXsrfProtection = false","maxUploadSize = 500","","[browser]","gatherUsageStats = false","","[theme]",f'base = "{base}"',f'primaryColor = "{primary}"',f'backgroundColor = "{bg}"',f'secondaryBackgroundColor = "{sbg}"',f'textColor = "{text}"',f'font = "{font}"',""]
    try:
        os.makedirs(os.path.dirname(config_pfad), exist_ok=True)
        with open(config_pfad, "w", encoding="utf-8") as f:
            f.write("\n".join(zeilen))
        return True
    except Exception:
        return False

def _ist_dunkel(theme):
    bg = theme.get("light_bg", "#FFFFFF").lstrip("#")
    try:
        r,g,b = int(bg[0:2],16), int(bg[2:4],16), int(bg[4:6],16)
        return (r*299 + g*587 + b*114) / 1000 < 128
    except Exception:
        return False

def theme_zu_css(theme):
    return f":root {{--cb: {theme.get('primary_color', '#36A9E1')};--cd: {theme.get('dark_color', '#3C3C3B')};--cl: {theme.get('light_bg', '#F4F8FC')};--cborder: {theme.get('border_color', '#D0E8F5')};--ca: {theme.get('accent_color', '#0078B8')};--ok: {theme.get('success_color', '#27AE60')};--warn: {theme.get('warning_color', '#E67E22')};--err: {theme.get('error_color', '#E74C3C')};--radius: {theme.get('border_radius', '10px')};--shadow: {theme.get('card_shadow', '0 2px 8px rgba(0,0,0,0.06)')};--grad-start: {theme.get('header_gradient_start', '#1a6fa8')};--grad-end: {theme.get('header_gradient_end', '#5bc4f5')};--font: '{theme.get('font_family', 'DM Sans')}', sans-serif;--font-size: {theme.get('font_size_base', '14px')};}}"
