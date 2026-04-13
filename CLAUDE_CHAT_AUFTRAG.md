# Auftrag: Waermepumpen_Auslegung.py -> HTML konvertieren

## Prompt fuer Claude Chat

Konvertiere die unten stehende Streamlit-App (Python) in eine **einzelne, selbststaendige HTML-Datei**.
Identische Berechnungslogik. Coolsulting Branding: Background #36A9E1, Text #3C3C3B, weisse Cards mit border-radius 12px.

### CDN Libraries einbinden:
```html
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
```

### Alle Features muessen rein:
1. Eingaben: Projekt, Flaeche, Baustandard-Dropdown (aktualisiert W/m2), Sperrzeit-Slider, Normtemp, Vorlauftemp, Heizsystem, Warmwasser-Option, Bivalenz-Modus
2. Berechnung: identisch zur Python-Logik (siehe Quellcode)
3. Pie-Chart (Plotly): Gebaeude / Warmwasser / Sperrzeit - Donut hole=0.5
4. Line-Chart (Plotly): Heizlastkennlinie mit Bivalenzpunkt (rot gestrichelt), Uebergang +7C (gruen gepunktet), WW-Grundlast (dunkelrot)
5. Hinweise/Warnungen je nach Vorlauftemperatur
6. PDF-Export per jsPDF: Header mit blauem Balken, Ergebnis gross, Systemdaten, Charts als Bilder (html2canvas), Disclaimer im Footer
7. Responsive (mobile: Spalten untereinander)
8. Einbettbar per iframe

---

## QUELLCODE: Waermepumpen_Auslegung.py

```python
# ==========================================
# DATEI: Waermepumpen_Auslegung.py
# ZEITSTEMPEL: 10.02.2026 - 17:50 Uhr
# VERSION: 3.8
#
# AENDERUNGEN:
# 1. TEXT: Platzhalter bei "Projekt / Kunde" auf "z.B.: Elke Muster" geaendert.
# 2. VERSIONING: App Version auf 3.8 hochgesetzt.
# 3. BEIBEHALTEN: Striktes Header-Format, gedrehte X-Achse (Kalt -> Warm), Logo & Text oben buendig (Y=10), Disclaimer mit geistigem Eigentum.
# ==========================================

import streamlit as st
import os
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import tempfile

# Globale Variable fuer die App-Version (wird in UI und PDF genutzt)
APP_VERSION = "3.8"

# ==========================================
# 1. PDF KLASSE
# ==========================================
class PDF(FPDF):
    def __init__(self, font_family="Helvetica"):
        super().__init__()
        self.font_family = font_family

    def header(self):
        blue = (54, 169, 225)
        self.set_fill_color(*blue)
        self.rect(0, 0, 210, 40, 'F')
        start_y = 10
        logo = "Coolsulting_Logo_ohneHG_outlines_weiss.png"
        if os.path.exists(logo):
            self.image(logo, x=10, y=start_y, w=100)
        self.set_y(start_y)
        self.set_font(self.font_family, 'B', 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, 'Waermepumpen-Auslegung', align='R', ln=True)
        self.set_font(self.font_family, '', 12)
        self.cell(0, 6, 'Modul 1: Heizlast-Berechnung', align='R', ln=True)
        self.set_font(self.font_family, 'I', 10)
        self.cell(0, 6, f'App Version: {APP_VERSION}', align='R', ln=True)
        self.ln(15)

    def footer(self):
        self.set_y(-25)
        self.set_font(self.font_family, 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f'Seite {self.page_no()}', align='C', ln=True)
        self.set_font(self.font_family, '', 7)
        self.set_text_color(150, 150, 150)
        disclaimer = ("HINWEIS: Diese Berechnung ist eine ueberschlaegige Auslegung auf Basis der Nutzerangaben "
                      "und geistiges Eigentum des Erstellers. Sie dient als Orientierungshilfe und ersetzt keine "
                      "detaillierte Heizlastberechnung nach DIN EN 12831. Alle Angaben ohne Gewaehr. "
                      "Eine fachgerechte Detailplanung ist erforderlich.")
        self.multi_cell(0, 3, disclaimer, align='C')

# ==========================================
# 2. MAIN APP - BERECHNUNGSLOGIK
# ==========================================
# Gebaeudestandards (Dropdown -> W/m2):
standards_dict = {
    "Unsanierter Altbau (vor 1980, Einfachverglasung)": 150,
    "Teilsanierter Altbau (Fenster neu/Doppelverglasung)": 100,
    "Standard Bestand (Bj. 1990-2000, Teilweise Daemmung)": 60,   # DEFAULT
    "Neubau / Gut gedaemmt (nach 2010)": 50,
    "KfW Effizienzhaus / Passivhaus": 30
}

# Kernberechnung:
# load_building_base = (flaeche * wm2) / 1000          # kW
# ww_faktor = (1.45 * 2.0 * 365) / 2400                # wenn WW aktiv
# load_ww_base = personen * ww_faktor                   # 0 wenn WW deaktiviert
# laufzeit = 24 - sperrzeit
# sperr_faktor = 24 / laufzeit
# load_building_real = load_building_base * sperr_faktor
# total_kw = load_building_real + load_ww_base
# sperr_aufschlag = load_building_real - load_building_base

# Heizlastkennlinie (Line-Chart):
# heizgrenze = 15.0
# fuer jede Temperatur t von (norm_temp-5) bis 20:
#   wenn t < 15: y = load_building_real * (15 - t) / (15 - norm_temp) + load_ww_base
#   sonst: y = load_ww_base

# Hinweise:
# flaeche > 300 && hatWW -> info "Gewerbe-Hinweis: WW-Bedarf pruefen."
# vl_temp <= 55 -> info "Vorlauftemperatur optimal."
# 55 < vl_temp <= 65 -> info "Hochtemperatur: R290/R744 empfohlen."
# 65 < vl_temp <= 75 -> info "Sehr hohe Temp: R290/R744 zwingend."
# vl_temp > 75 -> critical "Kritisch: >75C erfordert Sanierung."
# vl_temp > 50 && heizsystem == FBH -> warning ">50C bei FBH pruefen!"

# Bivalenz:
# Monoenergetisch: backup = "Heizstab", slider -20 bis 0, default -15
# Bivalent: backup = "Kessel (Bestand)", slider -10 bis 10, default 0

# PDF-Report soll enthalten:
# - Blauer Header-Balken mit "Waermepumpen-Auslegung" + "Modul 1"
# - Projektname, Datum, Bearbeiter
# - Ergebnis (total_kw) gross und blau
# - Lastaufstellung: Gebaeude, Sperrzeit-Zuschlag, WW-Zuschlag
# - Beide Charts als Bilder (html2canvas)
# - System-Parameter (Normtemp, Vorlauf, Heizsystem, Bivalenz)
# - Hinweise & Warnungen
# - Disclaimer im Footer
```
