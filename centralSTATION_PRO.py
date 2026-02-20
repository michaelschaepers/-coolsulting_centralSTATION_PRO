# ============================================================================
# DATEI: centralSTATION_PRO.py
# VERSION: 4.8.0
# STAND: 20.02.2026
# AUTOR: Michael Schäpers, coolsulting
# BESCHREIBUNG: °central_STATION_PRO - Dashboard für Berechnungsmodule
# ÄNDERUNGEN v4.8.0:
#  
# ============================================================================

import streamlit as st
import os
import base64
from datetime import datetime

# ============================================================
# 1. SEITE KONFIGURIEREN
# ============================================================
st.set_page_config(
    page_title="°central_STATION_PRO | coolsulting", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_font_as_base64(font_path):
    """Konvertiert eine lokale Schriftart in Base64 für CSS-Injektion."""
    if os.path.exists(font_path):
        with open(font_path, "rb") as font_file:
            return base64.b64encode(font_file.read()).decode()
    return None

def run_app(file_path):
    """
    Liest eine externe .py Datei ein, entfernt Seitenkonfigurationen 
    und führt den Code im aktuellen Kontext aus.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
        
        # Unterdrückung der Page-Config in Unter-Apps
        modified_code = code_content.replace("st.set_page_config", "pass #")
        
        try:
            # Ausführung im globalen Namensraum
            exec(modified_code, globals())
        except Exception as e:
            st.error(f"⚠️ Fehler beim Laden von {file_path}: {str(e)}")
    else:
        st.error(f"❌ Datei '{file_path}' wurde nicht gefunden.")

def main():
    # --- DESIGN VARIABLEN ---
    BG_COLOR = "#36A9E1"    # Coolsulting Blau
    TEXT_GRAY = "#3C3C3B"   # Dunkelgrau
    FONT_FILE = "POE_Vetica_UI.ttf"
    LOGO_PATH = "Coolsulting_Logo_ohneHG_outlines_weiß.png"
    
    VERSION = "4.8.0"
    ZEIT = datetime.now().strftime("%d.%m.%Y | %H:%M Uhr")

    # --- CSS STYLING ---
    font_base64 = get_font_as_base64(FONT_FILE)
    st.markdown(f"""
    <style>
    {f"@font-face {{ font-family: 'POE Helvetica UI'; src: url(data:font/ttf;base64,{font_base64}) format('truetype'); }}" if font_base64 else ""}
    
    html, body, [data-testid="stAppViewContainer"], * {{
        font-family: 'POE Helvetica UI', sans-serif !important;
    }}
    
    .stApp {{ background-color: {BG_COLOR}; }}
    
    .cs-welcome {{ 
        font-size: 30px !important;
        text-align: center;
        color: {TEXT_GRAY} !important;
        margin-top: -40px !important;
    }}
    
    .cs-title-line {{ 
        font-size: 48px !important;
        font-weight: bold !important;
        text-align: center;
        margin-top: -30px !important;
        background: none !important;
        background-color: transparent !important;
    }}
    
    .cs-title-line span {{
        background: none !important;
        background-color: transparent !important;
    }}
    
    .cs-title-line .white-part {{ 
        color: white !important; 
        background: none !important;
    }}
    
    .cs-title-line .gray-part {{ 
        color: {TEXT_GRAY} !important;
        background: none !important;
    }}
    
    hr {{ border: 1px solid {TEXT_GRAY} !important; opacity: 0.2 !important; margin: 20px 0 !important; }}
    
    div[data-baseweb="select"] {{ 
        background-color: white !important; 
        border-radius: 10px !important; 
        border: 2px solid {TEXT_GRAY} !important; 
    }}
    div[data-baseweb="select"] div {{ 
        color: {BG_COLOR} !important; 
        font-weight: bold !important; 
    }}
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown('<p class="cs-welcome">Willkommen im Cockpit der</p>', unsafe_allow_html=True)

    _, col_m, _ = st.columns([1, 1.2, 1])
    with col_m:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
    
    st.markdown(f"""
        <div class="cs-title-line">
            <span class="white-part">°central</span><span class="gray-part">STATION_PRO</span>
            <div style="font-size: 14px; font-weight: normal; color: {TEXT_GRAY}; opacity: 0.8; margin-top: 10px;">
                Version {VERSION} | Autor: Michael Schäpers | {ZEIT}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- NAVIGATION ---
    menu_options = {
        "°Übersicht": None,
        "°Heizlast WP (Modul 1)": "Waermepumpen_Auslegung.py",
        "°WP Quick-Kalkulator (Quickie)": "WP_Quick_Kalkulator.py",
        "°coolTEC (Kühllast Kühlräume)": "coolTEC.py",
        "°coolINDUTEC (Industrielle Kühllastberechnung)": "coolINDUTEC.py",
        "°coolFLOW (Hydraulik)": "coolFLOW.py",
        "°Kältemittel-Füllmengenrechner": "Kältemittel_Füllmenge.py"
    }

    tool_wahl = st.selectbox("Anwendung auswählen und starten:", list(menu_options.keys()))
    st.markdown("---")

    # --- INHALT LADEN ---
    selected_file = menu_options[tool_wahl]

    if tool_wahl == "°Übersicht":
        st.info("### System-Status: Bereit\nWählen Sie oben ein Modul aus, um die Berechnung zu starten.")
        st.write("Dies ist die zentrale Steuereinheit für alle Coolsulting-Berechnungsmodule.")
    elif selected_file:
        run_app(selected_file)

if __name__ == '__main__':
    main()
