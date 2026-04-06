# modules/auth.py
# °coolWIRE v1.0 – Authentifizierung & Nutzerverwaltung
# (c) coolsulting e.U. | Michael Schäpers

import streamlit as st
import hashlib
import hmac
from datetime import datetime

# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================

def _hash_passwort(passwort: str) -> str:
    """SHA256-Hash eines Passworts."""
    return hashlib.sha256(passwort.encode()).hexdigest()


def _lade_nutzer_aus_secrets() -> dict:
    """
    Lädt Nutzer aus st.secrets.
    Struktur in secrets.toml:
      [users]
      michael = "passwort_klartext"
      [roles]
      michael = "admin"
    """
    nutzer = {}
    try:
        users_raw = dict(st.secrets.get("users", {}))
        roles_raw = dict(st.secrets.get("roles", {}))
        display_raw = dict(st.secrets.get("display_names", {}))

        for username, passwort in users_raw.items():
            nutzer[username.lower()] = {
                "username": username.lower(),
                "display_name": display_raw.get(username, username.title()),
                "passwort_hash": _hash_passwort(str(passwort)),
                "rolle": roles_raw.get(username, "partner"),
                "quelle": "secrets"
            }
    except Exception:
        pass
    return nutzer


def _lade_nutzer_dynamisch() -> dict:
    """Lädt zur Laufzeit angelegte Nutzer aus Session State (Admin-Funktion)."""
    return st.session_state.get("_dynamic_users", {})


def _speichere_dynamischen_nutzer(username: str, passwort: str,
                                   display_name: str, rolle: str):
    """Speichert einen neuen Nutzer im Session State (temporär bis Neustart)."""
    if "_dynamic_users" not in st.session_state:
        st.session_state["_dynamic_users"] = {}

    st.session_state["_dynamic_users"][username.lower()] = {
        "username": username.lower(),
        "display_name": display_name or username.title(),
        "passwort_hash": _hash_passwort(passwort),
        "rolle": rolle,
        "quelle": "dynamisch",
        "angelegt_am": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "angelegt_von": st.session_state.get("username", "admin")
    }


def _loesche_dynamischen_nutzer(username: str):
    """Entfernt einen dynamisch angelegten Nutzer."""
    dynamic = st.session_state.get("_dynamic_users", {})
    dynamic.pop(username.lower(), None)
    st.session_state["_dynamic_users"] = dynamic


def get_alle_nutzer() -> dict:
    """Gibt alle Nutzer (secrets + dynamisch) zurück."""
    nutzer = _lade_nutzer_aus_secrets()
    nutzer.update(_lade_nutzer_dynamisch())
    return nutzer


def pruefe_login(username: str, passwort: str) -> dict | None:
    """
    Prüft Zugangsdaten. Gibt Nutzerdaten zurück oder None.
    """
    alle = get_alle_nutzer()
    user_key = username.strip().lower()
    if user_key not in alle:
        return None
    nutzer = alle[user_key]
    if hmac.compare_digest(nutzer["passwort_hash"], _hash_passwort(passwort)):
        return nutzer
    return None


def ist_eingeloggt() -> bool:
    return st.session_state.get("eingeloggt", False)


def ist_admin() -> bool:
    return st.session_state.get("rolle", "") == "admin"


def get_display_name() -> str:
    return st.session_state.get("display_name", "Nutzer")


def logout():
    for key in ["eingeloggt", "username", "rolle", "display_name"]:
        st.session_state.pop(key, None)

# =============================================================================
# LOGIN-FORMULAR
# =============================================================================

def zeige_login():
    """Zeigt das Login-Formular. Gibt True zurück wenn erfolgreich."""

    # Zentriertes Layout
    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown("""
        <div style="text-align:center; padding: 2rem 0 1rem 0;">
            <div style="
                background: linear-gradient(135deg, #1a6fa8 0%, #36A9E1 100%);
                color: white;
                border-radius: 16px;
                padding: 2rem 2rem 1.5rem 2rem;
                box-shadow: 0 8px 32px rgba(54,169,225,0.3);
            ">
                <div style="font-size:2.5rem;">⚡</div>
                <div style="font-size:1.6rem; font-weight:800; letter-spacing:-1px;">°coolWIRE</div>
                <div style="font-size:0.8rem; opacity:0.85; margin-top:4px;">
                    Kabelplanungstool · coolsulting e.U.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            st.markdown("**Benutzername**")
            username = st.text_input("", placeholder="z.B. michael", label_visibility="collapsed")
            st.markdown("**Passwort**")
            passwort = st.text_input("", type="password", placeholder="••••••••",
                                      label_visibility="collapsed")
            submitted = st.form_submit_button("🔐 Anmelden", use_container_width=True, type="primary")

        if submitted:
            if not username or not passwort:
                st.error("Bitte Benutzername und Passwort eingeben.")
                return False

            nutzer = pruefe_login(username, passwort)
            if nutzer:
                st.session_state["eingeloggt"] = True
                st.session_state["username"] = nutzer["username"]
                st.session_state["rolle"] = nutzer["rolle"]
                st.session_state["display_name"] = nutzer["display_name"]
                st.rerun()
                return True
            else:
                st.error("❌ Ungültige Zugangsdaten.")
                return False

        st.markdown("""
        <div style="text-align:center; margin-top:1.5rem; color:#aaa; font-size:0.75rem;">
            Zugang nur für autorisierte Nutzer<br>
            coolsulting e.U. · Mozartstraße 11, 4020 Linz
        </div>
        """, unsafe_allow_html=True)

    return False

# =============================================================================
# ADMIN: NUTZERVERWALTUNG
# =============================================================================

def zeige_nutzerverwaltung():
    """Vollständige Nutzerverwaltung für Admins."""

    st.markdown("""
    <div style="border-left:4px solid #36A9E1; padding-left:12px;
                font-size:1.05rem; font-weight:700; margin-bottom:1rem;">
        👥 Nutzerverwaltung
    </div>
    """, unsafe_allow_html=True)

    alle_nutzer = get_alle_nutzer()

    # -----------------------------------------------------------------------
    # Nutzerübersicht
    # -----------------------------------------------------------------------
    st.markdown("**Aktuelle Nutzer**")

    if alle_nutzer:
        import pandas as pd
        rows = []
        for u, data in alle_nutzer.items():
            rows.append({
                "Benutzername": data["username"],
                "Anzeigename": data["display_name"],
                "Rolle": "🔑 Admin" if data["rolle"] == "admin" else "🤝 Partner",
                "Quelle": "🔒 secrets.toml" if data.get("quelle") == "secrets" else "✏️ Dynamisch",
                "Angelegt am": data.get("angelegt_am", "–"),
                "Angelegt von": data.get("angelegt_von", "–"),
            })

        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={
                         "Rolle": st.column_config.TextColumn(width=100),
                         "Quelle": st.column_config.TextColumn(width=130),
                     })
    else:
        st.info("Keine Nutzer gefunden.")

    st.markdown("---")

    # -----------------------------------------------------------------------
    # Neuen Nutzer anlegen
    # -----------------------------------------------------------------------
    st.markdown("**Neuen Nutzer anlegen**")
    st.caption("Hinweis: Dynamisch angelegte Nutzer bleiben bis zum App-Neustart aktiv. "
               "Für dauerhafte Zugänge → secrets.toml aktualisieren.")

    with st.form("neuer_nutzer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            neu_username = st.text_input("Benutzername *", placeholder="z.B. lexx")
            neu_passwort = st.text_input("Passwort *", type="password", placeholder="Min. 6 Zeichen")
        with col2:
            neu_display = st.text_input("Anzeigename", placeholder="z.B. LEXX Kälte GmbH")
            neu_rolle = st.selectbox("Rolle", ["partner", "admin"],
                                      format_func=lambda x: "🤝 Partner" if x == "partner" else "🔑 Admin")

        anlegen = st.form_submit_button("➕ Nutzer anlegen", type="primary", use_container_width=True)

    if anlegen:
        if not neu_username or not neu_passwort:
            st.error("Benutzername und Passwort sind Pflichtfelder.")
        elif len(neu_passwort) < 6:
            st.error("Passwort muss mindestens 6 Zeichen haben.")
        elif neu_username.lower() in alle_nutzer:
            st.error(f"Benutzername '{neu_username}' existiert bereits.")
        else:
            _speichere_dynamischen_nutzer(neu_username, neu_passwort, neu_display, neu_rolle)
            st.success(f"✅ Nutzer '{neu_username}' ({neu_rolle}) angelegt.")
            st.rerun()

    st.markdown("---")

    # -----------------------------------------------------------------------
    # Dynamischen Nutzer löschen
    # -----------------------------------------------------------------------
    dynamic_users = _lade_nutzer_dynamisch()
    if dynamic_users:
        st.markdown("**Dynamischen Nutzer entfernen**")
        zu_loeschen = st.selectbox(
            "Nutzer auswählen",
            options=list(dynamic_users.keys()),
            format_func=lambda u: f"{dynamic_users[u]['display_name']} ({u})"
        )
        if st.button("🗑️ Nutzer entfernen", type="secondary"):
            _loesche_dynamischen_nutzer(zu_loeschen)
            st.success(f"Nutzer '{zu_loeschen}' entfernt.")
            st.rerun()
    else:
        st.caption("Keine dynamisch angelegten Nutzer vorhanden.")

    st.markdown("---")

    # -----------------------------------------------------------------------
    # Anleitung für dauerhafte Nutzer
    # -----------------------------------------------------------------------
    with st.expander("📋 Dauerhafte Nutzer in secrets.toml eintragen"):
        st.code("""
# .streamlit/secrets.toml

[users]
michael  = "dein_passwort"
niklas   = "passwort2"
polar    = "polar_pw"
weichselbaumer = "wb_pw"
venturi  = "venturi_pw"
hörtenhuber = "hoe_pw"
kristandl = "kri_pw"
lexx     = "lexx_pw"
arktis   = "arktis_pw"

[roles]
michael  = "admin"
niklas   = "admin"
polar    = "partner"
weichselbaumer = "partner"
venturi  = "partner"
hörtenhuber = "partner"
kristandl = "partner"
lexx     = "partner"
arktis   = "partner"

[display_names]
michael  = "Michael Schäpers"
niklas   = "Niklas Reisner"
polar    = "Polar Energy"
weichselbaumer = "Weichselbaumer GmbH"
venturi  = "Venturi Kälte OHG"
hörtenhuber = "Hörtenhuber"
kristandl = "Kristandl"
lexx     = "LEXX"
arktis   = "Arktis"
""", language="toml")
        st.caption("Diese Datei liegt NUR auf dem Server / in Streamlit Cloud Secrets – niemals im Repo!")
