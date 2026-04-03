# ============================================================================
# DATEI: coolPOOL.py
# VERSION: 6.96
# DATUM: 29.03.2026
# AUTOR: Michael Schäpers - °coolsulting
# BESCHREIBUNG: °coolPOOL – Poolwasser-Temperierungs-Simulation
#               Vollständig rekonstruiert & in centralSTATION_PRO integriert
# ============================================================================

import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# --- META ---
APP_NAME = "°coolPOOL – Poolwasser-Temperierungs-Simulation"
VERSION  = "6.96"
COMPANY  = "°coolsulting"
AUTHOR   = "Michael Schäpers"

# --- PFADE & BRANDING ---
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH  = os.path.join(BASE_DIR, "Coolsulting_Logo_ohneHG_blau_weiß.png")
COLOR_BLUE = "#36A9E1"
COLOR_GREY = "#3C3C3B"

# --- GERÄTEDATENBANK ---
# WICHTIG: Alle Modelle haben identische Keys (inkl. "pipe" und "cop_nom")
HP_MODELS = {
    "--- Bitte wählen ---": {
        "power": 0.0, "fuse": "N/A", "cable": "N/A", "pipe": "N/A",
        "flow_min": 0.0, "sound": 0, "cop_max": 0.0, "cop_nom": 0.0,
        "dim": "N/A", "weight": "N/A"
    },
    "Modell 11-H9 [CL25560]": {
        "power": 10.9, "fuse": "C16A", "cable": "3x2.5 mm²", "pipe": "50 mm",
        "flow_min": 3.7, "sound": 42, "cop_max": 14.5, "cop_nom": 5.8,
        "dim": "1000 x 418 x 605 mm", "weight": "54 kg"
    },
    "Modell 17-H9 [CL25561]": {
        "power": 17.4, "fuse": "C20A", "cable": "3x4.0 mm²", "pipe": "50 mm",
        "flow_min": 5.9, "sound": 45, "cop_max": 14.8, "cop_nom": 6.2,
        "dim": "1060 x 438 x 758 mm", "weight": "74 kg"
    },
    "Modell 21-H9 [CL25563]": {
        "power": 21.2, "fuse": "C25A", "cable": "3x4.0 mm²", "pipe": "50 mm",
        "flow_min": 7.3, "sound": 48, "cop_max": 15.0, "cop_nom": 6.3,
        "dim": "1161 x 470 x 858 mm", "weight": "95 kg"
    },
    "Manuelle Leistungseingabe": {
        "power": 0.0, "fuse": "C25A", "cable": "3x4.0 mm²", "pipe": "50 mm",
        "flow_min": 7.0, "sound": 48, "cop_max": 15.0, "cop_nom": 6.0,
        "dim": "Variabel", "weight": "Variabel"
    },
}

REGIONAL_CLIMATE = {
    "1xxx (Wien/Ost)":        {"Tag": [3.5, 5.8, 11.2, 16.5, 21.8, 24.9, 27.2, 26.9, 21.5, 15.4,  8.5, 4.2],
                               "Nacht": [-1.2, -0.2, 3.1, 7.2, 11.8, 15.1, 17.0, 16.8, 12.5, 8.1, 3.2, 0.1]},
    "4xxx (OÖ/Zentralraum)":  {"Tag": [2.9, 5.1, 10.3, 15.2, 20.5, 23.4, 25.6, 25.4, 20.3, 14.2,  7.5, 4.0],
                               "Nacht": [-2.0, -0.9, 2.4, 5.8, 10.5, 13.5, 15.4, 15.3, 11.7, 7.0, 2.4, -0.5]},
    "5xxx (Salzburg/Alpin)":  {"Tag": [2.5, 4.8,  9.8, 14.8, 19.8, 22.8, 24.9, 24.7, 19.8, 13.8,  7.1, 3.2],
                               "Nacht": [-2.5, -1.5, 1.8, 5.4,  9.8, 13.1, 14.9, 14.8, 11.2, 6.5, 2.0, -1.2]},
    "8xxx (Steiermark)":      {"Tag": [3.4, 5.7, 10.9, 16.1, 21.3, 24.3, 26.5, 26.2, 21.0, 15.0,  8.2, 4.0],
                               "Nacht": [-2.2, -1.1, 2.1, 6.1, 10.7, 13.9, 15.8, 15.6, 11.5, 7.2, 2.3, -0.8]},
}


# ============================================================
# HELPER: MATPLOTLIB-BILDER FÜR PDF
# ============================================================
def render_mpl(fig_type, **kwargs):
    plt.figure(figsize=(10, 5), facecolor="white")
    if fig_type == "klima":
        df = kwargs["df"]
        plt.plot(df["Monat"], df["Tag"],   marker="o", color=COLOR_BLUE, label="Tag (°C)")
        plt.plot(df["Monat"], df["Nacht"], marker="s", color="grey", linestyle="--", label="Nacht (°C)")
        plt.title("Regionaler Klimaverlauf")
        plt.ylabel("Temp (°C)")
    elif fig_type == "sim":
        plt.plot(kwargs["times"], kwargs["temps"], color=COLOR_BLUE, linewidth=3, label="Poolwasser (°C)")
        plt.axhline(y=kwargs["soll"], color="red", linestyle="--", label="Sollwert")
        plt.title("24h Thermische Simulation")
        plt.ylabel("Temp (°C)")
        plt.xticks(np.arange(0, 25, 2))
    elif fig_type == "aufheiz":
        plt.plot(kwargs["x"], kwargs["y"], color="#FF9800", linewidth=3, label="Aufheizkurve")
        plt.title(f"Initial-Aufheizung ({kwargs['vol']:.1f} m³)")
        plt.xlabel("h")
        plt.ylabel("°C")
    plt.legend(loc="upper right", frameon=True)
    plt.grid(True, linestyle=":", alpha=0.6)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    return buf.getvalue()


# ============================================================
# PDF-GENERATOR
# ============================================================
def generate_pdf(data, imgs):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    meta = f"{APP_NAME} | Michael Schäpers – °coolsulting | Version {VERSION}"

    # ---- SEITE 1 ----
    p.setFont("Helvetica", 7)
    p.setFillColor(colors.grey)
    p.drawRightString(w - 50, h - 25, meta)
    if os.path.exists(LOGO_PATH):
        p.drawImage(ImageReader(LOGO_PATH), 50, h - 65, width=70, preserveAspectRatio=True, mask="auto")
    p.setFillColor(colors.HexColor(COLOR_BLUE))
    p.setFont("Helvetica-Bold", 16)
    p.drawString(140, h - 55, "ENGINEERING-ANALYSE-BERICHT")
    p.line(50, h - 75, 550, h - 75)
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, h - 95, "PROJEKT-BASISDATEN")
    p.setFont("Helvetica", 10)
    y = h - 115
    for line in [
        f"Kunde: {data['name']}",
        f"Bearbeiter: {data['bearbeiter']}",
        f"Firma: {data['firma']}",
        f"Standort: {data['adresse']}  (H = {data['hoehe']} m)",
        f"Beckenvolumen: {data['volumen']:.1f} m³  ({data['laenge']} × {data['breite']} × {data['tiefe']} m)",
    ]:
        p.drawString(50, y, line); y -= 15
    if imgs[0]:
        p.drawImage(ImageReader(io.BytesIO(imgs[0])), 50, y - 190, width=500, height=170, preserveAspectRatio=True)
        y -= 200
    if imgs[1]:
        p.drawImage(ImageReader(io.BytesIO(imgs[1])), 50, y - 190, width=500, height=170, preserveAspectRatio=True)

    # ---- SEITE 2 ----
    p.showPage()
    p.setFont("Helvetica", 7); p.setFillColor(colors.grey); p.drawRightString(w - 50, h - 25, meta)
    y = h - 60
    p.setFillColor(colors.HexColor(COLOR_BLUE)); p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "TECHNISCHE SPEZIFIKATIONEN & LEISTUNG")
    p.line(50, y - 5, 550, y - 5); y -= 30
    p.setFillColor(colors.black); p.setFont("Helvetica-Bold", 11); p.drawString(50, y, "ANLAGEN-DATEN")
    ts = data["tech"]; p.setFont("Helvetica", 10); y -= 15
    for line in [
        f"Modell: {data['wp_mod']}",
        f"Elektrik: {ts['cable']}  |  Absicherung: {ts['fuse']}",
        f"Hydraulik: Anschluss {ts['pipe']}  |  Mindestfluss: {ts['flow_min']} m³/h",
        f"Schall (1 m): {ts['sound']} dB(A)  |  Max. COP: {ts['cop_max']}",
    ]:
        p.drawString(55, y, line); y -= 13
    y -= 10
    p.setFont("Helvetica-Bold", 11); p.drawString(50, y, "ERGEBNIS LEISTUNGSANALYSE")
    y -= 15
    p.setFont("Helvetica-Bold", 10); p.setFillColor(colors.HexColor(COLOR_BLUE))
    p.drawString(55, y, f"VORGESCHLAGENE MINDESTLEISTUNG (+20 %): {data['rec_p']:.1f} kW"); y -= 20
    p.setFillColor(colors.black); p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "DETAILLIERTE VERLUST-ANALYSE (kW/h)"); y -= 5
    p.line(50, y, 250, y); y -= 15
    p.setFont("Helvetica-Bold", 10)
    p.drawString(55, y, f"TAG:   Oberfläche {data['ls_t_s']:.2f} kW  |  Hülle {data['ls_t_h']:.2f} kW"); y -= 15
    p.drawString(55, y, f"NACHT: Oberfläche {data['ls_n_s']:.2f} kW  |  Hülle {data['ls_n_h']:.2f} kW"); y -= 25

    # ---- SEITE 3 ----
    p.showPage()
    p.setFont("Helvetica", 7); p.drawRightString(w - 50, h - 25, meta)
    if imgs[2]:
        p.setFont("Helvetica-Bold", 14); p.drawString(50, h - 55, "AUFHEIZ-SIMULATION ERSTBEFÜLLUNG")
        p.line(50, h - 70, 550, h - 70)
        p.drawImage(ImageReader(io.BytesIO(imgs[2])), 50, h - 350, width=500, height=250, preserveAspectRatio=True)
    y = h - 380
    p.setFont("Helvetica-Bold", 11); p.drawString(50, y, "HYDRAULISCHE RESULTATE"); y -= 20
    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"Energiebedarf: {data['e_fill']:.1f} kWh  |  Dauer: ca. {data['h_fill']:.1f} h"); y -= 15
    p.drawString(50, y, f"Berechneter Volumenstrom Pumpe: {data['v_flow']:.2f} m³/h")
    p.showPage(); p.save(); buffer.seek(0)
    return buffer


# ============================================================
# HAUPTFUNKTION
# ============================================================
def main():
    # --- CSS ---
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; background-color: #000000; color: #FFFFFF; }}
        .stApp {{ background-color: #000000; }}
        label {{ color: {COLOR_BLUE} !important; font-weight: 600 !important; font-size: 1.05rem; }}
        div[data-testid="stMetric"] {{ background-color: {COLOR_GREY}; border: 1px solid {COLOR_BLUE}; padding: 15px; border-radius: 10px; }}
        .stButton>button {{ background-color: {COLOR_BLUE}; color: #000000; font-weight: 700; width: 100%; height: 3.5em; border-radius: 8px; border: none; }}
        .report-container {{ background-color: {COLOR_GREY}; padding: 25px; border-radius: 12px; border-left: 8px solid {COLOR_BLUE}; margin-top: 20px; border: 1px solid #4a4a4a; }}
        h1, h2, h3 {{ color: {COLOR_BLUE} !important; }}
        </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    col_l, col_t = st.columns([1, 4])
    with col_l:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=120)
    with col_t:
        st.title(APP_NAME)
        st.caption(f"Version {VERSION}  |  {AUTHOR} – {COMPANY}")

    # ============================================================
    # SIDEBAR – COCKPIT
    # ============================================================
    st.sidebar.header("📋 1. Projekt-Basisdaten")
    bearbeiter = st.sidebar.text_input("Bearbeiter", value=AUTHOR)
    firma      = st.sidebar.text_input("Firma",      value=COMPANY)
    name       = st.sidebar.text_input("Kunde / Projekt", value="Neues Projekt")
    adresse    = st.sidebar.text_input("Standort",   value="Riedau, AT")
    region     = st.sidebar.selectbox("Klimazone", list(REGIONAL_CLIMATE.keys()), index=1)
    hoehe      = st.sidebar.number_input("Meereshöhe (m ü. A.)", value=380,
                                         help="Höhenmeter reduzieren die Lufttemperatur (~0,65 K/100 m)")

    st.sidebar.markdown("---")
    st.sidebar.header("📏 2. Becken-Parameter")
    l_p = st.sidebar.number_input("Länge (m)", value=12.0)
    b_p = st.sidebar.number_input("Breite (m)", value=3.5)
    d_p = st.sidebar.number_input("Tiefe (m)",  value=1.45)
    flaeche = l_p * b_p
    volumen = l_p * b_p * d_p
    wind  = st.sidebar.select_slider("Windlast", options=["Gering", "Mäßig", "Stark"], value="Mäßig")
    decke = st.sidebar.toggle("Thermodecke vorhanden", value=False,
                               help="Reduziert Oberflächenverluste um ~85 %")

    st.sidebar.markdown("---")
    st.sidebar.header("🔥 3. Geräte-Engineering")
    wp_sel = st.sidebar.selectbox("Wärmepumpen-Modell", list(HP_MODELS.keys()), index=0)
    if wp_sel == "Manuelle Leistungseingabe":
        man_p     = st.sidebar.number_input("Heizleistung (kW)", value=21.0, min_value=0.1)
        tech_data = {**HP_MODELS["Manuelle Leistungseingabe"], "power": man_p}
    else:
        tech_data = HP_MODELS[wp_sel]

    # ⚠️  KRITISCHE VARIABLE – muss VOR der Physik-Engine gesetzt sein
    wp_p    = tech_data["power"]
    delta_t = st.sidebar.number_input("Hydraulik ΔT (K)", value=2.0,
                                       help="Spreizung Vor-/Rücklauf")

    st.sidebar.markdown("---")
    st.sidebar.header("🎯 4. Sollwerte & Betrieb")
    t_soll   = st.sidebar.number_input("Soll Tag (°C)",   value=26.0)
    t_soll_n = st.sidebar.number_input("Soll Nacht (°C)", value=26.0)

    # --- TAG-ZEITEN ---
    st.sidebar.markdown("**☀️ Tagheizung**")
    col_t1, col_t2 = st.sidebar.columns(2)
    with col_t1:
        tag_von = col_t1.number_input("Von (h)", min_value=0, max_value=23, value=6,  step=1, key="tag_von")
    with col_t2:
        tag_bis = col_t2.number_input("Bis (h)", min_value=1, max_value=24, value=22, step=1, key="tag_bis")
    runtime_tag = max(0, tag_bis - tag_von)

    # --- NACHT-ZEITEN ---
    nacht_on = st.sidebar.toggle("🌙 Nachtheizung aktivieren", value=True)
    if nacht_on:
        st.sidebar.markdown("**🌙 Nachtheizung** (Abends → Morgens)")
        col_n1, col_n2 = st.sidebar.columns(2)
        with col_n1:
            nacht_von = col_n1.number_input("Von (h)", min_value=0, max_value=23, value=22, step=1, key="nacht_von")
        with col_n2:
            nacht_bis = col_n2.number_input("Bis (h)", min_value=0, max_value=12,  value=6,  step=1, key="nacht_bis")
        # Über Mitternacht: z.B. 22→6 = (24-22)+6 = 8h
        runtime_nacht = (24 - nacht_von) + nacht_bis if nacht_von > nacht_bis else max(0, nacht_bis - nacht_von)
    else:
        nacht_von, nacht_bis = 22, 6
        runtime_nacht = 0

    # --- GESAMTSTUNDEN ANZEIGE ---
    runtime_gesamt = runtime_tag + runtime_nacht
    st.sidebar.markdown(
        f"**⏱️ Laufzeit:** ☀️ {runtime_tag}h Tag  +  🌙 {runtime_nacht}h Nacht  =  **{runtime_gesamt}h gesamt**"
    )

    # ============================================================
    # PHYSIK-ENGINE
    # ============================================================
    lapse     = ((hoehe - 300) / 100) * 0.65
    base_k    = REGIONAL_CLIMATE[region]
    adj_tag   = [round(t - lapse, 1) for t in base_k["Tag"]]
    adj_nacht = [round(n - lapse, 1) for n in base_k["Nacht"]]
    months    = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

    m_range = st.select_slider(
        "Analyse-Saison (Detailansicht)", options=months, value=("Apr", "Okt")
    )
    idx_s   = months.index(m_range[0])
    idx_e   = months.index(m_range[1])
    worst_at = min(adj_tag[idx_s:idx_e + 1] + adj_nacht[idx_s:idx_e + 1])

    wf_val = {"Gering": 1.2, "Mäßig": 3.0, "Stark": 5.8}[wind]

    def calc_losses(at, target):
        dt   = max(0.0, target - at)
        surf = flaeche * (0.004 + 0.003 * wf_val) * dt * 0.62 * (0.15 if decke else 1.0)
        hull = flaeche * d_p * 0.0015 * (target - 10.0)
        return surf, hull

    ls_t_s, ls_t_h = calc_losses(adj_tag[idx_s],   t_soll)
    ls_n_s, ls_n_h = calc_losses(adj_nacht[idx_s],  t_soll_n)

    # Erhaltungsleistung: Worst-Case Verluste × 1.2 Sicherheit
    worst_losses = sum(calc_losses(worst_at, t_soll))
    rec_p = worst_losses * 1.2

    at_avg  = (adj_tag[idx_s] + adj_nacht[idx_s]) / 2
    cop_sim = (
        max(2.0, min(tech_data["cop_max"], tech_data["cop_nom"] + (at_avg - 15) * 0.25))
        if tech_data["cop_max"] > 0 else 0.0
    )

    # ============================================================
    # PHASE 1 – KLIMAPROFIL
    # ============================================================
    st.header("Phase 1: Lokales Klimaprofil")
    fig_k = go.Figure(data=[
        go.Scatter(x=months, y=adj_tag,   name="Tag (°C)",   line=dict(color=COLOR_BLUE, width=3)),
        go.Scatter(x=months, y=adj_nacht, name="Nacht (°C)", line=dict(color="grey", dash="dot")),
    ])
    fig_k.update_layout(
        xaxis_title="Monat", yaxis_title="°C", height=300,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
    )
    st.plotly_chart(fig_k, use_container_width=True)

    # ============================================================
    # PHASE 2 – LEISTUNGSANALYSE
    # ============================================================
    st.header("Phase 2: Physikalische Leistungs-Analyse")

    # Aufheizzeit mit gewähltem Gerät unter Worst-Case Bedingungen
    net_heiz_power = (wp_p * 0.9) - worst_losses  # Netto-Heizleistung nach Verlustabzug
    t_fill_default = 11.0
    e_aufheiz = volumen * 1.162 * (t_soll - t_fill_default)
    if net_heiz_power > 0 and wp_p > 0:
        aufheiz_stunden = e_aufheiz / net_heiz_power
    else:
        aufheiz_stunden = None  # Gerät zu schwach

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Verlust Tag (kW)",  f"{(ls_t_s + ls_t_h):.2f}")
        st.caption(f"Oberfläche: {ls_t_s:.2f}  |  Hülle: {ls_t_h:.2f}")
    with m2:
        st.metric("Min. Erhaltungsleistung", f"{rec_p:.1f} kW")
        st.caption(f"Worst-Case {worst_at:.1f}°C + 20% Reserve")
        st.metric("COP simuliert", f"{cop_sim:.1f}")
    with m3:
        st.metric("Verlust Nacht (kW)", f"{(ls_n_s + ls_n_h):.2f}")
        st.caption(f"Oberfläche: {ls_n_s:.2f}  |  Hülle: {ls_n_h:.2f}")

    st.info(f"⏱️ **Laufzeit:** ☀️ {runtime_tag}h Tag  +  🌙 {runtime_nacht}h Nacht  =  **{runtime_gesamt}h gesamt**")

    # Gerätebewertung
    if wp_p == 0:
        st.warning("⚠️ Bitte Wärmepumpen-Modell auswählen.")
    elif wp_p < rec_p:
        st.error(f"❌ **{wp_sel}** ({wp_p} kW) reicht NICHT aus! Mindestens **{rec_p:.1f} kW** erforderlich.")
    else:
        st.success(f"✅ **{wp_sel}** ({wp_p} kW) kann den Pool bei Worst-Case ({worst_at:.1f}°C) halten.")

    # Aufheizzeit-Analyse
    if wp_p > 0:
        st.markdown("#### 🌡️ Erstaufheizung mit gewähltem Gerät (Worst-Case)")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Netto-Heizleistung", f"{max(0, net_heiz_power):.1f} kW",
                      help="Geräte-Heizleistung minus Wärmeverluste bei Worst-Case")
        with c2:
            if aufheiz_stunden:
                st.metric("Aufheizzeit (11→26°C)", f"{aufheiz_stunden:.0f} h",
                          delta=f"≈ {aufheiz_stunden/24:.1f} Tage")
            else:
                st.metric("Aufheizzeit", "∞", delta="Gerät zu schwach!")
        with c3:
            st.metric("Aufheizenergie", f"{e_aufheiz:.0f} kWh")

    # ============================================================
    # PHASE 3 – 24h SIMULATION
    # ============================================================
    st.header("Phase 3: 24h Thermische Simulation")
    temps      = [t_soll]
    power_grid = []
    hours      = list(range(24))

    for hr in hours:
        is_tag = tag_von <= hr < tag_bis
        # Nacht: über Mitternacht (z.B. 22→6)
        if nacht_von > nacht_bis:
            is_nacht = hr >= nacht_von or hr < nacht_bis
        else:
            is_nacht = nacht_von <= hr < nacht_bis
        is_heiz = is_tag or (nacht_on and is_nacht)

        t_now  = t_soll   if (6 <= hr < 18) else t_soll_n
        at_now = adj_tag[idx_s] if (6 <= hr < 18) else adj_nacht[idx_s]
        ls_sum = sum(calc_losses(at_now, t_now))
        power_grid.append(ls_sum)

        gain = (wp_p * 0.9 - ls_sum) if is_heiz else -ls_sum
        new_t = temps[-1] + (gain / (volumen * 1.162))
        temps.append(min(t_now, new_t))

    fig_sim = go.Figure(go.Scatter(
        x=hours, y=temps[1:], name="Poolwasser (°C)",
        line=dict(color=COLOR_BLUE, width=4)
    ))
    fig_sim.update_layout(
        title="24h Temperaturverlauf", xaxis_title="Stunde (h)", yaxis_title="°C",
        height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    fig_bar = go.Figure(go.Bar(x=hours, y=power_grid, name="Heizlast (kW)", marker_color="#E91E63"))
    fig_bar.update_layout(
        title="Stündliches Lastprofil", xaxis_title="Stunde (h)", yaxis_title="kW",
        height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ============================================================
    # PHASE 4 – ERSTBEFÜLLUNG
    # ============================================================
    st.header("Phase 4: Erstbefüllung & Hydraulik")
    t_fill = st.number_input("💧 Füllwasser-Temperatur (°C)", value=11.0,
                              help="Typisch April: ~10–12 °C Stadtwasser")
    e_f  = volumen * 1.162 * (t_soll - t_fill)
    h_f  = (e_f / (wp_p * 0.9)) if wp_p > 0 else 0.0
    v_f  = (wp_p / (1.162 * delta_t)) if wp_p > 0 else 0.0
    x_f  = np.linspace(0, max(h_f, 0.1), 20)
    y_f  = [min(t_soll, t_fill + (wp_p * 0.9 * t / (volumen * 1.162))) for t in x_f]

    fig_fill = go.Figure(go.Scatter(
        x=x_f, y=y_f, name="Aufheizkurve", line=dict(color="#FF9800", width=4)
    ))
    fig_fill.update_layout(
        title=f"Initial-Aufheizung ({volumen:.1f} m³)",
        xaxis_title="h", yaxis_title="°C", height=300,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
    )
    st.plotly_chart(fig_fill, use_container_width=True)

    st.markdown(
        f'<div class="report-container">'
        f'<b>Anlage:</b> {wp_sel}<br>'
        f'Elektro: {tech_data["cable"]}  |  Absicherung: {tech_data["fuse"]}<br>'
        f'Anschluss: {tech_data["pipe"]}  |  Volumenstrom: {v_f:.2f} m³/h<br>'
        f'Schall (1 m): {tech_data["sound"]} dB(A)  |  Max. COP: {tech_data["cop_max"]}<br>'
        f'Energiebedarf Erstbefüllung: <b>{e_f:.1f} kWh</b>  |  Dauer: ca. <b>{h_f:.1f} h</b>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ============================================================
    # PHASE 5 – PDF-EXPORT
    # ============================================================
    st.header("Phase 5: Engineering-Bericht (PDF)")
    if st.button("🚀 PDF-Analyse generieren"):
        img_klima  = render_mpl("klima",  df=pd.DataFrame({"Monat": months, "Tag": adj_tag, "Nacht": adj_nacht}))
        img_sim    = render_mpl("sim",    times=hours, temps=temps[1:], soll=t_soll)
        img_fill   = render_mpl("aufheiz", x=x_f, y=y_f, vol=volumen)
        pdf_data = {
            "name": name, "bearbeiter": bearbeiter, "firma": firma,
            "adresse": adresse, "hoehe": hoehe,
            "volumen": volumen, "laenge": l_p, "breite": b_p, "tiefe": d_p,
            "worst_temp": worst_at, "t_soll": t_soll, "t_soll_nacht": t_soll_n,
            "wp_mod": wp_sel, "tech": tech_data, "v_flow": v_f,
            "rec_p": rec_p, "ls_t_s": ls_t_s, "ls_t_h": ls_t_h,
            "ls_n_s": ls_n_s, "ls_n_h": ls_n_h,
            "e_fill": e_f, "h_fill": h_f,
        }
        st.session_state["coolpool_pdf"] = generate_pdf(pdf_data, [img_klima, img_sim, img_fill])
        st.success("✅ Bericht erfolgreich generiert!")

    if "coolpool_pdf" in st.session_state:
        st.download_button(
            "📥 PDF herunterladen",
            data=st.session_state["coolpool_pdf"],
            file_name=f"coolPOOL_Analyse_{name.replace(' ', '_')}.pdf",
            mime="application/pdf",
        )


if __name__ == "__main__":
    main()
