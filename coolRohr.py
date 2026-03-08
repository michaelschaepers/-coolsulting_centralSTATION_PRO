# ==============================================================================
# APP NAME: °coolRohr (CU-Rohrdimensionierung · Kältemittelleitungen)
# VERSION: 1.0
# DATUM: 08.03.2026
# AUTOR: Michael Schäpers, coolsulting
# BESCHREIBUNG: Dimensionierung von Kältemittelleitungen (Saug-, Druck-,
#               Flüssigkeitsleitung) inkl. Double Suction Riser & Teillast
#               Stoffdaten via REFPROP-Lookup-Tabellen (v6.3)
# ==============================================================================

import streamlit as st
import streamlit.components.v1 as components
import os
import base64

# --- SICHERUNG FÜR DASHBOARD ---
try:
    st.set_page_config(page_title="°coolRohr", layout="wide", page_icon="🔧")
except:
    pass

# --- HTML LADEN UND ANZEIGEN ---
# Robuste Pfadauflösung: funktioniert standalone und via exec() in centralSTATION_PRO
_script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
html_path = os.path.join(_script_dir, "coolRohr.html")

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    # Base64-encode logo and inject into HTML
    logo_path = os.path.join(_script_dir, "Coolsulting_Logo_ohneHG_blau.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_f:
            logo_b64 = base64.b64encode(img_f.read()).decode("utf-8")
        html_content = html_content.replace("__LOGO__", logo_b64)
    else:
        html_content = html_content.replace("__LOGO__", "")
    components.html(html_content, height=1600, scrolling=True)
else:
    st.error(f"❌ Datei 'coolRohr.html' nicht gefunden. Bitte sicherstellen, dass die Datei im selben Verzeichnis liegt.")
