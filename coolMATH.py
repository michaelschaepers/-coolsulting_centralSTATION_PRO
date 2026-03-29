# ============================================================================
# DATEI: coolMATH.py
# VERSION: 1.0.0
# STAND: 29.03.2026
# AUTOR: Michael Schäpers, coolsulting
# BESCHREIBUNG: °coolMATH – KI-Assistent für Kälte- und Klimatechnik (Gemini)
#               Gemini-Chat mit persistenter Memory via st.session_state
# ============================================================================

import streamlit as st
import os

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# ============================================================
# DESIGN
# ============================================================
BG_COLOR   = "#36A9E1"
TEXT_GRAY  = "#3C3C3B"
WHITE      = "#FFFFFF"

FONT_FILE  = "POE Vetica UI.ttf"
LOGO_PATH  = "Coolsulting_Logo_ohneHG_outlines_weiß.png"

def _get_font_b64(path):
    if os.path.exists(path):
        import base64
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def _inject_css():
    font_b64 = _get_font_b64(FONT_FILE)
    font_face = (
        f"@font-face {{ font-family: 'POE Helvetica UI'; "
        f"src: url(data:font/ttf;base64,{font_b64}) format('truetype'); }}"
        if font_b64 else ""
    )
    st.markdown(f"""
    <style>
    {font_face}
    html, body, [data-testid="stAppViewContainer"], * {{
        font-family: 'POE Helvetica UI', 'Helvetica', sans-serif !important;
    }}
    .stApp {{ background-color: {BG_COLOR}; }}

    /* Chat-Container */
    [data-testid="stChatMessage"] {{
        background-color: rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        margin-bottom: 8px !important;
    }}
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {{
        color: {WHITE} !important;
    }}
    /* Nutzernachrichten heller abheben */
    [data-testid="stChatMessage"][data-testid*="user"] {{
        background-color: rgba(255,255,255,0.22) !important;
    }}

    /* Chat-Eingabefeld */
    [data-testid="stChatInputContainer"] textarea {{
        background-color: rgba(255,255,255,0.15) !important;
        color: {WHITE} !important;
        border: 2px solid rgba(255,255,255,0.5) !important;
        border-radius: 10px !important;
    }}
    [data-testid="stChatInputContainer"] textarea::placeholder {{
        color: rgba(255,255,255,0.6) !important;
    }}

    /* Seitentitel */
    .cm-title {{
        font-size: 36px;
        font-weight: bold;
        color: {WHITE};
        margin-bottom: 0px;
    }}
    .cm-subtitle {{
        font-size: 14px;
        color: {TEXT_GRAY};
        margin-bottom: 20px;
    }}
    .cm-info-box {{
        background-color: rgba(255,255,255,0.15);
        border-radius: 10px;
        padding: 14px 18px;
        color: {WHITE};
        font-size: 14px;
        margin-bottom: 16px;
    }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# GEMINI INITIALISIERUNG  –  NUR EINMAL PRO SESSION
# ============================================================
SYSTEM_PROMPT = """Du bist °coolMATH, ein hochspezialisierter KI-Assistent für
Kälte- und Klimatechnik von coolsulting. Du hilfst Ingenieuren und Technikern bei:

- Kühllast- und Heizlastberechnungen
- Auslegung von Kälteanlagen, Wärmepumpen und Klimageräten
- Kältemittelfragen (R32, R410A, R290, R744 usw.)
- Rohrdimensionierung und Hydraulik
- Energieeffizienz und COP/EER-Berechnungen
- Normen und Vorschriften (EN 378, EN 12831, F-Gase-Verordnung)
- Samsung-Klimaanlagen und VRF-Systeme

Antworte präzise, professionell und auf Deutsch. Verwende Formeln und Zahlenwerte
wo sinnvoll. Wenn du Annahmen triffst, weise explizit darauf hin.
Gedächtnisfunktion: Du erinnerst dich an alle vorherigen Nachrichten in diesem Gespräch."""


def _init_gemini():
    """
    Initialisiert das Gemini-Modell und die Chat-Session EINMALIG in
    st.session_state. Bei nachfolgenden Streamlit-Reruns (Widget-Interaktionen)
    wird diese Funktion zwar erneut aufgerufen, aber der bestehende Chat bleibt
    erhalten – Gemini vergisst nichts mehr.
    """
    if not GEMINI_AVAILABLE:
        return False

    # API-Key aus Streamlit-Secrets oder Umgebungsvariable laden
    api_key = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("gemini_api_key")
    except Exception:
        pass
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        return False

    # ⚠️  WICHTIG: Chat-Session nur beim ersten Mal erstellen
    if "coolmath_chat" not in st.session_state:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=SYSTEM_PROMPT,
        )
        # history=[] → leerer Start; Gemini-Objekt übernimmt ab jetzt
        # die gesamte Konversationsverwaltung intern
        st.session_state.coolmath_chat = model.start_chat(history=[])

    # Anzeigeliste für st.chat_message ebenfalls einmalig initialisieren
    if "coolmath_messages" not in st.session_state:
        st.session_state.coolmath_messages = []

    return True


# ============================================================
# HAUPTFUNKTION
# ============================================================
def main():
    _inject_css()

    # --- HEADER ---
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
    with col_title:
        st.markdown('<div class="cm-title">°coolMATH</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="cm-subtitle">KI-Assistent für Kälte- und Klimatechnik | powered by Google Gemini</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # --- GEMINI INITIALISIERUNG ---
    ready = _init_gemini()

    if not GEMINI_AVAILABLE:
        st.error(
            "⚠️  Das Paket **google-generativeai** ist nicht installiert.\n\n"
            "Bitte ausführen: `pip install google-generativeai`"
        )
        return

    if not ready:
        st.warning(
            "🔑  Kein Gemini API-Key gefunden.\n\n"
            "Bitte hinterlege den Key als:\n"
            "- Streamlit-Secret: `GEMINI_API_KEY`\n"
            "- Oder Umgebungsvariable: `GEMINI_API_KEY` / `GOOGLE_API_KEY`"
        )
        with st.expander("Wie bekomme ich einen Gemini API-Key?"):
            st.markdown(
                "1. Gehe zu [Google AI Studio](https://aistudio.google.com/app/apikey)\n"
                "2. Erstelle einen neuen API-Key\n"
                "3. Trage ihn in `.streamlit/secrets.toml` ein:\n"
                "```toml\nGEMINI_API_KEY = \"dein-key-hier\"\n```"
            )
        return

    # --- CHAT-VERLAUF ANZEIGEN ---
    st.markdown(
        '<div class="cm-info-box">💬  Stelle Fragen zu Kühllast, Kältemitteln, '
        'Rohrdimensionierung, Wärmepumpen und mehr. Der Assistent erinnert sich '
        'an alle Nachrichten in dieser Sitzung.</div>',
        unsafe_allow_html=True,
    )

    for msg in st.session_state.coolmath_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- NEUE NACHRICHT ---
    if prompt := st.chat_input("Frage an °coolMATH stellen …"):
        # Nutzernachricht sofort anzeigen und speichern
        st.session_state.coolmath_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Antwort von Gemini holen
        # st.session_state.coolmath_chat enthält die vollständige History →
        # Gemini antwortet im Kontext aller bisherigen Nachrichten
        with st.chat_message("assistant"):
            with st.spinner("°coolMATH denkt …"):
                try:
                    response = st.session_state.coolmath_chat.send_message(prompt)
                    answer = response.text
                except Exception as e:
                    answer = f"⚠️  Fehler bei der Gemini-Anfrage: {str(e)}"

            st.markdown(answer)

        st.session_state.coolmath_messages.append(
            {"role": "assistant", "content": answer}
        )

    # --- SITZUNG ZURÜCKSETZEN ---
    st.markdown("---")
    if st.button("🔄  Gespräch zurücksetzen"):
        # Chat-Session und Anzeigeliste löschen → beim nächsten Rerun neu erstellt
        del st.session_state.coolmath_chat
        del st.session_state.coolmath_messages
        st.rerun()


if __name__ == "__main__":
    main()
