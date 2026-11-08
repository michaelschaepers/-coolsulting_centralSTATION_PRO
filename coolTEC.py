# ==============================================================================
# APP NAME: °coolTEC (Kühlraumlast & Auslegung)
# VERSION: 4.0 - Pro-Upgrade mit Warendatenbank, Abkühlzeit, Luftwechsel, Interne Lasten
# DATUM: 08.11.2026
# ==============================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
import tempfile
import os
import base64
import math

try:
    st.set_page_config(page_title="°coolTEC", layout="wide", page_icon="❄️")
except:
    pass

APP_VERSION = "4.0"

# === FARBEN ===
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
    "Benutzerdefiniert":  {"cp_plus": 3.20, "cp_minus": 1.70, "t_freeze": -1.5, "h_freeze": 230},
}

PERSON_HEAT = {-25: 300, -20: 270, -10: 250, 0: 230, 4: 210, 7: 190, 10: 170, 15: 150, 20: 120}

def get_person_heat(t_raum):
    temps = sorted(PERSON_HEAT.keys())
    if t_raum <= temps[0]:
        return PERSON_HEAT[temps[0]]
    if t_raum >= temps[-1]:
        return PERSON_HEAT[temps[-1]]
    for i in range(len(temps) - 1):
        if temps[i] <= t_raum <= temps[i + 1]:
            f = (t_raum - temps[i]) / (temps[i + 1] - temps[i])
            return PERSON_HEAT[temps[i]] * (1 - f) + PERSON_HEAT[temps[i + 1]] * f
    return 200

def calc_ware(m_kg, t_ein, t_ziel, ware, abkuehl_h):
    cp_p, cp_m = ware["cp_plus"], ware["cp_minus"]
    t_fr, h_fr = ware["t_freeze"], ware["h_freeze"]
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
    q_spitze = (q_kj * 1000) / (abkuehl_h * 3600) if abkuehl_h > 0 else 0
    q_24h = (q_kj * 1000) / (24 * 3600)
    return q_kj, q_spitze, q_24h, crosses

def calc_luftwechsel(t_raum, t_umg, b_tuer, h_tuer, n_open, t_open_s, vorhang):
    if n_open == 0 or t_open_s == 0:
        return 0.0, 0.0
    A = b_tuer * h_tuer
    rho_w = 353.0 / (t_umg + 273.15)
    rho_c = 353.0 / (t_raum + 273.15)
    if rho_w >= rho_c:
        return 0.0, 0.0
    ratio = rho_w / rho_c
    Fm = math.sqrt(1 - ratio) * (2.0 / (1 + ratio ** (1.0 / 3))) ** 1.5
    q_dot = 0.221 * A * math.sqrt(9.81 * h_tuer) * Fm
    v = q_dot * n_open * t_open_s
    dh = 1.005 * abs(t_umg - t_raum) * (1.5 if t_raum < 0 else 1.2)
    q_w = (v * rho_w * dh * 1000) / 86400
    if vorhang:
        q_w *= 0.15
        v *= 0.15
    return q_w, v

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
    .stApp {{ background-color: {C_BLUE}; }}
    .section-head {{ color: {C_BLUE}; font-weight: bold; border-bottom: 2px solid {C_BLUE}; padding-bottom: 4px; margin-bottom: 10px; }}
    div[data-testid="stMetric"] {{ background-color: {C_GRAY} !important; border-radius: 10px; padding: 20px !important; }}
    div[data-testid="stMetricLabel"] > div {{ color: white !important; font-weight: bold !important; justify-content: center !important; }}
    div[data-testid="stMetricValue"] > div {{ color: white !important; font-size: 30px !important; text-align: center !important; }}
    div[data-testid="stMetricDelta"] > div {{ color: white !important; justify-content: center !important; }}
    .hint-box {{ background: rgba(255,255,255,0.15); border-radius: 8px; padding: 12px; color: white; font-size: 13px; margin-top: 10px; line-height: 1.6; }}
    </style>
""", unsafe_allow_html=True)

# === PDF ===
class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        fp = "POE_Vetica_UI.ttf"
        self._fl = False
        if os.path.exists(fp):
            try:
                self.add_font('POE', '', fp, uni=True)
                self.add_font('POE', 'B', fp, uni=True)
                self.add_font('POE', 'I', fp, uni=True)
                self._fl = True
            except: pass
    def _f(self, s='', sz=10):
        self.set_font('POE' if self._fl else 'Arial', s, sz)
    def header(self):
        self.set_fill_color(54, 169, 225)
        self.rect(0, 0, 210, 28, 'F')
        self._f('B', 18); self.set_text_color(255,255,255); self.set_y(7)
        self.cell(0, 8, chr(176)+'coolTEC Berechnungs-Protokoll', 0, 1, 'L')
        self._f('', 9); self.cell(0, 5, f'Version {APP_VERSION}', 0, 1, 'L'); self.ln(6)
    def footer(self):
        self.set_y(-18); self._f('I', 7); self.set_text_color(150,150,150)
        self.cell(0, 4, f'Seite {self.page_no()}', align='C', ln=True)
        self.multi_cell(0, 3, "Ueberschlaegige Berechnung. Ersetzt keine Kühllastberechnung nach VDI 2078 / EN 13215. Ohne Gewaehr.", align='C')

# === HEADER ===
st.markdown(f"""
    <div style='display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:20px; flex-wrap:wrap;'>
        <div style='font-size:52px; font-weight:bold; line-height:1;'><span style='color:white;'>°cool</span><span style='color:{C_GRAY};'>TEC</span></div>
        <div style='color:rgba(255,255,255,0.8); font-size:14px; padding-bottom:8px;'>Kühlraumlast Pro | v{APP_VERSION} | {datetime.now().strftime('%d.%m.%Y')}</div>
    </div>
""", unsafe_allow_html=True)

# === PROJEKTDATEN ===
cp1, cp2, cp3 = st.columns(3)
kunde = cp1.text_input("Kunde", "Musterkunde GmbH")
raum_bez = cp2.text_input("Raumbezeichnung", "Tiefkühllager 1")
bearbeiter = cp3.text_input("Bearbeiter", "M. Schäpers")
st.markdown("<hr style='margin:10px 0; opacity:0.1;'>", unsafe_allow_html=True)

# === EINGABEN ===
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<p class="section-head">1. GEOMETRIE & DÄMMUNG</p>', unsafe_allow_html=True)
    l = st.number_input("Länge (m)", 1.0, 50.0, 4.0, step=0.1)
    b = st.number_input("Breite (m)", 1.0, 50.0, 3.0, step=0.1)
    h = st.number_input("Höhe (m)", 1.8, 10.0, 2.5, step=0.1)
    a_boden = l * b; vol = l * b * h
    st.caption(f"Fläche: {a_boden:.1f} m² | Volumen: {vol:.1f} m³")
    damm_mm = st.selectbox("Dämmstärke (mm)", [60, 80, 100, 120, 140, 160, 200], index=2)
    u_val = round(0.022 / (int(damm_mm) / 1000), 3)
    st.caption(f"U-Wert: {u_val} W/m²K")

with c2:
    st.markdown('<p class="section-head">2. TEMPERATUREN</p>', unsafe_allow_html=True)
    t_set = st.selectbox("Raum-Soll", ["+15°C Trockenlager", "+7°C Getränke", "+4°C Molkerei", "+2°C Fleisch", "0°C Frisch", "-18°C TK-Standard", "-22°C TK-Lager", "-24°C Eiscreme", "-28°C Schock"], index=5)
    t_raum = float(t_set.split("°C")[0].replace("+","").strip())
    t_umg = int(st.number_input("Umgebung (°C)", 10, 45, 25))
    t_decke = int(st.number_input("Decke/Dach (°C)", 10, 60, 30))
    t_boden = int(st.number_input("Boden (°C)", 5, 25, 12))
    is_tk = t_raum < 0

with c3:
    st.markdown('<p class="section-head">3. WARE & ABKÜHLUNG</p>', unsafe_allow_html=True)
    laufzeit = int(st.selectbox("Laufzeit Aggregat (h/Tag)", [12, 14, 16, 18, 20, 22], index=3))
    ware_name = st.selectbox("Kühlgut", list(WAREN_DB.keys()), index=0)
    ware_data = WAREN_DB[ware_name]
    if ware_name == "Benutzerdefiniert":
        ware_data = dict(ware_data)
        ware_data["cp_plus"] = st.number_input("cp oberhalb GP (kJ/kgK)", 0.5, 5.0, 3.2, step=0.1)
        ware_data["cp_minus"] = st.number_input("cp unterhalb GP (kJ/kgK)", 0.5, 3.0, 1.7, step=0.1)
        ware_data["t_freeze"] = st.number_input("Gefrierpunkt (°C)", -10.0, 0.0, -1.5, step=0.1)
        ware_data["h_freeze"] = int(st.number_input("Gefrier-Enthalpie (kJ/kg)", 0, 400, 230))
    else:
        st.caption(f"cp: {ware_data['cp_plus']}/{ware_data['cp_minus']} kJ/kgK | GP: {ware_data['t_freeze']}°C | h_fr: {ware_data['h_freeze']} kJ/kg")
    ware_kg_m2 = int(st.number_input("Beschickung (kg/m²)", 0, 1000, 80))
    t_einbring = int(st.number_input("Einbringtemperatur (°C)", -10, 40, 20))
    abkuehl_h = int(st.number_input("Abkühlzeit (Stunden)", 1, 48, 8))
    m_ware = ware_kg_m2 * a_boden

st.markdown("<hr style='margin:10px 0; opacity:0.1;'>", unsafe_allow_html=True)
c4, c5 = st.columns(2)

with c4:
    st.markdown('<p class="section-head">4. LUFTWECHSEL / TÜRÖFFNUNGEN</p>', unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    b_tuer = float(tc1.number_input("Türbreite (m)", 0.5, 4.0, 1.2, step=0.1))
    h_tuer = float(tc2.number_input("Türhöhe (m)", 1.5, 4.0, 2.2, step=0.1))
    n_open = int(st.number_input("Öffnungen / Tag", 0, 500, 30))
    t_open_s = int(st.number_input("Dauer pro Öffnung (Sek.)", 5, 300, 30))
    streifenvorhang = st.checkbox("Streifenvorhang (~85% Reduktion)", value=False)
    if n_open > 0:
        st.caption(f"Gesamte Öffnungszeit: {n_open * t_open_s / 60:.1f} min/Tag")

with c5:
    st.markdown('<p class="section-head">5. INTERNE WÄRMEQUELLEN</p>', unsafe_allow_html=True)
    licht_wm2 = int(st.number_input("Beleuchtung (W/m²)", 0, 30, 8))
    licht_h = int(st.number_input("Beleuchtung (h/Tag)", 0, 24, 10))
    n_pers = int(st.number_input("Personen gleichzeitig", 0, 20, 1))
    pers_h = int(st.number_input("Aufenthalt Personen (h/Tag)", 0, 24, 4))
    q_mot_w = int(st.number_input("Stapler/Motoren/Ventilatoren (W)", 0, 10000, 300))
    mot_h = int(st.number_input("Motoren (h/Tag)", 0, 24, 10))

# === BERECHNUNG ===
a_wand = 2 * (l + b) * h
q_wand = u_val * a_wand * max(0, t_umg - t_raum)
q_decke = u_val * a_boden * max(0, t_decke - t_raum)
u_bod = u_val if is_tk else min(u_val * 2, 1.5)
q_boden = u_bod * a_boden * max(0, t_boden - t_raum)
q_trans = q_wand + q_decke + q_boden

q_ware_kj, q_ware_spitze, q_ware_24h, crosses_freeze = calc_ware(m_ware, t_einbring, t_raum, ware_data, abkuehl_h)
q_luft, v_luft = calc_luftwechsel(t_raum, t_umg, b_tuer, h_tuer, n_open, t_open_s, streifenvorhang)

q_licht = (licht_wm2 * a_boden * licht_h) / 24
q_pers = (get_person_heat(t_raum) * n_pers * pers_h) / 24
q_motor = (q_mot_w * mot_h) / 24
q_intern = q_licht + q_pers + q_motor

q_sum = q_trans + q_ware_24h + q_luft + q_intern
zuschlag = q_sum * 0.10
q_sum_z = q_sum + zuschlag
q_bedarf = q_sum_z * (24 / laufzeit)
q_spitz = (q_trans + q_ware_spitze + q_luft + q_intern) * 1.10

# === ERGEBNISSE ===
st.markdown("<hr style='margin:15px 0; opacity:0.1;'>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color:white;'>Ergebnisse – {raum_bez}</h3>", unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)
r1.metric("KÄLTEBEDARF", f"{q_bedarf/1000:.2f} kW", f"{q_bedarf:.0f} W")
r2.metric("SPITZENLAST", f"{q_spitz/1000:.2f} kW", "bei Wareneinbringung")
r3.metric("ENERGIE / TAG", f"{(q_sum_z*24)/1000:.1f} kWh", f"Ware: {m_ware:.0f} kg")
r4.metric("KENNZAHL", f"{q_bedarf/vol:.0f} W/m³", f"Vol: {vol:.1f} m³")

if crosses_freeze:
    st.info(f"Ware durchläuft Gefrierpunkt ({ware_data['t_freeze']}°C) – Gefrierenthalpie {ware_data['h_freeze']} kJ/kg berücksichtigt.")

if st.button("Im Verlauf speichern"):
    if "verlauf_heute" not in st.session_state:
        st.session_state.verlauf_heute = []
    st.session_state.verlauf_heute.append({
        "uhrzeit": datetime.now().strftime("%H:%M Uhr"), "modul": "coolTEC",
        "bezeichnung": f"{kunde} | {raum_bez}", "ergebnis": f"Kältebedarf: {q_bedarf/1000:.2f} kW"
    })
    st.success("Im Verlauf gespeichert.")

# === DIAGRAMME ===
st.markdown("<hr style='margin:10px 0; opacity:0.1;'>", unsafe_allow_html=True)
col_pie, col_time = st.columns(2)

labels = ["Transmission", "Ware (24h)", "Luftwechsel", "Beleuchtung", "Personen", "Motoren", "Zuschlag"]
values = [q_trans, q_ware_24h, q_luft, q_licht, q_pers, q_motor, zuschlag]
colors = ["#FF8C00", "#FF4B4B", "#5DADE2", "#F4D03F", "#AF7AC5", "#85929E", "#3C3C3B"]

with col_pie:
    st.markdown("<p style='color:white; font-weight:bold; text-align:center;'>LASTVERTEILUNG (24h-Schnitt)</p>", unsafe_allow_html=True)
    cl, cv, cc = [], [], []
    for lb, vl, co in zip(labels, values, colors):
        if vl > 0.5:
            cl.append(lb); cv.append(round(vl,1)); cc.append(co)
    fig_pie = go.Figure(data=[go.Pie(labels=cl, values=cv, hole=0.45, sort=False,
        marker=dict(colors=cc, line=dict(color='#fff', width=2)), textinfo='percent+label', textfont=dict(size=11))])
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10,b=10,l=10,r=10), height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_time:
    st.markdown("<p style='color:white; font-weight:bold; text-align:center;'>LASTVERLAUF ÜBER 24 STUNDEN</p>", unsafe_allow_html=True)
    hrs = list(range(25))
    y_t = [q_trans/1000]*25
    y_l = [q_luft/1000]*25
    y_i = [q_intern/1000]*25
    y_w = [(q_ware_spitze/1000 if hr < abkuehl_h else 0) for hr in hrs]

    fig_t = go.Figure()
    fig_t.add_trace(go.Scatter(x=hrs, y=y_t, fill='tozeroy', name='Transmission', line=dict(width=0), fillcolor='rgba(255,140,0,0.5)'))
    s1 = [a+b for a,b in zip(y_t, y_l)]
    fig_t.add_trace(go.Scatter(x=hrs, y=s1, fill='tonexty', name='Luftwechsel', line=dict(width=0), fillcolor='rgba(93,173,226,0.5)'))
    s2 = [a+b for a,b in zip(s1, y_i)]
    fig_t.add_trace(go.Scatter(x=hrs, y=s2, fill='tonexty', name='Intern', line=dict(width=0), fillcolor='rgba(175,122,197,0.4)'))
    s3 = [a+b for a,b in zip(s2, y_w)]
    fig_t.add_trace(go.Scatter(x=hrs, y=s3, fill='tonexty', name=f'Ware ({abkuehl_h}h)', line=dict(color='#FF4B4B', width=1), fillcolor='rgba(255,75,75,0.5)'))

    fig_t.update_layout(xaxis_title="Stunde", yaxis_title="kW",
        paper_bgcolor='rgba(255,255,255,0.9)', plot_bgcolor='rgba(255,255,255,0.9)',
        margin=dict(t=10,b=40,l=50,r=10), height=350,
        legend=dict(orientation='h', y=-0.15, font=dict(size=11)))
    st.plotly_chart(fig_t, use_container_width=True)

# === DETAILTABELLE ===
st.markdown("<p style='color:white; font-weight:bold;'>DETAILLIERTE LASTAUFSTELLUNG</p>", unsafe_allow_html=True)
df = pd.DataFrame({"Komponente": labels, "Last (W)": [round(v,1) for v in values],
    "Anteil (%)": [round(v/q_sum_z*100,1) if q_sum_z > 0 else 0 for v in values]})
st.table(df)

# === ZUSAMMENFASSUNG ===
st.markdown(f"""<div class="hint-box">
<b>Zusammenfassung:</b><br>
• Transmission: <b>{q_trans:.0f} W</b> (Wände {q_wand:.0f} + Decke {q_decke:.0f} + Boden {q_boden:.0f})<br>
• Ware: <b>{q_ware_kj:.0f} kJ</b> gesamt, Spitze <b>{q_ware_spitze:.0f} W</b> über {abkuehl_h}h{' (inkl. Gefrierenthalpie)' if crosses_freeze else ''}<br>
• Luftwechsel: <b>{q_luft:.0f} W</b> ({n_open}× à {t_open_s}s{', Streifenvorhang' if streifenvorhang else ''})<br>
• Intern: Licht {q_licht:.0f} + Pers. {q_pers:.0f} + Mot. {q_motor:.0f} = <b>{q_intern:.0f} W</b><br>
• <b>Kälteleistung bei {laufzeit}h: {q_bedarf/1000:.2f} kW</b> (inkl. 10% Zuschlag)
</div>""", unsafe_allow_html=True)

# === PDF ===
st.markdown("<hr style='margin:10px 0; opacity:0.1;'>", unsafe_allow_html=True)
if st.button("PDF-Bericht generieren"):
    pdf = PDFReport(); pdf.add_page(); pdf.set_text_color(60,60,59)
    pdf._f('B',12); pdf.cell(0,8,f'Projekt: {kunde} | {raum_bez}', ln=True)
    pdf._f('',10)
    pdf.cell(0,6,f'Bearbeiter: {bearbeiter} | Datum: {datetime.now().strftime("%d.%m.%Y")}', ln=True)
    pdf.cell(0,6,f'Geometrie: {l}x{b}x{h} m = {a_boden:.1f} m2, {vol:.1f} m3 | Daemmung: {damm_mm} mm (U={u_val})', ln=True)
    pdf.cell(0,6,f'Temperaturen: Raum {t_raum} C | Umgebung {t_umg} C | Decke {t_decke} C | Boden {t_boden} C', ln=True)
    pdf.ln(4)
    pdf.set_fill_color(240,240,240); pdf.rect(10, pdf.get_y(), 190, 18, 'F')
    pdf.set_y(pdf.get_y()+2); pdf._f('B',11); pdf.cell(0,6,'Erforderliche Kaelteleistung:', align='C', ln=True)
    pdf._f('B',18); pdf.set_text_color(54,169,225); pdf.cell(0,8,f'{q_bedarf/1000:.2f} kW', align='C', ln=True)
    pdf.set_text_color(60,60,59); pdf.ln(4)
    pdf._f('B',11); pdf.cell(0,7,'Lastaufstellung:', ln=True); pdf._f('',10)
    for lb, vl in zip(labels, values):
        if vl > 0.1:
            pct = vl/q_sum_z*100 if q_sum_z > 0 else 0
            pdf.cell(70,6,f'  {lb}:'); pdf.cell(30,6,f'{vl:.0f} W'); pdf.cell(0,6,f'({pct:.1f}%)', ln=True)
    pdf.ln(3); pdf._f('B',11); pdf.cell(0,7,'Ware:', ln=True); pdf._f('',10)
    pdf.cell(0,6,f'  {ware_name} | {m_ware:.0f} kg | {t_einbring} C -> {t_raum} C in {abkuehl_h}h', ln=True)
    pdf.cell(0,6,f'  Energie: {q_ware_kj:.0f} kJ | Spitze: {q_ware_spitze:.0f} W | 24h: {q_ware_24h:.0f} W', ln=True)
    if crosses_freeze:
        pdf.cell(0,6,f'  Gefrierpunkt {ware_data["t_freeze"]} C – Enthalpie {ware_data["h_freeze"]} kJ/kg', ln=True)
    pdf.ln(3); pdf._f('B',11); pdf.cell(0,7,'Kennzahlen:', ln=True); pdf._f('',10)
    pdf.cell(70,6,'  Kaeltebedarf:'); pdf.cell(0,6,f'{q_bedarf/1000:.2f} kW ({q_bedarf:.0f} W)', ln=True)
    pdf.cell(70,6,'  Spitzenlast:'); pdf.cell(0,6,f'{q_spitz/1000:.2f} kW', ln=True)
    pdf.cell(70,6,'  Energie/Tag:'); pdf.cell(0,6,f'{(q_sum_z*24)/1000:.1f} kWh', ln=True)
    pdf.cell(70,6,'  Spez. Leistung:'); pdf.cell(0,6,f'{q_bedarf/vol:.0f} W/m3', ln=True)
    pdf.cell(70,6,'  Laufzeit:'); pdf.cell(0,6,f'{laufzeit} h/Tag', ln=True)
    pdf_bytes = bytes(pdf.output(dest='S'))
    st.download_button("PDF herunterladen", data=pdf_bytes,
        file_name=f"coolTEC_{raum_bez.replace(' ','_')}_{datetime.now().strftime('%Y-%m-%d')}.pdf", mime="application/pdf")
