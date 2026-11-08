# ==========================================
# DATEI: coolINDUTEC.py
# VERSION: 5.0 - Warendatenbank, Dashboard, Zeitverlauf
# DATUM: 08.11.2026
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
import base64
import math

st.set_page_config(page_title="°coolINDUTEC PRO", layout="wide")

APP_VERSION = "5.0"
C_BLUE = "#36A9E1"
C_GRAY = "#3C3C3B"

# === WARENDATENBANK (ASHRAE Refrigeration Handbook) ===
WAREN_DB = {
    "Rindfleisch":        {"cp_plus": 3.22, "cp_minus": 1.67, "t_freeze": -1.7, "h_freeze": 233},
    "Schweinefleisch":    {"cp_plus": 2.85, "cp_minus": 1.55, "t_freeze": -2.2, "h_freeze": 197},
    "Geflügel":           {"cp_plus": 3.31, "cp_minus": 1.55, "t_freeze": -2.8, "h_freeze": 247},
    "Fisch (mager)":      {"cp_plus": 3.60, "cp_minus": 1.72, "t_freeze": -2.2, "h_freeze": 268},
    "Fisch (fett)":       {"cp_plus": 3.00, "cp_minus": 1.50, "t_freeze": -2.0, "h_freeze": 210},
    "Milch / Joghurt":    {"cp_plus": 3.93, "cp_minus": 1.80, "t_freeze": -0.6, "h_freeze": 302},
    "Käse (hart)":        {"cp_plus": 2.50, "cp_minus": 1.30, "t_freeze": -7.0, "h_freeze": 126},
    "Butter":             {"cp_plus": 2.04, "cp_minus": 1.17, "t_freeze": -0.5, "h_freeze":  32},
    "Äpfel / Birnen":     {"cp_plus": 3.81, "cp_minus": 1.88, "t_freeze": -1.5, "h_freeze": 280},
    "Bananen":            {"cp_plus": 3.56, "cp_minus": 1.76, "t_freeze": -0.8, "h_freeze": 251},
    "Gemüse (Mischung)":  {"cp_plus": 3.77, "cp_minus": 1.84, "t_freeze": -1.2, "h_freeze": 276},
    "Kartoffeln":         {"cp_plus": 3.51, "cp_minus": 1.80, "t_freeze": -0.6, "h_freeze": 262},
    "Backwaren":          {"cp_plus": 2.93, "cp_minus": 1.42, "t_freeze": -3.0, "h_freeze": 138},
    "Eiscreme":           {"cp_plus": 3.27, "cp_minus": 1.68, "t_freeze": -5.6, "h_freeze": 210},
    "TK-Pizza / Fertig":  {"cp_plus": 2.51, "cp_minus": 1.30, "t_freeze": -3.5, "h_freeze": 165},
    "Manuell (Enthalpie)": None,
}

# Enthalpie-Stützstellen (Fallback für manuelle Eingabe)
ENTHALPIE_STUETZ_X = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]
ENTHALPIE_STUETZ_Y = [28, 38, 49, 62, 86, 304, 321, 339, 357, 374, 392]

def get_h_ware(temp):
    return float(np.interp(temp, ENTHALPIE_STUETZ_X, ENTHALPIE_STUETZ_Y))

def calc_ware_enthalpie(m_kg, t_ein, t_ziel, ware_data, abkuehl_h):
    if ware_data is None:
        return None
    cp_p, cp_m = ware_data["cp_plus"], ware_data["cp_minus"]
    t_fr, h_fr = ware_data["t_freeze"], ware_data["h_freeze"]
    q_kj = 0.0
    crosses = t_ein > t_fr and t_ziel < t_fr
    if crosses:
        q_kj += m_kg * cp_p * (t_ein - t_fr)
        q_kj += m_kg * h_fr
        q_kj += m_kg * cp_m * abs(t_fr - t_ziel)
    elif t_ein >= t_fr:
        q_kj += m_kg * cp_p * (t_ein - t_ziel)
    else:
        q_kj += m_kg * cp_m * (t_ein - t_ziel)
    q_kwh = q_kj / 3600
    q_peak_kw = (q_kj * 1000) / (abkuehl_h * 3600) / 1000 if abkuehl_h > 0 else 0
    return q_kwh, q_peak_kw, crosses

PERSON_HEAT = {-28: 310, -25: 300, -20: 270, -10: 250, 0: 230, 4: 210, 7: 190, 10: 170, 15: 150, 20: 120}
def get_person_heat(t):
    temps = sorted(PERSON_HEAT.keys())
    if t <= temps[0]: return PERSON_HEAT[temps[0]]
    if t >= temps[-1]: return PERSON_HEAT[temps[-1]]
    for i in range(len(temps)-1):
        if temps[i] <= t <= temps[i+1]:
            f = (t - temps[i]) / (temps[i+1] - temps[i])
            return PERSON_HEAT[temps[i]]*(1-f) + PERSON_HEAT[temps[i+1]]*f
    return 200

# === FONT ===
def get_font_base64(fp):
    if os.path.exists(fp):
        with open(fp, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

font_b64 = get_font_base64("POE_Vetica_UI.ttf")

# === CSS ===
st.markdown(f"""
    <style>
    {f"@font-face {{ font-family: 'POE Helvetica UI'; src: url(data:font/ttf;base64,{font_b64}) format('truetype'); }}" if font_b64 else ""}
    * {{ font-family: 'POE Helvetica UI', 'Helvetica', sans-serif !important; }}
    [data-testid="stExpander"] summary::before {{ display: none !important; }}
    .title-box {{ font-size: 42px; font-weight: bold; margin-bottom: 20px; padding-top: 10px; background-color: transparent !important; }}
    .title-box .blue-t {{ color: #FFFFFF !important; background-color: transparent !important; }}
    .title-box .gray-t {{ color: #3C3C3B !important; background-color: transparent !important; }}
    .stNumberInput input {{ background-color: white !important; }}
    .stSelectbox div[data-baseweb="select"] > div {{ background-color: white !important; }}
    .section-head {{ color: {C_BLUE}; font-weight: bold; border-bottom: 2px solid {C_BLUE}; padding-bottom: 4px; margin-bottom: 10px; }}
    div[data-testid="stMetric"] {{ background-color: {C_GRAY} !important; border-radius: 10px; padding: 18px !important; }}
    div[data-testid="stMetricLabel"] > div {{ color: white !important; font-weight: bold !important; justify-content: center !important; }}
    div[data-testid="stMetricValue"] > div {{ color: white !important; font-size: 28px !important; text-align: center !important; }}
    div[data-testid="stMetricDelta"] > div {{ color: white !important; justify-content: center !important; }}
    .hint-box {{ background: rgba(255,255,255,0.15); border-radius: 8px; padding: 12px; color: white; font-size: 13px; margin-top: 10px; line-height: 1.6; }}
    </style>
    <div class="title-box">
        <span class="blue-t">°cool</span><span class="gray-t">INDUTEC</span>
        <span style="font-size:14px; color:rgba(255,255,255,0.7); margin-left:12px;">Pro v{APP_VERSION} | {__import__('datetime').datetime.now().strftime('%d.%m.%Y')}</span>
    </div>
""", unsafe_allow_html=True)

# === PDF ===
def create_cooling_curve_mpl(t_start, t_target, duration_h, t_freeze=-2.0):
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(0, duration_h, 100)
    y = []
    is_freezing = (t_target < 0 and t_start > t_freeze)
    if is_freezing:
        p1_end = int(len(x) * 0.20)
        p2_end = int(len(x) * 0.60)
        for i, t in enumerate(x):
            if i < p1_end:
                y.append(t_start - (t_start - t_freeze) * (i / p1_end))
            elif i < p2_end:
                y.append(t_freeze)
            else:
                progress = (i - p2_end) / (len(x) - p2_end)
                y.append(t_target + (t_freeze - t_target) * np.exp(-3.0 * progress))
        label_add = "(mit Gefrierplateau)"
    else:
        k = 3.0 / duration_h
        for t in x:
            y.append(t_target + (t_start - t_target) * np.exp(-k * t))
        label_add = "(TK)" if t_target < 0 else "(NK)"
    ax.plot(x, y, color='#36A9E1', linewidth=3, label="Kerntemperatur")
    ax.axhline(y=t_target, color='gray', linestyle='--', label=f"Ziel ({t_target} C)")
    if is_freezing:
        ax.axhline(y=t_freeze, color='#FF4B4B', linestyle=':', alpha=0.5, label=f"Gefrierpunkt ({t_freeze} C)")
    ax.set_title(f"Temperaturverlauf {label_add}", fontsize=12, fontweight='bold')
    ax.set_xlabel("Zeit (h)"); ax.set_ylabel("Temperatur (C)")
    ax.grid(True, linestyle=':', alpha=0.6); ax.legend()
    ax.set_ylim([min(min(y), t_target)-5, max(max(y), t_start)+5])
    plt.tight_layout()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    plt.savefig(tmp.name, dpi=150, bbox_inches='tight'); plt.close(fig)
    return tmp.name

class PDF(FPDF):
    def __init__(self, kunde, projekt, raum):
        super().__init__()
        self.kunde, self.projekt, self.raum = kunde, projekt, raum
        fp = "POE_Vetica_UI.ttf"
        self._fl = False
        if os.path.exists(fp):
            try:
                self.add_font('POE','',fp,uni=True); self.add_font('POE','B',fp,uni=True); self.add_font('POE','I',fp,uni=True)
                self._fl = True
            except: pass
    def _f(self, s='', sz=10):
        self.set_font('POE' if self._fl else 'helvetica', s, sz)
    def header(self):
        self.set_fill_color(54,169,225); self.rect(0,0,210,32,'F')
        logo = "Coolsulting_Logo_ohneHG_outlines_weiß.png"
        if os.path.exists(logo): self.image(logo, x=150, y=6, w=50)
        self.set_y(8); self._f('B',22); self.set_text_color(255,255,255)
        self.text(10, 18, chr(176)+"cool"); self.set_text_color(60,60,59); self.text(31, 18, "INDUTEC")
        self.set_y(22); self.set_text_color(255,255,255); self._f('',9)
        self.cell(0, 5, f'{self.kunde} | {self.projekt} | {self.raum}', 0, 1, 'L'); self.ln(12)
    def footer(self):
        self.set_y(-15); self._f('I',8); self.set_text_color(150)
        self.cell(0, 10, f'coolINDUTEC v{APP_VERSION} | Seite {self.page_no()}', 0, 0, 'C')

# === EINGABEN ===
with st.expander("Stammdaten", expanded=True):
    c1, c2, c3 = st.columns(3)
    k_name = c1.text_input("Kunde", "Fleischwerk Muster")
    p_name = c2.text_input("Projekt", "TK-Erweiterung")
    r_name = c3.text_input("Raum", "Froster 1")

st.write("---")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown('<p class="section-head">1. GEOMETRIE</p>', unsafe_allow_html=True)
    l = st.number_input("Länge (m)", value=20.0, step=0.5)
    b = st.number_input("Breite (m)", value=5.0, step=0.5)
    h = st.number_input("Höhe (m)", value=9.0, step=0.5)
    iso = st.number_input("Iso (mm)", value=120.0, step=10.0)
    u_calc = 0.022 / (iso / 1000) if iso > 0 else 0.0
    v_raum = l * b * h
    a_boden = l * b
    st.caption(f"U: {u_calc:.3f} W/m²K | V: {v_raum:.0f} m³ | A: {a_boden:.0f} m²")

with c2:
    st.markdown('<p class="section-head">2. TEMPERATUREN</p>', unsafe_allow_html=True)
    t_r = st.number_input("Raum (°C)", value=-24.0, step=1.0)
    t_w = st.number_input("Wand/Umgebung (°C)", value=25.0, step=1.0)
    t_b = st.number_input("Boden (°C)", value=10.0, step=1.0)
    t_d = st.number_input("Dach (°C)", value=35.0, step=1.0)
    is_tk = t_r < 0

with c3:
    st.markdown('<p class="section-head">3. LOGISTIK & INTERN</p>', unsafe_allow_html=True)
    t_fl = st.number_input("Tür (m²)", value=5.0, step=0.5)
    h_o = st.number_input("Tür offen (h/Tag)", value=1.5, step=0.1)
    n_luft = st.number_input("Luftwechsel (1/h)", value=0.5, step=0.1)
    f_s = st.slider("Schutzfaktor (Tür)", 0.1, 1.0, 0.7)
    tc1, tc2 = st.columns(2)
    n_pers = int(tc1.number_input("Personen", value=2, step=1))
    n_stap = int(tc2.number_input("Stapler", value=1, step=1))
    h_pers = tc1.number_input("h Pers.", value=4.0, step=0.5)
    h_stap = tc2.number_input("h Stapl.", value=2.0, step=0.5)

with c4:
    st.markdown('<p class="section-head">4. TECHNIK</p>', unsafe_allow_html=True)
    t_run = st.number_input("Laufzeit (h)", value=16.0, step=1.0)
    p_fan = st.number_input("Lüfter (W)", value=1350.0, step=50.0)
    p_def = st.number_input("Abtauheizung (kW)", value=36.0, step=1.0)
    c4a, c4b = st.columns(2)
    n_def = int(c4a.number_input("Abt./Tag", value=4, step=1))
    t_def = int(c4b.number_input("Dauer (min)", value=35, step=5))
    q_beleuchtung_wm2 = int(st.number_input("Beleuchtung (W/m²)", 0, 30, 5))
    h_licht = int(st.number_input("Licht (h/Tag)", 0, 24, 8))

# === WARENLAST ===
st.markdown("### 5. WARENLAST")
w1, w2, w3 = st.columns(3)

with w1:
    ware_modus = st.radio("Eingabemodus", ["Warendatenbank", "Manuelle Enthalpie"], horizontal=True)
    m_w = st.number_input("Masse (kg)", value=5000.0, step=100.0)
    t_ein = st.number_input("Einbringtemperatur (°C)", value=-15.0, step=0.5)
    t_c = st.number_input("Abkühlzeit (h)", value=12.0, step=0.5)

with w2:
    if ware_modus == "Warendatenbank":
        ware_sel = st.selectbox("Kühlgut", [k for k in WAREN_DB.keys() if WAREN_DB[k] is not None])
        ware_data = WAREN_DB[ware_sel]
        st.caption(f"cp: {ware_data['cp_plus']}/{ware_data['cp_minus']} kJ/kgK")
        st.caption(f"GP: {ware_data['t_freeze']}°C | h_fr: {ware_data['h_freeze']} kJ/kg")
        result = calc_ware_enthalpie(m_w, t_ein, t_r, ware_data, t_c)
        if result:
            q_ware_day, q_ware_peak_kw, crosses_freeze = result
            h_in = get_h_ware(t_ein)
            h_out = get_h_ware(t_r)
            use_db = True
        else:
            q_ware_day, q_ware_peak_kw, crosses_freeze = 0, 0, False
            h_in, h_out = get_h_ware(t_ein), get_h_ware(t_r)
            use_db = True
    else:
        use_db = False
        h_in = st.number_input("h Ein (kJ/kg)", value=get_h_ware(t_ein))
        h_out = st.number_input("h Ziel (kJ/kg)", value=get_h_ware(t_r))
        dh_w = h_in - h_out
        q_ware_day = (m_w * dh_w) / 3600
        q_ware_peak_kw = (m_w * dh_w) / (3600 * t_c) / 1000 if t_c > 0 else 0
        crosses_freeze = t_ein > -2.0 and t_r < -2.0

with w3:
    st.markdown("**Waren-Kennzahlen:**")
    st.markdown(f"Gesamtenergie: **{q_ware_day:.1f} kWh**")
    st.markdown(f"Spitzenlast: **{q_ware_peak_kw:.2f} kW**")
    st.markdown(f"24h-Schnitt: **{q_ware_day/24*1000:.0f} W**")
    if crosses_freeze:
        st.info(f"Gefrierpunkt wird durchlaufen – Gefrierenthalpie berücksichtigt!")

# === BERECHNUNG ===
q_trans_kwh = ((2*(l*h+b*h)*(t_w-t_r) + a_boden*(t_b-t_r) + a_boden*(t_d-t_r)) * u_calc * 24) / 1000
rho_luft, dh_luft = 1.2, 55.0
v_austausch = min(t_fl * 2.0, v_raum * 0.3)
q_inf_tuer = (v_austausch * rho_luft * dh_luft * h_o * f_s) / 3600
q_luftwechsel = (n_luft * v_raum * rho_luft * dh_luft * 24) / 3600
q_inf = q_inf_tuer + q_luftwechsel

q_pers_kwh = (n_pers * get_person_heat(t_r) * h_pers) / 1000
q_stap_kwh = (n_stap * 3000 * h_stap) / 1000
q_licht_kwh = (q_beleuchtung_wm2 * a_boden * h_licht) / 1000
q_intern = q_pers_kwh + q_stap_kwh + q_licht_kwh

q_def_entry = p_def * (t_def / 60) * n_def * 0.4
q_sys = ((p_fan * t_run) / 1000) + q_def_entry

q_tot = (q_trans_kwh + q_ware_day + q_inf + q_intern + q_sys) * 1.1

if t_run > 0:
    q_konstant_kw = (q_trans_kwh + q_inf + q_intern + q_sys) / t_run
    q0 = (q_konstant_kw + q_ware_peak_kw) * 1.1
else:
    q0 = 0.0

# === ERGEBNISSE ===
st.write("---")
st.markdown(f"<h3 style='color:white;'>Ergebnisse – {r_name}</h3>", unsafe_allow_html=True)

r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("Q0 KÄLTELEISTUNG", f"{q0:.2f} kW", f"{q0*1000:.0f} W")
r2.metric("SPITZENLAST WARE", f"{q_ware_peak_kw:.2f} kW", f"über {t_c:.0f}h")
r3.metric("ARBEIT / TAG", f"{q_tot:.1f} kWh", f"inkl. 10% Zuschlag")
r4.metric("KENNZAHL", f"{q0*1000/v_raum:.0f} W/m³", f"Vol: {v_raum:.0f} m³")
r5.metric("LAUFZEIT", f"{t_run:.0f} h/Tag", f"Raum: {t_r}°C")

if st.button("Im Verlauf speichern"):
    if "verlauf_heute" not in st.session_state:
        st.session_state.verlauf_heute = []
    st.session_state.verlauf_heute.append({
        "uhrzeit": __import__('datetime').datetime.now().strftime("%H:%M Uhr"), "modul": "coolINDUTEC",
        "bezeichnung": f"{k_name} | {r_name}", "ergebnis": f"Q0: {q0:.2f} kW"
    })
    st.success("Im Verlauf gespeichert.")

# === DIAGRAMME ===
st.write("---")
col_pie, col_time = st.columns(2)

labels = ["Transmission", "Ware", "Tür-Infiltr.", "Luftwechsel", "Personen", "Stapler", "Beleuchtung", "Technik/Abtau", "Zuschlag 10%"]
values_kwh = [q_trans_kwh, q_ware_day, q_inf_tuer, q_luftwechsel, q_pers_kwh, q_stap_kwh, q_licht_kwh, q_sys, q_tot - (q_trans_kwh+q_ware_day+q_inf+q_intern+q_sys)]
colors = ["#FF8C00", "#FF4B4B", "#5DADE2", "#2E86C1", "#AF7AC5", "#85929E", "#F4D03F", "#3C3C3B", "#555555"]

with col_pie:
    st.markdown("<p style='color:white; font-weight:bold; text-align:center;'>LASTVERTEILUNG (kWh/Tag)</p>", unsafe_allow_html=True)
    cl, cv, cc = [], [], []
    for lb, vl, co in zip(labels, values_kwh, colors):
        if vl > 0.01:
            cl.append(lb); cv.append(round(vl, 2)); cc.append(co)
    fig_pie = go.Figure(data=[go.Pie(labels=cl, values=cv, hole=0.45, sort=False,
        marker=dict(colors=cc, line=dict(color='#fff', width=2)), textinfo='percent+label', textfont=dict(size=10))])
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10,b=10,l=10,r=10), height=380)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_time:
    st.markdown("<p style='color:white; font-weight:bold; text-align:center;'>LASTVERLAUF ÜBER 24 STUNDEN</p>", unsafe_allow_html=True)
    hrs = list(range(25))
    q_trans_kw = q_trans_kwh / 24
    q_inf_kw = q_inf / 24
    q_intern_kw = q_intern / 24
    q_sys_kw = q_sys / t_run if t_run > 0 else 0
    abk_h = int(t_c)

    y_t = [q_trans_kw] * 25
    y_inf = [q_inf_kw] * 25
    y_int = [q_intern_kw] * 25
    y_sys = [(q_sys_kw if hr < t_run else 0) for hr in hrs]
    y_ware = [(q_ware_peak_kw if hr < abk_h else 0) for hr in hrs]

    fig_t = go.Figure()
    fig_t.add_trace(go.Scatter(x=hrs, y=y_t, fill='tozeroy', name='Transmission', line=dict(width=0), fillcolor='rgba(255,140,0,0.5)'))
    s1 = [a+b for a,b in zip(y_t, y_inf)]
    fig_t.add_trace(go.Scatter(x=hrs, y=s1, fill='tonexty', name='Infiltration', line=dict(width=0), fillcolor='rgba(93,173,226,0.5)'))
    s2 = [a+b for a,b in zip(s1, y_int)]
    fig_t.add_trace(go.Scatter(x=hrs, y=s2, fill='tonexty', name='Intern', line=dict(width=0), fillcolor='rgba(175,122,197,0.4)'))
    s3 = [a+b for a,b in zip(s2, y_sys)]
    fig_t.add_trace(go.Scatter(x=hrs, y=s3, fill='tonexty', name='Technik', line=dict(width=0), fillcolor='rgba(60,60,59,0.4)'))
    s4 = [a+b for a,b in zip(s3, y_ware)]
    fig_t.add_trace(go.Scatter(x=hrs, y=s4, fill='tonexty', name=f'Ware ({abk_h}h)', line=dict(color='#FF4B4B', width=1), fillcolor='rgba(255,75,75,0.5)'))

    fig_t.update_layout(xaxis_title="Stunde", yaxis_title="kW",
        paper_bgcolor='rgba(255,255,255,0.9)', plot_bgcolor='rgba(255,255,255,0.9)',
        margin=dict(t=10,b=40,l=50,r=10), height=380,
        legend=dict(orientation='h', y=-0.15, font=dict(size=10)))
    st.plotly_chart(fig_t, use_container_width=True)

# === ZUSAMMENFASSUNG ===
st.markdown(f"""<div class="hint-box">
<b>Zusammenfassung {r_name}:</b><br>
• Transmission: <b>{q_trans_kwh:.1f} kWh/d</b> (Wände + Decke + Boden, U={u_calc:.3f} W/m²K)<br>
• Ware: <b>{q_ware_day:.1f} kWh</b> gesamt, Spitze <b>{q_ware_peak_kw:.2f} kW</b> über {t_c:.0f}h{' (inkl. Gefrierenthalpie)' if crosses_freeze else ''}<br>
• Infiltration: Tür <b>{q_inf_tuer:.1f}</b> + Luftwechsel <b>{q_luftwechsel:.1f}</b> = <b>{q_inf:.1f} kWh/d</b><br>
• Intern: Personen {q_pers_kwh:.1f} + Stapler {q_stap_kwh:.1f} + Licht {q_licht_kwh:.1f} = <b>{q_intern:.1f} kWh/d</b><br>
• Technik: Lüfter + Abtauung = <b>{q_sys:.1f} kWh/d</b><br>
• <b>Q0 = {q0:.2f} kW</b> bei {t_run:.0f}h Laufzeit (inkl. 10% Zuschlag)
</div>""", unsafe_allow_html=True)

# === PDF ===
st.write("---")
if st.button("PDF Report erstellen"):
    from datetime import datetime
    pdf = PDF(k_name, p_name, r_name)
    pdf.add_page(); pdf.set_text_color(60,60,59)
    pdf._f('B',12); pdf.cell(0,10,"1. Technische Auslegung & Ergebnisse",0,1)
    pdf.set_fill_color(240); pdf._f('B',16)
    pdf.cell(100,16,"Kaelteleistung Q0:",1,0,fill=True)
    pdf.set_text_color(54,169,225); pdf.cell(90,16,f"{q0:.2f} kW",1,1,'C',fill=True)
    pdf.set_text_color(0); pdf.ln(5); pdf._f('',10)
    rows = [
        ("Raum / Laufzeit", f"{t_r} C / {t_run} h"),
        ("Geometrie", f"{l}x{b}x{h} m = {v_raum:.0f} m3"),
        ("Daemmung", f"{iso:.0f} mm (U={u_calc:.3f} W/m2K)"),
        ("Ware", f"{ware_sel if ware_modus=='Warendatenbank' else 'Manuell'} | {m_w:.0f} kg | {t_ein} -> {t_r} C in {t_c:.0f}h"),
        ("Ware Energie/Spitze", f"{q_ware_day:.1f} kWh / {q_ware_peak_kw:.2f} kW"),
        ("Infiltration (Tuer+LW)", f"{q_inf:.1f} kWh/d"),
        ("Intern (Pers/Stap/Licht)", f"{q_intern:.1f} kWh/d"),
        ("Technik/Abtauung", f"{q_sys:.1f} kWh/d"),
        ("Gesamt-Arbeit/Tag", f"{q_tot:.1f} kWh/d"),
        ("Spez. Leistung", f"{q0*1000/v_raum:.0f} W/m3"),
    ]
    pdf._f('B',10); pdf.cell(95,8,"Parameter",1,0,fill=True); pdf.cell(95,8,"Wert",1,1,fill=True); pdf._f('',10)
    for lt, vt in rows:
        pdf.cell(95,8,lt,1); pdf.cell(95,8,vt,1,1)
    if crosses_freeze:
        pdf.ln(3); pdf._f('I',9); pdf.cell(0,6,"Gefrierpunkt durchlaufen – Gefrierenthalpie beruecksichtigt.",0,1)
    pdf.ln(5); pdf.multi_cell(0,5,"Sicherheitsfaktor 10% inkludiert. Ueberschlaegige Berechnung, ersetzt keine Detailplanung.")

    pdf.add_page(); pdf._f('B',12); pdf.cell(0,10,"2. Grafische Auswertung",0,1); pdf.ln(3)
    t_freeze_val = WAREN_DB.get(ware_sel, {}).get("t_freeze", -2.0) if ware_modus == "Warendatenbank" else -2.0
    f2 = create_cooling_curve_mpl(t_ein, t_r, t_c, t_freeze_val)
    pdf._f('B',11); pdf.cell(0,8,"Temperaturverlauf Ware (Simulation)",0,1)
    pdf.image(f2, x=10, w=180)
    try: os.remove(f2)
    except: pass

    st.download_button("PDF herunterladen", data=bytes(pdf.output()),
        file_name=f"coolINDUTEC_{p_name}_{datetime.now().strftime('%Y-%m-%d')}.pdf", mime="application/pdf")
