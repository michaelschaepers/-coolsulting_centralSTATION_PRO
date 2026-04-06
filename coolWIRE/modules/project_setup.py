# modules/project_setup.py
# °coolWIRE v1.0 – Projektverwaltung & Raumdatenbank
# (c) coolsulting e.U. | Michael Schäpers

import json
import os
from datetime import datetime

# =============================================================================
# VOLLSTÄNDIGE RAUMDATENBANK MIT KABELSET-MAPPING
# =============================================================================

RAUMDATENBANK = {

    # =========================================================================
    # BÄCKEREI
    # =========================================================================
    "Bäckerei": {
        "kategorie": "Bäckerei",
        "icon": "🥐",
        "raeume": {
            "Gärverzögerungsschrank (GV)": {
                "id": "BK_GV",
                "beschreibung": "Klimatisierter Gärverzögerungsschrank für Teigwaren",
                "temperatur_bereich": (-5, +8),
                "feuchte_bereich": (70, 95),
                "typische_leistung_kw": (1.5, 7.5),
                "betrieb": "24/7",
                "besonderheiten": ["Feuchteregelung", "Programmuhr", "Heißgas oder Elektroabtau"],
                "kabelsets": {
                    "pflicht": [
                        "BK-GV-VER",    # Hauptversorgung
                        "BK-GV-TF",     # Temperaturfühler innen
                        "BK-GV-ST",     # Steuerung/Timer
                        "EM-VD-ABT",    # Abtauheizung (SIHF)
                    ],
                    "optional": [
                        "BK-GV-FF",     # Feuchtefühler
                        "ICK-RS485",    # Kiconex Monitoring
                        "ICK-TF",       # Kiconex Extrafühler
                        "MSR-TF-NTC",   # Zusatzfühler
                    ],
                    "empfohlen": [
                        "PA-NT-TAST",   # Personennotruf wenn begehbar
                        "MSR-GWA-SEN",  # Gaswarnanlage bei NH3
                    ]
                }
            },
            "Gärschrank": {
                "id": "BK_GS",
                "beschreibung": "Aktiver Gärschrank mit Wärme und Feuchte",
                "temperatur_bereich": (+28, +38),
                "feuchte_bereich": (75, 95),
                "typische_leistung_kw": (1.0, 4.0),
                "betrieb": "Tagesschicht",
                "besonderheiten": ["Nur Heizung + Befeuchtung", "kein Kältebetrieb", "Feuchte wichtig"],
                "kabelsets": {
                    "pflicht": [
                        "BK-GV-VER",    # Versorgung
                        "BK-GV-TF",     # Temperaturfühler
                        "BK-GV-FF",     # Feuchtefühler
                        "BK-GV-ST",     # Steuerung
                    ],
                    "optional": [
                        "ICK-RS485",
                        "ICK-TF",
                    ],
                    "empfohlen": []
                }
            },
            "Stikkenofen / Stikkenkühlschrank": {
                "id": "BK_ST",
                "beschreibung": "Stikkenofen mit Schnellkühlstufe",
                "temperatur_bereich": (-5, +220),
                "feuchte_bereich": (0, 100),
                "typische_leistung_kw": (6.0, 20.0),
                "betrieb": "Tagesschicht",
                "besonderheiten": ["Hohe Anschlussleistung", "Kombination Heizen+Kühlen", "Robust"],
                "kabelsets": {
                    "pflicht": [
                        "BK-ST-VER",    # Hauptversorgung stark
                        "BK-GV-TF",     # Temperaturfühler
                        "BK-GV-ST",     # Steuerung
                        "BK-ABT-HZ",    # Abtauheizung
                    ],
                    "optional": [
                        "ICK-RS485",
                        "MSR-TF-PT100",
                    ],
                    "empfohlen": []
                }
            },
            "Kühlraum Bäckerei": {
                "id": "BK_KR",
                "beschreibung": "Kühlraum Rohstoffe/Fertigwaren Bäckerei",
                "temperatur_bereich": (+2, +8),
                "feuchte_bereich": (60, 80),
                "typische_leistung_kw": (1.5, 5.0),
                "betrieb": "24/7",
                "besonderheiten": ["Feuchte Umgebung", "FI-Schutz nötig", "Abtauheizung"],
                "kabelsets": {
                    "pflicht": [
                        "BK-GV-VER",
                        "EM-VD-L",
                        "EM-VD-ABT",
                        "EM-VD-TF",
                        "BK-RUE-TF",
                    ],
                    "optional": [
                        "PA-NT-TAST",
                        "PA-NT-HORN",
                        "ICK-RS485",
                        "EEV-MOT",
                        "EEV-TF-SAUG",
                    ],
                    "empfohlen": [
                        "MSR-TF-NTC",
                    ]
                }
            },
            "Tiefkühlraum Bäckerei": {
                "id": "BK_TK",
                "beschreibung": "Tiefkühlraum Bäckerei, Teiglinge und Fertigprodukte",
                "temperatur_bereich": (-22, -18),
                "feuchte_bereich": (50, 70),
                "typische_leistung_kw": (3.0, 10.0),
                "betrieb": "24/7",
                "besonderheiten": ["Heißgasabtau oder Elektroabtau", "Türheizung", "Personennotruf pflicht"],
                "kabelsets": {
                    "pflicht": [
                        "BK-GV-VER",
                        "EM-VD-3P",
                        "EM-VD-ABT",
                        "EM-VD-TF",
                        "EM-VD-HZ",
                        "PA-NT-TAST",
                        "PA-NT-HORN",
                        "PA-NT-LED",
                        "PA-NT-VER",
                    ],
                    "optional": [
                        "ICK-RS485",
                        "ICK-TF",
                        "EEV-MOT",
                        "EEV-DRUCK",
                        "MSR-GWA-SEN",
                    ],
                    "empfohlen": [
                        "PA-NT-ZE",
                        "MSR-TF-NTC",
                    ]
                }
            },
        }
    },

    # =========================================================================
    # GASTRO
    # =========================================================================
    "Gastro": {
        "kategorie": "Gastro",
        "icon": "🍽️",
        "raeume": {
            "Fleisch-Kühlraum": {
                "id": "GA_FK",
                "beschreibung": "Kühlraum Fleisch & Wurst, Profiküche",
                "temperatur_bereich": (0, +4),
                "feuchte_bereich": (85, 95),
                "typische_leistung_kw": (1.0, 4.0),
                "betrieb": "24/7",
                "besonderheiten": ["Hohe Luftfeuchtigkeit", "IP67 Fühler", "FI-Schutz"],
                "kabelsets": {
                    "pflicht": [
                        "GA-KZ-VER",
                        "GA-KZ-TF-IN",
                        "GA-KZ-TF-ABT",
                        "GA-KZ-HZ",
                        "EM-VD-L",
                        "EM-VD-TF",
                    ],
                    "optional": [
                        "GA-KZ-TUE",
                        "ICK-RS485",
                        "MSR-TF-NTC",
                    ],
                    "empfohlen": [
                        "PA-NT-TAST",
                    ]
                }
            },
            "Gemüse-Kühlraum": {
                "id": "GA_GK",
                "beschreibung": "Kühlraum Gemüse & Salat, Profiküche",
                "temperatur_bereich": (+4, +10),
                "feuchte_bereich": (85, 95),
                "typische_leistung_kw": (0.75, 3.0),
                "betrieb": "24/7",
                "besonderheiten": ["Hohe Feuchte", "Ethylen-sensitiv", "direkte Kühlung"],
                "kabelsets": {
                    "pflicht": [
                        "GA-KZ-VER",
                        "GA-KZ-TF-IN",
                        "GA-KZ-TF-ABT",
                        "GA-KZ-HZ",
                        "EM-VD-L",
                    ],
                    "optional": [
                        "GA-KZ-TUE",
                        "ICK-TF",
                        "ICK-DI",
                    ],
                    "empfohlen": []
                }
            },
            "Tiefkühllager Gastro": {
                "id": "GA_TK",
                "beschreibung": "Tiefkühlraum Gastronomie",
                "temperatur_bereich": (-22, -18),
                "feuchte_bereich": (50, 70),
                "typische_leistung_kw": (2.0, 8.0),
                "betrieb": "24/7",
                "besonderheiten": ["Heißgasabtau bevorzugt", "Personennotruf pflicht EN 378"],
                "kabelsets": {
                    "pflicht": [
                        "GA-KZ-VER",
                        "GA-KZ-TF-IN",
                        "GA-KZ-TF-ABT",
                        "GA-KZ-HZ",
                        "EM-VD-3P",
                        "EM-VD-ABT",
                        "EM-VD-HZ",
                        "PA-NT-TAST",
                        "PA-NT-HORN",
                        "PA-NT-LED",
                        "PA-NT-VER",
                    ],
                    "optional": [
                        "EEV-MOT",
                        "EEV-TF-SAUG",
                        "ICK-RS485",
                        "MSR-GWA-SEN",
                    ],
                    "empfohlen": [
                        "PA-NT-ZE",
                        "ICK-TF",
                    ]
                }
            },
            "Kühltheke Frischetheke": {
                "id": "GA_KTH",
                "beschreibung": "Offene Kühltheke / Frischetheke Selbstbedienung",
                "temperatur_bereich": (+2, +8),
                "feuchte_bereich": (70, 90),
                "typische_leistung_kw": (0.5, 2.5),
                "betrieb": "Öffnungszeiten",
                "besonderheiten": ["Abtau mehrmals täglich", "LED-Beleuchtung getrennt", "Nassbereich"],
                "kabelsets": {
                    "pflicht": [
                        "GA-THE-VER",
                        "GA-THE-LED",
                        "GA-KZ-TF-IN",
                        "GA-KZ-HZ",
                        "EM-VD-L",
                    ],
                    "optional": [
                        "ICK-TF",
                        "MSR-TF-NTC",
                    ],
                    "empfohlen": []
                }
            },
            "Getränkekühlanlage": {
                "id": "GA_GET",
                "beschreibung": "Getränkekühlung, Split-Geräte oder Zentralanlage",
                "temperatur_bereich": (+2, +12),
                "feuchte_bereich": (60, 80),
                "typische_leistung_kw": (0.3, 2.0),
                "betrieb": "Öffnungszeiten",
                "besonderheiten": ["Oft 1-phasig", "Schankanlage integriert", "CO2-Warnung"],
                "kabelsets": {
                    "pflicht": [
                        "GA-GET-VER",
                        "GA-KZ-TF-IN",
                        "EM-VD-L",
                    ],
                    "optional": [
                        "MSR-GWA-SEN",  # CO2-Warnung
                        "ICK-TF",
                        "ICK-DI",
                    ],
                    "empfohlen": [
                        "MSR-GWA-HORN",
                    ]
                }
            },
            "Weinkühlschrank": {
                "id": "GA_WK",
                "beschreibung": "Weinklimaschrank / Weinkühlzelle",
                "temperatur_bereich": (+8, +18),
                "feuchte_bereich": (60, 75),
                "typische_leistung_kw": (0.2, 1.5),
                "betrieb": "24/7",
                "besonderheiten": ["Erschütterungsarm", "UV-geschützt", "Feuchteausgleich"],
                "kabelsets": {
                    "pflicht": [
                        "GA-GET-VER",
                        "GA-KZ-TF-IN",
                    ],
                    "optional": [
                        "ICK-TF",
                        "BK-GV-FF",
                    ],
                    "empfohlen": []
                }
            },
        }
    },

    # =========================================================================
    # SUPERMARKT
    # =========================================================================
    "Supermarkt": {
        "kategorie": "Supermarkt",
        "icon": "🛒",
        "raeume": {
            "Frischekühlregal (offen)": {
                "id": "SM_FKR",
                "beschreibung": "Offenes Kühlregal Molkerei/Wurst, Verbundanlage",
                "temperatur_bereich": (+2, +7),
                "feuchte_bereich": (75, 90),
                "typische_leistung_kw": (0.8, 2.0),
                "betrieb": "Öffnungszeiten + Nacht",
                "besonderheiten": ["Verbundanlage", "Zentralsteuerung", "Nachtrollladen"],
                "kabelsets": {
                    "pflicht": [
                        "VA-SPS",           # Verbundanlage Bus
                        "EM-VD-L",          # Lüfter
                        "EM-VD-TF",         # Fühler
                        "GA-THE-LED",       # LED-Beleuchtung
                    ],
                    "optional": [
                        "EEV-MOT",
                        "EEV-TF-SAUG",
                        "ICK-RS485",
                        "MSR-TF-NTC",
                    ],
                    "empfohlen": [
                        "ICK-TF",
                    ]
                }
            },
            "TK-Truhe (offen)": {
                "id": "SM_TKT",
                "beschreibung": "Offene Tiefkühltruhe, Verbundanlage",
                "temperatur_bereich": (-25, -18),
                "feuchte_bereich": (40, 65),
                "typische_leistung_kw": (0.5, 1.5),
                "betrieb": "24/7",
                "besonderheiten": ["Heißgasabtau Verbund", "Nachtabdeckung"],
                "kabelsets": {
                    "pflicht": [
                        "VA-SPS",
                        "VA-ABT",
                        "EM-VD-L",
                        "EM-VD-TF",
                    ],
                    "optional": [
                        "EEV-MOT",
                        "ICK-RS485",
                    ],
                    "empfohlen": []
                }
            },
            "TK-Kühlraum Lager": {
                "id": "SM_TKLR",
                "beschreibung": "Tiefkühllager Supermarkt, Zentralanlage",
                "temperatur_bereich": (-22, -18),
                "feuchte_bereich": (50, 70),
                "typische_leistung_kw": (5.0, 20.0),
                "betrieb": "24/7",
                "besonderheiten": ["Personennotruf pflicht", "Großraum", "Verbund oder Monoblock"],
                "kabelsets": {
                    "pflicht": [
                        "VA-VD-HV",
                        "VA-VD-ST",
                        "VA-HD-LP",
                        "VA-ABT",
                        "EM-VD-3P",
                        "EM-VD-ABT",
                        "EM-VD-HZ",
                        "PA-NT-TAST",
                        "PA-NT-HORN",
                        "PA-NT-LED",
                        "PA-NT-VER",
                        "PA-NT-ZE",
                    ],
                    "optional": [
                        "ICK-RS485",
                        "MSR-GWA-SEN",
                        "EEV-MOT",
                        "EEV-DRUCK",
                    ],
                    "empfohlen": [
                        "ICK-TF",
                        "MSR-TF-NTC",
                    ]
                }
            },
            "Verbundzentrale (Maschinenraum)": {
                "id": "SM_VBZ",
                "beschreibung": "Maschinensatz Verbundanlage Supermarkt",
                "temperatur_bereich": (+15, +35),
                "feuchte_bereich": (40, 70),
                "typische_leistung_kw": (15.0, 80.0),
                "betrieb": "24/7",
                "besonderheiten": ["Mehrere Verdichter", "FU", "Gaswarnanlage", "Zentralsteuerung"],
                "kabelsets": {
                    "pflicht": [
                        "VA-VD-HV",
                        "VA-VD-ST",
                        "VA-HD-LP",
                        "VA-OLR",
                        "VA-SAMMLER",
                        "VA-LUE",
                        "VA-FU",
                        "VA-SPS",
                        "MSR-GWA-SEN",
                        "MSR-GWA-HORN",
                        "MSR-GWA-REL",
                        "MSR-GWA-BUS",
                        "VFL-VER",
                        "VFL-LUE",
                        "VFL-FU-LUE",
                    ],
                    "optional": [
                        "ICK-RS485",
                        "ICK-ETH",
                        "MSR-DI-DO",
                        "MSR-ANALOG",
                        "MSR-VER",
                    ],
                    "empfohlen": [
                        "ICK-VER",
                        "MSR-TF-PT100",
                        "VFL-DRUCK",
                    ]
                }
            },
            "Backwarenkühlregal": {
                "id": "SM_BKR",
                "beschreibung": "Brot/Backwaren Kühlpräsentation",
                "temperatur_bereich": (+10, +18),
                "feuchte_bereich": (55, 70),
                "typische_leistung_kw": (0.3, 1.2),
                "betrieb": "Öffnungszeiten",
                "besonderheiten": ["Niedrige Kälteleistung", "Feuchteausgleich wichtig"],
                "kabelsets": {
                    "pflicht": [
                        "GA-THE-VER",
                        "GA-KZ-TF-IN",
                        "GA-THE-LED",
                        "EM-VD-L",
                    ],
                    "optional": [
                        "ICK-TF",
                    ],
                    "empfohlen": []
                }
            },
        }
    },

    # =========================================================================
    # INDUSTRIE
    # =========================================================================
    "Industrie": {
        "kategorie": "Industrie",
        "icon": "🏭",
        "raeume": {
            "Produktionshalle Kühlung": {
                "id": "IND_PH",
                "beschreibung": "Prozesskühlung Produktion, SPS-gesteuert",
                "temperatur_bereich": (+5, +18),
                "feuchte_bereich": (40, 70),
                "typische_leistung_kw": (10.0, 200.0),
                "betrieb": "24/7 / 3-Schicht",
                "besonderheiten": ["SPS S7", "PROFIBUS/PROFINET", "FU", "EMV-kritisch"],
                "kabelsets": {
                    "pflicht": [
                        "S7-PB",            # PROFIBUS
                        "S7-AI-STR",        # Analog 4-20mA
                        "S7-DO-REL",        # Digitalausgang
                        "S7-VER-SCHRANK",   # Schaltschrank
                        "S7-VER-24V",       # SPS-Versorgung
                        "VA-VD-HV",         # Verdichter
                        "VA-FU",            # FU-Steuerleitung
                        "MSR-GWA-SEN",      # Gaswarnanlage
                        "MSR-GWA-HORN",
                    ],
                    "optional": [
                        "S7-PN-KABEL",      # PROFINET statt PROFIBUS
                        "S7-MPI",
                        "S7-SIMATIC-HMI",
                        "EEV-MOT",
                        "EEV-DRUCK",
                        "ICK-RS485",
                        "ICK-ETH",
                    ],
                    "empfohlen": [
                        "MSR-TF-PT100",
                        "MSR-ANALOG",
                        "VFL-VER",
                        "VFL-FU-LUE",
                    ]
                }
            },
            "Kühlraum Rohstoffe Industrie": {
                "id": "IND_KR",
                "beschreibung": "Industriekühlraum Rohstofflagerung",
                "temperatur_bereich": (0, +8),
                "feuchte_bereich": (60, 85),
                "typische_leistung_kw": (5.0, 30.0),
                "betrieb": "24/7",
                "besonderheiten": ["Großraum", "Personennotruf", "Gaswarnanlage bei Ammoniak"],
                "kabelsets": {
                    "pflicht": [
                        "VA-VD-HV",
                        "VA-VD-ST",
                        "VA-HD-LP",
                        "EM-VD-3P",
                        "EM-VD-TF",
                        "EM-VD-ABT",
                        "PA-NT-TAST",
                        "PA-NT-HORN",
                        "PA-NT-LED",
                        "PA-NT-VER",
                        "MSR-GWA-SEN",
                        "MSR-GWA-HORN",
                        "MSR-GWA-REL",
                    ],
                    "optional": [
                        "S7-PB",
                        "S7-AI-STR",
                        "EEV-MOT",
                        "ICK-RS485",
                    ],
                    "empfohlen": [
                        "PA-NT-ZE",
                        "MSR-TF-PT100",
                        "ICK-ETH",
                    ]
                }
            },
            "Schockfroster": {
                "id": "IND_SF",
                "beschreibung": "Schnellfroster / Schockfroster Industriebetrieb",
                "temperatur_bereich": (-40, -18),
                "feuchte_bereich": (40, 65),
                "typische_leistung_kw": (15.0, 60.0),
                "betrieb": "Zyklusbetrieb",
                "besonderheiten": ["Heißgasabtau", "Hochleistungsverdampfer", "Automatikbetrieb"],
                "kabelsets": {
                    "pflicht": [
                        "VA-VD-HV",
                        "VA-VD-ST",
                        "VA-HD-LP",
                        "VA-ABT",
                        "EM-VD-3P",
                        "EM-VD-ABT",
                        "EM-VD-HZ",
                        "EEV-MOT",
                        "EEV-TF-SAUG",
                        "EEV-TF-AUS",
                        "EEV-DRUCK",
                        "MSR-GWA-SEN",
                        "MSR-GWA-HORN",
                    ],
                    "optional": [
                        "S7-PB",
                        "S7-AI-STR",
                        "ICK-RS485",
                        "MSR-DI-DO",
                    ],
                    "empfohlen": [
                        "PA-NT-TAST",
                        "PA-NT-HORN",
                        "PA-NT-VER",
                        "MSR-TF-PT100",
                    ]
                }
            },
            "Ammoniakanlage (NH3)": {
                "id": "IND_NH3",
                "beschreibung": "NH3-Kälteanlage Industrie, EN 378 Kat. A",
                "temperatur_bereich": (-40, +10),
                "feuchte_bereich": (40, 80),
                "typische_leistung_kw": (50.0, 2000.0),
                "betrieb": "24/7",
                "besonderheiten": ["EN 378 Kat. A", "ATEX Zone 2", "Pflicht-GWA", "Sicherheitstechnik"],
                "kabelsets": {
                    "pflicht": [
                        "MSR-GWA-SEN",      # Gaswarnanlage (mehrere Sensoren)
                        "MSR-GWA-BUS",      # GWA-Bus
                        "MSR-GWA-HORN",     # Alarmhorn
                        "MSR-GWA-REL",      # Lüftungsfreigabe
                        "PA-NT-TAST",       # Personennotruf überall
                        "PA-NT-HORN",
                        "PA-NT-LED",
                        "PA-NT-VER",
                        "PA-NT-ZE",
                        "S7-PB",            # SPS-Steuerung
                        "S7-VER-SCHRANK",
                        "S7-AI-STR",
                        "S7-DO-REL",
                        "VA-VD-HV",
                        "VA-HD-LP",
                        "VA-OLR",
                        "VA-SPS",
                        "VFL-VER",
                        "VFL-FU-LUE",
                    ],
                    "optional": [
                        "S7-PN-KABEL",
                        "S7-SIMATIC-HMI",
                        "ICK-ETH",
                        "EEV-DRUCK",
                    ],
                    "empfohlen": [
                        "MSR-TF-PT100",
                        "MSR-DI-DO",
                        "MSR-VER",
                        "ICK-RS485",
                    ]
                }
            },
            "Prozesskältemaschine": {
                "id": "IND_PKM",
                "beschreibung": "Prozesskältemaschine / Chiller Industrie",
                "temperatur_bereich": (+5, +20),
                "feuchte_bereich": (40, 80),
                "typische_leistung_kw": (20.0, 500.0),
                "betrieb": "24/7",
                "besonderheiten": ["Inverterregelung", "Modbus-Fernsteuerung", "Wasserseite"],
                "kabelsets": {
                    "pflicht": [
                        "S7-VER-SCHRANK",
                        "S7-AI-STR",
                        "VA-FU",
                        "VA-VD-HV",
                        "MSR-GWA-SEN",
                        "MSR-ANALOG",
                        "ICK-RS485",
                    ],
                    "optional": [
                        "S7-PB",
                        "S7-PN-KABEL",
                        "EEV-MOT",
                        "EEV-DRUCK",
                        "VFL-DRUCK",
                    ],
                    "empfohlen": [
                        "MSR-TF-PT100",
                        "BK-RUE-TF",        # Wasserrücklauf
                        "ICK-ETH",
                    ]
                }
            },
        }
    },

}

# =============================================================================
# PROJEKTSTRUKTUR
# =============================================================================

PROJEKT_TEMPLATE = {
    "projektname": "",
    "projektnummer": "",
    "erstellt_am": "",
    "erstellt_von": "coolsulting e.U.",
    "kunde": "",
    "standort": "",
    "land": "AT",
    "ansprechpartner": "",
    "raeume": [],
    "notizen": "",
    "version": "1.0"
}

LAND_OPTIONEN = {
    "AT": "Österreich (ÖVE/ÖNORM)",
    "DE": "Deutschland (DIN VDE / DVGW)",
    "HR": "Kroatien (HRN / EN)"
}

TECHNIKER_OPTIONEN = [
    "Michael Schäpers",
    "Niklas Reisner",
]

# =============================================================================
# PROJEKTFUNKTIONEN
# =============================================================================

def erstelle_neues_projekt(projektname: str, projektnummer: str,
                            kunde: str, standort: str,
                            land: str = "AT") -> dict:
    """Erstellt ein neues leeres Projektdokument."""
    projekt = PROJEKT_TEMPLATE.copy()
    projekt["projektname"] = projektname
    projekt["projektnummer"] = projektnummer
    projekt["erstellt_am"] = datetime.now().strftime("%d.%m.%Y %H:%M")
    projekt["kunde"] = kunde
    projekt["standort"] = standort
    projekt["land"] = land
    return projekt


def get_kategorien() -> list:
    """Gibt alle Raumkategorien zurück."""
    return list(RAUMDATENBANK.keys())


def get_raeume_fuer_kategorie(kategorie: str) -> dict:
    """Gibt alle Raumtypen einer Kategorie zurück."""
    if kategorie in RAUMDATENBANK:
        return RAUMDATENBANK[kategorie]["raeume"]
    return {}


def get_raum_details(kategorie: str, raumtyp: str) -> dict:
    """Gibt Details eines Raumtyps zurück."""
    raeume = get_raeume_fuer_kategorie(kategorie)
    return raeume.get(raumtyp, {})


def get_kabelsets_fuer_raum(kategorie: str, raumtyp: str) -> dict:
    """Gibt die Kabelsets für einen Raumtyp zurück."""
    raum = get_raum_details(kategorie, raumtyp)
    return raum.get("kabelsets", {"pflicht": [], "optional": [], "empfohlen": []})


def speichere_projekt(projekt: dict, pfad: str) -> bool:
    """Speichert ein Projekt als JSON-Datei."""
    try:
        os.makedirs(os.path.dirname(pfad) if os.path.dirname(pfad) else ".", exist_ok=True)
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump(projekt, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def lade_projekt(pfad: str) -> dict:
    """Lädt ein Projekt aus einer JSON-Datei."""
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def validiere_projekt(projekt: dict) -> list:
    """Prüft Pflichtfelder und gibt Fehlerliste zurück."""
    fehler = []
    if not projekt.get("projektname"):
        fehler.append("Projektname fehlt")
    if not projekt.get("projektnummer"):
        fehler.append("Projektnummer fehlt")
    if not projekt.get("kunde"):
        fehler.append("Kundenname fehlt")
    if not projekt.get("standort"):
        fehler.append("Standort fehlt")
    if not projekt.get("raeume"):
        fehler.append("Keine Räume definiert")
    return fehler
