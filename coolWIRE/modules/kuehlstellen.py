# modules/kuehlstellen.py
# °coolWIRE v2.0 – Kühlstellen-Datenmodell & Komponentendefinitionen
# (c) coolsulting e.U. | Michael Schäpers

import copy
from datetime import datetime

# =============================================================================
# VERDAMPFUNGSTEMPERATUR-BEREICHE
# =============================================================================

TEMP_BEREICHE = {
    "HNK": {
        "label": "HNK – Hochnormalkühlung",
        "verdampfung_c": +5,
        "raum_temp_c": (+12, +18),
        "farbe": "#27AE60",
        "beispiele": "Obst, Gemüse, Weinkeller"
    },
    "NK": {
        "label": "NK – Normalkühlung",
        "verdampfung_c": -8,
        "raum_temp_c": (0, +8),
        "farbe": "#36A9E1",
        "beispiele": "Fleisch, Molkerei, Kühlraum allgemein"
    },
    "NK+": {
        "label": "NK+ – Tiefnormalkühlung",
        "verdampfung_c": -10,
        "raum_temp_c": (-5, +2),
        "farbe": "#2980B9",
        "beispiele": "Frische Fische, Eis, Gärverzögerung"
    },
    "TK": {
        "label": "TK – Tiefkühlung",
        "verdampfung_c": -31,
        "raum_temp_c": (-22, -18),
        "farbe": "#8E44AD",
        "beispiele": "Tiefkühlraum, TK-Truhe"
    },
    "TK+": {
        "label": "TK+ – Schockfrost",
        "verdampfung_c": -33,
        "raum_temp_c": (-40, -30),
        "farbe": "#6C3483",
        "beispiele": "Schockfroster, Blast Freezer"
    },
    "CUSTOM": {
        "label": "Benutzerdefiniert",
        "verdampfung_c": None,
        "raum_temp_c": (None, None),
        "farbe": "#E67E22",
        "beispiele": "Freie Eingabe"
    }
}

# =============================================================================
# KOMPONENTEN-DEFINITIONEN
# =============================================================================

KOMPONENTEN = {

    # -------------------------------------------------------------------------
    # VERDAMPFER / LÜFTER
    # -------------------------------------------------------------------------
    "verdampfer_luefter": {
        "label": "Verdampfer / Lüftermotor",
        "icon": "❄️",
        "gruppe": "Verdampfer",
        "pflicht": True,
        "parameter": {
            "anzahl_verdampfer": {
                "typ": "zahl",
                "label": "Anzahl Verdampfer",
                "min": 1, "max": 10,
                "vorschlag": 1,
                "hinweis": "Bei mehreren Verdampfern pro Kühlstelle z.B. große Kühlhallen – jeder Verdampfer bekommt eigenes Kabel"
            },
            "spannung": {
                "typ": "auswahl",
                "label": "Spannung Lüftermotor",
                "optionen": ["230V 1-phasig", "400V 3-phasig"],
                "vorschlag": "230V 1-phasig",
                "hinweis": "230V Standard bis ca. 750W je Lüfter – ab 1kW → 400V empfohlen"
            },
            "anzahl_luefter": {
                "typ": "zahl",
                "label": "Anzahl Lüfter je Verdampfer",
                "min": 1, "max": 8,
                "vorschlag": 1,
                "hinweis": "Standard: 1 Lüfter pro Verdampfer. Nur erhöhen wenn im Plan explizit mehrere erkennbar sind"
            },
            "leistung_w": {
                "typ": "zahl",
                "label": "Leistung je Lüfter [W]",
                "min": 10, "max": 5000,
                "vorschlag": 150
            }
        },
        "kabel_mapping": {
            "230V 1-phasig": "EM-VD-L",
            "400V 3-phasig": "EM-VD-3P"
        }
    },

    # -------------------------------------------------------------------------
    "abtauheizung": {
        "label": "Abtauheizung",
        "icon": "🔥",
        "gruppe": "Verdampfer",
        "pflicht": False,
        "parameter": {
            "spannung": {
                "typ": "auswahl",
                "label": "Spannung Abtauheizung",
                "optionen": ["230V 1-phasig", "400V 3-phasig"],
                "vorschlag": "230V 1-phasig",
                "hinweis": "Standard ist 230V, bei großen Verdampfern (>3kW) → 400V sinnvoll"
            },
            "leistung_w": {
                "typ": "zahl",
                "label": "Abtauleistung [W]",
                "min": 100, "max": 20000,
                "vorschlag": 800
            },
            "typ_abtau": {
                "typ": "auswahl",
                "label": "Abtauart",
                "optionen": ["Elektro-Abtau", "Heißgas-Abtau", "Natural (Umlufttauen)"],
                "vorschlag": "Elektro-Abtau",
                "hinweis": "Heißgas-Abtau: kein Heizungskabel, aber Magnetventil nötig"
            }
        },
        "kabel_mapping": {
            "Elektro-Abtau": "EM-VD-ABT",
            "Heißgas-Abtau": "VA-ABT",
            "Natural (Umlufttauen)": None
        }
    },

    # -------------------------------------------------------------------------
    "temperaturfuehler_innen": {
        "label": "Temperaturfühler Innenraum",
        "icon": "🌡️",
        "gruppe": "Fühler",
        "pflicht": True,
        "parameter": {
            "typ_fuehler": {
                "typ": "auswahl",
                "label": "Fühlertyp",
                "optionen": ["NTC", "PT100", "PT1000"],
                "vorschlag": "NTC",
                "hinweis": "NTC: Standard Kälte, PT100/PT1000: bei MSR/SPS oder langen Leitungen"
            },
            "anzahl": {
                "typ": "zahl",
                "label": "Anzahl Fühler",
                "min": 1, "max": 6,
                "vorschlag": 1
            }
        },
        "kabel_mapping": {
            "NTC": "EM-VD-TF",
            "PT100": "MSR-TF-PT100",
            "PT1000": "MSR-TF-PT100"
        }
    },

    # -------------------------------------------------------------------------
    "temperaturfuehler_abtau": {
        "label": "Abtaufühler (am Verdampfer)",
        "icon": "🌡️",
        "gruppe": "Fühler",
        "pflicht": True,
        "parameter": {
            "typ_fuehler": {
                "typ": "auswahl",
                "label": "Fühlertyp",
                "optionen": ["NTC", "PT100"],
                "vorschlag": "NTC",
                "hinweis": "Abtauendpunkt-Erkennung, direkt am Verdampferblock"
            }
        },
        "kabel_mapping": {
            "NTC": "EM-VD-TF",
            "PT100": "MSR-TF-PT100"
        }
    },

    # -------------------------------------------------------------------------
    "eev": {
        "label": "Elektronisches Expansionsventil (EEV)",
        "icon": "🎛️",
        "gruppe": "Regelung",
        "pflicht": False,
        "parameter": {
            "eev_typ": {
                "typ": "auswahl",
                "label": "EEV-Typ / Ausführung",
                "optionen": [
                    "Schrittmotor EEV + externer Treiber (Standard)",
                    "Carel EVD ice / EVD Evolution (vormontiert am Verdampfer)",
                    "PWM-Ventil Danfoss AKV (Magnetspule)",
                    "Schrittmotor EEV – Treiber integriert im Regler",
                ],
                "vorschlag": "Schrittmotor EEV + externer Treiber (Standard)",
                "hinweis": (
                    "Schrittmotor + Treiber: Motorkabel MAX 5–8m (Treiber sitzt nah am Ventil)! "
                    "EVD ice: Elektronik am Verdampfer vormontiert → nur 230V Versorgung wie Magnetventil. "
                    "PWM AKV: einfache Magnetspule → 2-adriges Steuerkabel vom Regler. "
                    "Treiber integriert im Regler: Motorkabel direkt zum Regler max. 8m!"
                )
            },
            "hersteller": {
                "typ": "auswahl",
                "label": "Hersteller / Modell",
                "optionen": [
                    "Danfoss ETS + AKV (Treiber)",
                    "Danfoss ETS + EKE 1A (Treiber)",
                    "Alco EX + ECM (Treiber)",
                    "Carel EVD ice (integriert)",
                    "Carel EVD Evolution (integriert)",
                    "Sanhua SEI + Treiber",
                    "Sporlan SEI + Treiber",
                    "Sonstiger"
                ],
                "vorschlag": "Danfoss ETS + AKV (Treiber)",
                "hinweis": "Anschlussbelegung je nach Hersteller – Datenblatt prüfen"
            },
            "treiber_standort": {
                "typ": "auswahl",
                "label": "Treiber-Standort (nur bei externem Treiber)",
                "optionen": [
                    "Direkt am Verdampfer / Ventil (max. 5m Motorkabel)",
                    "Schaltkasten an der Zelle",
                    "Zentraler Schaltschrank (NUR wenn Motorkabel ≤8m!)",
                ],
                "vorschlag": "Direkt am Verdampfer / Ventil (max. 5m Motorkabel)",
                "hinweis": "WICHTIG: Motorkabel Schrittmotor max. 5–8m! Längeres Kabel zerstört Treiber/Motor durch Induktivität!"
            },
            "laenge_motorkabel_m": {
                "typ": "zahl",
                "label": "Länge Motorkabel Ventil → Treiber [m]",
                "min": 0, "max": 8,
                "vorschlag": 3,
                "hinweis": "Absolutes Maximum: 8m – besser 3–5m. Bei EVD ice / PWM: dieses Feld irrelevant."
            }
        },
        "kabel_mapping": "EEV-MOT"
    },

    # -------------------------------------------------------------------------
    "gehaeuse_heizung": {
        "label": "Gehäuse-/Kondensatheizung",
        "icon": "♨️",
        "gruppe": "Verdampfer",
        "pflicht": False,
        "parameter": {
            "spannung": {
                "typ": "auswahl",
                "label": "Spannung",
                "optionen": ["230V 1-phasig"],
                "vorschlag": "230V 1-phasig",
                "hinweis": "Immer 230V, Dauerbetrieb, Silikonleitung SIHF"
            },
            "leistung_w": {
                "typ": "zahl",
                "label": "Heizleistung [W]",
                "min": 10, "max": 500,
                "vorschlag": 40
            }
        },
        "kabel_mapping": "EM-VD-HZ"
    },

    # -------------------------------------------------------------------------
    "tuer_heizung": {
        "label": "Türrahmenheizung",
        "icon": "🚪",
        "gruppe": "Zubehör",
        "pflicht": False,
        "parameter": {
            "spannung": {
                "typ": "auswahl",
                "label": "Spannung",
                "optionen": ["230V 1-phasig", "24V DC"],
                "vorschlag": "230V 1-phasig",
                "hinweis": "230V Standard, 24V nur bei speziellen Systemen"
            }
        },
        "kabel_mapping": "GA-KZ-TUE"
    },

    # -------------------------------------------------------------------------
    "ablaufheizung": {
        "label": "Ablaufheizung (Kondensat)",
        "icon": "🌊",
        "gruppe": "Verdampfer",
        "pflicht": False,
        "auto_aktivierung": "raum_temp_soll_c < -1",
        "parameter": {
            "spannung": {
                "typ": "auswahl",
                "label": "Spannung",
                "optionen": ["230V 1-phasig", "24V AC"],
                "vorschlag": "230V 1-phasig",
                "hinweis": "Nur bei Raumtemperaturen unter -1°C notwendig – Kondensatwasser würde sonst einfrieren"
            },
            "leistung_w": {
                "typ": "zahl",
                "label": "Heizleistung [W]",
                "min": 10, "max": 500,
                "vorschlag": 25,
                "hinweis": "Typisch 15–50W, Silikonheizkabel im Ablaufrohr"
            },
            "typ_heizung": {
                "typ": "auswahl",
                "label": "Ausführung",
                "optionen": [
                    "Silikonheizkabel im Ablaufrohr",
                    "Ablaufwanne beheizt",
                    "Ablaufrohr + Wanne beheizt",
                ],
                "vorschlag": "Silikonheizkabel im Ablaufrohr",
                "hinweis": "Dauerbetrieb oder thermostatgesteuert – Silikonleitung SIHF verwenden"
            }
        },
        "kabel_mapping": "EM-VD-HZ"
    },

    # -------------------------------------------------------------------------
    "tuer_kontakt": {
        "label": "Türkontakt",
        "icon": "🚪",
        "gruppe": "Zubehör",
        "pflicht": True,
        "parameter": {
            "anzahl_tueren": {
                "typ": "zahl",
                "label": "Anzahl Türen",
                "min": 1, "max": 10,
                "vorschlag": 1,
                "hinweis": "1 Türkontakt pro Tür – pro Tür ein separates Kabel einplanen"
            },
            "typ": {
                "typ": "auswahl",
                "label": "Kontakttyp",
                "optionen": ["NC (Schließer)", "NO (Öffner)"],
                "vorschlag": "NC (Schließer)",
                "hinweis": "NC = Schließer: Alarm bei offenem Kontakt – empfohlen für Überwachung"
            },
            "tuerlicht_schaltung": {
                "typ": "bool",
                "label": "Türkontakt schaltet Innenlicht",
                "vorschlag": True,
                "hinweis": "Türkontakt steuert Innenbeleuchtung – spart Energie wenn Tür zu"
            }
        },
        "kabel_mapping": "GA-KZ-TUE"
    },

    # -------------------------------------------------------------------------
    "innenbeleuchtung": {
        "label": "Innenbeleuchtung",
        "icon": "💡",
        "gruppe": "Zubehör",
        "pflicht": True,
        "parameter": {
            "licht_typ": {
                "typ": "auswahl",
                "label": "Leuchtmitteltyp",
                "optionen": ["LED (Standard)", "LED feuchtraumgeeignet IP65", "LED tiefkühlgeeignet IP66 -40°C", "Leuchtstofflampe (Altbestand)"],
                "vorschlag": "LED feuchtraumgeeignet IP65",
                "hinweis": "TK-Bereich: LED min. IP66 und für -40°C geeignet verwenden"
            },
            "spannung": {
                "typ": "auswahl",
                "label": "Spannung",
                "optionen": ["230V 1-phasig", "24V DC (Sicherheitsbeleuchtung)"],
                "vorschlag": "230V 1-phasig"
            },
            "schaltung": {
                "typ": "auswahl",
                "label": "Schaltung",
                "optionen": ["Türkontakt (automatisch)", "Lichtschalter innen", "Türkontakt + Lichtschalter", "Regler gesteuert"],
                "vorschlag": "Türkontakt (automatisch)",
                "hinweis": "Türkontakt-Schaltung spart Energie – Licht aus wenn Tür geschlossen"
            },
            "leistung_w": {
                "typ": "zahl",
                "label": "Leistung gesamt [W]",
                "min": 5, "max": 2000,
                "vorschlag": 30
            }
        },
        "kabel_mapping": "GA-THE-LED"
    },

    # -------------------------------------------------------------------------
    "bewegungsmelder": {
        "label": "Bewegungsmelder",
        "icon": "👁️",
        "gruppe": "Zubehör",
        "pflicht": True,
        "parameter": {
            "typ_melder": {
                "typ": "auswahl",
                "label": "Meldertyp",
                "optionen": ["PIR (passiv infrarot, Standard)", "Mikrowelle (für TK -40°C)", "Dual PIR+Mikrowelle"],
                "vorschlag": "PIR (passiv infrarot, Standard)",
                "hinweis": "TK-Bereich: Standard-PIR bis ca. -25°C, darunter Mikrowellen-Melder verwenden"
            },
            "funktion": {
                "typ": "auswahl",
                "label": "Funktion",
                "optionen": ["Lichtschaltung", "Alarmanlage / Einbruch", "Licht + Alarm", "Energiesparmodus Verdampfer"],
                "vorschlag": "Lichtschaltung",
                "hinweis": "Kombination Licht+Alarm spart separate Verdrahtung"
            },
            "spannung": {
                "typ": "auswahl",
                "label": "Spannung",
                "optionen": ["230V 1-phasig", "12V DC", "24V DC"],
                "vorschlag": "230V 1-phasig"
            }
        },
        "kabel_mapping": "GA-KZ-TUE"
    },

    # -------------------------------------------------------------------------
    "personennotruf": {
        "label": "Personennotruf (EN 378)",
        "icon": "🚨",
        "gruppe": "Sicherheit",
        "pflicht": False,
        "parameter": {
            "taster_innen": {
                "typ": "bool",
                "label": "Notruf-Taster innen",
                "vorschlag": True,
                "hinweis": "Pflicht bei begehbaren Kühlräumen EN 378-3"
            },
            "horn_aussen": {
                "typ": "bool",
                "label": "Akustischer Alarm außen",
                "vorschlag": True
            },
            "blitz_aussen": {
                "typ": "bool",
                "label": "Optischer Alarm (Blitzleuchte)",
                "vorschlag": True
            },
            "zentrale_meldung": {
                "typ": "bool",
                "label": "Zentrale Meldung / BMS",
                "vorschlag": False
            }
        },
        "kabel_mapping": ["PA-NT-TAST", "PA-NT-HORN", "PA-NT-LED", "PA-NT-VER"]
    },

    # -------------------------------------------------------------------------
    "gaswarnanlage": {
        "label": "Gaswarnanlage (GWA)",
        "icon": "⚠️",
        "gruppe": "Sicherheit",
        "pflicht": False,
        "parameter": {
            "kaeltemittel": {
                "typ": "auswahl",
                "label": "Kältemittel",
                "optionen": ["R290 (Propan)", "R600a (Isobutan)", "NH3 (Ammoniak)",
                             "CO2 (R744)", "R32", "R410A", "R404A", "R134a", "Sonstiges"],
                "vorschlag": "R290 (Propan)",
                "hinweis": "Bestimmt Sensor-Typ und ATEX-Anforderung"
            },
            "sensor_typ": {
                "typ": "auswahl",
                "label": "Sensortyp",
                "optionen": ["4-20mA Analog", "RS485 Digital", "Binär (Ein/Aus)"],
                "vorschlag": "4-20mA Analog"
            }
        },
        "kabel_mapping": ["MSR-GWA-SEN", "MSR-GWA-HORN", "MSR-GWA-REL"]
    },

    # -------------------------------------------------------------------------
    "monitoring_kiconex": {
        "label": "Monitoring Kiconex / ICOOL",
        "icon": "🌐",
        "gruppe": "Monitoring",
        "pflicht": False,
        "parameter": {
            "schnittstelle": {
                "typ": "auswahl",
                "label": "Schnittstelle",
                "optionen": ["RS485 Modbus", "Ethernet LAN", "RS485 + LAN"],
                "vorschlag": "RS485 Modbus",
                "hinweis": "RS485: direkt an Regler, LAN: Gateway zum Router"
            }
        },
        "kabel_mapping": ["ICK-RS485", "ICK-VER"]
    },

    # -------------------------------------------------------------------------
    "schaltkasten": {
        "label": "Kühlstellenregler / Steuerung",
        "icon": "🔌",
        "gruppe": "Steuerung",
        "pflicht": True,
        "parameter": {
            "steuerung_typ": {
                "typ": "auswahl",
                "label": "Steuerungsart",
                "optionen": [
                    "Eigener Regler (coolsulting liefert)",
                    "Fremdsteuerung am Gerät – Bus-kompatibel (Standard)",
                    "Fremdsteuerung am Gerät – Bus NICHT kompatibel",
                    "Fremdsteuerung am Gerät – unbekannt",
                ],
                "vorschlag": "Eigener Regler (coolsulting liefert)",
                "hinweis": (
                    "Bus-kompatibel: Regler im Gerät hat RS485/Modbus – wir legen nur Busleitung und ggf. HACCP-Fühler. "
                    "Bus NICHT kompatibel: kein Datenbus möglich, nur potenzialfreie Kontakte (Stoermeldung, Abtau). "
                    "Fremdsteuerung = Regler ist im Gerät verbaut (Kühlmöbel, Gastrogerät)."
                )
            },
            "regler_typ": {
                "typ": "auswahl",
                "label": "Reglertyp (nur bei eigenem Regler)",
                "optionen": [
                    "Intarcon MTM-N-11161 / XM670 (Standard)",
                    "Danfoss EKC 202 / AK-CC 210",
                    "Danfoss EKC 301 / AK-CC 550",
                    "Wurm UDO-4",
                    "Wurm UNO-4",
                    "Pego Nector",
                    "Carel Ultracella UCO*H",
                    "Carel IR33",
                    "Eliwell ID974",
                    "Eliwell EWPC 900",
                    "Dixell XR75CX",
                    "Dixell XR60CX",
                    "Sonstiger / Fremdregler",
                ],
                "vorschlag": "Intarcon MTM-N-11161 / XM670 (Standard)",
                "hinweis": "Nur relevant wenn eigener Regler geliefert wird. Bei Fremdsteuerung: Regler-Typ des Geräts eintragen falls bekannt."
            },
            "bus_protokoll": {
                "typ": "auswahl",
                "label": "Bus-Protokoll (bei Bus-kompatibel)",
                "optionen": [
                    "RS485 Modbus RTU (Standard)",
                    "RS485 proprietär (Hersteller-Bus)",
                    "CAN-Bus",
                    "LON",
                    "Kein Bus",
                ],
                "vorschlag": "RS485 Modbus RTU (Standard)",
                "hinweis": "RS485 Modbus: Standard bei Dixell, Carel, Danfoss, Pego. Bei Bus-kompatibel: nur Busleitung + HACCP-Fühler nötig."
            },
            "montageort": {
                "typ": "auswahl",
                "label": "Montageort Regler",
                "optionen": [
                    "An der Kuehlzelle (Front)",
                    "Im Geraet integriert (Fremdsteuerung)",
                    "Im zentralen Schaltschrank",
                    "Schaltschrank + Bedienteil an Zelle",
                    "Im Aggregatschrank",
                ],
                "vorschlag": "An der Kuehlzelle (Front)",
                "hinweis": "Fremdsteuerung: Regler ist im Gerät verbaut – kein eigener Einbau nötig"
            },
            "versorgung": {
                "typ": "auswahl",
                "label": "Spannungsversorgung",
                "optionen": ["230V 1-phasig", "400V 3-phasig", "Geraet selbstversorgt"],
                "vorschlag": "230V 1-phasig",
                "hinweis": "Bei Kühlmöbeln/Gastrogeräten: oft selbstversorgt aus Geräteanschluss"
            }
        },
        "kabel_mapping": "EM-VD-SK"
    },

    # -------------------------------------------------------------------------
    "magnetventil": {
        "label": "Magnetventil Liquid Line",
        "icon": "🔧",
        "gruppe": "Regelung",
        "pflicht": False,
        "parameter": {
            "spannung": {
                "typ": "auswahl",
                "label": "Spulenspannung",
                "optionen": ["230V AC", "24V AC", "24V DC", "12V DC"],
                "vorschlag": "230V AC",
                "hinweis": "230V AC: Standard – Danfoss EVR, Castel, Alco. 24V nur bei speziellen Zentralsteuerungen. Kabel: 3x1,0mm² oder 3x1,5mm² – Spulenstrom typisch unter 0,1A."
            },
            "anzahl": {
                "typ": "zahl",
                "label": "Anzahl Magnetventile",
                "min": 1, "max": 6,
                "vorschlag": 1,
                "hinweis": "1x Liquid Line Standard. Bei Heißgasabtau: zusätzlich Heißgasventil."
            }
        },
        "kabel_mapping": "EM-VD-L"
    },

    # -------------------------------------------------------------------------
    "druckfuehler": {
        "label": "Druckfühler HD/ND",
        "icon": "📊",
        "gruppe": "Fühler",
        "pflicht": False,
        "parameter": {
            "typ": {
                "typ": "auswahl",
                "label": "Signaltyp",
                "optionen": ["4-20mA", "0-10V", "Binär (Pressostat)"],
                "vorschlag": "4-20mA",
                "hinweis": "4-20mA: genauere Regelung, Pressostat: nur Sicherheitsabschaltung"
            },
            "anzahl": {
                "typ": "zahl",
                "label": "Anzahl (HD+ND)",
                "min": 1, "max": 4,
                "vorschlag": 2
            }
        },
        "kabel_mapping": "EEV-DRUCK"
    },

    # -------------------------------------------------------------------------
    "haccp_aufzeichnung": {
        "label": "HACCP Temperaturaufzeichnung",
        "icon": "📋",
        "gruppe": "HACCP",
        "pflicht": True,
        "parameter": {
            "anzahl_fuehler": {
                "typ": "zahl",
                "label": "Anzahl Temperaturfühler je Raum",
                "min": 1, "max": 6,
                "vorschlag": 1,
                "hinweis": "Standard: 1 Fühler pro Raum. Großräume (>200m³) oder HACCP-Klasse A: 2 Fühler empfohlen"
            },
            "fuehler_typ": {
                "typ": "auswahl",
                "label": "Fühlertyp",
                "optionen": ["NTC (Standard)", "PT100", "PT1000", "4-20mA (kalibrierbar)"],
                "vorschlag": "NTC (Standard)",
                "hinweis": "NTC: günstig, ausreichend für Standardanwendungen. PT100/PT1000: höhere Genauigkeit, für akkreditierte HACCP-Systeme"
            },
            "aufzeichnung_system": {
                "typ": "auswahl",
                "label": "Aufzeichnungssystem",
                "optionen": [
                    "Regler-intern (Datalogging im Regler)",
                    "Dixell Xweb (zentrale Aufzeichnung)",
                    "Wurm Frigodata (zentrale Aufzeichnung)",
                    "Carel boss (zentrale Aufzeichnung)",
                    "Kiconex Cloud",
                    "Separates HACCP-Modul",
                    "Sonstiges"
                ],
                "vorschlag": "Regler-intern (Datalogging im Regler)",
                "hinweis": "Zentrales System empfohlen – alle Räume in einer Auswertung, EU-VO 37/2005 konform"
            },
            "alarm_grenzwert_oben": {
                "typ": "zahl",
                "label": "Alarm-Grenzwert oben [°C]",
                "min": -40, "max": 30,
                "vorschlag": 8,
                "hinweis": "Oberer Temperaturalarm – bei Überschreitung wird Alarm ausgelöst"
            },
            "alarm_grenzwert_unten": {
                "typ": "zahl",
                "label": "Alarm-Grenzwert unten [°C]",
                "min": -50, "max": 20,
                "vorschlag": -1,
                "hinweis": "Unterer Temperaturalarm (Gefriergrenze bei Kühlräumen)"
            },
            "alarm_verzoegerung_min": {
                "typ": "zahl",
                "label": "Alarm-Verzögerung [min]",
                "min": 0, "max": 120,
                "vorschlag": 30,
                "hinweis": "Verzögerung nach Grenzwertüberschreitung – verhindert Fehlalarme bei Türöffnung"
            },
            "haccp_klasse": {
                "typ": "auswahl",
                "label": "HACCP-Klasse / Anforderung",
                "optionen": [
                    "Standard (EU-VO 37/2005)",
                    "Klasse A (Akkreditierung, ±0,5°C)",
                    "Pharma / GDP",
                    "Fleisch (VO 853/2004)",
                ],
                "vorschlag": "Standard (EU-VO 37/2005)",
                "hinweis": "Bestimmt Genauigkeitsanforderung und Kalibrierungsintervall des Fühlers"
            }
        },
        "kabel_mapping": "EM-VD-TF"
    },
}

# Gruppen für Anzeige
KOMPONENTEN_GRUPPEN = ["Verdampfer", "Fühler", "HACCP", "Regelung", "Steuerung", "Sicherheit", "Monitoring", "Zubehör"]

# =============================================================================
# STEUERUNGSSYSTEME
# =============================================================================

STEUERUNGSSYSTEME = {
    "Einzelregler": {
        "label": "Einzelregler pro Kühlstelle",
        "icon": "🎛️",
        "beschreibung": "Jede Kühlstelle hat eigenen Regler direkt an der Zelle (Intarcon MTM, Dixell, Wurm, Carel...) – kein zentrales Bussystem erforderlich.",
        "kabel": ["EM-VD-SK"],
        "bus": None,
        "typisch_fuer": "Kleine Anlagen, Gastro, Bäckerei, bis ca. 10 Kühlstellen",
        "zubehör": [
            "Regler an Zellenfronten montiert",
            "Optional: Datenfernübertragung via Kiconex/Xweb nachrüstbar",
            "Ggf. Gassensoranzeige und Notruf-Taster ebenfalls an Zelle"
        ]
    },
    "Verbundsteuerung": {
        "label": "Verbundsteuerung (Zentralregler)",
        "icon": "⚙️",
        "beschreibung": "Zentrale Steuerung für Verdichterverbund und alle Kühlstellen – z.B. Danfoss AK-SM, Eliwell MPXPRO, Dixell über RS485-Bus.",
        "kabel": ["VA-SPS", "ICK-RS485"],
        "bus": "RS485 Modbus RTU",
        "typisch_fuer": "Supermarkt, Verbundanlage, 5–50 Kühlstellen",
        "zubehör": [
            "Zentraler Schaltschrank mit Verbundregler",
            "RS485 Bus zu allen Kühlstellenreglern",
            "Bedienteil / Display optional an jeder Kühlstelle"
        ]
    },
    "Wurm_Frigodata": {
        "label": "Wurm Frigodata / Frigolink",
        "icon": "🔵",
        "beschreibung": "Wurm Verbundsteuerung und Monitoring. Hardware: FRIGOLINK (Haupt- + Feldmodule) oder FRIGOENTRY. Software: FRIGODATA XP (lokal) oder FRIGODATA Online (Cloud). FRIDA App für mobile Bedienung. CAN-Bus intern, RS485 zu Feldgeräten.",
        "kabel": ["ICK-RS485", "ICK-ETH", "MSR-GWA-BUS"],
        "bus": "CAN-Bus (intern) + RS485 (Feld) + LAN (Online)",
        "typisch_fuer": "Supermarkt, Lebensmittelhandel, Filialketten, HACCP-Pflicht",
        "zubehör": [
            "FRIGOLINK Hauptmodul + Feldmodule (CAN-Bus)",
            "FRIGODATA XP PC-Software oder FRIGODATA Online Cloud",
            "FRIDA App (iOS/Android) für mobilen Zugriff",
            "Wurm Gateways für RS485-Anbindung",
            "Ferndisplays an Kühlstellen möglich",
            "HACCP-zertifiziertes Monitoring, EU-VO 37/2005 konform"
        ]
    },
    "Carel_Boss": {
        "label": "Carel boss / boss-mini",
        "icon": "🟦",
        "beschreibung": "Carel lokaler Supervisor für Kälteanlagen. boss: bis 300 Geräte, boss-mini: bis 50 Geräte. Protokolle: Modbus RTU/TCP, BACnet MS/TP + TCP/IP, SNMP. RS485 + Ethernet. boss-micro: 4G-Modem integriert, bis 15 Geräte.",
        "kabel": ["ICK-RS485", "ICK-ETH", "MSR-GWA-BUS"],
        "bus": "Modbus RTU / BACnet / RS485 + Ethernet",
        "typisch_fuer": "Supermarkt, Industrie, HVAC-Integration, BMS-Anbindung",
        "zubehör": [
            "boss (bis 300 Geräte): Wandmontage oder DIN-Schiene",
            "boss-mini (bis 50 Geräte): kompaktere Version",
            "boss-micro (bis 15 Geräte): 4G-Modem integriert",
            "RS485 zu allen Carel Reglern (Ultracella, IR33, pCO...)",
            "BACnet-Anbindung an übergeordnetes BMS möglich",
            "Web-Interface, responsive – Zugriff via Smartphone"
        ]
    },
    "Dixell_Xweb": {
        "label": "Dixell Xweb 500 PRO / EVO",
        "icon": "🟩",
        "beschreibung": "Dixell Aufzeichnungs- und Fernüberwachungssystem. Xweb 500 PRO: bis 100 Messstellen, 4 RS485-Ports, Hutschiene (10 DIN). Xweb 500 EVO: Wandaufbaugerät mit Display. Linux-OS, Webserver integriert. Protokoll: Modbus RTU.",
        "kabel": ["ICK-RS485", "ICK-ETH", "MSR-GWA-BUS"],
        "bus": "Modbus RTU RS485 + Ethernet/LAN",
        "typisch_fuer": "Mittlere Anlagen, Supermarkt, Lager – 5 bis 100 Kühlstellen",
        "zubehör": [
            "Xweb 500 PRO (Hutschiene, 10 DIN, bis 100 Adressen)",
            "Xweb 500 EVO (Wandaufbau mit Display, bis 36 Adressen)",
            "XJ485 / XJRS485 Adapter für Dixell TTL-Regler ohne RS485",
            "RS485 Kabel: 2–3 Leiter geschirmt, min. 0,5mm² (z.B. Belden 8772)",
            "GPRS/LTE-Modem für Fernzugriff ohne LAN",
            "MEMO BOX / FUE BOX für Nachrüstung",
            "HACCP-Aufzeichnung, EU-VO 37/2005 konform"
        ]
    },
    "SPS_S7": {
        "label": "SPS Siemens S7",
        "icon": "🏭",
        "beschreibung": "Vollautomatisierung via SPS, PROFIBUS oder PROFINET. Für komplexe Industrieautomation.",
        "kabel": ["S7-PB", "S7-PN-KABEL", "S7-VER-SCHRANK"],
        "bus": "PROFIBUS / PROFINET",
        "typisch_fuer": "Industrie, NH3-Anlagen, Prozessanlagen",
        "zubehör": [
            "Siemens S7-300/400/1500 SPS",
            "PROFIBUS DP oder PROFINET IO",
            "Simatic HMI Touch-Panel",
            "Frequenzumrichter via PROFIBUS"
        ]
    },
    "Kiconex": {
        "label": "Kiconex IoT Gateway",
        "icon": "🌐",
        "beschreibung": "Cloud-IoT-Monitoring und Fernsteuerung für alle Reglerhersteller. RS485 Modbus zu bestehenden Reglern, LAN/4G zur Cloud. Kein eigener Verbundregler – reine Überwachungsebene.",
        "kabel": ["ICK-RS485", "ICK-ETH", "ICK-VER"],
        "bus": "RS485 Modbus + LAN / 4G Cloud",
        "typisch_fuer": "Nachrüstung, Fernüberwachung, alle Anlagentypen",
        "zubehör": [
            "Kiconex Gateway (DIN-Schiene oder Wandmontage)",
            "RS485 zu bestehenden Reglern",
            "LAN oder 4G SIM für Cloud-Anbindung",
            "Kiconex Cloud-Portal (Web + App)"
        ]
    },
}

# =============================================================================
# KÜHLSTELLEN-DATENMODELL
# =============================================================================

def neue_kuehlstelle(nummer: int) -> dict:
    """Erstellt eine neue leere Kühlstelle."""
    return {
        "id": f"KS_{nummer:03d}",
        "nummer": nummer,
        "name": f"Kühlstelle {nummer}",
        "beschreibung": "",
        "temp_bereich": "NK",
        "verdampfung_custom_c": None,
        "raum_temp_soll_c": None,
        "kaelteleistung_kw": None,
        "lieferumfang": "direkt",
        "kreis": 1,
        "komponenten": {},
        "leitungslaenge_m": 20,
        "laenge_aussenteil_m": 15,
        "laenge_router_m": 20,
        "laenge_schaltschrank_m": 10,
        "standort_raum": "",
        "standort_etage": "",
        "zentraler_sk_override": None,
        "erstellt_am": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "notizen": "",
        "status": "offen"
    }


def kopiere_kuehlstelle(ks: dict, neue_nummer: int) -> dict:
    """Kopiert eine Kühlstelle mit neuer Nummer."""
    kopie = copy.deepcopy(ks)
    kopie["id"] = f"KS_{neue_nummer:03d}"
    kopie["nummer"] = neue_nummer
    kopie["name"] = f"Kühlstelle {neue_nummer}"
    kopie["erstellt_am"] = datetime.now().strftime("%d.%m.%Y %H:%M")
    kopie["status"] = "offen"
    return kopie


def get_temp_bereich_info(bereich: str) -> dict:
    return TEMP_BEREICHE.get(bereich, TEMP_BEREICHE["CUSTOM"])


def get_komponente_info(komp_key: str) -> dict:
    return KOMPONENTEN.get(komp_key, {})


def berechne_kuehlstellen_kabel(kuehlstelle: dict) -> list:
    """
    Ermittelt alle benötigten Kabeltypen für eine Kühlstelle
    basierend auf den gewählten Komponenten und Parametern.
    """
    kabel_liste = []
    for komp_key, komp_data in kuehlstelle.get("komponenten", {}).items():
        if not komp_data.get("aktiv", False):
            continue
        komp_info = KOMPONENTEN.get(komp_key, {})
        mapping = komp_info.get("kabel_mapping")
        params = komp_data.get("parameter", {})

        if isinstance(mapping, str):
            # Direkte Zuordnung
            if mapping:
                kabel_liste.append({
                    "kuerzel": mapping,
                    "komponente": komp_info.get("label", komp_key),
                    "parameter": params
                })
        elif isinstance(mapping, dict):
            # Parameter-abhängige Zuordnung
            for param_key, kuerzel in mapping.items():
                param_wert = params.get(list(params.keys())[0] if params else "", "")
                if param_wert == param_key and kuerzel:
                    kabel_liste.append({
                        "kuerzel": kuerzel,
                        "komponente": komp_info.get("label", komp_key),
                        "parameter": params
                    })
                    break
        elif isinstance(mapping, list):
            for k in mapping:
                if k:
                    kabel_liste.append({
                        "kuerzel": k,
                        "komponente": komp_info.get("label", komp_key),
                        "parameter": params
                    })

    return kabel_liste


def gruppiere_nach_kreis(kuehlstellen: list) -> dict:
    """Gruppiert Kühlstellen nach Kältekreis und Verdampfungstemperatur."""
    kreise = {}
    for ks in kuehlstellen:
        kreis_nr = ks.get("kreis", 1)
        temp = ks.get("temp_bereich", "NK")
        key = f"Kreis {kreis_nr} – {TEMP_BEREICHE.get(temp, {}).get('label', temp)}"
        if key not in kreise:
            kreise[key] = []
        kreise[key].append(ks)
    return kreise


def kreis_zusammenfassung(kuehlstellen: list) -> list:
    """
    Erstellt eine vollständige Kreiszusammenfassung mit Kennzahlen.
    Gibt Liste von Kreis-Dicts zurück, sortiert nach Kreis-Nr.
    """
    kreise_raw = gruppiere_nach_kreis(kuehlstellen)
    ergebnis = []

    for kreis_label, ks_liste in kreise_raw.items():
        kreis_nr = ks_liste[0].get("kreis", 1)
        temp_bereich = ks_liste[0].get("temp_bereich", "NK")
        temp_info = TEMP_BEREICHE.get(temp_bereich, {})

        # Verdampfungstemperatur: kälteste nehmen
        verdampfungen = [k.get("verdampfung_custom_c") or temp_info.get("verdampfung_c", -8)
                         for k in ks_liste if k.get("verdampfung_custom_c") or temp_info.get("verdampfung_c")]
        verdampfung = min(verdampfungen) if verdampfungen else temp_info.get("verdampfung_c", -8)

        # Kälteleistung summieren
        leistung_gesamt = sum(
            float(k.get("kaelteleistung_kw") or 0) for k in ks_liste
        )

        # Direkt vs Extern
        direkt = [k for k in ks_liste if k.get("lieferumfang") == "direkt"]
        extern = [k for k in ks_liste if k.get("lieferumfang") == "extern"]

        # Maschinenstandorte
        standorte = list(set(k.get("maschinenstandort", "–") for k in ks_liste))

        # Kühlstellen Namen
        namen_direkt = [k["name"] for k in direkt]
        namen_extern = [k["name"] for k in extern]

        ergebnis.append({
            "kreis_nr": kreis_nr,
            "label": kreis_label,
            "temp_bereich": temp_bereich,
            "temp_label": temp_info.get("label", temp_bereich),
            "farbe": temp_info.get("farbe", "#36A9E1"),
            "verdampfung_c": verdampfung,
            "anzahl_gesamt": len(ks_liste),
            "anzahl_direkt": len(direkt),
            "anzahl_extern": len(extern),
            "leistung_kw_gesamt": round(leistung_gesamt, 2),
            "maschinenstandorte": standorte,
            "kuehlstellen_direkt": namen_direkt,
            "kuehlstellen_extern": namen_extern,
            "kuehlstellen_alle": ks_liste,
        })

    return sorted(ergebnis, key=lambda x: x["kreis_nr"])
