# ============================================================================
# DATEI: centralSTATION_PRO.py
# VERSION: 4.9.0
# STAND: 29.03.2026
# AUTOR: Michael Schäpers, coolsulting
# BESCHREIBUNG: °central_STATION_PRO - Optimierte Menüstruktur & Reihung
# ============================================================================

import streamlit as st
import os
import base64
from datetime import datetime
from PIL import Image

# ============================================================
# 1. SEITE KONFIGURIEREN
# ============================================================
icon_image = Image.open("Coolsulting_Logo_ohneHG_weiß_grau.png")
st.set_page_config(
    page_title="°central_STATION_PRO | coolsulting", 
    page_icon=icon_image,
    layout="wide",
    initial_sidebar_state="auto"
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
    Unterstützt auch Apps in Unterverzeichnissen (z.B. coolWIRE/coolWIRE_main.py).
    """
    import sys
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()

        # Unterdrückung der Page-Config in Unter-Apps (mehrzeilige Aufrufe)
        import re
        modified_code = re.sub(
            r'st\.set_page_config\s*\(.*?\)',
            'pass',
            code_content,
            flags=re.DOTALL
        )

        # Bei Apps in Unterverzeichnissen: Verzeichnis zu sys.path hinzufügen
        app_dir = os.path.dirname(os.path.abspath(file_path))
        original_dir = os.getcwd()
        path_added = False
        if app_dir != original_dir and app_dir not in sys.path:
            sys.path.insert(0, app_dir)
            path_added = True

        try:
            # Arbeitsverzeichnis temporär wechseln für relative Pfade
            os.chdir(app_dir)
            # Ausführung im globalen Namensraum
            exec(modified_code, globals())
        except (SystemExit, KeyboardInterrupt):
            raise
        except BaseException as e:
            # st.rerun() und st.stop() werfen spezielle Exceptions
            # die NICHT abgefangen werden dürfen
            err_name = type(e).__name__
            if "Rerun" in err_name or "Stop" in err_name or "Halt" in err_name:
                raise
            st.error(f"⚠️ Fehler beim Laden von {file_path}: {str(e)}")
        finally:
            os.chdir(original_dir)
            if path_added:
                sys.path.remove(app_dir)
    else:
        st.error(f"❌ Datei '{file_path}' wurde nicht gefunden.")

def main():
    # --- DESIGN VARIABLEN ---
    BG_COLOR = "#36A9E1"    # Coolsulting Blau
    TEXT_GRAY = "#3C3C3B"   # Dunkelgrau
    FONT_FILE = "POE Vetica UI.ttf"
    LOGO_PATH = "Coolsulting_Logo_ohneHG_outlines_weiß.png"

    VERSION = "5.1.0"
    ZEIT = datetime.now().strftime("%d.%m.%Y | %H:%M Uhr")

    # --- VERLAUF INITIALISIEREN ---
    if "verlauf_heute" not in st.session_state:
        st.session_state.verlauf_heute = []

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
    }}
    
    .white-part {{ color: white !important; }}
    .gray-part {{ color: {TEXT_GRAY} !important; }}
    
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

    /* === GLOBALER FIX: Arrow-Platzhalter in allen Expandern verstecken === */
    [data-testid="stExpander"] summary::before {{display: none !important;}}
    [data-testid="stExpander"] summary span[data-testid="stMarkdownContainer"] p::before {{content: none !important;}}
    [data-testid="stExpander"] [data-testid="stIcon"] {{display: none !important;}}
    details summary span.css-1ixbkrg {{display: none !important;}}
    .arrow_down, .arrowDown, [class*="arrow"] {{display: none !important;}}
    /* Expander-Text der mit .arrow beginnt – Punkt+Text entfernen */
    [data-testid="stExpander"] summary > span:first-child {{
        font-size: 0 !important;
    }}
    [data-testid="stExpander"] summary > span:first-child > * {{
        font-size: 1rem !important;
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
            <span class="white-part">°central_</span><span class="gray-part">STATION_PRO</span>
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
        "°coolMATCH (Samsung Kalkulator)": "coolMATCH_v7.py",
        "°coolQUINT (Samsung Quint Auslegung)": "Samsung_Quint.py",
        "°coolMATH PRO (6-Methoden Kühllast-Simulation)": "coolMATH_PRO.py",
        "°coolTEC (Kühllast Kühlräume)": "coolTEC.py",
        "°coolINDUTEC (Industrieelle Kühllastberechnung)": "coolINDUTEC.py",
        "°coolFLOW (Hydraulik)": "coolFLOW.py",
        "°coolRohr (Kältemittel-Rohrdimensionierung)": "coolRohr.py",
        "°Kältemittel-Füllmengenrechner": "Kältemittel_Füllmenge.py",
        "°coolPOOL (Pool-Temperierungs-Simulation)": "coolPOOL.py",
        "°coolNEIGHBOR (Schallimmissions-Prognose)": "coolNEIGHBOR.py",
        "°coolWIRE (Kabelplanungstool)": "coolWIRE/coolWIRE_main.py"
    }

    # Module die eine Sidebar verwenden
    SIDEBAR_APPS = {
        "°coolPOOL (Pool-Temperierungs-Simulation)",
        "°coolNEIGHBOR (Schallimmissions-Prognose)",
        "°coolTEC (Kühllast Kühlräume)",
        "°coolINDUTEC (Industrieelle Kühllastberechnung)",
        "°coolFLOW (Hydraulik)",
        "°Heizlast WP (Modul 1)",
        "°WP Quick-Kalkulator (Quickie)",
        "°coolWIRE (Kabelplanungstool)",
    }

    tool_wahl = st.selectbox("Anwendung auswählen und starten:", list(menu_options.keys()))

    # Sidebar automatisch öffnen wenn Modul eine Sidebar hat
    if tool_wahl in SIDEBAR_APPS:
        st.sidebar.markdown("### ⚙️ Eingaben")

    st.markdown("---")

    # --- INHALT LADEN ---
    selected_file = menu_options[tool_wahl]

    if tool_wahl == "°Übersicht":
        st.info("### System-Status: Bereit\nWählen Sie oben ein Modul aus, um die Berechnung zu starten.")
        st.write("Dies ist die zentrale Steuereinheit für alle Coolsulting-Berechnungsmodule.")

        # --- VERLAUF VON HEUTE ---
        st.markdown("---")
        st.markdown("### 📋 Verlauf von heute")
        datum_heute = datetime.now().strftime("%d.%m.%Y")
        eintraege = st.session_state.verlauf_heute
        if eintraege:
            st.caption(f"Gespeicherte Berechnungen am {datum_heute} ({len(eintraege)} Einträge):")
            for e in reversed(eintraege):
                if isinstance(e, dict):
                    st.markdown(
                        f"**{e['uhrzeit']}** &nbsp;|&nbsp; `{e['modul']}` &nbsp;|&nbsp; "
                        f"{e['bezeichnung']} &nbsp;→&nbsp; **{e['ergebnis']}**"
                    )
                else:
                    st.markdown(f"- {e}")
        else:
            st.caption(f"Noch keine Berechnungen am {datum_heute} gespeichert.")

    elif selected_file:
        run_app(selected_file)

if __name__ == '__main__':
    main()
