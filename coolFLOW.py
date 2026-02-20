# ==============================================================================
# APP NAME: °coolFLOW (Hydraulik & Rohrnetz)
# VERSION: 2.5 - POE Font Integration
# DATUM: 20.02.2026
# ==============================================================================

import streamlit as st
import math
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import tempfile
import os
import base64

# --- SICHERUNG FÜR DASHBOARD ---
try:
    st.set_page_config(page_title="°coolFLOW", layout="wide", page_icon="💧")
except:
    pass

# --- FARBEN ---
COLOR_BLUE = "#36A9E1"
COLOR_GRAY = "#3C3C3B"
COLOR_WHITE = "#FFFFFF"

# --- FONT LADEN ---
def get_font_base64(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

font_b64 = get_font_base64("POE_Vetica_UI.ttf")

# --- CSS STYLING ---
st.markdown(f"""
    <style>
    {f"@font-face {{ font-family: 'POE Helvetica UI'; src: url(data:font/ttf;base64,{font_b64}) format('truetype'); }}" if font_b64 else ""}
    
    * {{
        font-family: 'POE Helvetica UI', 'Helvetica', sans-serif !important;
    }}
    
    .stApp {{ background-color: {COLOR_BLUE}; }}
    .header-container {{ display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; }}
    .title-box-left {{ text-align: left; font-family: 'POE Helvetica UI', sans-serif; font-weight: bold; font-size: 52px; line-height: 1.0; }}
    .version-tag-right {{ text-align: right; color: rgba(255,255,255,0.8); font-size: 16px; padding-bottom: 5px; }}
    .cool-part {{ color: {COLOR_WHITE}; }}
    .name-part {{ color: {COLOR_GRAY}; text-transform: uppercase; }}
    div[data-testid="stVerticalBlock"] > div[style*="background-color"] {{ background-color: white; padding: 25px; border-radius: 12px; }}
    div[data-testid="stMetric"] {{ background-color: {COLOR_GRAY} !important; border-radius: 10px; padding: 20px !important; text-align: center !important; }}
    div[data-testid="stMetricLabel"] > div {{ color: white !important; font-weight: bold !important; justify-content: center !important; text-align: center !important; width: 100%; }}
    div[data-testid="stMetricValue"] > div {{ color: white !important; font-size: 34px !important; text-align: center !important; width: 100%; }}
    
    .styled-table {{ width: 100%; color: white; border-collapse: collapse; margin-top: 10px; }}
    .styled-table th {{ background-color: {COLOR_GRAY}; text-align: left; padding: 8px; border-bottom: 2px solid {COLOR_BLUE}; }}
    .styled-table td {{ padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2); }}
    .selected-row {{ background-color: rgba(255, 255, 255, 0.15); font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# --- PDF KLASSE ---
class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        
        font_path = "POE_Vetica_UI.ttf"
        if os.path.exists(font_path):
            self.add_font('POE', '', font_path, uni=True)
            self.add_font('POE', 'B', font_path, uni=True)
            self.add_font('POE', 'I', font_path, uni=True)
            self.font_loaded = True
        else:
            self.font_loaded = False
    
    def _set_font(self, style='', size=10):
        if self.font_loaded:
            self.set_font('POE', style, size)
        else:
            self.set_font('Arial', style, size)
    
    def header(self):
        logo_path = "Coolsulting_Logo_ohneHG_weiss_grau.png"
        if os.path.exists(logo_path):
            try:
                self.image(logo_path, 155, 10, 45)
            except:
                pass
        self._set_font('B', 16)
        self.set_text_color(54, 169, 225)
        grad = chr(176)
        self.cell(0, 10, f'{grad}coolFLOW Hydraulik-Protokoll', 0, 1, 'L')
        self.set_draw_color(60, 60, 59)
        self.line(10, 25, 200, 25)
        self.ln(18)

# --- HEADER ---
st.markdown(f"""
    <div class='header-container'>
        <div class='title-box-left'><span class='cool-part'>°cool</span><span class='name-part'>FLOW</span></div>
        <div class='version-tag-right'>Hydraulik-Kalkulation | v2.5 | {datetime.now().strftime('%d.%m.%Y')}</div>
    </div>
""", unsafe_allow_html=True)

# --- INPUT BEREICH ---
with st.container():
    c_p1, c_p2, c_p3 = st.columns(3)
    kunde = c_p1.text_input("Kunde", "Musterkunde GmbH")
    projekt = c_p2.text_input("Projekt / Strang", "Hauptleitung Kälte")
    bearbeiter = c_p3.text_input("Bearbeiter", "M. Schäpers")
    
    st.markdown("<hr style='margin: 10px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"<p style='color:{COLOR_BLUE}; font-weight:bold; border-bottom:2px solid {COLOR_BLUE};'>1. LEISTUNGSDATEN</p>", unsafe_allow_html=True)
        q_kw = st.number_input("Kälteleistung (kW)", 1.0, 5000.0, 50.0, step=1.0)
        dt = st.number_input("Spreizung ΔT (K)", 1.0, 30.0, 6.0, step=0.5)
        
    with c2:
        st.markdown(f"<p style='color:{COLOR_BLUE}; font-weight:bold; border-bottom:2px solid {COLOR_BLUE};'>2. MEDIUM</p>", unsafe_allow_html=True)
        fluids = {"Wasser (100%)": [4.19, 999], "Ethylenglykol 34%": [3.65, 1050], "Propylenglykol 35%": [3.80, 1040]}
        fluid_sel = st.selectbox("Kälteträger", list(fluids.keys()))
        cp, rho = fluids[fluid_sel]
        
    with c3:
        st.markdown(f"<p style='color:{COLOR_BLUE}; font-weight:bold; border-bottom:2px solid {COLOR_BLUE};'>3. ROHRLEITUNG</p>", unsafe_allow_html=True)
        pipe_data = [
            ("DN 20", 21.6), ("DN 25", 27.3), ("DN 32", 36.0), ("DN 40", 41.9), 
            ("DN 50", 53.1), ("DN 65", 68.9), ("DN 80", 80.9), ("DN 100", 105.3), ("DN 125", 130.8)
        ]
        pipe_names = [p[0] for p in pipe_data]
        dn_sel_idx = st.selectbox("Nennweite (DN)", range(len(pipe_names)), format_func=lambda x: pipe_names[x], index=3)
        di = pipe_data[dn_sel_idx][1]

# --- BERECHNUNG ---
m_dot_s = q_kw / (cp * dt)
m_dot_h = m_dot_s * 3600
v_dot = (m_dot_s / rho) * 3600

def calc_vel(d_inner_mm, flow_m3h):
    return (flow_m3h / 3600) / (math.pi * (d_inner_mm/1000/2)**2)

velocity = calc_vel(di, v_dot)

# --- ERGEBNISSE ---
st.divider()
res1, res2, res3 = st.columns(3)
res1.metric("VOLUMENSTROM", f"{v_dot:.2f} m³/h", f"{q_kw:.1f} kW Leistung")
res2.metric("GESCHWINDIGKEIT", f"{velocity:.2f} m/s", f"{pipe_data[dn_sel_idx][0]}")
res3.metric("MASSENSTROM", f"{m_dot_h:.0f} kg/h", f"{m_dot_s:.2f} kg/s")

# --- VERGLEICHSTABELLE ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<p style='color:white; font-weight:bold;'>DIMENSIONIERUNGS-VERGLEICH</p>", unsafe_allow_html=True)

indices = [dn_sel_idx + 1, dn_sel_idx, dn_sel_idx - 1]
comparison_rows = []
for idx in indices:
    if 0 <= idx < len(pipe_data):
        name, d_inner = pipe_data[idx]
        v = calc_vel(d_inner, v_dot)
        status = "✅ OK" if 0.5 <= v <= 1.5 else "⚠️ Hoch" if v > 1.5 else "💧 Niedrig"
        style = "selected-row" if idx == dn_sel_idx else ""
        comparison_rows.append(f"<tr class='{style}'><td>{name}</td><td>{d_inner} mm</td><td>{v:.2f} m/s</td><td>{status}</td></tr>")

st.markdown(f"<table class='styled-table'><thead><tr><th>Nennweite</th><th>Innen-Ø</th><th>v [m/s]</th><th>Status</th></tr></thead><tbody>{''.join(comparison_rows)}</tbody></table>", unsafe_allow_html=True)

# --- PDF EXPORT ---
if st.button("📄 PDF-Bericht generieren"):
    pdf = PDFReport()
    pdf.add_page()
    pdf._set_font('B', 12)
    pdf.cell(0, 10, 'Projektdaten:', 0, 1)
    pdf._set_font('', 11)
    pdf.cell(0, 8, f'Kunde: {kunde} | Projekt: {projekt} | Bearbeiter: {bearbeiter}', 0, 1)
    pdf.cell(0, 8, f'Kaeltetraeger: {fluid_sel} | Dichte: {rho} kg/m3', 0, 1)
    pdf.ln(5)
    
    pdf._set_font('B', 12)
    pdf.cell(0, 10, 'Berechnungsergebnisse:', 0, 1)
    pdf._set_font('', 11)
    pdf.cell(90, 8, f'Uebertragene Kaelteleistung:', 0, 0)
    pdf.cell(0, 8, f'{q_kw:.1f} kW', 0, 1)
    pdf.cell(90, 8, f'Spreizung (Delta T):', 0, 0)
    pdf.cell(0, 8, f'{dt} K', 0, 1)
    pdf.cell(90, 8, f'Massenstrom:', 0, 0)
    pdf.cell(0, 8, f'{m_dot_h:.0f} kg/h ({m_dot_s:.2f} kg/s)', 0, 1)
    pdf.cell(90, 8, f'Volumenstrom:', 0, 0)
    pdf.cell(0, 8, f'{v_dot:.2f} m3/h', 0, 1)
    pdf.cell(90, 8, f'Gewaehlte Dimension:', 0, 0)
    pdf.cell(0, 8, f'{pipe_data[dn_sel_idx][0]} ({di} mm)', 0, 1)
    pdf.cell(90, 8, f'Fliessgeschwindigkeit:', 0, 0)
    pdf.cell(0, 8, f'{velocity:.2f} m/s', 0, 1)
    
    pdf_path = tempfile.mktemp(".pdf")
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button(label="💾 PDF herunterladen", data=f, file_name=f"Coolsulting_Flow_{projekt}.pdf", mime="application/pdf")
