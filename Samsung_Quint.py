# ============================================================================
# DATEI: Samsung_Quint.py
# VERSION: 1.0.0
# STAND: 12.03.2026
# AUTOR: Michael Schäpers, coolsulting
# BESCHREIBUNG: Samsung Quint – Systemkonfiguration & Stückliste
# ============================================================================

import streamlit as st
import os
import base64
from datetime import datetime

# ============================================================
# SEITE KONFIGURIEREN
# ============================================================
try:
    from PIL import Image
    icon_image = Image.open("Coolsulting_Logo_ohneHG_weiß_grau.png")
    st.set_page_config(
        page_title="Samsung Quint | coolsulting",
        page_icon=icon_image,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except Exception:
    st.set_page_config(
        page_title="Samsung Quint | coolsulting",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

# ============================================================
# PRODUKTDATEN
# ============================================================

AUSSENGERAETE = {
    "ODU 12.5 kW (1-phasig)": {
        "artikelnr": "AE125HCTPES/EU",
        "kuehl_kw": 12.5,
        "heiz_kw": 12.5,
        "schall_db": "51 / 49",
        "schallleistung_db": 62,
        "abmessungen": "1270 × 850 × 500",
        "gewicht_kg": 126.5,
        "spannung": "230V / 1Ph",
        "mca_a": 32,
        "phase": "1-phasig",
    },
    "ODU 16.0 kW (1-phasig)": {
        "artikelnr": "AE160HCTPES/EU",
        "kuehl_kw": 14.5,
        "heiz_kw": 16.0,
        "schall_db": "55 / 49",
        "schallleistung_db": 62,
        "abmessungen": "1270 × 850 × 500",
        "gewicht_kg": 126.5,
        "spannung": "230V / 1Ph",
        "mca_a": 32,
        "phase": "1-phasig",
    },
    "ODU 12.5 kW (3-phasig)": {
        "artikelnr": "AE125HCTPGS/EU",
        "kuehl_kw": 12.5,
        "heiz_kw": 12.5,
        "schall_db": "51 / 49",
        "schallleistung_db": 62,
        "abmessungen": "1270 × 850 × 500",
        "gewicht_kg": 126.5,
        "spannung": "400V / 3Ph",
        "mca_a": 16.1,
        "phase": "3-phasig",
    },
    "ODU 16.0 kW (3-phasig)": {
        "artikelnr": "AE160HCTPGS/EU",
        "kuehl_kw": 14.5,
        "heiz_kw": 16.0,
        "schall_db": "55 / 49",
        "schallleistung_db": 62,
        "abmessungen": "1270 × 850 × 500",
        "gewicht_kg": 126.5,
        "spannung": "400V / 3Ph",
        "mca_a": 16.1,
        "phase": "3-phasig",
    },
}

HYDRO_UNITS = {
    "ClimateHub 200L – 1 Zone": {
        "artikelnr": "AE200DNWMPK/EU",
        "zonen": 1,
        "typ": "ClimateHub",
        "schall_db": 28,
        "schallleistung_db": 42,
        "abmessungen": "598 × 1850 × 600",
        "gewicht_kg": 132,
        "spannung": "230V / 400V",
        "mca_a": 18.3,
        "beschreibung": "Mit integriertem 200L-Speicher für Warmwasser"
    },
    "ClimateHub 200L – 2 Zonen": {
        "artikelnr": "AE200DNXMPK/EU",
        "zonen": 2,
        "typ": "ClimateHub",
        "schall_db": 30,
        "schallleistung_db": 44,
        "abmessungen": "598 × 1850 × 600",
        "gewicht_kg": 139,
        "spannung": "230V / 400V",
        "mca_a": 18.7,
        "beschreibung": "Mit integriertem 200L-Speicher + 2-Zonen-Regelung"
    },
    "Wandgerät – 1 Zone": {
        "artikelnr": "AE160DNYMPK/EU",
        "zonen": 1,
        "typ": "Wandgerät",
        "schall_db": 28,
        "schallleistung_db": 42,
        "abmessungen": "530 × 840 × 350",
        "gewicht_kg": 43,
        "spannung": "230V / 400V",
        "mca_a": 18.3,
        "beschreibung": "Kompakte Wandmontage, ohne Speicher"
    },
    "Wandgerät – 2 Zonen": {
        "artikelnr": "AE160DNZMPK/EU",
        "zonen": 2,
        "typ": "Wandgerät",
        "schall_db": 30,
        "schallleistung_db": 44,
        "abmessungen": "530 × 840 × 350",
        "gewicht_kg": 54,
        "spannung": "230V / 400V",
        "mca_a": 18.7,
        "beschreibung": "Kompakte Wandmontage + 2-Zonen-Regelung"
    },
}

INNENGERAETE = {
    # --- RAC Wandgeräte ---
    "RAC Wandgerät 1.5 kW": {
        "artikelnr": "AE015HEADKG/EU",
        "kategorie": "RAC Wandgerät",
        "kuehl_kw": 1.5,
        "heiz_kw": 1.7,
        "schall_db": "31 / 30 / 29",
        "schallleistung_db": 50,
        "abmessungen": "682 × 299 × 215",
        "gewicht_kg": 7.8,
        "mca_a": 0.16,
    },
    "RAC Wandgerät 2.2 kW": {
        "artikelnr": "AE022HEADKG/EU",
        "kategorie": "RAC Wandgerät",
        "kuehl_kw": 2.2,
        "heiz_kw": 2.5,
        "schall_db": "33 / 31 / 29",
        "schallleistung_db": 51,
        "abmessungen": "682 × 299 × 215",
        "gewicht_kg": 7.8,
        "mca_a": 0.20,
    },
    "RAC Wandgerät 2.8 kW": {
        "artikelnr": "AE028HEADKG/EU",
        "kategorie": "RAC Wandgerät",
        "kuehl_kw": 2.8,
        "heiz_kw": 3.2,
        "schall_db": "34 / 33 / 31",
        "schallleistung_db": 50,
        "abmessungen": "820 × 299 × 215",
        "gewicht_kg": 9.2,
        "mca_a": 0.25,
    },
    "RAC Wandgerät 3.6 kW": {
        "artikelnr": "AE036HEADKG/EU",
        "kategorie": "RAC Wandgerät",
        "kuehl_kw": 3.6,
        "heiz_kw": 4.0,
        "schall_db": "39 / 36 / 33",
        "schallleistung_db": 56,
        "abmessungen": "820 × 299 × 215",
        "gewicht_kg": 9.2,
        "mca_a": 0.31,
    },
    "RAC Wandgerät 5.6 kW": {
        "artikelnr": "AM056DNVDKG/EU",
        "kategorie": "RAC Wandgerät",
        "kuehl_kw": 5.6,
        "heiz_kw": 6.3,
        "schall_db": "40 / 37 / 34",
        "schallleistung_db": 58,
        "abmessungen": "1055 × 299 × 215",
        "gewicht_kg": 12.0,
        "mca_a": 0.44,
    },
    "RAC Wandgerät 7.1 kW": {
        "artikelnr": "AM071DNVDKG/EU",
        "kategorie": "RAC Wandgerät",
        "kuehl_kw": 6.8,
        "heiz_kw": 7.0,
        "schall_db": "43 / 40 / 37",
        "schallleistung_db": 62,
        "abmessungen": "1055 × 299 × 215",
        "gewicht_kg": 12.0,
        "mca_a": 0.50,
    },
    # --- 1-Weg Kassetten ---
    "1-Weg Kassette 1.7 kW": {
        "artikelnr": "AM017DN1DKG/EU",
        "kategorie": "1-Weg Kassette",
        "kuehl_kw": 1.7,
        "heiz_kw": 1.9,
        "schall_db": "28 / 26 / 24",
        "schallleistung_db": 46,
        "abmessungen": "740 × 135 × 360",
        "gewicht_kg": 8.0,
        "mca_a": 0.18,
    },
    "1-Weg Kassette 2.2 kW": {
        "artikelnr": "AM022DN1DKG/EU",
        "kategorie": "1-Weg Kassette",
        "kuehl_kw": 2.2,
        "heiz_kw": 2.5,
        "schall_db": "29 / 26 / 24",
        "schallleistung_db": 47,
        "abmessungen": "740 × 135 × 360",
        "gewicht_kg": 8.0,
        "mca_a": 0.18,
    },
    "1-Weg Kassette 2.8 kW": {
        "artikelnr": "AM028DN1DKG/EU",
        "kategorie": "1-Weg Kassette",
        "kuehl_kw": 2.8,
        "heiz_kw": 3.2,
        "schall_db": "32 / 28 / 24",
        "schallleistung_db": 50,
        "abmessungen": "970 × 135 × 410",
        "gewicht_kg": 10.0,
        "mca_a": 0.29,
    },
    "1-Weg Kassette 3.6 kW": {
        "artikelnr": "AM036DN1DKG/EU",
        "kategorie": "1-Weg Kassette",
        "kuehl_kw": 3.6,
        "heiz_kw": 4.0,
        "schall_db": "37 / 33 / 30",
        "schallleistung_db": 55,
        "abmessungen": "970 × 135 × 410",
        "gewicht_kg": 10.0,
        "mca_a": 0.31,
    },
    "1-Weg Kassette 5.6 kW": {
        "artikelnr": "AM056DN1DKG/EU",
        "kategorie": "1-Weg Kassette",
        "kuehl_kw": 5.6,
        "heiz_kw": 6.3,
        "schall_db": "41 / 38 / 35",
        "schallleistung_db": 59,
        "abmessungen": "1200 × 138 × 450",
        "gewicht_kg": 13.5,
        "mca_a": 0.35,
    },
    # --- LSP Kanalgeräte ---
    "LSP Kanalgerät 2.2 kW": {
        "artikelnr": "AM022DNLDKG/EU",
        "kategorie": "LSP Kanalgerät",
        "kuehl_kw": 2.2,
        "heiz_kw": 2.5,
        "schall_db": "26 / 23 / 19",
        "schallleistung_db": 42,
        "abmessungen": "700 × 199 × 440",
        "gewicht_kg": 15.9,
        "mca_a": 0.38,
    },
    "LSP Kanalgerät 2.8 kW": {
        "artikelnr": "AM028DNLDKG/EU",
        "kategorie": "LSP Kanalgerät",
        "kuehl_kw": 2.8,
        "heiz_kw": 3.2,
        "schall_db": "28 / 24 / 19",
        "schallleistung_db": 44,
        "abmessungen": "700 × 199 × 440",
        "gewicht_kg": 15.9,
        "mca_a": 0.45,
    },
    "LSP Kanalgerät 3.6 kW": {
        "artikelnr": "AM036DNLDKG/EU",
        "kategorie": "LSP Kanalgerät",
        "kuehl_kw": 3.6,
        "heiz_kw": 4.0,
        "schall_db": "31 / 26 / 20",
        "schallleistung_db": 46,
        "abmessungen": "700 × 199 × 440",
        "gewicht_kg": 16.3,
        "mca_a": 0.53,
    },
    "LSP Kanalgerät 5.6 kW": {
        "artikelnr": "AM056DNLDKG/EU",
        "kategorie": "LSP Kanalgerät",
        "kuehl_kw": 5.6,
        "heiz_kw": 6.3,
        "schall_db": "34 / 30 / 26",
        "schallleistung_db": 49,
        "abmessungen": "900 × 199 × 440",
        "gewicht_kg": 19.3,
        "mca_a": 0.92,
    },
    # --- MSP Kanalgeräte ---
    "MSP Kanalgerät 3.6 kW": {
        "artikelnr": "AM036DNMDKG/EU",
        "kategorie": "MSP Kanalgerät",
        "kuehl_kw": 3.6,
        "heiz_kw": 4.0,
        "schall_db": "30 / 27 / 24",
        "schallleistung_db": 53,
        "abmessungen": "850 × 250 × 700",
        "gewicht_kg": 27.0,
        "mca_a": 0.81,
    },
    "MSP Kanalgerät 5.6 kW": {
        "artikelnr": "AM056DNMDKG/EU",
        "kategorie": "MSP Kanalgerät",
        "kuehl_kw": 5.6,
        "heiz_kw": 6.3,
        "schall_db": "32 / 29 / 25",
        "schallleistung_db": 57,
        "abmessungen": "850 × 250 × 700",
        "gewicht_kg": 27.0,
        "mca_a": 1.08,
    },
    "MSP Kanalgerät 7.1 kW": {
        "artikelnr": "AM071DNMDKG/EU",
        "kategorie": "MSP Kanalgerät",
        "kuehl_kw": 7.1,
        "heiz_kw": 8.0,
        "schall_db": "36 / 32 / 27",
        "schallleistung_db": 60,
        "abmessungen": "850 × 250 × 700",
        "gewicht_kg": 27.0,
        "mca_a": 1.48,
    },
    "MSP Kanalgerät 9.0 kW": {
        "artikelnr": "AM090DNMDKG/EU",
        "kategorie": "MSP Kanalgerät",
        "kuehl_kw": 9.0,
        "heiz_kw": 10.0,
        "schall_db": "37 / 33 / 29",
        "schallleistung_db": 61,
        "abmessungen": "1200 × 250 × 700",
        "gewicht_kg": 34.2,
        "mca_a": 1.78,
    },
}

KASSETTEN_PANEELE = {
    "Paneel klein (960mm)":  {"artikelnr": "PC1MWFMANW", "abmessungen": "960 × 34 × 420",  "gewicht_kg": 2.6},
    "Paneel mittel (1198mm)": {"artikelnr": "PC1NWFMANW", "abmessungen": "1198 × 34 × 500", "gewicht_kg": 4.3},
    "Paneel groß (1410mm)":  {"artikelnr": "PC1BWFMANW", "abmessungen": "1410 × 34 × 500", "gewicht_kg": 5.0},
}

ZUBEHOER = {
    "Control Kit (Regeleinheit) – MIM-E03FN":       {"artikelnr": "MIM-E03FN"},
    "Kabelfernbedienung – MWR-WW10N":               {"artikelnr": "MWR-WW10N"},
}


# ============================================================
# HILFSFUNKTIONEN
# ============================================================
def get_font_as_base64(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def render_css(bg_color, text_main):
    font_b64 = get_font_as_base64("POE Vetica UI.ttf") or get_font_as_base64("POE_Vetica_UI.ttf")
    font_face = (
        f"@font-face {{ font-family: 'POE Helvetica UI'; "
        f"src: url(data:font/ttf;base64,{font_b64}) format('truetype'); }}"
        if font_b64 else ""
    )
    st.markdown(f"""
    <style>
    {font_face}
    html, body, [data-testid="stAppViewContainer"], * {{
        font-family: 'POE Helvetica UI', 'Segoe UI', sans-serif !important;
    }}
    .stApp {{ background-color: {bg_color}; }}
    * {{ color: {text_main} !important; }}

    .quint-title {{
        font-size: 48px !important;
        font-weight: bold !important;
        color: white !important;
        line-height: 1.1;
    }}
    .quint-sub {{
        font-size: 18px;
        color: {text_main} !important;
        margin-top: -6px;
    }}
    .section-header {{
        font-size: 22px;
        font-weight: bold;
        color: white !important;
        margin-top: 10px;
    }}
    .spec-box {{
        background-color: rgba(255,255,255,0.18);
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 6px;
        color: white !important;
    }}
    .spec-row {{
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        padding: 4px 0;
        color: white !important;
    }}
    .ok-badge {{
        background-color: #27ae60;
        color: white !important;
        font-weight: bold;
        border-radius: 6px;
        padding: 4px 14px;
        font-size: 15px;
    }}
    .warn-badge {{
        background-color: #e67e22;
        color: white !important;
        font-weight: bold;
        border-radius: 6px;
        padding: 4px 14px;
        font-size: 15px;
    }}
    .err-badge {{
        background-color: #c0392b;
        color: white !important;
        font-weight: bold;
        border-radius: 6px;
        padding: 4px 14px;
        font-size: 15px;
    }}

    input, .stNumberInput div[data-baseweb="input"],
    .stSelectbox div[data-baseweb="select"] {{
        background-color: white !important;
        color: {bg_color} !important;
        -webkit-text-fill-color: {bg_color} !important;
        font-weight: bold !important;
        border: 2px solid {text_main} !important;
        border-radius: 8px !important;
    }}
    div.stButton > button {{
        background-color: white !important;
        color: {text_main} !important;
        border: 2px solid {text_main} !important;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
    }}
    div.stButton > button:hover {{
        background-color: {text_main} !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def spec_box(items: dict, title: str = None):
    rows = ""
    for k, v in items.items():
        rows += f'<div class="spec-row"><span>{k}</span><strong>{v}</strong></div>'
    title_html = f'<div style="font-weight:bold; color:white; margin-bottom:6px;">{title}</div>' if title else ""
    st.markdown(f'<div class="spec-box">{title_html}{rows}</div>', unsafe_allow_html=True)


# ============================================================
# HAUPTFUNKTION
# ============================================================
def main():
    BG_COLOR   = "#36A9E1"
    TEXT_MAIN  = "#3C3C3B"
    LOGO_PATH  = "Coolsulting_Logo_ohneHG_outlines_weiß.png"
    VERSION    = "1.0.0"
    ZEIT       = datetime.now().strftime("%d.%m.%Y | %H:%M Uhr")

    render_css(BG_COLOR, TEXT_MAIN)

    # ---- HEADER ----
    col_logo, col_title = st.columns([1, 3])
    with col_logo:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
    with col_title:
        st.markdown(
            '<div class="quint-title">Samsung Quint</div>'
            '<div class="quint-sub">Systemkonfiguration &amp; Stückliste | '
            f'Version {VERSION} | {ZEIT}</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ============================================================
    # SESSION STATE INIT
    # ============================================================
    if "innengeraete_liste" not in st.session_state:
        st.session_state.innengeraete_liste = []   # list of dicts
    if "zubehoer_liste" not in st.session_state:
        st.session_state.zubehoer_liste = []

    # ============================================================
    # STEP 1 – PROJEKTDATEN
    # ============================================================
    st.markdown('<div class="section-header">① Projektdaten</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        projekt_name  = st.text_input("Projektname", placeholder="z.B. EFH Müller, Köln")
    with c2:
        ersteller     = st.text_input("Erstellt von", placeholder="z.B. Michael Schäpers")
    with c3:
        projekt_datum = st.date_input("Datum", value=datetime.now())

    st.markdown("---")

    # ============================================================
    # STEP 2 – AUßENGERÄT
    # ============================================================
    st.markdown('<div class="section-header">② Außengerät (ODU)</div>', unsafe_allow_html=True)

    col_odu, col_odu_spec = st.columns([1, 1])
    with col_odu:
        phase_filter = st.radio(
            "Netzanschluss", ["1-phasig (230V)", "3-phasig (400V)"],
            horizontal=True, key="phase_filter"
        )
        phase_key = "1-phasig" if "1-phasig" in phase_filter else "3-phasig"

        odu_gefiltert = {k: v for k, v in AUSSENGERAETE.items() if v["phase"] == phase_key}
        odu_wahl = st.selectbox("Außengerät auswählen", list(odu_gefiltert.keys()), key="odu_wahl")
        odu = AUSSENGERAETE[odu_wahl]

    with col_odu_spec:
        spec_box({
            "Artikelnummer":     odu["artikelnr"],
            "Kühlleistung":      f"{odu['kuehl_kw']} kW",
            "Heizleistung":      f"{odu['heiz_kw']} kW",
            "Schalldruck":       f"{odu['schall_db']} dB(A)  (Hi/Med)",
            "Schallleistung":    f"{odu['schallleistung_db']} dB(A)",
            "Abmessungen":       f"{odu['abmessungen']} mm",
            "Gewicht":           f"{odu['gewicht_kg']} kg",
            "Spannung / MCA":    f"{odu['spannung']} | {odu['mca_a']} A",
        }, title=odu_wahl)

    st.markdown("---")

    # ============================================================
    # STEP 3 – HYDRO UNIT
    # ============================================================
    st.markdown('<div class="section-header">③ Hydro Unit</div>', unsafe_allow_html=True)

    col_hu, col_hu_spec = st.columns([1, 1])
    with col_hu:
        hu_wahl = st.selectbox("Hydro Unit auswählen", list(HYDRO_UNITS.keys()), key="hu_wahl")
        hu = HYDRO_UNITS[hu_wahl]
        st.caption(hu["beschreibung"])

    with col_hu_spec:
        spec_box({
            "Artikelnummer":   hu["artikelnr"],
            "Zonen":           str(hu["zonen"]),
            "Schalldruck":     f"{hu['schall_db']} dB(A)",
            "Schallleistung":  f"{hu['schallleistung_db']} dB(A)",
            "Abmessungen":     f"{hu['abmessungen']} mm",
            "Gewicht":         f"{hu['gewicht_kg']} kg",
            "Spannung / MCA":  f"{hu['spannung']} | {hu['mca_a']} A",
        }, title=hu_wahl)

    st.markdown("---")

    # ============================================================
    # STEP 4 – INNENGERÄTE
    # ============================================================
    st.markdown('<div class="section-header">④ Innengeräte</div>', unsafe_allow_html=True)

    # Kategorie-Filter
    kategorien = sorted(set(v["kategorie"] for v in INNENGERAETE.values()))
    kat_filter = st.selectbox("Gerätetyp", kategorien, key="kat_filter")

    innen_gefiltert = {k: v for k, v in INNENGERAETE.items() if v["kategorie"] == kat_filter}

    col_ig, col_ig_menge, col_ig_zone, col_ig_add = st.columns([2, 1, 1, 1])
    with col_ig:
        ig_wahl = st.selectbox("Gerät", list(innen_gefiltert.keys()), key="ig_wahl")
    with col_ig_menge:
        ig_menge = st.number_input("Menge", 1, 20, 1, key="ig_menge")
    with col_ig_zone:
        ig_zone = st.number_input("Zone", 1, hu["zonen"], 1, key="ig_zone")
    with col_ig_add:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Hinzufügen", key="btn_add_ig"):
            ig_data = INNENGERAETE[ig_wahl]
            st.session_state.innengeraete_liste.append({
                "name":      ig_wahl,
                "artikelnr": ig_data["artikelnr"],
                "kategorie": ig_data["kategorie"],
                "kuehl_kw":  ig_data["kuehl_kw"],
                "heiz_kw":   ig_data["heiz_kw"],
                "gewicht_kg": ig_data["gewicht_kg"],
                "abmessungen": ig_data["abmessungen"],
                "schall_db": ig_data["schall_db"],
                "mca_a":     ig_data["mca_a"],
                "menge":     ig_menge,
                "zone":      int(ig_zone),
            })
            st.rerun()

    # Kassetten-Paneel Auswahl (nur bei Kassette)
    if "Kassette" in kat_filter:
        paneel_wahl = st.selectbox(
            "Paneel für 1-Weg Kassette (optional)",
            ["– keines –"] + list(KASSETTEN_PANEELE.keys()),
            key="paneel_wahl"
        )
    else:
        paneel_wahl = "– keines –"

    # Liste der hinzugefügten Innengeräte
    if st.session_state.innengeraete_liste:
        st.markdown("**Konfigurierte Innengeräte:**")
        for idx, ig in enumerate(st.session_state.innengeraete_liste):
            col_a, col_b, col_c, col_d = st.columns([3, 1, 1, 1])
            with col_a:
                st.markdown(
                    f'<span style="color:white;">{ig["menge"]}× {ig["name"]}</span>'
                    f'<span style="opacity:0.6; font-size:12px;"> &nbsp;[Zone {ig["zone"]}] &nbsp;{ig["artikelnr"]}</span>',
                    unsafe_allow_html=True
                )
            with col_b:
                st.markdown(
                    f'<span style="color:white; font-size:13px;">❄ {ig["kuehl_kw"]} kW</span>',
                    unsafe_allow_html=True
                )
            with col_c:
                st.markdown(
                    f'<span style="color:white; font-size:13px;">♨ {ig["heiz_kw"]} kW</span>',
                    unsafe_allow_html=True
                )
            with col_d:
                if st.button("🗑", key=f"del_ig_{idx}"):
                    st.session_state.innengeraete_liste.pop(idx)
                    st.rerun()

        if st.button("Alle Innengeräte zurücksetzen", key="reset_ig"):
            st.session_state.innengeraete_liste = []
            st.rerun()
    else:
        st.info("Noch keine Innengeräte hinzugefügt.")

    st.markdown("---")

    # ============================================================
    # STEP 5 – ZUBEHÖR
    # ============================================================
    st.markdown('<div class="section-header">⑤ Zubehör (optional)</div>', unsafe_allow_html=True)

    zub_wahl = st.multiselect(
        "Zubehör auswählen",
        list(ZUBEHOER.keys()),
        key="zub_wahl"
    )

    st.markdown("---")

    # ============================================================
    # SYSTEMCHECK & STÜCKLISTE
    # ============================================================
    st.markdown('<div class="section-header">⑥ Systemcheck &amp; Stückliste</div>', unsafe_allow_html=True)

    if not st.session_state.innengeraete_liste:
        st.warning("Bitte mindestens ein Innengerät hinzufügen (Schritt ④).")
        return

    # Leistungsberechnung
    total_kuehl = sum(ig["kuehl_kw"] * ig["menge"] for ig in st.session_state.innengeraete_liste)
    total_heiz  = sum(ig["heiz_kw"]  * ig["menge"] for ig in st.session_state.innengeraete_liste)
    odu_kuehl   = odu["kuehl_kw"]
    odu_heiz    = odu["heiz_kw"]

    ausn_kuehl  = total_kuehl / odu_kuehl * 100 if odu_kuehl > 0 else 0
    ausn_heiz   = total_heiz  / odu_heiz  * 100 if odu_heiz  > 0 else 0

    def ausn_badge(pct):
        if pct <= 100:
            return "ok-badge", f"✓ {pct:.0f}% – OK"
        elif pct <= 130:
            return "warn-badge", f"⚠ {pct:.0f}% – Grenzwertig"
        else:
            return "err-badge", f"✗ {pct:.0f}% – Überladen!"

    badge_k_cls, badge_k_txt = ausn_badge(ausn_kuehl)
    badge_h_cls, badge_h_txt = ausn_badge(ausn_heiz)

    ch1, ch2, ch3, ch4 = st.columns(4)
    with ch1:
        st.metric("Ø Kühlleistung (Innen)", f"{total_kuehl:.1f} kW")
    with ch2:
        st.metric("Ø Heizleistung (Innen)", f"{total_heiz:.1f} kW")
    with ch3:
        st.markdown(
            f'<br><span class="{badge_k_cls}">{badge_k_txt} Kühlen</span>',
            unsafe_allow_html=True
        )
    with ch4:
        st.markdown(
            f'<br><span class="{badge_h_cls}">{badge_h_txt} Heizen</span>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ---- STÜCKLISTE ----
    st.markdown("### Stückliste")

    stückliste = []

    # Außengerät
    stückliste.append({
        "Pos": len(stückliste) + 1,
        "Menge": 1,
        "Kategorie": "Außengerät",
        "Bezeichnung": odu_wahl,
        "Artikelnummer": odu["artikelnr"],
        "Kühl kW": odu["kuehl_kw"],
        "Heiz kW": odu["heiz_kw"],
        "Abmessungen mm": odu["abmessungen"],
        "Gewicht kg": odu["gewicht_kg"],
    })

    # Hydro Unit
    stückliste.append({
        "Pos": len(stückliste) + 1,
        "Menge": 1,
        "Kategorie": "Hydro Unit",
        "Bezeichnung": hu_wahl,
        "Artikelnummer": hu["artikelnr"],
        "Kühl kW": "–",
        "Heiz kW": "–",
        "Abmessungen mm": hu["abmessungen"],
        "Gewicht kg": hu["gewicht_kg"],
    })

    # Innengeräte
    for ig in st.session_state.innengeraete_liste:
        stückliste.append({
            "Pos": len(stückliste) + 1,
            "Menge": ig["menge"],
            "Kategorie": ig["kategorie"],
            "Bezeichnung": ig["name"] + f" (Zone {ig['zone']})",
            "Artikelnummer": ig["artikelnr"],
            "Kühl kW": ig["kuehl_kw"],
            "Heiz kW": ig["heiz_kw"],
            "Abmessungen mm": ig["abmessungen"],
            "Gewicht kg": ig["gewicht_kg"],
        })

    # Kassetten-Paneel
    if paneel_wahl != "– keines –" and any(
        "Kassette" in ig["kategorie"] for ig in st.session_state.innengeraete_liste
    ):
        pan = KASSETTEN_PANEELE[paneel_wahl]
        kassetten_menge = sum(
            ig["menge"] for ig in st.session_state.innengeraete_liste
            if "Kassette" in ig["kategorie"]
        )
        stückliste.append({
            "Pos": len(stückliste) + 1,
            "Menge": kassetten_menge,
            "Kategorie": "Zubehör",
            "Bezeichnung": paneel_wahl,
            "Artikelnummer": pan["artikelnr"],
            "Kühl kW": "–",
            "Heiz kW": "–",
            "Abmessungen mm": pan["abmessungen"],
            "Gewicht kg": pan["gewicht_kg"],
        })

    # Zubehör
    for z in zub_wahl:
        stückliste.append({
            "Pos": len(stückliste) + 1,
            "Menge": 1,
            "Kategorie": "Zubehör",
            "Bezeichnung": z.split(" – ")[0],
            "Artikelnummer": ZUBEHOER[z]["artikelnr"],
            "Kühl kW": "–",
            "Heiz kW": "–",
            "Abmessungen mm": "–",
            "Gewicht kg": "–",
        })

    # Anzeige
    import pandas as pd
    df = pd.DataFrame(stückliste)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ---- EXPORT ----
    st.markdown("---")
    st.markdown("### Export")

    def build_csv(df):
        header_info = (
            f"Samsung Quint – Stückliste\n"
            f"Projekt: {projekt_name or '–'}\n"
            f"Erstellt von: {ersteller or '–'}\n"
            f"Datum: {projekt_datum}\n\n"
        )
        return header_info + df.to_csv(index=False, sep=";", decimal=",")

    csv_data = build_csv(df)
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            label="📥 Stückliste als CSV herunterladen",
            data=csv_data.encode("utf-8-sig"),
            file_name=f"Samsung_Quint_{projekt_name or 'Projekt'}_{projekt_datum}.csv",
            mime="text/csv",
        )
    with col_exp2:
        zusammenfassung = (
            f"Samsung Quint – Systemkonfiguration\n"
            f"{'='*50}\n"
            f"Projekt:      {projekt_name or '–'}\n"
            f"Erstellt von: {ersteller or '–'}\n"
            f"Datum:        {projekt_datum}\n\n"
            f"AUSSENGERÄT:  {odu_wahl} ({odu['artikelnr']})\n"
            f"HYDRO UNIT:  {hu_wahl} ({hu['artikelnr']})\n\n"
            f"INNENGERÄTE:\n"
        )
        for ig in st.session_state.innengeraete_liste:
            zusammenfassung += f"  {ig['menge']}× {ig['name']} – Zone {ig['zone']} [{ig['artikelnr']}]\n"
        zusammenfassung += (
            f"\nLEISTUNGSBILANZ:\n"
            f"  Kühlen gesamt: {total_kuehl:.1f} kW / ODU {odu_kuehl} kW → {ausn_kuehl:.0f}%\n"
            f"  Heizen gesamt: {total_heiz:.1f} kW / ODU {odu_heiz} kW → {ausn_heiz:.0f}%\n"
        )
        st.download_button(
            label="📄 Zusammenfassung als TXT",
            data=zusammenfassung.encode("utf-8"),
            file_name=f"Samsung_Quint_{projekt_name or 'Projekt'}_{projekt_datum}.txt",
            mime="text/plain",
        )


if __name__ == "__main__":
    main()
