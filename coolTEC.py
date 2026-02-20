# ==============================================================================
# APP NAME: °coolTEC (Kühlraumlast & Auslegung)
# VERSION: 3.3 - POE Font Integration
# DATUM: 20.02.2026
# ==============================================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import tempfile
import os
import base64

# --- SICHERUNG FÜR DASHBOARD ---
try:
    st.set_page_config(page_title="°coolTEC", layout="wide", page_icon="❄️")
except:
    pass

# --- FARBEN ---
COLOR_BLUE = "#36A9E1"
COLOR_GRAY = "#3C3C3B"
COLOR_WHITE = "#FFFFFF"
CHART_ORANGE = "#FF8C00"
CHART_RED = "#FF0000"

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
    div[data-testid="stMetricDelta"] > div {{ color: white !important; justify-content: center !important; }}
    </style>
""", unsafe_allow_html=True)

# --- PDF KLASSE ---
class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        
        # Font laden
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
        self.cell(0, 10, f'{grad}coolTEC Berechnungs-Protokoll', 0, 1, 'L')
        self.set_draw_color(60, 60, 59)
        self.line(10, 25, 200, 25)
        self.ln(18)

# --- HEADER ---
st.markdown(f"""
    <div class='header-container'>
        <div class='title-box-left'><span class='cool-part'>°cool</span><span class='name-part'>TEC</span></div>
        <div class='version-tag-right'>Pro-Kalkulation | v3.3 | {datetime.now().strftime('%d.%m.%Y')}</div>
    </div>
""", unsafe_allow_html=True)

# --- INPUT BEREICH ---
with st.container():
    c_p1, c_p2, c_p3 = st.columns(3)
    kunde = c_p1.text_input("Kunde", "Musterkunde GmbH")
    raum_bez = c_p2.text_input("Raumbezeichnung", "Tiefkühllager 1")
    bearbeiter = c_p3.text_input("Bearbeiter", "M. Schäpers")
    
    st.markdown("<hr style='margin: 10px 0; opacity: 0.1;'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"<p style='color:{COLOR_BLUE}; font-weight:bold; border-bottom:2px solid {COLOR_BLUE};'>1. GEOMETRIE & DÄMMUNG</p>", unsafe_allow_html=True)
        l = st.number_input("Länge (m)", 1.0, 50.0, 4.0, step=0.1)
        b = st.number_input("Breite (m)", 1.0, 50.0, 3.0, step=0.1)
        h = st.number_input("Höhe (m)", 1.8, 10.0, 2.5, step=0.1)
        
        st.markdown(f"<p style='font-size:0.85em; color:gray; margin-top:-10px;'>Fläche: {l*b:.2f} m² | Volumen: {l*b*h:.2f} m³</p>", unsafe_allow_html=True)
        
        damm_mm = st.selectbox("Dämmstärke (mm)", [60, 80, 100, 120, 140, 160], index=2)
        u_val = round(0.022 / (damm_mm / 1000), 3)
        st.caption(f"U-Wert: {u_val} W/m²K")
        
    with c2:
        st.markdown(f"<p style='color:{COLOR_BLUE}; font-weight:bold; border-bottom:2px solid {COLOR_BLUE};'>2. TEMPERATUREN</p>", unsafe_allow_html=True)
        t_set = st.selectbox("Raum-Soll", ["+15°C Trockenlager", "+7°C Getränke", "+4°C Molkerei", "+2°C Fleisch", "-18°C TK-Standard", "-22°C TK-Lager", "-24°C Eiscreme"], index=4)
        t_raum = float(t_set.split("°C")[0].replace("+","").strip())
        t_umg = st.number_input("Umgebung (°C)", 10, 45, 25)
        t_decke = st.number_input("Decke/Dach (°C)", 10, 60, 30)
        t_boden = st.number_input("Boden (°C)", 5, 25, 12)

    with c3:
        st.markdown(f"<p style='color:{COLOR_BLUE}; font-weight:bold; border-bottom:2px solid {COLOR_BLUE};'>3. WARE & NUTZUNG</p>", unsafe_allow_html=True)
        laufzeit = st.selectbox("Laufzeit Aggregat (h/Tag)", [12, 14, 16, 18, 20, 22], index=3)
        ware_kg_m2 = st.number_input("Beschickung (kg/m²)", 0, 1000, 80)
        dt_ware = st.number_input("Abkühlung Ware (K)", 0, 50, 15)
        m_ware = ware_kg_m2 * (l * b)

# --- BERECHNUNG ---
a_decke, a_wand, is_tk = l * b, 2 * (l + b) * h, t_raum < 0
q_wand, q_decke = u_val * a_wand * (t_umg - t_raum), u_val * a_decke * (t_decke - t_raum)
u_bod = u_val if is_tk else 1.5
q_boden = u_bod * a_decke * (t_boden - t_raum)
q_trans = max(0, q_wand + q_decke + q_boden)
c_ware = 1.7 if is_tk else 3.2
q_ware_24h = (m_ware * c_ware * dt_ware * 1000) / (24 * 3600)
q_sum_24h = (q_trans + q_ware_24h) * 1.15
q_bedarf = q_sum_24h * (24 / laufzeit)

# --- ERGEBNISSE ---
st.divider()
res1, res2, res3 = st.columns(3)
res1.metric("KÄLTEBEDARF", f"{q_bedarf:.0f} W", f"{q_bedarf/1000:.2f} kW")
res2.metric("LAUFZEIT", f"{laufzeit} h/d", f"Raum: {raum_bez}")
res3.metric("ENERGIE / TAG", f"{(q_sum_24h*24)/1000:.1f} kWh", f"Ware: {m_ware:.0f} kg")

# --- DIAGRAMM ---
col_table, col_chart = st.columns([1.2, 1])
detail_df = pd.DataFrame({"Komponente": ["Wände", "Decke", "Boden", "Ware", "Zuschlag"], "Last": [q_wand, q_decke, q_boden, q_ware_24h, q_sum_24h * 0.15]})

with col_table:
    st.markdown(f"<p style='color:white; font-weight:bold;'>LASTVERTEILUNG (WATT Schnitt)</p>", unsafe_allow_html=True)
    st.table(detail_df.style.format({"Last": "{:.0f}"}))

with col_chart:
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor('none')
    colors = [CHART_ORANGE, '#5DADE2', '#AED6F1', CHART_RED, '#85929E']
    ax.pie(detail_df["Last"], labels=detail_df["Komponente"], autopct='%1.1f%%', startangle=140, colors=colors, textprops={'color':"white", 'weight':'bold'})
    ax.axis('equal')
    st.pyplot(fig)

# --- PDF EXPORT ---
if st.button("📄 PDF-Bericht generieren"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.savefig(tmpfile.name, format='png', bbox_inches='tight', transparent=True)
        chart_path = tmpfile.name

    pdf = PDFReport()
    pdf.add_page()
    pdf._set_font('B', 12)
    pdf.cell(0, 10, 'Projektdaten:', 0, 1)
    pdf._set_font('', 11)
    pdf.cell(0, 8, f'Kunde: {kunde}', 0, 1)
    pdf.cell(0, 8, f'Raum: {raum_bez} | Flaeche: {l*b:.2f} m2 | Volumen: {l*b*h:.2f} m3', 0, 1)
    pdf.cell(0, 8, f'Bearbeiter: {bearbeiter} | Datum: {datetime.now().strftime("%d.%m.%Y")}', 0, 1)
    pdf.ln(5)
    pdf._set_font('B', 12)
    pdf.cell(0, 10, 'Berechnungsergebnisse:', 0, 1)
    pdf._set_font('', 11)
    pdf.cell(90, 8, f'Erforderliche Kaelteleistung:', 0, 0)
    pdf.cell(0, 8, f'{q_bedarf:.0f} W', 0, 1)
    pdf.cell(90, 8, f'Maschinenlaufzeit:', 0, 0)
    pdf.cell(0, 8, f'{laufzeit} h/Tag', 0, 1)
    pdf.cell(90, 8, f'Energiebedarf pro 24h:', 0, 0)
    pdf.cell(0, 8, f'{(q_sum_24h*24)/1000:.1f} kWh', 0, 1)
    pdf.ln(10)
    pdf.image(chart_path, x=60, y=105, w=90)
    
    pdf_path = tempfile.mktemp(".pdf")
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        st.download_button(label="💾 PDF herunterladen", data=f, file_name=f"Coolsulting_{raum_bez}.pdf", mime="application/pdf")
    os.remove(chart_path)
