# ==========================================
# DATEI: coolINDUTEC.py
# VERSION: 4.1 - FIXED Infiltration + fpdf2 Kompatibilität
# DATUM: 20.02.2026
# AUTOR: Michael Schäpers, coolsulting
# ==========================================

import streamlit as st
import os
import plotly.graph_objects as go
from fpdf import FPDF
import numpy as np
import tempfile
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- 1. SETUP & CSS ---
st.set_page_config(page_title="°coolINDUTEC PRO", layout="wide")

# Font laden
import base64
def get_font_base64(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

font_b64 = get_font_base64("POE_Vetica_UI.ttf")

st.markdown(f"""
    <style>
    {f"@font-face {{ font-family: 'POE Helvetica UI'; src: url(data:font/ttf;base64,{font_b64}) format('truetype'); }}" if font_b64 else ""}
    
    * {{
        font-family: 'POE Helvetica UI', 'Helvetica', sans-serif !important;
    }}
    
    .title-box {{ 
        font-size: 42px; 
        font-weight: bold; 
        margin-bottom: 20px; 
        padding-top: 10px;
    }}
    .blue-t {{ color: #36A9E1; }}
    .gray-t {{ color: #3C3C3B; }}
    .stNumberInput input {{ background-color: white !important; }}
    .stSelectbox div[data-baseweb="select"] > div {{ background-color: white !important; }}
    </style>
    <div class="title-box">
        <span class="blue-t">°cool</span><span class="gray-t">INDUTEC</span>
    </div>
""", unsafe_allow_html=True)

# --- 2. PHYSIK-KERN ---
ENTHALPIE_STUETZ_X = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]
ENTHALPIE_STUETZ_Y = [28, 38, 49, 62, 86, 304, 321, 339, 357, 374, 392]

def get_h_ware(temp):
    return float(np.interp(temp, ENTHALPIE_STUETZ_X, ENTHALPIE_STUETZ_Y))

# --- 3. DIAGRAMME ---
def create_pie_chart_mpl_detailed(labels, sizes, units="kWh"):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#36A9E1', '#FF4B4B', '#3C3C3B', '#FFCC00', '#A0A0A0'] 
    
    wedges, texts, autotexts = ax.pie(
        sizes, autopct='%1.1f%%', startangle=90, colors=colors, 
        pctdistance=0.85, explode=[0.05] * len(sizes)
    )
    
    plt.setp(autotexts, size=10, weight="bold", color="white")
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    legend_labels = [f"{l}: {s:.1f} {units}" for l, s in zip(labels, sizes)]
    ax.legend(wedges, legend_labels, title="Lastaufteilung",
              loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), frameon=False)
    
    ax.axis('equal')
    plt.tight_layout()
    
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(tmp.name, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return tmp.name

def create_cooling_curve_mpl(t_start, t_target, duration_h):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(0, duration_h, 100)
    y = []
    freezing_point = -2.0
    
    if t_start <= freezing_point: 
        for t in x:
            k = 3.0 / duration_h
            temp = t_target + (t_start - t_target) * np.exp(-k * t)
            y.append(temp)
        label_add = "(Tiefkuehlbereich)"
    else: 
        p_start, p_end = 20, 60
        for i, t in enumerate(x):
            if i < p_start: y.append(t_start - (t_start - freezing_point) * (i/p_start))
            elif i < p_end: y.append(freezing_point)
            else:
                rem = 100 - p_end
                prog = (i - p_end) / rem
                y.append(t_target + (freezing_point - t_target) * np.exp(-3 * prog))
        label_add = "(mit Gefrierplateau)"

    ax.plot(x, y, color='#36A9E1', linewidth=3, label="Kerntemperatur")
    ax.axhline(y=t_target, color='gray', linestyle='--', label=f"Soll ({t_target} C)")
    ax.set_title(f"Simulierter Temperaturverlauf {label_add}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Zeit (h)")
    ax.set_ylabel("Temperatur (C)")
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()
    plt.tight_layout()
    
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(tmp.name, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return tmp.name

# --- 4. PDF KLASSE ---
class PDF(FPDF):
    def __init__(self, kunde, projekt, raum):
        super().__init__()
        self.kunde = kunde
        self.projekt = projekt
        self.raum = raum
        
        # Custom Font laden
        font_path = "POE_Vetica_UI.ttf"
        if os.path.exists(font_path):
            self.add_font('POE', '', font_path, uni=True)
            self.add_font('POE', 'B', font_path, uni=True)
            self.add_font('POE', 'I', font_path, uni=True)
            self.font_loaded = True
        else:
            self.font_loaded = False

    def header(self):
        self.set_fill_color(54, 169, 225) 
        self.rect(0, 0, 210, 35, 'F') 
        logo = "Coolsulting_Logo_ohneHG_outlines_weiss.png"
        if os.path.exists(logo): 
            self.image(logo, x=150, y=8, w=50)
        
        self.set_y(10)
        
        # Font wählen
        if self.font_loaded:
            self.set_font('POE', 'B', 24)
        else:
            self.set_font('helvetica', 'B', 24)
        
        # °cool in WEISS
        self.set_text_color(255, 255, 255)
        grad_symbol = chr(176)
        self.text(10, 20, f"{grad_symbol}cool")
        
        # INDUTEC in GRAU
        self.set_text_color(60, 60, 59)
        self.text(34, 20, "INDUTEC") 
        
        self.set_y(24)
        self.set_text_color(255, 255, 255)
        
        if self.font_loaded:
            self.set_font('POE', '', 9)
        else:
            self.set_font('helvetica', '', 9)
            
        self.cell(0, 5, f'Kunde: {self.kunde} | Projekt: {self.projekt} | Raum: {self.raum}', 0, 1, 'L')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        
        if self.font_loaded:
            self.set_font('POE', 'I', 8)
        else:
            self.set_font('helvetica', 'I', 8)
            
        self.set_text_color(150)
        self.cell(0, 10, f'Erstellt mit coolINDUTEC | Seite {self.page_no()}', 0, 0, 'C')
    
    def set_body_font(self, style='', size=10):
        """Helper für Body-Text"""
        if self.font_loaded:
            self.set_font('POE', style, size)
        else:
            self.set_font('helvetica', style, size)

# --- 5. EINGABEN ---
with st.expander("📋 Stammdaten", expanded=True):
    c1, c2, c3 = st.columns(3)
    k_name = c1.text_input("Kunde", "Fleischwerk Muster")
    p_name = c2.text_input("Projekt", "TK-Erweiterung")
    r_name = c3.text_input("Raum", "Froster 1")

st.write("---")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("### 🏠 Gebäude")
    l = st.number_input("Länge (m)", value=20.0, step=0.5)
    b = st.number_input("Breite (m)", value=5.0, step=0.5)
    h = st.number_input("Höhe (m)", value=9.0, step=0.5)
    iso = st.number_input("Iso (mm)", value=120.0, step=10.0)
    
    if iso > 0: 
        u_calc = 0.022 / (iso / 1000)
    else: 
        u_calc = 0.0

with c2:
    st.markdown("### 🌡️ Temperatur")
    t_r = st.number_input("Raum (°C)", value=-24.0, step=1.0)
    t_w = st.number_input("Wand (°C)", value=25.0, step=1.0)
    t_b = st.number_input("Boden (°C)", value=10.0, step=1.0)
    t_d = st.number_input("Dach (°C)", value=35.0, step=1.0)

with c3:
    st.markdown("### 🚪 Logistik & Intern")
    t_fl = st.number_input("Tür (m²)", value=5.0, step=0.5)
    h_o = st.number_input("Tür offen (h/Tag)", value=1.5, step=0.1)
    
    st.markdown("**Interne Lasten:**")
    col_i1, col_i2 = st.columns(2)
    with col_i1: 
        n_pers = st.number_input("Personen", value=2, step=1)
        n_stap = st.number_input("Stapler", value=1, step=1)
    with col_i2:
        h_pers = st.number_input("Zeit Pers (h)", value=4.0, step=0.5)
        h_stap = st.number_input("Zeit Stapler (h)", value=2.0, step=0.5)
    
    f_s = st.slider("Schutzfaktor (Tür)", 0.1, 1.0, 0.7)

with c4:
    st.markdown("### ❄️ Technik")
    t_run = st.number_input("Laufzeit (h)", value=16.0, step=1.0)
    p_fan = st.number_input("Lüfter (W)", value=1350.0, step=50.0)
    p_def = st.number_input("Abtauheizung (kW)", value=36.0, step=1.0)
    
    st.markdown("**Abtauung:**")
    c4a, c4b = st.columns(2)
    with c4a:
        n_def = st.number_input("Anzahl/Tag", value=4, step=1)
    with c4b:
        t_def = st.number_input("Dauer (min)", value=35, step=5)

# --- WARENLAST ---
st.markdown("### 📦 Warenlast")
w1, w2, w3, w4 = st.columns(4)
with w1: 
    m_w = st.number_input("Masse (kg)", value=5000.0, step=100.0)
    t_ein = st.number_input("Ein (°C)", value=-15.0, step=0.5)

def_h_in = get_h_ware(t_ein)
def_h_out = get_h_ware(t_r)

with w2: 
    h_in = st.number_input("h Ein (kJ/kg)", value=def_h_in, help="Aus Produkttabelle")
    st.caption("(Spezifische Produktdaten)")
with w3: 
    h_out = st.number_input("h Ziel (kJ/kg)", value=def_h_out, help="Aus Produkttabelle")
    st.caption("(Spezifische Produktdaten)")
with w4: 
    t_c = st.number_input("Abkühlzeit (h)", value=12.0, step=0.5)

# --- 6. BERECHNUNG ---
# Transmission
q_trans = ((2*(l*h+b*h)*(t_w-t_r) + l*b*(t_b-t_r) + l*b*(t_d-t_r)) * u_calc * 24) / 1000

# Ware
dh_w = h_in - h_out
if t_c > 0:
    q_ware_kw = (m_w * dh_w) / (3600 * t_c)
else:
    q_ware_kw = 0
q_ware_day = (m_w * dh_w) / 3600

# Infiltration - KORRIGIERT
v_raum = l * b * h
rho_luft = 1.2
dh_luft = 55.0
v_austausch = min(t_fl * 2.0, v_raum * 0.3)
q_inf = (v_austausch * rho_luft * dh_luft * h_o * f_s) / 3600

# Interne Lasten 
q_pers_day = (n_pers * 350 * h_pers) / 1000
q_stap_day = (n_stap * 3000 * h_stap) / 1000
q_intern = q_pers_day + q_stap_day

# Technik
q_def_entry = p_def * (t_def / 60) * n_def * 0.4
q_sys = ((p_fan * t_run) / 1000) + q_def_entry

# Gesamt
q_tot = (q_trans + q_ware_day + q_inf + q_intern + q_sys) * 1.1

# Kälteleistung Q0
if t_run > 0:
    q0 = q_tot / t_run
else:
    q0 = 0.0

# --- 7. DASHBOARD ---
st.write("---")
res1, res2 = st.columns([1.2, 0.8])
with res1:
    st.markdown(f"""
    <div style="background-color: white; border-radius: 12px; padding: 25px; border-left: 12px solid #3C3C3B; box-shadow: 0px 4px 15px rgba(0,0,0,0.1);">
        <p style="color:#3C3C3B; margin:0;">Erforderliche Kälteleistung Q<sub>0</sub>:</p>
        <h2 style="color:#36A9E1; font-size:58px; margin:0;">{q0:.2f} kW</h2>
        <p style="margin-top:10px;">
           Arbeit: <b>{q_tot:.1f} kWh/d</b><br>
           <span style="color:#888; font-size:12px;">Infiltration: {q_inf:.1f} kWh/d | Austauschvol.: {v_austausch:.1f} m³</span>
        </p>
    </div>""", unsafe_allow_html=True)

with res2:
    labels = ['Transmission', 'Ware', 'Tür/Infiltration', 'Intern (Pers/Stap)', 'Technik/Abtau']
    values = [q_trans, q_ware_day, q_inf, q_intern, q_sys]
    if sum(values) == 0: values = [1,0,0,0,0]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
    fig.update_layout(height=250, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# --- 8. PDF GENERATOR ---
if st.button("📄 PDF Report erstellen"):
    pdf = PDF(k_name, p_name, r_name)
    
    # SEITE 1
    pdf.add_page()
    pdf.set_body_font('B', 12)
    pdf.cell(0, 10, "1. Technische Auslegung & Ergebnisse", 0, 1)
    
    # Q0 Highlight
    pdf.set_fill_color(240)
    pdf.set_body_font('B', 16)
    pdf.cell(100, 16, "Kaelteleistung Q0:", 1, 0, fill=True)
    pdf.set_text_color(54, 169, 225)
    pdf.cell(90, 16, f"{q0:.2f} kW", 1, 1, 'C', fill=True)
    pdf.set_text_color(0)
    pdf.ln(5)
    pdf.set_body_font('', 10)
    
    rows = [
        ("Raum-Soll / Laufzeit", f"{t_r} C / {t_run} h"),
        ("Ware (Masse/Temp)", f"{m_w} kg @ {t_ein} C"), 
        ("Enthalpie (Ein/Ziel)", f"{h_in:.1f} / {h_out:.1f} kJ/kg"),
        ("Tuer (Flaeche/Offen)", f"{t_fl} m2 / {h_o} h"),
        ("Infiltration (korrigiert)", f"{q_inf:.1f} kWh/d ({v_austausch:.1f} m3)"),
        ("Intern (Pers/Stapler)", f"{n_pers} Pers / {n_stap} Stapler"),
        ("Abtauung", f"{n_def}x taegl. a {t_def} min ({p_def} kW)"),
        ("Gesamt-Arbeit pro Tag", f"{q_tot:.1f} kWh/d")
    ]
    
    pdf.set_body_font('B', 10)
    pdf.cell(95, 8, "Parameter", 1, 0, fill=True)
    pdf.cell(95, 8, "Wert", 1, 1, fill=True)
    pdf.set_body_font('', 10)
    
    for l_txt, v_txt in rows:
        pdf.cell(95, 8, l_txt, 1)
        pdf.cell(95, 8, v_txt, 1, 1)

    pdf.ln(10)
    pdf.multi_cell(0, 5, "HINWEIS: Infiltration nach korrigiertem Volumen-Modell. Sicherheitsfaktor 10% inkludiert.")

    # SEITE 2
    pdf.add_page()
    pdf.set_body_font('B', 12)
    pdf.cell(0, 10, "2. Grafische Auswertung", 0, 1)
    pdf.ln(5)
    
    pdf.set_body_font('B', 11)
    pdf.cell(0, 8, "Detaillierte Lastverteilung (kWh/Tag)", 0, 1)
    
    labels_detail = ['Transmission', 'Warenabkuehlung', 'Tuer/Infiltration', 'Interne Lasten', 'Technik/Abtauung']
    f1 = create_pie_chart_mpl_detailed(labels_detail, values, units="kWh")
    pdf.image(f1, x=10, w=180)
    pdf.ln(5)
    
    pdf.set_body_font('B', 11)
    pdf.cell(0, 8, "Temperaturverlauf Ware (Simulation)", 0, 1)
    
    f2 = create_cooling_curve_mpl(t_ein, t_r, t_c)
    pdf.image(f2, x=10, w=180)
    
    try: 
        os.remove(f1)
        os.remove(f2)
    except: 
        pass
    
    st.download_button("💾 PDF Report Herunterladen", 
                       data=bytes(pdf.output()), 
                       file_name=f"coolINDUTEC_{p_name}.pdf",
                       mime="application/pdf")
