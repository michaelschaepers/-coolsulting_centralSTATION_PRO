# ============================================================================
# DATEI: Samsung_Quint.py
# VERSION: 2.0.0
# STAND: 12.03.2026
# AUTOR: Michael Schäpers, coolsulting
# BESCHREIBUNG: Samsung Quint – Discovery → Auslegung → Stückliste
# ============================================================================

import streamlit as st
import os
import base64
import uuid
from datetime import datetime, date
import pandas as pd

# ============================================================
# SEITE KONFIGURIEREN
# ============================================================
try:
    from PIL import Image
    icon_image = Image.open("Coolsulting_Logo_ohneHG_weiß_grau.png")
    st.set_page_config(page_title="coolQUINT | Samsung Quint Auslegung",
                       page_icon=icon_image, layout="wide",
                       initial_sidebar_state="collapsed")
except Exception:
    st.set_page_config(page_title="coolQUINT | Samsung Quint Auslegung",
                       layout="wide", initial_sidebar_state="collapsed")

# ============================================================
# PRODUKTDATEN
# ============================================================
AUSSENGERAETE = {
    "ODU 12.5 kW (1-phasig)": {
        "artikelnr": "AE125HCTPES/EU", "kuehl_kw": 12.5, "heiz_kw": 12.5,
        "schall_db": "51 / 49", "schallleistung_db": 62,
        "abmessungen": "1270 × 850 × 500", "gewicht_kg": 126.5,
        "spannung": "230V / 1Ph", "mca_a": 32.0, "phase": "1-phasig",
    },
    "ODU 16.0 kW (1-phasig)": {
        "artikelnr": "AE160HCTPES/EU", "kuehl_kw": 14.5, "heiz_kw": 16.0,
        "schall_db": "55 / 49", "schallleistung_db": 62,
        "abmessungen": "1270 × 850 × 500", "gewicht_kg": 126.5,
        "spannung": "230V / 1Ph", "mca_a": 32.0, "phase": "1-phasig",
    },
    "ODU 12.5 kW (3-phasig)": {
        "artikelnr": "AE125HCTPGS/EU", "kuehl_kw": 12.5, "heiz_kw": 12.5,
        "schall_db": "51 / 49", "schallleistung_db": 62,
        "abmessungen": "1270 × 850 × 500", "gewicht_kg": 126.5,
        "spannung": "400V / 3Ph", "mca_a": 16.1, "phase": "3-phasig",
    },
    "ODU 16.0 kW (3-phasig)": {
        "artikelnr": "AE160HCTPGS/EU", "kuehl_kw": 14.5, "heiz_kw": 16.0,
        "schall_db": "55 / 49", "schallleistung_db": 62,
        "abmessungen": "1270 × 850 × 500", "gewicht_kg": 126.5,
        "spannung": "400V / 3Ph", "mca_a": 16.1, "phase": "3-phasig",
    },
}

HYDRO_UNITS = {
    "ClimateHub 200L – 1 Zone": {
        "artikelnr": "AE200DNWMPK/EU", "zonen": 1, "typ": "ClimateHub",
        "speicher_l": 200, "schall_db": 28, "schallleistung_db": 42,
        "abmessungen": "598 × 1850 × 600", "gewicht_kg": 132,
        "spannung": "230V / 400V", "mca_a": 18.3,
        "beschreibung": "Standgerät mit integriertem 200L Warmwasserspeicher – 1 Heizkreis",
    },
    "ClimateHub 200L – 2 Zonen": {
        "artikelnr": "AE200DNXMPK/EU", "zonen": 2, "typ": "ClimateHub",
        "speicher_l": 200, "schall_db": 30, "schallleistung_db": 44,
        "abmessungen": "598 × 1850 × 600", "gewicht_kg": 139,
        "spannung": "230V / 400V", "mca_a": 18.7,
        "beschreibung": "Standgerät mit integriertem 200L Speicher – 2 Heizkreise",
    },
    "Wandgerät – 1 Zone": {
        "artikelnr": "AE160DNYMPK/EU", "zonen": 1, "typ": "Wandgerät",
        "speicher_l": 0, "schall_db": 28, "schallleistung_db": 42,
        "abmessungen": "530 × 840 × 350", "gewicht_kg": 43,
        "spannung": "230V / 400V", "mca_a": 18.3,
        "beschreibung": "Kompakte Wandmontage, externer Speicher nötig – 1 Heizkreis",
    },
    "Wandgerät – 2 Zonen": {
        "artikelnr": "AE160DNZMPK/EU", "zonen": 2, "typ": "Wandgerät",
        "speicher_l": 0, "schall_db": 30, "schallleistung_db": 44,
        "abmessungen": "530 × 840 × 350", "gewicht_kg": 54,
        "spannung": "230V / 400V", "mca_a": 18.7,
        "beschreibung": "Kompakte Wandmontage, externer Speicher nötig – 2 Heizkreise",
    },
}

INNENGERAETE = {
    "RAC Wandgerät 1.5 kW":  {"artikelnr": "AE015HEADKG/EU",  "kategorie": "RAC Wandgerät",  "kuehl_kw": 1.5, "heiz_kw": 1.7, "schall_db": "31/30/29", "abmessungen": "682×299×215",  "gewicht_kg": 7.8,  "mca_a": 0.16},
    "RAC Wandgerät 2.2 kW":  {"artikelnr": "AE022HEADKG/EU",  "kategorie": "RAC Wandgerät",  "kuehl_kw": 2.2, "heiz_kw": 2.5, "schall_db": "33/31/29", "abmessungen": "682×299×215",  "gewicht_kg": 7.8,  "mca_a": 0.20},
    "RAC Wandgerät 2.8 kW":  {"artikelnr": "AE028HEADKG/EU",  "kategorie": "RAC Wandgerät",  "kuehl_kw": 2.8, "heiz_kw": 3.2, "schall_db": "34/33/31", "abmessungen": "820×299×215",  "gewicht_kg": 9.2,  "mca_a": 0.25},
    "RAC Wandgerät 3.6 kW":  {"artikelnr": "AE036HEADKG/EU",  "kategorie": "RAC Wandgerät",  "kuehl_kw": 3.6, "heiz_kw": 4.0, "schall_db": "39/36/33", "abmessungen": "820×299×215",  "gewicht_kg": 9.2,  "mca_a": 0.31},
    "RAC Wandgerät 5.6 kW":  {"artikelnr": "AM056DNVDKG/EU",  "kategorie": "RAC Wandgerät",  "kuehl_kw": 5.6, "heiz_kw": 6.3, "schall_db": "40/37/34", "abmessungen": "1055×299×215", "gewicht_kg": 12.0, "mca_a": 0.44},
    "RAC Wandgerät 7.1 kW":  {"artikelnr": "AM071DNVDKG/EU",  "kategorie": "RAC Wandgerät",  "kuehl_kw": 6.8, "heiz_kw": 7.0, "schall_db": "43/40/37", "abmessungen": "1055×299×215", "gewicht_kg": 12.0, "mca_a": 0.50},
    "1-Weg Kassette 1.7 kW": {"artikelnr": "AM017DN1DKG/EU",  "kategorie": "1-Weg Kassette", "kuehl_kw": 1.7, "heiz_kw": 1.9, "schall_db": "28/26/24", "abmessungen": "740×135×360",  "gewicht_kg": 8.0,  "mca_a": 0.18},
    "1-Weg Kassette 2.2 kW": {"artikelnr": "AM022DN1DKG/EU",  "kategorie": "1-Weg Kassette", "kuehl_kw": 2.2, "heiz_kw": 2.5, "schall_db": "29/26/24", "abmessungen": "740×135×360",  "gewicht_kg": 8.0,  "mca_a": 0.18},
    "1-Weg Kassette 2.8 kW": {"artikelnr": "AM028DN1DKG/EU",  "kategorie": "1-Weg Kassette", "kuehl_kw": 2.8, "heiz_kw": 3.2, "schall_db": "32/28/24", "abmessungen": "970×135×410",  "gewicht_kg": 10.0, "mca_a": 0.29},
    "1-Weg Kassette 3.6 kW": {"artikelnr": "AM036DN1DKG/EU",  "kategorie": "1-Weg Kassette", "kuehl_kw": 3.6, "heiz_kw": 4.0, "schall_db": "37/33/30", "abmessungen": "970×135×410",  "gewicht_kg": 10.0, "mca_a": 0.31},
    "1-Weg Kassette 5.6 kW": {"artikelnr": "AM056DN1DKG/EU",  "kategorie": "1-Weg Kassette", "kuehl_kw": 5.6, "heiz_kw": 6.3, "schall_db": "41/38/35", "abmessungen": "1200×138×450", "gewicht_kg": 13.5, "mca_a": 0.35},
    "LSP Kanalgerät 2.2 kW": {"artikelnr": "AM022DNLDKG/EU",  "kategorie": "LSP Kanalgerät", "kuehl_kw": 2.2, "heiz_kw": 2.5, "schall_db": "26/23/19", "abmessungen": "700×199×440",  "gewicht_kg": 15.9, "mca_a": 0.38},
    "LSP Kanalgerät 2.8 kW": {"artikelnr": "AM028DNLDKG/EU",  "kategorie": "LSP Kanalgerät", "kuehl_kw": 2.8, "heiz_kw": 3.2, "schall_db": "28/24/19", "abmessungen": "700×199×440",  "gewicht_kg": 15.9, "mca_a": 0.45},
    "LSP Kanalgerät 3.6 kW": {"artikelnr": "AM036DNLDKG/EU",  "kategorie": "LSP Kanalgerät", "kuehl_kw": 3.6, "heiz_kw": 4.0, "schall_db": "31/26/20", "abmessungen": "700×199×440",  "gewicht_kg": 16.3, "mca_a": 0.53},
    "LSP Kanalgerät 5.6 kW": {"artikelnr": "AM056DNLDKG/EU",  "kategorie": "LSP Kanalgerät", "kuehl_kw": 5.6, "heiz_kw": 6.3, "schall_db": "34/30/26", "abmessungen": "900×199×440",  "gewicht_kg": 19.3, "mca_a": 0.92},
    "MSP Kanalgerät 3.6 kW": {"artikelnr": "AM036DNMDKG/EU",  "kategorie": "MSP Kanalgerät", "kuehl_kw": 3.6, "heiz_kw": 4.0, "schall_db": "30/27/24", "abmessungen": "850×250×700",  "gewicht_kg": 27.0, "mca_a": 0.81},
    "MSP Kanalgerät 5.6 kW": {"artikelnr": "AM056DNMDKG/EU",  "kategorie": "MSP Kanalgerät", "kuehl_kw": 5.6, "heiz_kw": 6.3, "schall_db": "32/29/25", "abmessungen": "850×250×700",  "gewicht_kg": 27.0, "mca_a": 1.08},
    "MSP Kanalgerät 7.1 kW": {"artikelnr": "AM071DNMDKG/EU",  "kategorie": "MSP Kanalgerät", "kuehl_kw": 7.1, "heiz_kw": 8.0, "schall_db": "36/32/27", "abmessungen": "850×250×700",  "gewicht_kg": 27.0, "mca_a": 1.48},
    "MSP Kanalgerät 9.0 kW": {"artikelnr": "AM090DNMDKG/EU",  "kategorie": "MSP Kanalgerät", "kuehl_kw": 9.0, "heiz_kw": 10.0,"schall_db": "37/33/29", "abmessungen": "1200×250×700", "gewicht_kg": 34.2, "mca_a": 1.78},
}

KASSETTEN_PANEELE = {
    "Paneel klein  (960mm)":   {"artikelnr": "PC1MWFMANW", "abmessungen": "960×34×420",  "gewicht_kg": 2.6},
    "Paneel mittel (1198mm)":  {"artikelnr": "PC1NWFMANW", "abmessungen": "1198×34×500", "gewicht_kg": 4.3},
    "Paneel groß   (1410mm)":  {"artikelnr": "PC1BWFMANW", "abmessungen": "1410×34×500", "gewicht_kg": 5.0},
}

ZUBEHOER_STANDARD = {
    "Control Kit (Regeleinheit) – MIM-E03FN": "MIM-E03FN",
    "Kabelfernbedienung – MWR-WW10N":         "MWR-WW10N",
}

DAEMMSTANDARD = {
    "Altbau ungedämmt (vor 1978)":      {"u_wert": 1.2, "faktor": 130},
    "Altbau teilsaniert (1978–2000)":   {"u_wert": 0.8, "faktor": 90},
    "Neubau Standard (2000–2015)":      {"u_wert": 0.4, "faktor": 60},
    "Neubau KfW 55 (2015–2020)":        {"u_wert": 0.28,"faktor": 45},
    "Neubau KfW 40 / Passivhaus":       {"u_wert": 0.15,"faktor": 30},
}

PUFFER_EINBINDUNG = [
    "Kein Pufferspeicher",
    "Hydraulische Weiche (Parallel)",
    "In Serie – Vorlauf",
    "In Serie – Rücklauf",
]

# ============================================================
# HILFSFUNKTIONEN
# ============================================================
def get_font_as_base64(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def render_css(bg, text):
    fb = get_font_as_base64("POE Vetica UI.ttf") or get_font_as_base64("POE_Vetica_UI.ttf")
    ff = (f"@font-face{{font-family:'POE Helvetica UI';"
          f"src:url(data:font/ttf;base64,{fb}) format('truetype');}}" if fb else "")
    st.markdown(f"""<style>
    {ff}
    html,body,[data-testid="stAppViewContainer"],*{{font-family:'POE Helvetica UI','Segoe UI',sans-serif!important;}}
    .stApp{{background-color:{bg};}}
    *{{color:{text}!important;}}
    .sec-header{{font-size:22px;font-weight:bold;color:white!important;margin:14px 0 4px 0;}}
    .sub-label{{font-size:13px;opacity:.75;color:white!important;margin-bottom:2px;}}
    .spec-box{{background:rgba(255,255,255,.18);border-radius:10px;padding:14px 18px;margin-top:6px;}}
    .spec-row{{display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,.2);padding:4px 0;}}
    .spec-row span,.spec-row strong{{color:white!important;}}
    .badge-ok{{background:#27ae60;color:white!important;font-weight:bold;border-radius:6px;padding:3px 12px;font-size:14px;}}
    .badge-warn{{background:#e67e22;color:white!important;font-weight:bold;border-radius:6px;padding:3px 12px;font-size:14px;}}
    .badge-err{{background:#c0392b;color:white!important;font-weight:bold;border-radius:6px;padding:3px 12px;font-size:14px;}}
    .proj-id{{font-size:13px;font-family:monospace!important;color:white!important;opacity:.8;}}
    .info-box{{background:rgba(255,255,255,.12);border-left:4px solid white;border-radius:6px;padding:10px 16px;margin:8px 0;}}
    .info-box *{{color:white!important;font-size:14px;}}
    input,.stNumberInput div[data-baseweb="input"],.stSelectbox div[data-baseweb="select"]{{
        background-color:white!important;color:{bg}!important;
        -webkit-text-fill-color:{bg}!important;font-weight:bold!important;
        border:2px solid {text}!important;border-radius:8px!important;}}
    div.stButton>button{{background-color:white!important;color:{text}!important;
        border:2px solid {text}!important;font-weight:bold;border-radius:8px;width:100%;}}
    div.stButton>button:hover{{background-color:{text}!important;color:white!important;}}
    div[data-testid="stExpander"]{{background:rgba(255,255,255,.1)!important;border-radius:10px!important;}}
    </style>""", unsafe_allow_html=True)

def spec_box(items, title=None):
    rows = "".join(
        f'<div class="spec-row"><span>{k}</span><strong>{v}</strong></div>'
        for k, v in items.items()
    )
    th = f'<div style="font-weight:bold;color:white;margin-bottom:6px;">{title}</div>' if title else ""
    st.markdown(f'<div class="spec-box">{th}{rows}</div>', unsafe_allow_html=True)

def info_box(text):
    st.markdown(f'<div class="info-box"><span>{text}</span></div>', unsafe_allow_html=True)

def badge(cls, txt):
    return f'<span class="badge-{cls}">{txt}</span>'

def heizlast_aus_verbrauch(verbrauch_kwh: float, wirkungsgrad: float,
                            hat_ww: bool, personen: int) -> tuple:
    """Heizlast aus Jahresverbrauch ermitteln (analog WP_Quick_Kalkulator)."""
    nutz = verbrauch_kwh * wirkungsgrad
    ww_anteil = personen * 1.45 * 2.0 * 365 if hat_ww else 0
    heiz_e = nutz - ww_anteil
    if heiz_e <= 0:
        return 0.0, nutz, ww_anteil
    heizstunden = 2400 if hat_ww else 2000
    return round(heiz_e / heizstunden, 2), heiz_e, ww_anteil

def heizlast_aus_flaeche(flaeche_m2: str_or_float, faktor: float) -> float:
    """Vereinfachte spezifische Heizlast aus Fläche × Faktor."""
    try:
        return round(float(flaeche_m2) * faktor / 1000, 2)
    except Exception:
        return 0.0

# workaround for type hint
str_or_float = float

def auto_projekt_id() -> str:
    heute = datetime.now().strftime("%Y%m%d")
    rand  = str(uuid.uuid4())[:4].upper()
    return f"CQ-{heute}-{rand}"

# ============================================================
# HAUPTFUNKTION
# ============================================================
def main():
    BG    = "#36A9E1"
    TEXT  = "#3C3C3B"
    LOGO  = "Coolsulting_Logo_ohneHG_outlines_weiß.png"
    VER   = "2.0.0"
    ZEIT  = datetime.now().strftime("%d.%m.%Y | %H:%M Uhr")

    render_css(BG, TEXT)

    # ── HEADER ──────────────────────────────────────────────
    hl, hr = st.columns([3, 1])
    with hl:
        st.markdown(
            f'<div style="font-size:42px;font-weight:bold;color:white;">coolQUINT</div>'
            f'<div style="font-size:16px;color:{TEXT};margin-top:-4px;">'
            f'Samsung Quint Systemauslegung &amp; Stückliste &nbsp;|&nbsp; '
            f'v{VER} &nbsp;|&nbsp; {ZEIT}</div>',
            unsafe_allow_html=True)
    with hr:
        if os.path.exists(LOGO):
            st.image(LOGO, use_container_width=True)

    st.markdown("---")

    # ── SESSION STATE ────────────────────────────────────────
    if "projekt_id"       not in st.session_state:
        st.session_state.projekt_id = auto_projekt_id()
    if "innengeraete"     not in st.session_state:
        st.session_state.innengeraete = []

    # ════════════════════════════════════════════════════════
    # BLOCK 1 – PROJEKT- & KONTAKTDATEN
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">① Projekt- &amp; Kontaktdaten</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        projekt_name = st.text_input("Projektname / Kommission", placeholder="z.B. EFH Müller")
        bearbeiter   = st.text_input("Bearbeiter (Name)", placeholder="z.B. Michael Schäpers")
        firma        = st.text_input("Firma / Fachbetrieb", placeholder="z.B. coolsulting / Polar / Kristandl")
    with c2:
        kunde_name   = st.text_input("Kunde – Name, Vorname", placeholder="z.B. Müller, Hans")
        kunde_str    = st.text_input("Straße, Hausnummer", placeholder="z.B. Musterstraße 12")
        plz_ort_col  = st.columns(2)
        with plz_ort_col[0]:
            kunde_plz = st.text_input("PLZ", placeholder="z.B. 50667", max_chars=5)
        with plz_ort_col[1]:
            kunde_ort = st.text_input("Ort", placeholder="z.B. Köln")
    with c3:
        kunde_tel    = st.text_input("Telefon", placeholder="+49 221 …")
        kunde_email  = st.text_input("E-Mail", placeholder="name@beispiel.de")
        angebots_nr  = st.text_input("Angebotsnummer", placeholder="z.B. ANG-2026-042")
        proj_datum   = st.date_input("Datum", value=datetime.now())

    st.markdown(
        f'<div class="proj-id">🔑 Projekt-ID: <b>{st.session_state.projekt_id}</b> &nbsp;'
        f'<span style="opacity:.5;">(automatisch generiert)</span></div>',
        unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # BLOCK 2 – GEBÄUDEDATEN & BESCHAFFENHEIT
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">② Gebäudedaten &amp; Beschaffenheit</div>', unsafe_allow_html=True)

    g1, g2, g3 = st.columns(3)
    with g1:
        flaeche_heiz = st.number_input("Zu beheizende Fläche (m²)", 20, 2000, 150, step=5)
        flaeche_kuehl= st.number_input("Zu kühlende Fläche (m²)",   0,  2000,  80, step=5)
        baujahr      = st.number_input("Baujahr des Gebäudes",       1870, 2026, 1985)
    with g2:
        daemm_wahl   = st.selectbox("Dämmstandard / Hausbeschaffenheit", list(DAEMMSTANDARD.keys()))
        daemm        = DAEMMSTANDARD[daemm_wahl]
        heizlast_manuell = st.number_input(
            "Heizlast bekannt? (kW – sonst 0 lassen)", 0.0, 50.0, 0.0, step=0.5,
            help="Falls eine Heizlastberechnung nach EN 12831 vorliegt, hier eintragen. Sonst wird sie geschätzt.")
    with g3:
        spec_box({
            "U-Wert (Anhalt)":        f"{daemm['u_wert']} W/(m²K)",
            "Spez. Heizlast (Anhalt)":f"{daemm['faktor']} W/m²",
            "Schätzung Heizlast":     f"{round(flaeche_heiz * daemm['faktor'] / 1000, 2)} kW",
        }, title="Gebäude-Kennwerte")

    hl_geschaetzt = round(flaeche_heiz * daemm["faktor"] / 1000, 2)
    hl_basis      = heizlast_manuell if heizlast_manuell > 0 else hl_geschaetzt

    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # BLOCK 3 – BESTAND & VERBRAUCH
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">③ Bestand &amp; aktueller Verbrauch</div>', unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        energietraeger = st.selectbox("Bisheriger Wärmeerzeuger",
            ["Gas", "Öl", "Pellet / Holz", "Elektro-Direktheizung", "Fernwärme", "Sonstiges"])

        if energietraeger == "Gas":
            einheit_opt = ["kWh/a", "m³/a"]
        elif energietraeger == "Öl":
            einheit_opt = ["Liter/a", "kWh/a"]
        elif energietraeger in ["Pellet / Holz"]:
            einheit_opt = ["kg/a", "kWh/a"]
        else:
            einheit_opt = ["kWh/a"]

        einheit   = st.radio("Einheit", einheit_opt, horizontal=True)
        verbrauch = st.number_input(f"Jahresverbrauch ({einheit})", 100, 200000, 20000, step=500)

        wirkungsgrad_pct = st.slider("Wirkungsgrad Altanlage (%)", 50, 105, 85)
        wirkungsgrad     = wirkungsgrad_pct / 100.0

    with b2:
        hat_ww    = st.checkbox("Warmwasserbereitung über diese Anlage?", value=True)
        personen  = st.slider("Personen im Haushalt", 1, 8, 3) if hat_ww else 0

        waerme_system = st.multiselect(
            "Vorhandenes Wärmeübergabesystem",
            ["Fußbodenheizung (FBH)", "Radiatoren / Heizkörper", "Gebläsekonvektoren (Fan Coils)"],
            default=["Fußbodenheizung (FBH)"])

        hat_fbh       = any("FBH" in w          for w in waerme_system)
        hat_heizk     = any("Radiator" in w      for w in waerme_system)
        hat_fancoil   = any("Gebläse" in w       for w in waerme_system)

        if hat_heizk and not hat_fbh:
            vl_temp_default = 55
        elif hat_heizk and hat_fbh:
            vl_temp_default = 50
        else:
            vl_temp_default = 35

        vl_temp = st.slider(
            "Benötigte Vorlauftemperatur (°C)",
            25, 75, vl_temp_default,
            help="FBH: 35–45°C | Heizkörper: 50–70°C")

        if hat_heizk and vl_temp > 55:
            info_box("⚠ Vorlauftemperatur > 55 °C: Samsung EHS Quint ist bis 60 °C ausgelegt – Plausibilitätsprüfung erforderlich!")

    with b3:
        # Verbrauch → kWh
        if einheit == "m³/a"    and energietraeger == "Gas":
            kwh = verbrauch * 10.5
        elif einheit == "Liter/a" and energietraeger == "Öl":
            kwh = verbrauch * 10.0
        elif einheit == "kg/a"    and energietraeger in ["Pellet / Holz"]:
            kwh = verbrauch * 4.8
        else:
            kwh = float(verbrauch)

        hl_verbrauch, heiz_e, ww_e = heizlast_aus_verbrauch(kwh, wirkungsgrad, hat_ww, personen)
        hl_final = heizlast_manuell if heizlast_manuell > 0 else max(hl_verbrauch, hl_basis)

        spec_box({
            "Verbrauch (umgerechnet)":   f"{kwh:,.0f} kWh/a",
            "Wärme genutzt":             f"{heiz_e:,.0f} kWh/a",
            "WW-Anteil (Schätzung)":     f"{ww_e:,.0f} kWh/a" if hat_ww else "–",
            "Heizlast aus Verbrauch":    f"{hl_verbrauch} kW",
            "Heizlast aus Fläche":       f"{hl_geschaetzt} kW",
            "→ Verwendete Heizlast":     f"{'MANUELL: ' if heizlast_manuell>0 else ''}{hl_final} kW",
        }, title="Energiebilanz")

    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # BLOCK 4 – HYDRAULIK & SPEICHER
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">④ Hydraulik &amp; Speicher</div>', unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3)
    with h1:
        hat_ww_speicher   = st.checkbox("Warmwasserspeicher vorhanden / gewünscht?", value=True)
        ww_speicher_l     = 0
        ww_wt_flaeche     = 0.0
        if hat_ww_speicher:
            ww_speicher_l    = st.number_input("Warmwasserspeicher – Volumen (Liter)", 50, 2000, 200, step=10)
            ww_wt_flaeche    = st.number_input("Glattrohr-Wärmetauscher Fläche (m²)", 0.1, 10.0, 1.5, step=0.1,
                help="Wichtig für die Übertragungsgeschwindigkeit. Samsung ClimateHub enthält integrierten WT.")
            if ww_wt_flaeche < 1.0 and ww_speicher_l > 150:
                info_box("⚠ Wärmetauscherfläche gering – Aufheizzeit des Speichers kann erhöht sein!")

    with h2:
        hat_puffer         = st.checkbox("Pufferspeicher vorhanden / gewünscht?", value=False)
        puffer_l           = 0
        puffer_einbindung  = "Kein Pufferspeicher"
        if hat_puffer:
            puffer_l          = st.number_input("Pufferspeicher – Volumen (Liter)", 50, 2000, 200, step=10)
            puffer_einbindung = st.selectbox("Einbindungsart Pufferspeicher", PUFFER_EINBINDUNG[1:])
        else:
            st.caption("Kein Pufferspeicher konfiguriert.")

    with h3:
        bivalenz_aktiv = st.checkbox("Bivalente Zusatzheizung / Heizstab?", value=False)
        bivalenz_temp  = -20.0
        bivalenz_art   = "–"
        if bivalenz_aktiv:
            bivalenz_temp = st.slider("Bivalenzpunkt (Außentemperatur in °C)", -20, 10, 0,
                help="Unter dieser Außentemperatur springt die Zusatzheizung ein.")
            bivalenz_art  = st.selectbox("Art der Zusatzheizung",
                ["Elektrischer Heizstab (integriert)", "Externer Heizstab",
                 "Gaskessel (Bivalent-Parallel)", "Ölkessel (Bivalent-Parallel)"])
            info_box(f"Bivalenzpunkt: {bivalenz_temp}°C → {bivalenz_art}")

    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # BLOCK 5 – SYSTEM-HARDWARE: ODU + HYDRO UNIT
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">⑤ System-Hardware: Außengerät &amp; Hydro Unit</div>', unsafe_allow_html=True)

    s1, s2 = st.columns(2)

    with s1:
        # --- ODU ---
        st.markdown("**Außengerät (ODU)**")
        phase_filter = st.radio("Netzanschluss", ["1-phasig (230V)", "3-phasig (400V)"], horizontal=True)
        phase_key    = "1-phasig" if "1-phasig" in phase_filter else "3-phasig"
        odu_optionen = {k: v for k, v in AUSSENGERAETE.items() if v["phase"] == phase_key}

        # Empfehlung basierend auf Heizlast
        odu_empfehlung = None
        for name, d in odu_optionen.items():
            if d["heiz_kw"] >= hl_final:
                odu_empfehlung = name
                break
        if odu_empfehlung:
            st.caption(f"💡 Empfehlung basierend auf Heizlast {hl_final} kW: **{odu_empfehlung}**")

        odu_wahl = st.selectbox("Außengerät wählen", list(odu_optionen.keys()),
                                index=list(odu_optionen.keys()).index(odu_empfehlung) if odu_empfehlung else 0)
        odu      = AUSSENGERAETE[odu_wahl]

        spec_box({
            "Artikelnummer": odu["artikelnr"],
            "Kühlleistung":  f"{odu['kuehl_kw']} kW",
            "Heizleistung":  f"{odu['heiz_kw']} kW",
            "Schalldruck":   f"{odu['schall_db']} dB(A)  (Hi/Med)",
            "Abmessungen":   f"{odu['abmessungen']} mm",
            "Spannung/MCA":  f"{odu['spannung']} | {odu['mca_a']} A",
        }, title=odu_wahl)

    with s2:
        # --- HYDRO UNIT ---
        st.markdown("**Hydro Unit**")

        # Filter: wenn ClimateHub – kein externer WW-Speicher nötig
        hu_wahl = st.selectbox("Hydro Unit wählen", list(HYDRO_UNITS.keys()))
        hu      = HYDRO_UNITS[hu_wahl]

        if hu["typ"] == "Wandgerät" and hat_ww_speicher and ww_speicher_l > 0:
            info_box(f"ℹ Wandgerät gewählt → externer Warmwasserspeicher {ww_speicher_l}L erforderlich ✓")
        elif hu["typ"] == "ClimateHub":
            info_box(f"ℹ ClimateHub: Integrierter {hu['speicher_l']}L Speicher – kein externer WW-Speicher nötig.")

        if hu["zonen"] < 2 and len(waerme_system) > 1:
            info_box("⚠ Gemischtes Heizsystem (FBH + HK) erkannt – 2-Zonen Hydro Unit empfohlen!")

        spec_box({
            "Artikelnummer":  hu["artikelnr"],
            "Zonen":          str(hu["zonen"]),
            "Typ":            hu["typ"],
            "Schalldruck":    f"{hu['schall_db']} dB(A)",
            "Abmessungen":    f"{hu['abmessungen']} mm",
            "Spannung/MCA":   f"{hu['spannung']} | {hu['mca_a']} A",
        }, title=hu_wahl)
        st.caption(hu["beschreibung"])

    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # BLOCK 6 – KÄLTESEITE: INNENGERÄTE
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">⑥ Kälteseite: Innengeräte (A2A / RAC)</div>', unsafe_allow_html=True)

    kat_liste    = sorted(set(v["kategorie"] for v in INNENGERAETE.values()))
    ig_c1, ig_c2, ig_c3, ig_c4, ig_c5 = st.columns([2, 2, 1, 1, 1])
    with ig_c1:
        kat_filter = st.selectbox("Gerätetyp", kat_liste)
    with ig_c2:
        ig_gefiltert = {k: v for k, v in INNENGERAETE.items() if v["kategorie"] == kat_filter}
        ig_wahl      = st.selectbox("Gerät", list(ig_gefiltert.keys()))
    with ig_c3:
        ig_menge = st.number_input("Menge", 1, 20, 1, key="ig_menge")
    with ig_c4:
        ig_zone  = st.number_input("Zone", 1, max(hu["zonen"], 1), 1, key="ig_zone")
    with ig_c5:
        ig_raum  = st.text_input("Raumbezeichnung", placeholder="z.B. Wohnzimmer", key="ig_raum")

    st.markdown("<br>", unsafe_allow_html=True)
    add_col, pan_col = st.columns([1, 2])
    with add_col:
        if st.button("➕ Innengerät hinzufügen"):
            ig_d = INNENGERAETE[ig_wahl]
            st.session_state.innengeraete.append({
                "name": ig_wahl, "artikelnr": ig_d["artikelnr"],
                "kategorie": ig_d["kategorie"],
                "kuehl_kw": ig_d["kuehl_kw"], "heiz_kw": ig_d["heiz_kw"],
                "schall_db": ig_d["schall_db"], "abmessungen": ig_d["abmessungen"],
                "gewicht_kg": ig_d["gewicht_kg"], "mca_a": ig_d["mca_a"],
                "menge": ig_menge, "zone": int(ig_zone),
                "raum": st.session_state.get("ig_raum", ""),
            })
            st.rerun()

    with pan_col:
        paneel_wahl = "– keines –"
        if "Kassette" in kat_filter:
            paneel_wahl = st.selectbox(
                "Kassetten-Paneel (optional)",
                ["– keines –"] + list(KASSETTEN_PANEELE.keys()))

    # Liste konfigurierter Innengeräte
    if st.session_state.innengeraete:
        st.markdown("**Konfigurierte Innengeräte:**")
        for idx, ig in enumerate(st.session_state.innengeraete):
            ca, cb, cc, cd, ce = st.columns([3, 1, 1, 1, 1])
            with ca:
                raum_txt = f" – {ig['raum']}" if ig.get("raum") else ""
                st.markdown(
                    f'<span style="color:white;">{ig["menge"]}× {ig["name"]}{raum_txt}</span>'
                    f'<span style="opacity:.6;font-size:12px;"> [Zone {ig["zone"]}] {ig["artikelnr"]}</span>',
                    unsafe_allow_html=True)
            with cb:
                st.markdown(f'<span style="color:white;font-size:13px;">❄ {ig["kuehl_kw"]} kW</span>', unsafe_allow_html=True)
            with cc:
                st.markdown(f'<span style="color:white;font-size:13px;">♨ {ig["heiz_kw"]} kW</span>', unsafe_allow_html=True)
            with cd:
                st.markdown(f'<span style="color:white;font-size:12px;">{ig["schall_db"]} dB</span>', unsafe_allow_html=True)
            with ce:
                if st.button("🗑", key=f"del_{idx}"):
                    st.session_state.innengeraete.pop(idx)
                    st.rerun()

        if st.button("🔄 Alle Innengeräte zurücksetzen"):
            st.session_state.innengeraete = []
            st.rerun()
    else:
        st.info("Noch keine Innengeräte hinzugefügt – oder nicht benötigt (reine Wärmepumpe).")

    # EEV Empfehlung
    anzahl_ig = sum(ig["menge"] for ig in st.session_state.innengeraete)
    eev_auto  = max(0, anzahl_ig - 1)
    eev_col1, eev_col2 = st.columns(2)
    with eev_col1:
        eev_modus = st.selectbox("Expansionsventilboxen (EEV-Kits)",
            ["Automatisch (vom System ermitteln)", "Manuell festlegen", "Keine"])
    with eev_col2:
        if eev_modus == "Automatisch (vom System ermitteln)":
            eev_anzahl = eev_auto
            st.caption(f"💡 Empfehlung: {eev_anzahl} EEV-Kit(s) bei {anzahl_ig} Innengerät(en)")
        elif eev_modus == "Manuell festlegen":
            eev_anzahl = st.number_input("Anzahl EEV-Kits", 0, 10, eev_auto)
        else:
            eev_anzahl = 0

    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # BLOCK 7 – LEITUNGSTOPOLOGIE
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">⑦ Leitungstopologie &amp; Kältemittelstränge</div>', unsafe_allow_html=True)

    lt1, lt2, lt3 = st.columns(3)
    with lt1:
        dist_odu_hydro = st.number_input("Distanz ODU → Hydro Unit / Verrohrung (m)", 0, 100, 5, step=1,
            help="Wasserseite – Länge der Anbindeleitung")
        dist_odu_abzweig = st.number_input("Distanz ODU → 1. Kältemittelabzweig (m)", 0, 100, 10, step=1,
            help="Kältemittelseite – bis zum ersten Y-Stück")
        hoehen_diff = st.number_input("Maximaler Höhenunterschied (m)", 0, 30, 4, step=1,
            help="Zwischen ODU und dem am höchsten gelegenen Innengerät")

    with lt2:
        strang_a_geraete = st.number_input("Strang A – Anzahl Innengeräte", 0, 8, min(2, anzahl_ig))
        strang_a_laenge  = st.number_input("Strang A – Leitungslänge (m)", 0, 100, 15)
        strang_b_geraete = st.number_input("Strang B – Anzahl Innengeräte", 0, 8, max(0, anzahl_ig - min(2, anzahl_ig)))
        strang_b_laenge  = st.number_input("Strang B – Leitungslänge (m)", 0, 100, 10)

    with lt3:
        gesamt_laenge = dist_odu_abzweig + max(strang_a_laenge, strang_b_laenge)
        aequiv_laenge = gesamt_laenge * 1.2  # +20% für Bögen etc.

        limit_laenge = 50  # Samsung EHS typisches Limit (äquivalent)
        limit_hoehe  = 15

        laenge_ok = aequiv_laenge <= limit_laenge
        hoehe_ok  = hoehen_diff <= limit_hoehe

        spec_box({
            "Äquiv. Gesamtlänge": f"{aequiv_laenge:.0f} m (Limit: {limit_laenge} m)",
            "Höhendiff.":         f"{hoehen_diff} m (Limit: {limit_hoehe} m)",
            "Leitungslänge":      badge("ok","✓ OK") if laenge_ok else badge("err","✗ Überschritten!"),
            "Höhendifferenz":     badge("ok","✓ OK") if hoehe_ok  else badge("warn","⚠ Prüfen!"),
        }, title="Topologie-Check")

        if not laenge_ok:
            info_box("✗ Äquivalente Leitungslänge überschreitet Samsung-Empfehlung (50 m). Bitte Leitungsführung überprüfen!")
        if not hoehe_ok:
            info_box("⚠ Höhenunterschied > 15 m: Ölhebebögen erforderlich – Anlage bleibt grundsätzlich möglich, aber aufwändiger.")

    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # BLOCK 8 – ZUBEHÖR
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">⑧ Zubehör &amp; Optionen</div>', unsafe_allow_html=True)

    z1, z2 = st.columns(2)
    with z1:
        zub_standard = st.multiselect("Standard-Zubehör", list(ZUBEHOER_STANDARD.keys()))
        hub_typ = st.selectbox("Hub / Verteilerregelung",
            ["– nicht benötigt –",
             "Switch-Hub (integriert WW + Heizen)  – Artikelnr. auf Anfrage",
             "Mini-Hub (externe Verteilung)         – Artikelnr. auf Anfrage"])
    with z2:
        extra_zub = st.text_area("Weiteres Zubehör / Sonderpositionen (Freitext)",
            placeholder="z.B. Montagerahmen, Frostschutzheizung, ext. Pufferspeicher XY ...",
            height=100)

    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # BLOCK 8b – VALIDIERUNGS-ENGINE (Plausibilitätsprüfung)
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">⑧b Plausibilitätsprüfung (Validation Engine)</div>', unsafe_allow_html=True)

    val_ok   = []   # grün
    val_warn = []   # gelb
    val_err  = []   # rot

    # ── Check 1: Spezifischer Verbrauch vs. Dämmstandard ──────────────
    if flaeche_heiz > 0 and kwh > 0:
        kwh_m2 = kwh / flaeche_heiz
        limits = {
            "Altbau ungedämmt (vor 1978)":      (0, 350),
            "Altbau teilsaniert (1978–2000)":   (0, 250),
            "Neubau Standard (2000–2015)":      (0, 150),
            "Neubau KfW 55 (2015–2020)":        (0, 100),
            "Neubau KfW 40 / Passivhaus":       (0, 60),
        }
        lo, hi = limits.get(daemm_wahl, (0, 999))
        if kwh_m2 > hi:
            val_err.append(
                f"✗ Verbrauch {kwh_m2:.0f} kWh/m²a ist für '{daemm_wahl}' untypisch hoch "
                f"(Grenzwert: {hi} kWh/m²a). Bitte Dämmstandard oder Verbrauch prüfen – "
                f"Gefahr der Überdimensionierung des ODU!")
        elif kwh_m2 > hi * 0.75:
            val_warn.append(
                f"⚠ Verbrauch {kwh_m2:.0f} kWh/m²a liegt im oberen Bereich für '{daemm_wahl}'. "
                f"Heizlastberechnung nach EN 12831 empfohlen.")
        else:
            val_ok.append(f"✓ Spez. Verbrauch {kwh_m2:.0f} kWh/m²a plausibel für gewählten Dämmstandard.")

    # ── Check 2: WW-Speicher Registerfläche vs. ODU-Leistung ──────────
    if hat_ww_speicher and ww_speicher_l > 0 and hu["typ"] == "Wandgerät":
        # Formel: Registerfläche [m²] >= ODU_heiz_kW / 4
        min_wt = odu["heiz_kw"] / 4.0
        if ww_wt_flaeche < min_wt:
            val_err.append(
                f"✗ Glattrohr-WT Fläche {ww_wt_flaeche:.1f} m² < Minimum {min_wt:.1f} m² "
                f"(= ODU {odu['heiz_kw']} kW ÷ 4). "
                f"→ WP kann Energie nicht schnell genug übertragen → Hochdruck-Störungen / Takten!")
        elif ww_wt_flaeche < min_wt * 1.25:
            val_warn.append(
                f"⚠ Glattrohr-WT {ww_wt_flaeche:.1f} m² ist knapp (Empfehlung ≥ {min_wt*1.25:.1f} m²). "
                f"Aufheizzeit des Speichers erhöht.")
        else:
            val_ok.append(f"✓ Wärmetauscherfläche {ww_wt_flaeche:.1f} m² ausreichend für ODU {odu['heiz_kw']} kW.")
    elif hu["typ"] == "ClimateHub":
        val_ok.append("✓ ClimateHub: Integrierter Wärmetauscher – kein externer WW-WT erforderlich.")

    # ── Check 3: Puffer-Einbindung vs. Wärmeübergabesystem ───────────
    if hat_puffer and puffer_einbindung in ["In Serie – Vorlauf", "In Serie – Rücklauf"]:
        if hat_heizk:
            val_warn.append(
                f"⚠ Reihenpuffer ({puffer_einbindung}) + Heizkörper: Bei Abtauvorgang (Defrost) "
                f"kann der Mindest-Volumenstrom nicht garantiert werden → "
                f"Hydraulische Weiche (Parallel) empfohlen für Heizkörper-Anlagen!")
        else:
            val_ok.append(f"✓ Puffer '{puffer_einbindung}' mit FBH/Fan Coil ist technisch zulässig.")

    # ── Check 4: Kältetechnische Grenzen ──────────────────────────────
    if hoehen_diff > 15:
        val_err.append(
            f"✗ Höhendifferenz {hoehen_diff} m überschreitet Samsung-Grenzwert (15 m). "
            f"→ Anlage in dieser Form technisch nicht zulässig! Ölhebebögen (DSR) prüfen oder ODU-Position ändern.")
    elif hoehen_diff > 10:
        val_warn.append(
            f"⚠ Höhendifferenz {hoehen_diff} m > 10 m: Ölhebebögen erforderlich, "
            f"Rohrdimensionierung sorgfältig prüfen (v_min in Steigleitungen beachten).")
    else:
        val_ok.append(f"✓ Höhendifferenz {hoehen_diff} m innerhalb Samsung-Limit (15 m).")

    if aequiv_laenge > limit_laenge:
        val_err.append(
            f"✗ Äquivalente Kältemittelleitungslänge {aequiv_laenge:.0f} m > {limit_laenge} m Samsung-Grenzwert. "
            f"→ Systemdruck und Ölrückführung kritisch. Leitungsführung überarbeiten!")

    # ── Check 5: EEV-Kit Stromversorgung ──────────────────────────────
    if eev_anzahl > 0:
        val_warn.append(
            f"⚠ {eev_anzahl} EEV-Kit(s) geplant: Zusätzliche 230V-Spannungsversorgung "
            f"am EEV-Montageort einplanen (oft vergessen bei Unterverteilung)!")
        if eev_modus == "Automatisch (vom System ermitteln)":
            val_ok.append(f"✓ {eev_anzahl} EEV-Kit(s) empfohlen bei {anzahl_ig} Innengeräten.")

    # ── Check 6: Mini-Hub ohne 3-Wege-Ventil ──────────────────────────
    if "Mini-Hub" in hub_typ:
        val_err.append(
            "✗ Mini-Hub gewählt: Externes 3-Wege-Ventil für hydraulische Warmwasser-Umschaltung "
            "fehlt in der Stückliste! → Bitte als Sonderposition unter Zubehör ergänzen.")

    # ── Check 7: Vorlauftemperatur vs. ODU-Spec ────────────────────────
    if vl_temp > 60:
        val_err.append(
            f"✗ Vorlauftemperatur {vl_temp}°C überschreitet Samsung EHS Quint Spezifikation (max. 60°C)! "
            f"→ Anlage nicht betreibbar. Heizflächen sanieren oder anderen WP-Typ wählen.")
    elif vl_temp > 55:
        val_warn.append(
            f"⚠ Vorlauftemperatur {vl_temp}°C: Im Grenzbereich (max. 60°C). "
            f"COP wird stark reduziert. Radiatoren-Sanierung empfohlen.")

    # ── Check 8: Heizlast vs. ODU-Leistung ────────────────────────────
    if hl_final > odu["heiz_kw"] * 1.1:
        val_err.append(
            f"✗ Heizlast {hl_final} kW > ODU Nennleistung {odu['heiz_kw']} kW (+10% Toleranz). "
            f"→ ODU unterdimensioniert! Größeres Modell oder bivalente Zusatzheizung einplanen.")
    elif hl_final > odu["heiz_kw"]:
        val_warn.append(
            f"⚠ Heizlast {hl_final} kW leicht über ODU {odu['heiz_kw']} kW. "
            f"Bivalenzpunkt prüfen – Heizstab als Backup empfohlen.")
    else:
        val_ok.append(f"✓ Heizlast {hl_final} kW durch ODU {odu['heiz_kw']} kW abgedeckt.")

    # ── Check 9: Hydro Unit Zonen vs. gemischtes System ───────────────
    if len(waerme_system) > 1 and hu["zonen"] < 2:
        val_warn.append(
            f"⚠ Gemischtes Heizsystem ({', '.join(waerme_system)}) aber nur 1-Zonen Hydro Unit gewählt. "
            f"→ Getrennte Temperaturregelung für FBH/HK nicht möglich!")
    elif len(waerme_system) > 1 and hu["zonen"] == 2:
        val_ok.append("✓ 2-Zonen Hydro Unit korrekt für gemischtes Heizsystem gewählt.")

    # ── AMPEL-ANZEIGE ─────────────────────────────────────────────────
    col_ok, col_warn, col_err = st.columns(3)
    with col_ok:
        st.markdown(f'<div style="background:rgba(39,174,96,.25);border-radius:8px;padding:12px;">'
                    f'<b style="color:#27ae60;">✓ OK ({len(val_ok)})</b>', unsafe_allow_html=True)
        for m in val_ok:
            st.markdown(f'<div style="font-size:12px;color:white;margin-top:4px;">{m}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_warn:
        st.markdown(f'<div style="background:rgba(230,126,34,.25);border-radius:8px;padding:12px;">'
                    f'<b style="color:#e67e22;">⚠ Warnung ({len(val_warn)})</b>', unsafe_allow_html=True)
        for m in val_warn:
            st.markdown(f'<div style="font-size:12px;color:white;margin-top:4px;">{m}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_err:
        st.markdown(f'<div style="background:rgba(192,57,43,.25);border-radius:8px;padding:12px;">'
                    f'<b style="color:#c0392b;">✗ Fehler ({len(val_err)})</b>', unsafe_allow_html=True)
        for m in val_err:
            st.markdown(f'<div style="font-size:12px;color:white;margin-top:4px;">{m}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if val_err:
        st.markdown(
            '<div style="background:rgba(192,57,43,.4);border-radius:8px;padding:10px;margin-top:8px;">'
            '<b style="color:white;">🚫 Kritische Fehler vorhanden – Stückliste wird trotzdem generiert, '
            'aber Anlage in dieser Konfiguration NICHT betreibbar!</b></div>',
            unsafe_allow_html=True)

    st.markdown("---")

    # ════════════════════════════════════════════════════════
    # BLOCK 9 – SYSTEMCHECK & STÜCKLISTE
    # ════════════════════════════════════════════════════════
    st.markdown('<div class="sec-header">⑨ Systemcheck &amp; Stückliste</div>', unsafe_allow_html=True)

    # --- Leistungscheck ---
    total_kuehl = sum(ig["kuehl_kw"] * ig["menge"] for ig in st.session_state.innengeraete)
    total_heiz  = sum(ig["heiz_kw"]  * ig["menge"] for ig in st.session_state.innengeraete)
    odu_kuehl   = odu["kuehl_kw"]
    odu_heiz    = odu["heiz_kw"]

    def ausn_badge(total, cap):
        if cap == 0: return "ok", "–"
        pct = total / cap * 100
        if pct <= 100:   return "ok",   f"✓ {pct:.0f}% OK"
        elif pct <= 130: return "warn",  f"⚠ {pct:.0f}% Grenzwertig"
        else:            return "err",   f"✗ {pct:.0f}% Überladen"

    hl_check_cls, hl_check_txt = ("ok",   f"✓ {hl_final} kW ≤ {odu_heiz} kW") \
        if hl_final <= odu_heiz else ("warn", f"⚠ {hl_final} kW > {odu_heiz} kW – ODU knapp!")

    ck1, ck2, ck3, ck4 = st.columns(4)
    with ck1:
        st.metric("Heizlast (Gebäude)", f"{hl_final} kW")
        st.markdown(badge(hl_check_cls, hl_check_txt), unsafe_allow_html=True)
    with ck2:
        st.metric("Innengeräte Kühlen", f"{total_kuehl:.1f} kW")
        c, t = ausn_badge(total_kuehl, odu_kuehl)
        st.markdown(badge(c, t), unsafe_allow_html=True)
    with ck3:
        st.metric("Innengeräte Heizen", f"{total_heiz:.1f} kW")
        c, t = ausn_badge(total_heiz, odu_heiz)
        st.markdown(badge(c, t), unsafe_allow_html=True)
    with ck4:
        vl_ok = vl_temp <= 60
        st.metric("Vorlauftemperatur", f"{vl_temp} °C")
        st.markdown(badge("ok" if vl_ok else "warn",
                          f"✓ {vl_temp}°C" if vl_ok else f"⚠ {vl_temp}°C – Samsung max. 60°C"),
                    unsafe_allow_html=True)

    st.markdown("---")

    # --- STÜCKLISTE AUFBAUEN ---
    st.markdown("### Stückliste")

    pos = []

    def add(menge, kat, bez, artnr, kw_k="–", kw_h="–", abm="–", gew="–"):
        pos.append({"Pos": len(pos)+1, "Menge": menge, "Kategorie": kat,
                    "Bezeichnung": bez, "Artikelnummer": artnr,
                    "Kühl kW": kw_k, "Heiz kW": kw_h,
                    "Abmessungen mm": abm, "Gewicht kg": gew})

    add(1, "Außengerät", odu_wahl, odu["artikelnr"],
        odu["kuehl_kw"], odu["heiz_kw"], odu["abmessungen"], odu["gewicht_kg"])

    add(1, "Hydro Unit", hu_wahl, hu["artikelnr"],
        "–", "–", hu["abmessungen"], hu["gewicht_kg"])

    for ig in st.session_state.innengeraete:
        raum_info = f" – {ig['raum']}" if ig.get("raum") else ""
        add(ig["menge"], ig["kategorie"],
            f"{ig['name']}{raum_info} (Zone {ig['zone']})", ig["artikelnr"],
            ig["kuehl_kw"], ig["heiz_kw"], ig["abmessungen"], ig["gewicht_kg"])

    if paneel_wahl != "– keines –" and any("Kassette" in ig["kategorie"]
                                            for ig in st.session_state.innengeraete):
        pan = KASSETTEN_PANEELE[paneel_wahl]
        kassetten_menge = sum(ig["menge"] for ig in st.session_state.innengeraete
                              if "Kassette" in ig["kategorie"])
        add(kassetten_menge, "Zubehör", paneel_wahl, pan["artikelnr"],
            "–", "–", pan["abmessungen"], pan["gewicht_kg"])

    if eev_anzahl > 0:
        add(eev_anzahl, "Zubehör", "Expansionsventilbox (EEV-Kit)", "– auf Anfrage –")

    if hub_typ != "– nicht benötigt –":
        add(1, "Zubehör", hub_typ.split("–")[0].strip(), "– auf Anfrage –")

    for z in zub_standard:
        add(1, "Zubehör", z.split("–")[0].strip(), ZUBEHOER_STANDARD[z])

    if hat_puffer and puffer_l > 0:
        add(1, "Hydraulik", f"Pufferspeicher {puffer_l}L ({puffer_einbindung})", "– nach Wahl –")

    if hat_ww_speicher and ww_speicher_l > 0 and hu["typ"] == "Wandgerät":
        add(1, "Hydraulik", f"Warmwasserspeicher {ww_speicher_l}L", "– nach Wahl –")

    if bivalenz_aktiv:
        add(1, "Zusatzheizung", f"Bivalenzpunkt {bivalenz_temp}°C – {bivalenz_art}", "– nach Wahl –")

    if extra_zub.strip():
        for line in extra_zub.strip().split("\n"):
            if line.strip():
                add(1, "Sonstiges", line.strip(), "–")

    df = pd.DataFrame(pos)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- EXPORT ---
    st.markdown("---")
    st.markdown("### Export")

    header_meta = (
        f"coolQUINT – Systemkonfiguration\n"
        f"{'='*55}\n"
        f"Projekt-ID:    {st.session_state.projekt_id}\n"
        f"Projektname:   {projekt_name or '–'}\n"
        f"Angebots-Nr.:  {angebots_nr or '–'}\n"
        f"Bearbeiter:    {bearbeiter or '–'}  |  {firma or '–'}\n"
        f"Kunde:         {kunde_name or '–'},  {kunde_str or '–'},  {kunde_plz or ''} {kunde_ort or ''}\n"
        f"Datum:         {proj_datum}\n\n"
        f"GEBÄUDE:\n"
        f"  Heizfläche: {flaeche_heiz} m²  |  Kühlfläche: {flaeche_kuehl} m²\n"
        f"  Baujahr: {baujahr}  |  Dämmung: {daemm_wahl}\n"
        f"  Heizlast (verwendet): {hl_final} kW\n"
        f"  Vorlauftemperatur: {vl_temp} °C  |  Wärmeübergabe: {', '.join(waerme_system) or '–'}\n\n"
        f"ENERGIETRÄGER BISHER:\n"
        f"  {energietraeger}: {verbrauch:,} {einheit}  |  Wirkungsgrad: {wirkungsgrad_pct}%\n\n"
        f"SYSTEM:\n"
        f"  ODU:        {odu_wahl} ({odu['artikelnr']})\n"
        f"  Hydro Unit: {hu_wahl} ({hu['artikelnr']})\n\n"
        f"INNENGERÄTE:\n"
    )
    for ig in st.session_state.innengeraete:
        header_meta += f"  {ig['menge']}× {ig['name']} – Zone {ig['zone']} [{ig['artikelnr']}]  {ig.get('raum','')}\n"

    header_meta += (
        f"\nLEISTUNGSBILANZ:\n"
        f"  A2A Kühlen: {total_kuehl:.1f} kW / ODU {odu_kuehl} kW\n"
        f"  A2A Heizen: {total_heiz:.1f} kW / ODU {odu_heiz} kW\n"
        f"  Heizlast:   {hl_final} kW / ODU {odu_heiz} kW\n\n"
        f"LEITUNGSTOPOLOGIE:\n"
        f"  ODU → Hydro: {dist_odu_hydro} m\n"
        f"  ODU → Abzweig: {dist_odu_abzweig} m\n"
        f"  Strang A: {strang_a_geraete} Geräte / {strang_a_laenge} m\n"
        f"  Strang B: {strang_b_geraete} Geräte / {strang_b_laenge} m\n"
        f"  Höhendifferenz: {hoehen_diff} m\n"
    )

    csv_data = (
        f"# {header_meta.replace(chr(10), chr(10)+'# ')}\n\n"
        + df.to_csv(index=False, sep=";", decimal=",")
    )

    ex1, ex2 = st.columns(2)
    with ex1:
        st.download_button(
            "📥 Stückliste als CSV",
            data=csv_data.encode("utf-8-sig"),
            file_name=f"coolQUINT_{st.session_state.projekt_id}_{proj_datum}.csv",
            mime="text/csv")
    with ex2:
        st.download_button(
            "📄 Zusammenfassung als TXT",
            data=header_meta.encode("utf-8"),
            file_name=f"coolQUINT_{st.session_state.projekt_id}_{proj_datum}.txt",
            mime="text/plain")


if __name__ == "__main__":
    main()
