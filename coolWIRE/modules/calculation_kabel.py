# modules/calculation_kabel.py
# °coolWIRE v1.0 – Kabelmatrix & Berechnung
# (c) coolsulting e.U. | Michael Schäpers

import pandas as pd
import math

# =============================================================================
# VOLLSTÄNDIGE KABELMATRIX – ALLE CLUSTER
# =============================================================================

KABEL_MATRIX = {

    # =========================================================================
    # CLUSTER 1: EM-VERDAMPFER (Elektromotor-Verdampfer / Lüftermotoren)
    # =========================================================================
    "EM-Verdampfer": {
        "beschreibung": "Lüftermotoren Verdampfer, Abtauheizung, Schaltkasten",
        "kabel_typen": [
            {
                "kuerzel": "EM-VD-L",
                "bezeichnung": "Lüftermotor Verdampfer – Leitung",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5, 2.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM EN 60228",
                "anmerkung": "1-phasig, Schutzleiter erforderlich"
            },
            {
                "kuerzel": "EM-VD-3P",
                "bezeichnung": "Lüftermotor Verdampfer – 3-phasig",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [1.5, 2.5],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM EN 60228",
                "anmerkung": "3-phasig, N+PE erforderlich"
            },
            {
                "kuerzel": "EM-VD-ABT",
                "bezeichnung": "Abtauheizung Verdampfer",
                "typ": "SIHF",
                "aderzahl": 2,
                "querschnitt_mm2": [1.5, 2.5, 4.0],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM EN 60228",
                "anmerkung": "Silikonleitung, hitzebeständig bis 180°C"
            },
            {
                "kuerzel": "EM-VD-SK",
                "bezeichnung": "Schaltkasten Verdampfer – Steuerkabel",
                "typ": "LIYY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Steuerung/Bus intern, abgeschirmt empfohlen"
            },
            {
                "kuerzel": "EM-VD-TF",
                "bezeichnung": "Temperaturfühler Verdampfer",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 12,
                "norm": "VDE 0812",
                "anmerkung": "Abgeschirmt, NTC/PT100, max. 50 m"
            },
            {
                "kuerzel": "EM-VD-HZ",
                "bezeichnung": "Gehäuseheizung / Kondensatheizung",
                "typ": "SIHF",
                "aderzahl": 2,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM EN 60228",
                "anmerkung": "Dauerbetrieb, Silikonleitung"
            },
        ]
    },

    # =========================================================================
    # CLUSTER 2: PA – PERSONENNOTRUF (EN 13133 / EN 378)
    # =========================================================================
    "PA-Personennotruf": {
        "beschreibung": "Personennotrufsystem Kühlraum, EN 13133 / EN 378-3",
        "kabel_typen": [
            {
                "kuerzel": "PA-NT-TAST",
                "bezeichnung": "Notruf-Taster innen",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.75, 1.0],
                "spannung_v": 24,
                "norm": "EN 13133 / EN 378-3",
                "anmerkung": "Abgeschirmt, Schleifenprinzip, beleuchtet"
            },
            {
                "kuerzel": "PA-NT-HORN",
                "bezeichnung": "Akustischer Alarm / Horn außen",
                "typ": "YMM-J",
                "aderzahl": 2,
                "querschnitt_mm2": [1.5],
                "spannung_v": 24,
                "norm": "EN 13133",
                "anmerkung": "DC-Versorgung Signalhorn"
            },
            {
                "kuerzel": "PA-NT-LED",
                "bezeichnung": "Optischer Alarm / Blitzleuchte außen",
                "typ": "YMM-J",
                "aderzahl": 2,
                "querschnitt_mm2": [1.5],
                "spannung_v": 24,
                "norm": "EN 13133",
                "anmerkung": "DC-Versorgung Blitzleuchte"
            },
            {
                "kuerzel": "PA-NT-ZE",
                "bezeichnung": "Zentrale Meldung / BMS-Schnittstelle",
                "typ": "LIYCY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 24,
                "norm": "EN 13133",
                "anmerkung": "Potenzialfreier Kontakt oder RS485"
            },
            {
                "kuerzel": "PA-NT-VER",
                "bezeichnung": "Versorgungsleitung Notrufzentrale",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "USV-Einspeisung empfohlen, Absicherung B10A"
            },
        ]
    },

    # =========================================================================
    # CLUSTER 3: MSR/GWA – MESS-, STEUER-, REGELUNG / GASWARNANLAGEN
    # =========================================================================
    "MSR/GWA": {
        "beschreibung": "MSR-Technik, Gaswarnanlage EN 378 / ATEX",
        "kabel_typen": [
            {
                "kuerzel": "MSR-GWA-SEN",
                "bezeichnung": "Gassensor / Detektor (4–20 mA)",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.75, 1.0],
                "spannung_v": 24,
                "norm": "EN 378-3 / IEC 60079",
                "anmerkung": "Abgeschirmt, 4–20 mA Analogsignal, max. 200 m"
            },
            {
                "kuerzel": "MSR-GWA-BUS",
                "bezeichnung": "GWA Buskabel (RS485/Modbus)",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 5,
                "norm": "EIA-485",
                "anmerkung": "Abgeschirmt, max. 1200 m, 120-Ohm Abschlusswiderstand"
            },
            {
                "kuerzel": "MSR-GWA-HORN",
                "bezeichnung": "GWA Horn / Sirene",
                "typ": "YMM-J",
                "aderzahl": 2,
                "querschnitt_mm2": [1.5],
                "spannung_v": 24,
                "norm": "EN 378-3",
                "anmerkung": "Alarmhorn, DC-Versorgung"
            },
            {
                "kuerzel": "MSR-GWA-REL",
                "bezeichnung": "GWA Relaisausgang / Lüftungsansteuerung",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5, 2.5],
                "spannung_v": 230,
                "norm": "EN 378-3",
                "anmerkung": "Schaltausgang für Lüftungsfreigabe"
            },
            {
                "kuerzel": "MSR-TF-PT100",
                "bezeichnung": "MSR Temperaturfühler PT100 / PT1000",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "IEC 60751",
                "anmerkung": "3-Leiter-Schaltung, abgeschirmt"
            },
            {
                "kuerzel": "MSR-TF-NTC",
                "bezeichnung": "MSR Temperaturfühler NTC",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "DIN 44081",
                "anmerkung": "Abgeschirmt, 10 kΩ @ 25°C Standard"
            },
            {
                "kuerzel": "MSR-DI-DO",
                "bezeichnung": "MSR Digital I/O Steuerkabel",
                "typ": "LIYY",
                "aderzahl": 8,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Digitale Ein-/Ausgänge SPS"
            },
            {
                "kuerzel": "MSR-ANALOG",
                "bezeichnung": "MSR Analogsignal 0–10V / 4–20mA",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.75],
                "spannung_v": 10,
                "norm": "IEC 60381",
                "anmerkung": "Abgeschirmt, Schirm einseitig auflegen"
            },
            {
                "kuerzel": "MSR-VER",
                "bezeichnung": "MSR-Schrank Versorgung",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [2.5, 4.0],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "3L+N+PE, Absicherung nach Last"
            },
            {
                "kuerzel": "MSR-XWEB-BUS",
                "bezeichnung": "Dixell XWEB Bus J-Y(ST)Y 2x2x0,8mm²",
                "typ": "J-Y(ST)Y",
                "aderzahl": 4,
                "querschnitt_mm2": [0.8],
                "spannung_v": 5,
                "norm": "EIA-485 / Dixell XWEB Manual",
                "anmerkung": "XWEB 300/500/800. Modbus RTU 9600/8/N/1. J-Y(ST)Y geschirmt paarweise verseilt. RS485 A+/B-/GND+Reserve. Schirm einseitig am XWEB erden. Max. 1200m Buslänge."
            },
            {
                "kuerzel": "MSR-BEWEGUNG",
                "bezeichnung": "Bewegungsmelder Steuerleitung 4x0,75mm²",
                "typ": "LIYY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.75],
                "spannung_v": 230,
                "norm": "VDE 0812 / ÖVE/ÖNORM E 8001",
                "anmerkung": "Bewegungsmelder → Kühlstellenregler. Schaltet Innenbeleuchtung + Verdampferlüfter (Zeitverzögerung). 4 Adern: Phase, N, Eingang Regler, Reserve."
            },
            {
                "kuerzel": "MSR-UNTERFRIER",
                "bezeichnung": "Unterfrierschutzheizung SIHF 3x1,5mm²",
                "typ": "SIHF",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001 / DIN VDE 0298",
                "anmerkung": "Bodenschutzheizung TK-Zellen (Estrich/Unterlüftung). Silikonleitung hitzestabil bis 180°C. Kaltenden-Anschluss 230V. Mit Reservekreis und Temperaturfühler."
            },
        ]
    },

    # =========================================================================
    # CLUSTER 4: EEV – ELEKTRONISCHES EXPANSIONSVENTIL
    # =========================================================================
    "EEV": {
        "beschreibung": "Elektronisches Expansionsventil – Kabel je nach EEV-Typ unterschiedlich!",
        "kabel_typen": [
            {
                "kuerzel": "EEV-MOT",
                "bezeichnung": "Schrittmotor EEV Motorkabel 6x0,5mm² (Ventil → Treiber)",
                "typ": "LIYY",
                "aderzahl": 6,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 12,
                "norm": "VDE 0812 / Herstellervorgabe",
                "anmerkung": "⚠️ MAX 5–8m! 6-adrig für Schrittmotorwicklungen (2 Phasen à 2 Adern + 2xNTC). Längeres Kabel → Induktivitätsschäden am Treiber. Treiber sitzt nahe am Ventil!"
            },
            {
                "kuerzel": "EEV-TREIBER-STEUER",
                "bezeichnung": "Schrittmotor Treiber Steuerleitung (Treiber → Regler)",
                "typ": "LIYCY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 24,
                "norm": "EIA-485 / VDE 0812",
                "anmerkung": "Vom externen Treiber (AKV, EXD, EKE) zum Regler. Normale Länge möglich. RS485/Analog/CAN je nach Treiber-Typ."
            },
            {
                "kuerzel": "EEV-TREIBER-VER",
                "bezeichnung": "Schrittmotor Treiber Versorgung 230V (Regler → Treiber)",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "Spannungsversorgung für externen EEV-Treiber (AKV, EXD...). Treiber sitzt nahe am Ventil."
            },
            {
                "kuerzel": "EEV-EVD-ICE",
                "bezeichnung": "Carel EVD ice / EVD Evolution Versorgung 230V",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001 / Carel EVD Manual",
                "anmerkung": "EVD ice: Elektronik + Treiber am Verdampfer vormontiert → wird wie Magnetventil angesteuert. Nur 230V Versorgung + RS485 Bus zum Regler. Normales Kabel, keine Längenbeschränkung."
            },
            {
                "kuerzel": "EEV-EVD-BUS",
                "bezeichnung": "Carel EVD ice RS485 Bus zum Regler",
                "typ": "J-Y(ST)Y",
                "aderzahl": 4,
                "querschnitt_mm2": [0.8],
                "spannung_v": 5,
                "norm": "EIA-485 / Carel EVD Manual",
                "anmerkung": "pLAN oder RS485 Modbus vom EVD ice zum Carel-Regler. Standard Buslänge max. 1200m."
            },
            {
                "kuerzel": "EEV-PWM-AKV",
                "bezeichnung": "PWM-Ventil Danfoss AKV Steuerleitung 2x0,5mm²",
                "typ": "LIYY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 24,
                "norm": "VDE 0812 / Danfoss AKV Manual",
                "anmerkung": "Danfoss AKV: Magnetspule, PWM-gesteuert vom Regler. Einfaches 2-adriges Steuerkabel. Keine Längenbeschränkung wie Schrittmotor."
            },
            {
                "kuerzel": "EEV-TF-SAUG",
                "bezeichnung": "EEV Temperaturfühler Saugleitung LIYCY 2x0,5mm²",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "IEC 60751 / VDE 0812",
                "anmerkung": "NTC oder PT100 für Überhitzungsregelung – abgeschirmt. Sitzt am Saugleitungsaustritt des Verdampfers."
            },
            {
                "kuerzel": "EEV-TF-AUS",
                "bezeichnung": "EEV Temperaturfühler Auslass LIYCY 2x0,5mm²",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "IEC 60751 / VDE 0812",
                "anmerkung": "NTC/PT100 abgeschirmt – Verdampfungstemperatur-Messung"
            },
            {
                "kuerzel": "EEV-DRUCK",
                "bezeichnung": "EEV Druckfühler 4-20mA LIYCY 3x0,75mm²",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "IEC 60381 / VDE 0812",
                "anmerkung": "3-Leiter 4-20mA Niederdruckfühler für Überhitzungsregelung – abgeschirmt"
            },
        ]
    },

    # =========================================================================
    # CLUSTER 5: ICOOL / KICONEX – IoT MONITORING
    # =========================================================================
    "ICOOL/Kiconex": {
        "beschreibung": "IoT-Gateway, Fernüberwachung, Cloud-Anbindung",
        "kabel_typen": [
            {
                "kuerzel": "ICK-RS485",
                "bezeichnung": "Kiconex RS485 Modbus Bus J-Y(ST)Y 2x2x0,8mm²",
                "typ": "J-Y(ST)Y",
                "aderzahl": 4,
                "querschnitt_mm2": [0.8],
                "spannung_v": 5,
                "norm": "EIA-485",
                "anmerkung": "A/B/GND, abgeschirmt, max. 1200 m, 120 Ω"
            },
            {
                "kuerzel": "ICK-ETH",
                "bezeichnung": "Kiconex LAN / Ethernet",
                "typ": "Cat6a S/FTP",
                "aderzahl": 8,
                "querschnitt_mm2": [0.25],
                "spannung_v": 5,
                "norm": "ISO/IEC 11801",
                "anmerkung": "Abgeschirmt Cat6a, max. 100 m, RJ45"
            },
            {
                "kuerzel": "ICK-VER",
                "bezeichnung": "Kiconex Gateway Versorgung",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "230 VAC Einspeisung, intern 24 VDC"
            },
            {
                "kuerzel": "ICK-DI",
                "bezeichnung": "Kiconex Digital Input (potenzialfrei)",
                "typ": "LIYY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.5],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Störmeldungen, Türkontakte"
            },
            {
                "kuerzel": "ICK-TF",
                "bezeichnung": "Kiconex Temperaturfühler NTC",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "DIN 44081",
                "anmerkung": "Abgeschirmt, direkt an Gateway"
            },
            {
                "kuerzel": "ICK-ANALOG",
                "bezeichnung": "Kiconex Analogeingang 0–10V",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.75],
                "spannung_v": 10,
                "norm": "IEC 60381",
                "anmerkung": "Abgeschirmt, Schirm einseitig"
            },
        ]
    },

    # =========================================================================
    # CLUSTER 6: VERBUNDANLAGE (Zentralkälteanlage)
    # =========================================================================
    "Verbundanlage": {
        "beschreibung": "Zentralkälteanlage, Verdichterverbund, Rack",
        "kabel_typen": [
            {
                "kuerzel": "VA-VD-HV",
                "bezeichnung": "Verdichter Hauptversorgung",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [4.0, 6.0, 10.0, 16.0],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "3L+N+PE, Querschnitt nach Motorleistung"
            },
            {
                "kuerzel": "VA-VD-ST",
                "bezeichnung": "Verdichter Steuerkabel",
                "typ": "LIYY",
                "aderzahl": 6,
                "querschnitt_mm2": [0.75, 1.0],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Freigabe, Störmeldung, Laufmeldung"
            },
            {
                "kuerzel": "VA-HD-LP",
                "bezeichnung": "Hochdruck-/Niederdruckwächter",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5],
                "spannung_v": 24,
                "norm": "EN 13313",
                "anmerkung": "Abgeschirmt, NC-Kontakt, Sicherheitskette"
            },
            {
                "kuerzel": "VA-OLR",
                "bezeichnung": "Ölstandsregler / Ölheizung",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "Ölheizung 50 W, Ölstandswächter"
            },
            {
                "kuerzel": "VA-SAMMLER",
                "bezeichnung": "Flüssigkeitssammler Fühler",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "DIN 44081",
                "anmerkung": "Füllstandssensor / Temperaturfühler"
            },
            {
                "kuerzel": "VA-LUE",
                "bezeichnung": "Lüftermotor Verflüssiger Verbund",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [1.5, 2.5],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM EN 60228",
                "anmerkung": "3-phasig, Drehzahlregelung via FU"
            },
            {
                "kuerzel": "VA-FU",
                "bezeichnung": "Frequenzumrichter Steuerleitung",
                "typ": "LIYCY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.75],
                "spannung_v": 10,
                "norm": "IEC 60381",
                "anmerkung": "Abgeschirmt, 0–10V Sollwert, EMV-kritisch"
            },
            {
                "kuerzel": "VA-SPS",
                "bezeichnung": "SPS/Verbundsteuerung Bus",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "EIA-485",
                "anmerkung": "Modbus RTU, abgeschirmt"
            },
            {
                "kuerzel": "VA-ABT",
                "bezeichnung": "Abtausteuerung Verbund",
                "typ": "LIYY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Zeitschaltuhr, Heißgas-/Elektroabtau"
            },
        ]
    },

    # =========================================================================
    # CLUSTER 7: VERFLÜSSIGER (Außengerät / Kondensator)
    # =========================================================================
    "Verflüssiger": {
        "beschreibung": "Außenverflüssiger, Luft- und Wasserverflüssiger",
        "kabel_typen": [
            {
                "kuerzel": "VFL-VER",
                "bezeichnung": "Verflüssiger Hauptversorgung",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [2.5, 4.0, 6.0],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "3L+N+PE, UV-beständig, Außeneinsatz"
            },
            {
                "kuerzel": "VFL-LUE",
                "bezeichnung": "Verflüssiger Lüftermotoren",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [1.5, 2.5],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM EN 60228",
                "anmerkung": "Mehrfachlüfter, Daisy-Chain möglich"
            },
            {
                "kuerzel": "VFL-TF",
                "bezeichnung": "Verflüssiger Temperaturfühler",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "DIN 44081",
                "anmerkung": "Abgeschirmt, Außeneinsatz IP65"
            },
            {
                "kuerzel": "VFL-DRUCK",
                "bezeichnung": "Verflüssiger Druckfühler HD",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "IEC 60381",
                "anmerkung": "4–20 mA, 0–40 bar HD-Seite"
            },
            {
                "kuerzel": "VFL-FU-LUE",
                "bezeichnung": "FU-Ansteuerung Verflüssigerlüfter",
                "typ": "LIYCY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.75],
                "spannung_v": 10,
                "norm": "IEC 60381",
                "anmerkung": "Abgeschirmt, 0–10V Sollwert"
            },
            {
                "kuerzel": "VFL-HEI",
                "bezeichnung": "Verflüssiger Kurbelgehäuseheizung",
                "typ": "SIHF",
                "aderzahl": 2,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "Dauerbetrieb, Silikonleitung"
            },
            {
                "kuerzel": "VFL-ST",
                "bezeichnung": "Verflüssiger Steuerkabel",
                "typ": "LIYY",
                "aderzahl": 5,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Freigabe, Störmeldung, Stufenregelung"
            },
        ]
    },

    # =========================================================================
    # CLUSTER 8: BÄCKEREI (Spezialanforderungen Profiküche Bäckerei)
    # =========================================================================
    "Bäckerei": {
        "beschreibung": "Kälteanlagen Bäckerei: Gärverzögerung, Stikkenkühlschrank, Gärschrank",
        "kabel_typen": [
            {
                "kuerzel": "BK-GV-VER",
                "bezeichnung": "Gärverzögerungsschrank Versorgung",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [2.5, 4.0],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "3L+N+PE, Feuchtigkeitsschutz IP44"
            },
            {
                "kuerzel": "BK-GV-ST",
                "bezeichnung": "Gärverzögerung Steuerung/Timer",
                "typ": "LIYY",
                "aderzahl": 6,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Programmuhr, Feuchtesteuerung, Lüfter"
            },
            {
                "kuerzel": "BK-GV-TF",
                "bezeichnung": "Gärverzögerung Temperaturfühler",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "DIN 44081",
                "anmerkung": "Innenraum NTC, abgeschirmt"
            },
            {
                "kuerzel": "BK-GV-FF",
                "bezeichnung": "Gärverzögerung Feuchtefühler",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "IEC 60381",
                "anmerkung": "Kapazitiv 4–20 mA, 0–100% rF"
            },
            {
                "kuerzel": "BK-ST-VER",
                "bezeichnung": "Stikkenofen/Stikkenkühlschrank Versorgung",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [4.0, 6.0],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "3L+N+PE, hohe Anschlussleistung"
            },
            {
                "kuerzel": "BK-ABT-HZ",
                "bezeichnung": "Abtauheizung Bäckerei (feuchte Umgebung)",
                "typ": "SIHF",
                "aderzahl": 2,
                "querschnitt_mm2": [2.5, 4.0],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "Silikonleitung, hohe Abtauleistung"
            },
            {
                "kuerzel": "BK-RUE-TF",
                "bezeichnung": "Rücklauftemperaturfühler Kühlwasser",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "DIN 44081",
                "anmerkung": "Tauchhülse, PT100 oder NTC"
            },
        ]
    },

    # =========================================================================
    # CLUSTER 9: GASTRO (Gastronomie / Profiküche)
    # =========================================================================
    "Gastro": {
        "beschreibung": "Kälteanlagen Gastronomie: Kühlzellen, Kühltheken, Getränkeanlagen",
        "kabel_typen": [
            {
                "kuerzel": "GA-KZ-VER",
                "bezeichnung": "Kühlzelle Versorgung",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [2.5, 4.0],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "3L+N+PE, GFCI/FI erforderlich, Nassbereich"
            },
            {
                "kuerzel": "GA-KZ-TF-IN",
                "bezeichnung": "Kühlzelle Innenfühler",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "DIN 44081",
                "anmerkung": "Abgeschirmt, NTC, lebensmitteltauglich IP67"
            },
            {
                "kuerzel": "GA-KZ-TF-ABT",
                "bezeichnung": "Kühlzelle Abtaufühler",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "DIN 44081",
                "anmerkung": "Am Verdampfer, Abtauendpunkt"
            },
            {
                "kuerzel": "GA-KZ-HZ",
                "bezeichnung": "Kühlzelle Abtauheizung",
                "typ": "SIHF",
                "aderzahl": 2,
                "querschnitt_mm2": [1.5, 2.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "Silikonleitung, Nassbereich"
            },
            {
                "kuerzel": "GA-KZ-TUE",
                "bezeichnung": "Kühlzelle Türheizung / Türkontakt",
                "typ": "LIYY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Rahmenheizband + NO-Türkontakt"
            },
            {
                "kuerzel": "GA-THE-VER",
                "bezeichnung": "Kühltheke Versorgung",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [2.5, 4.0],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "3L+N+PE, FI-Schutz Nassbereich"
            },
            {
                "kuerzel": "GA-THE-LED",
                "bezeichnung": "Kühltheke LED-Beleuchtung",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "Getrennte Beleuchtungsphase"
            },
            {
                "kuerzel": "GA-GET-VER",
                "bezeichnung": "Getränkekühlanlage Versorgung",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5, 2.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "1-phasig, Split-Geräte"
            },
        ]
    },


    # =========================================================================
    # CLUSTER: BUS-LEITUNGEN (alle Hersteller-Anforderungen)
    # =========================================================================
    "Bus-Leitungen": {
        "beschreibung": "Datenleitungen, Busse, strukturierte Verkabelung – alle Hersteller",
        "kabel_typen": [
            {
                "kuerzel": "BUS-RS485-2x2x08",
                "bezeichnung": "RS485/Modbus Bus J-Y(ST)Y 2x2x0,8mm² *** DEFAULT ***",
                "typ": "J-Y(ST)Y",
                "aderzahl": 4,
                "querschnitt_mm2": [0.8],
                "spannung_v": 5,
                "norm": "EIA-485 / VDE 0816 / DIN VDE 0816",
                "anmerkung": "STANDARD Bus-Leitung allgemein. 2 Adernpaare verseilt und geschirmt. Paar 1: A+/B- (Daten), Paar 2: GND/Reserve. Für XWEB, Modbus RTU, Kiconex, Carel, Danfoss. Max. 1200m, 120Ω Abschluss an beiden Enden."
            },
            {
                "kuerzel": "BUS-RS485-2x2x1",
                "bezeichnung": "RS485 Bus J-Y(ST)Y 2x2x1,0mm² gedrillt+geschirmt",
                "typ": "J-Y(ST)Y",
                "aderzahl": 4,
                "querschnitt_mm2": [1.0],
                "spannung_v": 5,
                "norm": "EIA-485 / VDE 0816",
                "anmerkung": "Für längere Strecken >500m oder EMV-kritische Umgebung (Maschinenraum, FU-Nähe)."
            },
            {
                "kuerzel": "BUS-RS485-3x05",
                "bezeichnung": "RS485 Modbus Bus LIYCY 3x0,5mm² geschirmt",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 5,
                "norm": "EIA-485 / IEC 61158",
                "anmerkung": "A/B/GND abgeschirmt. Alternativ zu J-Y(ST)Y, teils von Herstellern vorgegeben (Dixell XWEB: Belden 8772 äquivalent). Max. 1200m, 120Ω Abschluss."
            },
            {
                "kuerzel": "BUS-RS485-2x2x1",
                "bezeichnung": "RS485 Bus 2x2x1,0mm² gedrillt+geschirmt",
                "typ": "J-Y(ST)Y",
                "aderzahl": 4,
                "querschnitt_mm2": [1.0],
                "spannung_v": 5,
                "norm": "EIA-485 / VDE 0816",
                "anmerkung": "2 Adernpaare verseilt+geschirmt. Für längere Strecken >500m oder EMV-kritische Umgebung."
            },
            {
                "kuerzel": "BUS-CAN-2x2x075",
                "bezeichnung": "CAN-Bus / Wurm F-BUS 2x2x0,75mm² LiYCY(TP)",
                "typ": "LiYCY(TP)",
                "aderzahl": 4,
                "querschnitt_mm2": [0.75],
                "spannung_v": 5,
                "norm": "ISO 11898 / DIN 47100",
                "anmerkung": "Wurm Frigolink F-BUS Vorschrift: LiYCY(TP) 2x2x0,75mm², twisted pair, Kupfergeflecht. Wellenwiderstand 95-140Ω (ISO 11898-2). Max. 400m bei 20kBit/s. Schirm einseitig im Schaltschrank."
            },
            {
                "kuerzel": "BUS-DANBUSS",
                "bezeichnung": "Danfoss DANBUSS / LON RS485",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 5,
                "norm": "EIA-485 / Danfoss AK Design Guide",
                "anmerkung": "Danfoss ADAP-KOOL: geschirmtes Kabel, Schirm von Gerät zu Gerät durchschleifen, NICHT erden (wird intern geerdet). Max. 1200m. 120Ω Terminierung an beiden Enden."
            },
            {
                "kuerzel": "BUS-PROFIBUS",
                "bezeichnung": "PROFIBUS DP Standard (Siemens S7)",
                "typ": "PROFIBUS FC Standard",
                "aderzahl": 2,
                "querschnitt_mm2": [0.64],
                "spannung_v": 5,
                "norm": "IEC 61158 / EN 50170",
                "anmerkung": "Violett, 150Ω, max. 1200m/Segment, DB9-Stecker. Siemens S7 / PROFIBUS DP."
            },
            {
                "kuerzel": "BUS-DIXELL-RS485",
                "bezeichnung": "Dixell XWEB RS485 Bus",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "EIA-485 / Dixell XWEB Manual",
                "anmerkung": "Dixell XWEB Vorschrift: 2-3 Leiter geschirmt, min. 0,5mm² (z.B. Belden 8772). Modbus RTU 9600/8/N/1. TTL-Geräte: XJ485 Adapter nötig. Polarität A+/B- beachten."
            },
        ]
    },

    # =========================================================================
    # CLUSTER: SENSOR-LEITUNGEN (alle geschirmt)
    # =========================================================================
    "Sensor-Leitungen": {
        "beschreibung": "Alle Sensorleitungen – grundsätzlich geschirmt (LIYCY)",
        "kabel_typen": [
            {
                "kuerzel": "SEN-NTC-2x05",
                "bezeichnung": "NTC Temperaturfühler 2x0,5mm² geschirmt",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "DIN 44081 / VDE 0812",
                "anmerkung": "Standard NTC 10kΩ @ 25°C. LIYCY abgeschirmt – Schirm einseitig am Regler/HACCP-Modul auflegen. Max. 50m empfohlen."
            },
            {
                "kuerzel": "SEN-NTC-2x075",
                "bezeichnung": "NTC Temperaturfühler 2x0,75mm² geschirmt",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.75],
                "spannung_v": 5,
                "norm": "DIN 44081 / VDE 0812",
                "anmerkung": "Für längere Leitungen >50m. LIYCY abgeschirmt."
            },
            {
                "kuerzel": "SEN-PT100-3x05",
                "bezeichnung": "PT100/PT1000 3-Leiter 3x0,5mm² geschirmt",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "IEC 60751 / VDE 0812",
                "anmerkung": "3-Leiter-Schaltung für PT100/PT1000. LIYCY abgeschirmt. Höhere Genauigkeit als NTC."
            },
            {
                "kuerzel": "SEN-420MA-2x075",
                "bezeichnung": "4-20mA Analogsignal 2x0,75mm² geschirmt",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "IEC 60381 / VDE 0812",
                "anmerkung": "4-20mA Stromsignal – GWA-Sensor, Druckfühler, Feuchtefühler. LIYCY abgeschirmt, Schirm einseitig an Auswertegerät."
            },
            {
                "kuerzel": "SEN-GWA-2x075",
                "bezeichnung": "Gaswarnanlage Sensor 4-20mA 2x0,75mm² geschirmt",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "EN 378-3 / IEC 60079 / VDE 0812",
                "anmerkung": "GWA-Sensor 4-20mA. LIYCY abgeschirmt. Bei NH3/R290: ATEX-Zone 2 beachten. Max. 200m."
            },
            {
                "kuerzel": "SEN-010V-2x05",
                "bezeichnung": "0-10V Analogsignal 2x0,5mm² geschirmt",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.5],
                "spannung_v": 10,
                "norm": "IEC 60381 / VDE 0812",
                "anmerkung": "0-10V Sollwertvorgabe, FU-Steuerung, Regelventile. LIYCY abgeschirmt."
            },
        ]
    },

    # =========================================================================
    # CLUSTER: AUSSENUNIT / CONTROLLBOX (Betriebszustände + Störmeldungen)
    # =========================================================================
    "Aussenunit-Steuerung": {
        "beschreibung": "Außenunit / Controllerbox: Betriebszustände, Störmeldungen, potenzialfreie Kontakte",
        "kabel_typen": [
            {
                "kuerzel": "AU-7x1-STEUER",
                "bezeichnung": "Außenunit Steuerkabel 7x1,0mm²",
                "typ": "LIYY",
                "aderzahl": 7,
                "querschnitt_mm2": [1.0],
                "spannung_v": 24,
                "norm": "VDE 0812 / ÖVE/ÖNORM E 8001",
                "anmerkung": "Standard für Außenunit/Controllerbox. 7 Adern für: Freigabe, Lüfterstufen 1-3, Betrieb, Störung, Reserve. Potenzialfreie Kontakte 24V."
            },
            {
                "kuerzel": "AU-7x15-STEUER",
                "bezeichnung": "Außenunit Steuerkabel 7x1,5mm² (230V Kontakte)",
                "typ": "YMM-J",
                "aderzahl": 7,
                "querschnitt_mm2": [1.5],
                "spannung_v": 230,
                "norm": "ÖVE/ÖNORM E 8001 / VDE 0298",
                "anmerkung": "Für 230V Steuerkontakte an Außenunit. 7 Adern: Freigabe, Stufen, Betriebsmeldung, Störung, Reserve."
            },
            {
                "kuerzel": "AU-STOER-4x05",
                "bezeichnung": "Störmeldung Außenunit 4x0,5mm² potenzialfrei",
                "typ": "LIYY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Potenzialfreie Störmelde-Kontakte: Kältemittel-Hochdruck, Niederdruck, Motorschutz, Sammelstörung. NC-Kontakte empfohlen."
            },
            {
                "kuerzel": "AU-BETR-4x05",
                "bezeichnung": "Betriebszustand Außenunit 4x0,5mm²",
                "typ": "LIYY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.5, 0.75],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Betriebszustandsmeldungen: Verdichter läuft, Abtau aktiv, Lüfter aktiv, Reserve. Potenzialfreie Öffner/Schließer."
            },
            {
                "kuerzel": "AU-VERB-7x1",
                "bezeichnung": "Verbundanlage Controllerbox 7x1,0mm²",
                "typ": "LIYY",
                "aderzahl": 7,
                "querschnitt_mm2": [1.0],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Verbundanlage Controller: Freigabe, Druckstufen (HD/ND), Betrieb V1/V2/V3, Sammelstörung. Pro Controllerbox ein Kabel."
            },
            {
                "kuerzel": "AU-RS485-CTRL",
                "bezeichnung": "Controllerbox RS485 Bus 3x0,5mm² geschirmt",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "EIA-485 / VDE 0812",
                "anmerkung": "RS485 Modbus von Controllerbox zum Monitoring. LIYCY abgeschirmt. Ergänzend zu potenzialfreien Kontakten wenn Bus-kompatibel."
            },
        ]
    },

    # =========================================================================
    # CLUSTER 10: INDUSTRIE / S7 (Industriekälte, SPS Siemens S7)
    # =========================================================================
    "Industrie/S7": {
        "beschreibung": "Industriekälteanlagen, SPS S7, PROFIBUS/PROFINET",
        "kabel_typen": [
            {
                "kuerzel": "S7-PB",
                "bezeichnung": "PROFIBUS DP Kabel",
                "typ": "PROFIBUS FC Standard",
                "aderzahl": 2,
                "querschnitt_mm2": [0.64],
                "spannung_v": 5,
                "norm": "IEC 61158 / EN 50170",
                "anmerkung": "Violett, 150 Ω, max. 1200 m/Segment, DB9"
            },
            {
                "kuerzel": "S7-PN-KABEL",
                "bezeichnung": "PROFINET Industrie-Ethernet",
                "typ": "Cat6 Industrial IE FC",
                "aderzahl": 8,
                "querschnitt_mm2": [0.14],
                "spannung_v": 5,
                "norm": "IEC 61784 / IEEE 802.3",
                "anmerkung": "Siemens IE FC, geschirmt, max. 100 m"
            },
            {
                "kuerzel": "S7-MPI",
                "bezeichnung": "S7 MPI / PPI Kabel",
                "typ": "LIYCY",
                "aderzahl": 3,
                "querschnitt_mm2": [0.5],
                "spannung_v": 5,
                "norm": "IEC 61158",
                "anmerkung": "RS485-basiert, 9,6 kBit–12 MBit/s"
            },
            {
                "kuerzel": "S7-AI-STR",
                "bezeichnung": "S7 Analogeingang Strom 4–20 mA",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.75],
                "spannung_v": 24,
                "norm": "IEC 60381",
                "anmerkung": "Abgeschirmt, Schirm an SPS-Masse"
            },
            {
                "kuerzel": "S7-AI-SPAN",
                "bezeichnung": "S7 Analogeingang Spannung 0–10V",
                "typ": "LIYCY",
                "aderzahl": 2,
                "querschnitt_mm2": [0.75],
                "spannung_v": 10,
                "norm": "IEC 60381",
                "anmerkung": "Abgeschirmt"
            },
            {
                "kuerzel": "S7-DO-REL",
                "bezeichnung": "S7 Digitalausgang Relais 24VDC",
                "typ": "LIYY",
                "aderzahl": 2,
                "querschnitt_mm2": [1.0, 1.5],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "Schaltausgang, Freilaufdiode vorsehen"
            },
            {
                "kuerzel": "S7-VER-SCHRANK",
                "bezeichnung": "S7-Schaltschrank Haupteinspeisung",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [10.0, 16.0, 25.0],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "3L+N+PE, Querschnitt nach Schaltschrankleistung"
            },
            {
                "kuerzel": "S7-VER-24V",
                "bezeichnung": "S7 24VDC Versorgung SPS/IO",
                "typ": "YMM-J",
                "aderzahl": 3,
                "querschnitt_mm2": [1.5, 2.5],
                "spannung_v": 24,
                "norm": "VDE 0812",
                "anmerkung": "DC-Versorgung, Netzteil im Schrank"
            },
            {
                "kuerzel": "S7-ANTRIEB",
                "bezeichnung": "S7 Motoransteuerung Schütz/Sanftanlasser",
                "typ": "YMM-J",
                "aderzahl": 5,
                "querschnitt_mm2": [4.0, 6.0, 10.0],
                "spannung_v": 400,
                "norm": "ÖVE/ÖNORM E 8001",
                "anmerkung": "3L+N+PE, Abschirmung bei FU-Betrieb"
            },
            {
                "kuerzel": "S7-SIMATIC-HMI",
                "bezeichnung": "S7 Simatic HMI Verbindungskabel",
                "typ": "LIYCY",
                "aderzahl": 4,
                "querschnitt_mm2": [0.25],
                "spannung_v": 5,
                "norm": "RS232 / MPI",
                "anmerkung": "HMI-Display Anschluss, max. 15 m"
            },
        ]
    },

}

# =============================================================================
# HILFSFUNKTIONEN KABELBERECHNUNG
# =============================================================================

def berechne_leitungsquerschnitt(leistung_w: float, spannung_v: float,
                                  laenge_m: float, cos_phi: float = 0.9,
                                  spannungsfall_pct: float = 3.0,
                                  phasen: int = 1) -> dict:
    """
    Berechnet den Mindestquerschnitt nach Spannungsfall-Methode.
    Norm: ÖVE/ÖNORM E 8001 / DIN VDE 0298
    """
    rho = 0.0178  # spez. Widerstand Cu in Ω·mm²/m

    if phasen == 1:
        strom_a = leistung_w / (spannung_v * cos_phi)
        delta_u = spannung_v * (spannungsfall_pct / 100)
        querschnitt_mm2 = (2 * rho * laenge_m * strom_a) / delta_u
    else:
        strom_a = leistung_w / (math.sqrt(3) * spannung_v * cos_phi)
        delta_u = spannung_v * (spannungsfall_pct / 100)
        querschnitt_mm2 = (math.sqrt(3) * rho * laenge_m * strom_a) / delta_u

    # Normquerschnitte (DIN VDE 0298)
    norm_querschnitte = [0.5, 0.75, 1.0, 1.5, 2.5, 4.0, 6.0, 10.0, 16.0, 25.0, 35.0, 50.0]
    querschnitt_gewaehlt = next((q for q in norm_querschnitte if q >= querschnitt_mm2), 50.0)

    return {
        "leistung_w": leistung_w,
        "spannung_v": spannung_v,
        "phasen": phasen,
        "cos_phi": cos_phi,
        "laenge_m": laenge_m,
        "strom_a": round(strom_a, 2),
        "spannungsfall_pct_max": spannungsfall_pct,
        "querschnitt_berechnet_mm2": round(querschnitt_mm2, 3),
        "querschnitt_gewaehlt_mm2": querschnitt_gewaehlt,
        "hinweis": "Thermische Belastbarkeit (VDE 0298-4) separat prüfen!"
    }


def berechne_spannungsfall(querschnitt_mm2: float, strom_a: float,
                            laenge_m: float, spannung_v: float,
                            phasen: int = 1) -> dict:
    """
    Berechnet den tatsächlichen Spannungsfall für einen gegebenen Querschnitt.
    """
    rho = 0.0178
    if phasen == 1:
        delta_u_v = (2 * rho * laenge_m * strom_a) / querschnitt_mm2
    else:
        delta_u_v = (math.sqrt(3) * rho * laenge_m * strom_a) / querschnitt_mm2

    delta_u_pct = (delta_u_v / spannung_v) * 100

    return {
        "querschnitt_mm2": querschnitt_mm2,
        "strom_a": strom_a,
        "laenge_m": laenge_m,
        "spannungsfall_v": round(delta_u_v, 3),
        "spannungsfall_pct": round(delta_u_pct, 2),
        "ok": delta_u_pct <= 3.0
    }


def get_alle_cluster() -> list:
    """Gibt Liste aller verfügbaren Cluster zurück."""
    return list(KABEL_MATRIX.keys())


def get_kabeltypen_fuer_cluster(cluster: str) -> list:
    """Gibt alle Kabeltypen für einen Cluster zurück."""
    if cluster in KABEL_MATRIX:
        return KABEL_MATRIX[cluster]["kabel_typen"]
    return []


def erstelle_kabelliste_dataframe(cluster: str) -> pd.DataFrame:
    """Erstellt einen DataFrame der Kabelliste für einen Cluster."""
    kabel = get_kabeltypen_fuer_cluster(cluster)
    if not kabel:
        return pd.DataFrame()

    rows = []
    for k in kabel:
        querschnitte = ", ".join([f"{q} mm²" for q in k["querschnitt_mm2"]])
        rows.append({
            "Kürzel": k["kuerzel"],
            "Bezeichnung": k["bezeichnung"],
            "Kabeltyp": k["typ"],
            "Adern": k["aderzahl"],
            "Querschnitt": querschnitte,
            "Spannung [V]": k["spannung_v"],
            "Norm": k["norm"],
            "Anmerkung": k["anmerkung"],
        })
    return pd.DataFrame(rows)


def suche_kabel(suchbegriff: str) -> pd.DataFrame:
    """Durchsucht alle Cluster nach einem Stichwort."""
    results = []
    for cluster, data in KABEL_MATRIX.items():
        for k in data["kabel_typen"]:
            felder = [k["kuerzel"], k["bezeichnung"], k["typ"], k["anmerkung"]]
            if any(suchbegriff.lower() in f.lower() for f in felder):
                querschnitte = ", ".join([f"{q} mm²" for q in k["querschnitt_mm2"]])
                results.append({
                    "Cluster": cluster,
                    "Kürzel": k["kuerzel"],
                    "Bezeichnung": k["bezeichnung"],
                    "Kabeltyp": k["typ"],
                    "Adern": k["aderzahl"],
                    "Querschnitt": querschnitte,
                    "Spannung [V]": k["spannung_v"],
                    "Norm": k["norm"],
                    "Anmerkung": k["anmerkung"],
                })
    return pd.DataFrame(results)


def exportiere_gesamtliste() -> pd.DataFrame:
    """Exportiert die komplette Kabelmatrix als DataFrame."""
    rows = []
    for cluster, data in KABEL_MATRIX.items():
        for k in data["kabel_typen"]:
            querschnitte = ", ".join([f"{q} mm²" for q in k["querschnitt_mm2"]])
            rows.append({
                "Cluster": cluster,
                "Kürzel": k["kuerzel"],
                "Bezeichnung": k["bezeichnung"],
                "Kabeltyp": k["typ"],
                "Adern": k["aderzahl"],
                "Querschnitt": querschnitte,
                "Spannung [V]": k["spannung_v"],
                "Norm": k["norm"],
                "Anmerkung": k["anmerkung"],
            })
    return pd.DataFrame(rows)
