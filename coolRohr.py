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
    components.html(html_content, height=1600, scrolling=True)
else:
    st.error(f"❌ Datei 'coolRohr.html' nicht gefunden. Bitte sicherstellen, dass die Datei im selben Verzeichnis liegt.")
