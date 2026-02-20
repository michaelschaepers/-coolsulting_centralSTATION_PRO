# ==========================================
# DATEI: Kältemittel_Füllmenge.py
# VERSION: 4.2 - POE Font Integration
# DATUM: 20.02.2026
# ==========================================

import streamlit as st
import os
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from fpdf import FPDF
import base64

APP_VERSION = "4.2"
HEUTIGES_DATUM = datetime.now().strftime("%d.%m.%Y")

# --- FONT LADEN ---
def get_font_base64(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- PDF KLASSE ---
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        
        font_path = "POE_Vetica_UI.ttf"
        if os.path.exists(font_path):
            self.add_font('POE', '', font_path, uni=True)
            self.add_font('POE', 'B', font_path, uni=True)
            self.font_loaded = True
        else:
            self.font_loaded = False
    
    def _set_font(self, style='', size=10):
        if self.font_loaded:
            self.set_font('POE', style, size)
        else:
            self.set_font("Helvetica", style, size)
    
    def header(self):
        self.set_fill_color(54, 169, 225)
        self.rect(0, 0, 210, 40, 'F') 
        self.set_y(12)
        self.set_x(10)
        self.set_text_color(255, 255, 255)
        self._set_font('B', 18)
        self.cell(0, 10, 'Fuellmengen Check', 0, 1, 'L')
        self._set_font('', 10)
        self.cell(0, 5, 'Max. Fuellmenge nach OENORM EN 378', 0, 1, 'L')

    def footer(self):
        self.set_y(-15)
        self._set_font('I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, "Haftungsausschluss: Nur zur technischen Orientierung.", 0, 0, 'C')

# --- BERECHNUNGSLOGIK ---
def berechne_fuellmenge(gas, flaeche, hoehe, einbau):
    v_raum = flaeche * hoehe
    daten = {"R32": {"atel": 0.300, "lfl": 0.307}, "R410A": {"atel": 0.420, "lfl": 0.442}}
    
    m_tox = daten[gas]["atel"] * v_raum
    
    h0_dict = {"Deckeneinbau": 2.2, "Wandmontage": 1.8, "Bodenaufstellung": 0.6}
    h0 = h0_dict[einbau]
    
    if gas == "R32":
        m_burn = 2.5 * (daten[gas]["lfl"]**1.25) * h0 * np.sqrt(flaeche)
        m_burn = max(m_burn, 1.8)
    else:
        m_burn = 999.0
        
    m_max = min(m_tox, m_burn)
    grund = "Toxizitaet" if m_tox < m_burn else "Brennbarkeit"
    return m_max, v_raum, grund

# --- MAIN APP ---
def main():
    BG_COLOR = "#36A9E1"
    TEXT_GRAU = "#3C3C3B"
    HINWEIS_GRUEN = "rgba(46, 204, 113, 0.2)"

    st.set_page_config(page_title="Füllmengen Check", layout="wide")
    
    font_b64 = get_font_base64("POE_Vetica_UI.ttf")

    # CSS
    st.markdown(f"""
        <style>
        {f"@font-face {{ font-family: 'POE Helvetica UI'; src: url(data:font/ttf;base64,{font_b64}) format('truetype'); }}" if font_b64 else ""}
        
        .stApp {{ background-color: {BG_COLOR}; }}
        * {{ color: {TEXT_GRAU} !important; font-family: 'POE Helvetica UI', 'Segoe UI', sans-serif !important; }}
        
        [data-testid="stHeader"] {{ display: none !important; }}
        .block-container {{ padding-top: 1.5rem !important; }}
        
        .main-title {{ font-size: 45px !important; font-weight: bold; margin-bottom: 0px; margin-top: -20px; }}
        .sub-title {{ font-size: 18px; color: white !important; font-weight: normal !important; margin-top: -5px; }}
        .version-tag {{ font-size: 11px; color: white !important; opacity: 0.7; }}

        .card {{ background-color: rgba(255,255,255,0.95); border-radius: 12px; padding: 25px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }}
        .hinweis-box {{ background-color: {HINWEIS_GRUEN}; padding: 20px; border-radius: 10px; border: 1px solid rgba(60,60,59,0.2); font-size: 14px; line-height: 1.6; }}
        
        input, .stNumberInput div[data-baseweb="input"], .stSelectbox div[data-baseweb="select"], .stTextInput div[data-baseweb="input"] {{
            background-color: white !important; color: #36A9E1 !important; font-weight: bold !important; border: 2px solid {TEXT_GRAU} !important; border-radius: 8px !important;
        }}
        div.stButton > button {{ background-color: white !important; color: {TEXT_GRAU} !important; border: 2px solid {TEXT_GRAU} !important; font-weight: bold; border-radius: 10px; height: 3.5em; width: 100%; }}
        
        hr {{ display: none !important; }}
        </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown(f'<p class="main-title">Füllmengen Check</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-title">Max. Füllmenge nach ÖNORM EN 378</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="version-tag">Version {APP_VERSION} | Stand: {HEUTIGES_DATUM}</p>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 30px;"></div>', unsafe_allow_html=True)

    # CONTENT
    col_main, col_info = st.columns([1.3, 0.7])
    with col_main:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📋 Parameter")
        r1_1, r1_2, r1_3 = st.columns(3)
        with r1_1: kunde = st.text_input("Kunde / Projekt")
        with r1_2: raum = st.text_input("Raum")
        with r1_3: bearbeiter = st.text_input("Bearbeiter")
        
        st.markdown('<div style="border-top: 1px solid #3C3C3B; opacity:0.1; margin:15px 0;"></div>', unsafe_allow_html=True)
        
        r2_1, r2_2 = st.columns(2)
        with r2_1: gas = st.selectbox("Kältemittel", ["R32", "R410A"])
        with r2_2: einbau = st.selectbox("Einbausituation", ["Deckeneinbau", "Wandmontage", "Bodenaufstellung"], index=1)
        r3_1, r3_2 = st.columns(2)
        with r3_1: flaeche = st.number_input("Fläche (m²)", 1.0, 500.0, 25.0)
        with r3_2: hoehe = st.number_input("Höhe (m)", 1.5, 10.0, 2.5)
        calc_btn = st.button("BERECHNUNG STARTEN")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        st.markdown(f'''
            <div class="hinweis-box">
                <b>Berechnung nach ÖNORM EN 378:</b><br><br>
                • Toxizitätsklasse: A | Brennbarkeitsklasse: 2L<br>
                • Innengerät in allgemeinem Zugangsbereich (a) montiert.<br>
                • Außengerät: Klasse II (Verdichter im Freien)<br><br>
                Diese Füllmengen sind Maximalwerte ohne weitere Sicherheitsmaßnahmen. Größere Mengen erfordern Detektoren, Alarme oder Lüftung.<br><br>
                Bis zu einer Füllmenge von 1,8kg R32 sind grundsätzlich keine Sicherheitsmaßnahmen erforderlich.
            </div>
        ''', unsafe_allow_html=True)

    if calc_btn:
        m_max, v_raum, grund = berechne_fuellmenge(gas, flaeche, hoehe, einbau)
        st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
        
        res_l, res_r = st.columns([1, 1])
        with res_l:
            st.markdown(f"""
            <div class="card" style="border-left: 15px solid {TEXT_GRAU};">
                <h2 style="color:{TEXT_GRAU} !important;">Ergebnis</h2>
                <p style="font-size:20px; margin:0;">Zulässige Menge:</p>
                <p style="font-size:75px; font-weight:bold; color:#36A9E1 !important; margin:0;">{m_max:.3f} kg</p>
                <p style="opacity:0.8;">Begrenzung: <b>{grund}</b></p>
            </div>
            """, unsafe_allow_html=True)
        with res_r:
            st.markdown('<div class="card" style="background-color: white; text-align: center;">', unsafe_allow_html=True)
            max_g = max(m_max * 1.5, 3.5)
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = m_max,
                number = {'suffix': " kg", 'font': {'size': 45, 'color': TEXT_GRAU}},
                gauge = {
                    'axis': {'range': [0, max_g]},
                    'bar': {'color': TEXT_GRAU},
                    'steps': [
                        {'range': [0, m_max*0.85], 'color': "#2ecc71"},
                        {'range': [m_max*0.85, m_max], 'color': "#f1c40f"},
                        {'range': [m_max, 20], 'color': "#e74c3c"}
                    ],
                    'bgcolor': "white",
                }
            ))
            fig.update_layout(height=300, margin=dict(t=20, b=20), paper_bgcolor='white')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # PDF REPORT
        pdf = PDF()
        pdf.add_page()
        pdf._set_font("B", 14)
        pdf.cell(0, 10, f"Projekt: {kunde}", 0, 1)
        pdf._set_font("", 12)
        pdf.cell(0, 8, f"Raum: {raum} | Bearbeiter: {bearbeiter}", 0, 1)
        pdf.ln(5)
        pdf.set_fill_color(240, 240, 240)
        pdf.set_text_color(54, 169, 225)
        pdf._set_font("B", 16)
        pdf.cell(0, 15, f"ERGEBNIS: {m_max:.3f} kg", 0, 1, 'C', fill=True)
        
        pdf_name = f"Fuellmengen_{kunde.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        st.download_button("📄 PDF BERICHT SPEICHERN", data=bytes(pdf.output()), file_name=pdf_name)

if __name__ == '__main__':
    main()
