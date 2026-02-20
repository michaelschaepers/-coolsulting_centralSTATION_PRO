# ==========================================
# DATEI: WP_Quick_Kalkulator.py
# VERSION: 4.2 - POE Font Integration
# DATUM: 20.02.2026
# ==========================================

import streamlit as st
import os
import plotly.graph_objects as go
import base64

def get_font_base64(font_path):
    if os.path.exists(font_path):
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def main():
    # FARBEN
    BG_COLOR = "#36A9E1"
    TEXT_MAIN = "#3C3C3B"
    INPUT_TEXT_COLOR = "#36A9E1"
    INPUT_BG = "#FFFFFF"         
    BTN_BG = "#FFFFFF"           
    BTN_TEXT = "#3C3C3B"

    # Font laden
    font_b64 = get_font_base64("POE_Vetica_UI.ttf")

    # CSS STYLING
    st.markdown(f"""
        <style>
        {f"@font-face {{ font-family: 'POE Helvetica UI'; src: url(data:font/ttf;base64,{font_b64}) format('truetype'); }}" if font_b64 else ""}
        
        * {{ 
            color: {TEXT_MAIN} !important; 
            font-family: 'POE Helvetica UI', 'Segoe UI', sans-serif !important; 
        }}
        .stApp {{ background-color: {BG_COLOR}; }}
        
        .header-text {{ color: {TEXT_MAIN} !important; font-family: 'POE Helvetica UI', sans-serif !important; }}
        .quickie-style {{
            text-align: right; font-family: 'Arial Rounded MT Bold', sans-serif !important;
            font-size: 48px; font-weight: bold; color: white !important;
            margin-top: -100px; position: relative; z-index: 1000;
        }}

        input, .stNumberInput div[data-baseweb="input"], .stSelectbox div[data-baseweb="select"] {{
            background-color: {INPUT_BG} !important;
            color: {INPUT_TEXT_COLOR} !important;
            -webkit-text-fill-color: {INPUT_TEXT_COLOR} !important;
            font-weight: bold !important;
            border: 2px solid {TEXT_MAIN} !important;
            border-radius: 8px !important;
        }}
        div.stButton > button {{
            background-color: {BTN_BG} !important;
            color: {BTN_TEXT} !important;
            border: 2px solid {BTN_TEXT} !important;
            font-weight: bold;
            border-radius: 8px;
        }}
        .result-highlight {{ color: white !important; font-size: 32px !important; font-weight: bold; }}
        .rechenweg {{ 
            background-color: rgba(255,255,255,0.2); 
            padding: 10px; border-radius: 5px; 
            color: white !important; font-family: monospace !important; margin-top: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

    # HEADER
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<h1 class="header-text">WP Quick-Kalkulator</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="header-text" style="font-size: 20px;">Heizlast-Ermittlung nach Verbrauch</p>', unsafe_allow_html=True)
    with col2:
        logo = "Coolsulting_Logo_ohneHG_outlines_weiss.png"
        if os.path.exists(logo):
            st.image(logo, use_container_width=True)
        st.markdown('<div class="quickie-style">Quickie</div>', unsafe_allow_html=True)

    st.write("---")

    # LOGIK-FUNKTION
    def calculate_heizlast(verbrauch_kwh, wirkungsgrad, hat_ww, personen):
        verlust_kwh = verbrauch_kwh * (1 - wirkungsgrad)
        nutzenergie_gesamt = verbrauch_kwh * wirkungsgrad
        
        ww_anteil = 0
        heizstunden = 2000
        
        if hat_ww:
            ww_anteil = personen * (1.45 * 2.0) * 365
            heizstunden = 2400
        else:
            ww_anteil = 0
            heizstunden = 2000
        
        heizenergie_pur = nutzenergie_gesamt - ww_anteil
        
        if heizenergie_pur < 0:
            return 0, 0, 0, 0, "Fehler: WW > Verbrauch", ""

        heizlast = heizenergie_pur / heizstunden
        rechenweg_str = f"({verbrauch_kwh:,.0f} * {wirkungsgrad:.2f} - {ww_anteil:,.0f} [WW]) / {heizstunden} h = {heizlast:.2f} kW"
        
        return heizlast, heizenergie_pur, ww_anteil, verlust_kwh, rechenweg_str

    # DIAGRAMM
    def plot_energy_pie(heizung, ww, verlust):
        labels = ['Heizwärme (Haus)', 'Warmwasser', 'Kessel-Verlust']
        values = [heizung, ww, verlust]
        colors = ['#FF4B4B', '#8B0000', '#D3D3D3'] 
        
        if ww <= 0:
            labels.pop(1)
            values.pop(1)
            colors.pop(1)
            
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, sort=False)])
        fig.update_traces(hoverinfo='label+percent+value', textinfo='percent', 
                          marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))
        fig.update_layout(showlegend=True, 
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          margin=dict(t=0, b=0, l=0, r=0),
                          legend=dict(font=dict(color='white')))
        return fig

    # TABS & INPUTS
    tab1, tab2 = st.tabs(["🔥 GAS-ERSATZ", "🛢️ ÖL-ERSATZ"])

    # GAS
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            v_gas = st.number_input("Jahresverbrauch Gas", 1000, 200000, 25000, key="qk_g_v")
            einheit = st.radio("Einheit", ["kWh", "m³"], horizontal=True, key="qk_g_e")
            wirk_gas = st.slider("Wirkungsgrad Altkessel (%)", 60, 105, 85, key="qk_g_w") / 100
        
        with c2:
            st.markdown("<b>Warmwasser-Einstellungen</b>", unsafe_allow_html=True)
            ww_gas_active = st.checkbox("Warmwasser über Gasheizung?", value=True, key="qk_g_ww")
            
            if ww_gas_active:
                pers_gas = st.slider("Personen im Haushalt", 1, 6, 3, key="qk_g_p")
                st.markdown(f"<span style='font-size:12px; opacity:0.7;'>Formel: 1,45 kWh x 2 x {pers_gas} Pers.</span>", unsafe_allow_html=True)
            else:
                pers_gas = 0

        if st.button("BERECHNUNG STARTEN (GAS)"):
            input_kwh = v_gas * 10.5 if einheit == "m³" else v_gas
            
            hl, heiz_e, ww_e, verlust_e, pfad = calculate_heizlast(input_kwh, wirk_gas, ww_gas_active, pers_gas)
            
            res_c1, res_c2 = st.columns([1, 1])
            with res_c1:
                st.markdown(f'<p style="color:white; font-size:18px;">Empfohlene Heizlast:</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result-highlight">{hl:.2f} kW</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="rechenweg"><b>RECHENWEG:</b><br>{pfad}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style='margin-top:20px; color:white;'>
                <b>Energie-Bilanz:</b><br>
                Eingesetzte Energie: {input_kwh:,.0f} kWh<br>
                Davon genutzt: {(heiz_e + ww_e):,.0f} kWh ({(heiz_e + ww_e)/input_kwh*100:.1f}%)
                </div>
                """, unsafe_allow_html=True)

            with res_c2:
                st.markdown('<p style="color:white; text-align:center;">Verbrauchs-Aufteilung</p>', unsafe_allow_html=True)
                fig = plot_energy_pie(heiz_e, ww_e, verlust_e)
                st.plotly_chart(fig, use_container_width=True)

    # ÖL
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            v_oil = st.number_input("Jahresverbrauch Öl (Liter)", 500, 20000, 2500, key="qk_o_v")
            wirk_oil = st.slider("Wirkungsgrad Altkessel (%)", 60, 105, 80, key="qk_o_w") / 100
        
        with c2:
            st.markdown("<b>Warmwasser-Einstellungen</b>", unsafe_allow_html=True)
            ww_oil_active = st.checkbox("Warmwasser über Ölheizung?", value=True, key="qk_o_ww")
            
            if ww_oil_active:
                pers_oil = st.slider("Personen im Haushalt", 1, 6, 3, key="qk_o_p")
                st.markdown(f"<span style='font-size:12px; opacity:0.7;'>Formel: 1,45 kWh x 2 x {pers_oil} Pers.</span>", unsafe_allow_html=True)
            else:
                pers_oil = 0

        if st.button("BERECHNUNG STARTEN (ÖL)"):
            input_kwh_o = v_oil * 10.0
            
            hl_o, heiz_e_o, ww_e_o, verlust_e_o, pfad_o = calculate_heizlast(input_kwh_o, wirk_oil, ww_oil_active, pers_oil)
            
            res_c1, res_c2 = st.columns([1, 1])
            with res_c1:
                st.markdown(f'<p style="color:white; font-size:18px;">Empfohlene Heizlast:</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="result-highlight">{hl_o:.2f} kW</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="rechenweg"><b>RECHENWEG:</b><br>{pfad_o}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style='margin-top:20px; color:white;'>
                <b>Energie-Bilanz:</b><br>
                Eingesetzte Energie: {input_kwh_o:,.0f} kWh<br>
                Davon genutzt: {(heiz_e_o + ww_e_o):,.0f} kWh ({(heiz_e_o + ww_e_o)/input_kwh_o*100:.1f}%)
                </div>
                """, unsafe_allow_html=True)

            with res_c2:
                st.markdown('<p style="color:white; text-align:center;">Verbrauchs-Aufteilung</p>', unsafe_allow_html=True)
                fig_o = plot_energy_pie(heiz_e_o, ww_e_o, verlust_e_o)
                st.plotly_chart(fig_o, use_container_width=True)

if __name__ == '__main__':
    main()
