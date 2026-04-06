# modules/kabelliste.py
# °coolWIRE v2.2 – Strukturierte Kabelliste pro Verbraucher
# (c) coolsulting e.U. | Michael Schäpers

from modules.kuehlstellen import TEMP_BEREICHE, kreis_zusammenfassung
from modules.calculation_kabel import KABEL_MATRIX

# =============================================================================
# STANDORT-OPTIONEN (zentral für Von/Bis)
# =============================================================================

STANDORT_TYPEN = [
    # Schaltschränke
    "Zentralschaltschrank",
    "Schaltschrank an Zelle",
    "Verteiler",
    # Kältetechnik
    "Außenunit / Verflüssiger Dach",
    "Außenunit / Verflüssiger Außenwand",
    "Verbundanlage Maschinenraum",
    "Aggregat",
    # Monitoring / Daten
    "HACCP-Modul",
    "Xweb / Dixell",
    "Kiconex Gateway",
    "Frigodata Gateway",
    "Carel boss",
    "Routerschrank / Netzwerk",
    "BMS / GLT",
    # Kühlstelle
    "Kühlstelle / Verdampfer",
    "Regler an Zelle",
    # Sonstiges
    "Sonstiges",
]


def get_kabel_info(kuerzel: str) -> dict:
    """Gibt Kabelinformationen aus der Matrix zurück."""
    for cl_data in KABEL_MATRIX.values():
        for kt in cl_data["kabel_typen"]:
            if kt["kuerzel"] == kuerzel:
                return kt
    return {}


def erzeuge_kabelliste(kuehlstellen: list,
                       maschinenstandorte: list,
                       steuerung: str,
                       haccp_module: list = None) -> list:
    """
    Erzeugt vollständige strukturierte Kabelliste.
    Jede Zeile = ein Kabel mit Von/Bis/Meter/Typ.
    Geordnet nach Kreis → Kühlstelle → Kabeltyp.
    """
    if haccp_module is None:
        haccp_module = []

    kreise = kreis_zusammenfassung(kuehlstellen)
    kabelliste = []
    lfd_nr = 1

    for kreis in kreise:
        kreis_nr = kreis["kreis_nr"]
        kreis_label = kreis["label"]

        # Maschinenstandort für diesen Kreis
        ms_name = "Maschinenraum"
        for ms in maschinenstandorte:
            ms_name = (ms.get("anlage_typ","") + " " +
                       ms.get("standort_maschine","")).strip()
            break  # erstmal erste Anlage

        for ks in kreis["kuehlstellen_alle"]:
            ks_name = ks.get("name", "?")
            ks_pos = ks.get("pos_nr", "")
            ks_label = f"Pos. {ks_pos} – {ks_name}" if ks_pos else ks_name
            laenge = ks.get("leitungslaenge_m", 20)
            laenge_at = ks.get("laenge_aussenteil_m", 15)
            laenge_router = ks.get("laenge_router_m", 20)
            laenge_sk = ks.get("laenge_schaltschrank_m", 10)
            lieferumfang = ks.get("lieferumfang", "direkt")

            # Regler-Info
            komp = ks.get("komponenten", {})
            sk_data = komp.get("schaltkasten", {})
            sk_params = sk_data.get("parameter", {})
            steuerung_typ = sk_params.get("steuerung_typ", "Eigener Regler (coolsulting liefert)")
            regler = sk_params.get("regler_typ", "–")
            montageort = sk_params.get("montageort", "An der Kuehlzelle (Front)")
            bus_proto = sk_params.get("bus_protokoll", "RS485 Modbus RTU (Standard)")

            fremd = "Fremdsteuerung" in steuerung_typ
            bus_kompatibel = "Bus-kompatibel" in steuerung_typ
            bus_nicht_komp = "Bus NICHT kompatibel" in steuerung_typ

            regler_an_zelle = "Kuehlzelle" in montageort or "Geraet" in montageort
            regler_bis = "Regler an Zelle" if regler_an_zelle else "Zentralschaltschrank"
            kabel_laenge_regler = 2 if regler_an_zelle else laenge

            # ── KABEL PRO KOMPONENTE ──

            # 1. Verdampferlüfter
            vd = komp.get("verdampfer_luefter", {})
            if vd.get("aktiv"):
                vd_p = vd.get("parameter", {})
                spannung = vd_p.get("spannung", "230V 1-phasig")
                anz_vd = int(vd_p.get("anzahl_verdampfer", 1))
                anz_lue = int(vd_p.get("anzahl_luefter", 1))
                kuerzel = "EM-VD-3P" if "400V" in spannung else "EM-VD-L"
                kt = get_kabel_info(kuerzel)
                if not fremd or not bus_kompatibel:
                    for vd_i in range(anz_vd):
                        vd_suffix = f" VD{vd_i+1}" if anz_vd > 1 else ""
                        kabelliste.append(_zeile(
                            lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                            f"Verdampferlüfter{vd_suffix} ({anz_lue}x {spannung})",
                            kt.get("typ","YMM-J"), _qs(kt,0), _adern(kt),
                            ks_name, regler_bis,
                            kabel_laenge_regler, kt.get("norm",""), "Starkstrom"
                        ))
                        lfd_nr += 1

            # 2. Abtauheizung
            abt = komp.get("abtauheizung", {})
            if abt.get("aktiv"):
                abt_p = abt.get("parameter", {})
                abt_typ = abt_p.get("typ_abtau", "Elektro-Abtau")
                if "Elektro" in abt_typ and (not fremd or not bus_kompatibel):
                    kt = get_kabel_info("EM-VD-ABT")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        f"Abtauheizung {abt_p.get('leistung_w',800)}W 230V",
                        kt.get("typ","SIHF"), _qs(kt,0), _adern(kt),
                        ks_name, regler_bis, kabel_laenge_regler,
                        kt.get("norm",""), "Starkstrom"
                    ))
                    lfd_nr += 1
                elif "Heißgas" in abt_typ:
                    kt = get_kabel_info("VA-ABT")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        "Heißgas-Abtau Steuerleitung",
                        kt.get("typ","LIYY"), _qs(kt,0), _adern(kt),
                        ks_name, regler_bis, kabel_laenge_regler,
                        kt.get("norm",""), "Steuerung"
                    ))
                    lfd_nr += 1

            # 3. Ablaufheizung
            abl = komp.get("ablaufheizung", {})
            if abl.get("aktiv") and (not fremd or not bus_kompatibel):
                abl_p = abl.get("parameter", {})
                kt = get_kabel_info("EM-VD-HZ")
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                    f"Ablaufheizung {abl_p.get('leistung_w',25)}W 230V",
                    kt.get("typ","SIHF"), _qs(kt,0), _adern(kt),
                    ks_name, regler_bis, kabel_laenge_regler,
                    kt.get("norm",""), "Starkstrom"
                ))
                lfd_nr += 1

            # 4. Temperaturfühler Innenraum
            tf = komp.get("temperaturfuehler_innen", {})
            if tf.get("aktiv"):
                tf_p = tf.get("parameter", {})
                tf_typ = tf_p.get("typ_fuehler", "NTC")
                kuerzel = "MSR-TF-PT100" if "PT" in tf_typ else "EM-VD-TF"
                kt = get_kabel_info(kuerzel)
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                    f"Temperaturfühler Innenraum {tf_typ}",
                    kt.get("typ","LIYCY"), _qs(kt,0), _adern(kt),
                    ks_name, regler_bis, kabel_laenge_regler,
                    kt.get("norm",""), "Fühler"
                ))
                lfd_nr += 1

            # 5. Abtaufühler
            tfa = komp.get("temperaturfuehler_abtau", {})
            if tfa.get("aktiv"):
                kt = get_kabel_info("EM-VD-TF")
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                    "Abtaufühler NTC (am Verdampfer)",
                    kt.get("typ","LIYCY"), _qs(kt,0), _adern(kt),
                    ks_name, regler_bis, kabel_laenge_regler,
                    kt.get("norm",""), "Fühler"
                ))
                lfd_nr += 1

            # 6. EEV – je nach Typ unterschiedliche Kabel
            eev = komp.get("eev", {})
            if eev.get("aktiv") and (not fremd or not bus_kompatibel):
                eev_p = eev.get("parameter", {})
                eev_typ = eev_p.get("eev_typ", "Schrittmotor EEV + externer Treiber (Standard)")
                hersteller = eev_p.get("hersteller", "")
                treiber_standort = eev_p.get("treiber_standort", "Direkt am Verdampfer / Ventil (max. 5m Motorkabel)")
                laenge_motor = float(eev_p.get("laenge_motorkabel_m", 3))

                if "EVD ice" in eev_typ or "EVD Evolution" in eev_typ:
                    # Carel EVD ice: wie Magnetventil + Bus
                    kt = get_kabel_info("EEV-EVD-ICE")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        f"Carel EVD ice 230V Versorgung (am Verdampfer vormontiert)",
                        kt.get("typ","YMM-J"), "1,5", "3",
                        "Verteiler", ks_name, kabel_laenge_regler,
                        kt.get("norm",""), "Regelung"
                    ))
                    lfd_nr += 1
                    kt2 = get_kabel_info("EEV-EVD-BUS")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        "Carel EVD ice RS485/pLAN Bus → Regler",
                        kt2.get("typ","J-Y(ST)Y"), "0,8", "4",
                        f"EVD ice {ks_name}", regler_bis, kabel_laenge_regler,
                        kt2.get("norm",""), "Bus / Daten"
                    ))
                    lfd_nr += 1

                elif "PWM" in eev_typ or "AKV" in eev_typ:
                    # Danfoss AKV PWM
                    kt = get_kabel_info("EEV-PWM-AKV")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        "Danfoss AKV PWM-Ventil Steuerleitung",
                        kt.get("typ","LIYY"), "0,5", "2",
                        regler_bis, ks_name, kabel_laenge_regler,
                        kt.get("norm",""), "Regelung"
                    ))
                    lfd_nr += 1

                else:
                    # Schrittmotor EEV + externer Treiber (Standard)
                    # Motorkabel: Ventil → Treiber (MAX 8m!)
                    kt_mot = get_kabel_info("EEV-MOT")
                    treiber_bis = f"EEV-Treiber {ks_name}"
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        f"⚠️ EEV Motorkabel {hersteller} (MAX {laenge_motor}m!)",
                        kt_mot.get("typ","LIYY"), "0,5", "6",
                        ks_name, treiber_bis, laenge_motor,
                        "VDE 0812 – MAX 8m!", "Regelung"
                    ))
                    lfd_nr += 1
                    # Treiber Versorgung 230V
                    kt_ver = get_kabel_info("EEV-TREIBER-VER")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        "EEV-Treiber Versorgung 230V",
                        kt_ver.get("typ","YMM-J"), "1,5", "3",
                        regler_bis, treiber_bis, kabel_laenge_regler,
                        kt_ver.get("norm",""), "Starkstrom"
                    ))
                    lfd_nr += 1
                    # Treiber Steuerleitung zum Regler
                    kt_st = get_kabel_info("EEV-TREIBER-STEUER")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        "EEV-Treiber Steuerleitung → Regler",
                        kt_st.get("typ","LIYCY"), "0,5", "4",
                        treiber_bis, regler_bis, kabel_laenge_regler,
                        kt_st.get("norm",""), "Bus / Daten"
                    ))
                    lfd_nr += 1

                # Saugfühler immer bei EEV
                kt_tf = get_kabel_info("EEV-TF-SAUG")
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                    "EEV Temperaturfühler Saugleitung NTC/PT100",
                    kt_tf.get("typ","LIYCY"), _qs(kt_tf,0), _adern(kt_tf),
                    ks_name, regler_bis, kabel_laenge_regler,
                    kt_tf.get("norm",""), "Fühler"
                ))
                lfd_nr += 1

            # 7. Magnetventil
            mv = komp.get("magnetventil", {})
            if mv.get("aktiv") and (not fremd or not bus_kompatibel):
                mv_p = mv.get("parameter", {})
                kt = get_kabel_info("EM-VD-L")
                anz_mv = int(mv_p.get("anzahl", 1))
                for mv_i in range(anz_mv):
                    mv_suffix = f" {mv_i+1}" if anz_mv > 1 else ""
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        f"Magnetventil{mv_suffix} {mv_p.get('spannung','230V AC')}",
                        kt.get("typ","YMM-J"), "1,0–1,5", "3",
                        ks_name, regler_bis, kabel_laenge_regler,
                        kt.get("norm","ÖVE/ÖNORM"), "Starkstrom"
                    ))
                    lfd_nr += 1

            # 8. Türkontakt
            tk = komp.get("tuer_kontakt", {})
            if tk.get("aktiv"):
                tk_p = tk.get("parameter", {})
                anz_t = int(tk_p.get("anzahl_tueren", 1))
                kt = get_kabel_info("GA-KZ-TUE")
                for t_i in range(anz_t):
                    t_suffix = f" Tür {t_i+1}" if anz_t > 1 else ""
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        f"Türkontakt{t_suffix} {tk_p.get('typ','NC')}",
                        kt.get("typ","LIYY"), _qs(kt,0), _adern(kt),
                        f"{ks_name} Tür{t_suffix}", regler_bis, kabel_laenge_regler,
                        kt.get("norm",""), "Steuerung"
                    ))
                    lfd_nr += 1

            # 9. Innenbeleuchtung
            ib = komp.get("innenbeleuchtung", {})
            if ib.get("aktiv") and (not fremd or not bus_kompatibel):
                ib_p = ib.get("parameter", {})
                kt = get_kabel_info("GA-THE-LED")
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                    f"Innenbeleuchtung {ib_p.get('licht_typ','LED')} {ib_p.get('leistung_w',30)}W",
                    kt.get("typ","YMM-J"), _qs(kt,0), _adern(kt),
                    ks_name, regler_bis, kabel_laenge_regler,
                    kt.get("norm",""), "Starkstrom"
                ))
                lfd_nr += 1

            # 10. Bewegungsmelder
            bm = komp.get("bewegungsmelder", {})
            if bm.get("aktiv"):
                kt = get_kabel_info("GA-KZ-TUE")
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                    f"Bewegungsmelder {bm.get('parameter',{}).get('typ_melder','PIR')}",
                    kt.get("typ","LIYY"), _qs(kt,0), _adern(kt),
                    ks_name, regler_bis, kabel_laenge_regler,
                    kt.get("norm",""), "Steuerung"
                ))
                lfd_nr += 1

            # 11. Personennotruf
            pn = komp.get("personennotruf", {})
            if pn.get("aktiv"):
                pn_p = pn.get("parameter", {})
                if pn_p.get("taster_innen", True):
                    kt = get_kabel_info("PA-NT-TAST")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        "Personennotruf Taster innen 24V",
                        kt.get("typ","LIYCY"), _qs(kt,0), _adern(kt),
                        f"{ks_name} innen", "Notrufzentrale / SK",
                        kabel_laenge_regler, kt.get("norm","EN 13133"), "Sicherheit"
                    ))
                    lfd_nr += 1
                if pn_p.get("horn_aussen", True):
                    kt = get_kabel_info("PA-NT-HORN")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        "Personennotruf Horn außen 24V",
                        kt.get("typ","YMM-J"), _qs(kt,0), _adern(kt),
                        f"{ks_name} außen", "Notrufzentrale / SK",
                        kabel_laenge_regler + 2, kt.get("norm","EN 13133"), "Sicherheit"
                    ))
                    lfd_nr += 1
                if pn_p.get("blitz_aussen", True):
                    kt = get_kabel_info("PA-NT-LED")
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        "Personennotruf Blitzleuchte außen",
                        kt.get("typ","YMM-J"), _qs(kt,0), _adern(kt),
                        f"{ks_name} außen", "Notrufzentrale / SK",
                        kabel_laenge_regler + 2, kt.get("norm","EN 13133"), "Sicherheit"
                    ))
                    lfd_nr += 1

            # 12. Gaswarnanlage
            gwa = komp.get("gaswarnanlage", {})
            if gwa.get("aktiv"):
                gwa_p = gwa.get("parameter", {})
                kt = get_kabel_info("MSR-GWA-SEN")
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                    f"GWA Sensor {gwa_p.get('kaeltemittel','?')} 4-20mA",
                    kt.get("typ","LIYCY"), _qs(kt,0), _adern(kt),
                    ks_name, "Zentralschaltschrank",
                    laenge_sk or laenge, kt.get("norm","EN 378-3"), "Sicherheit"
                ))
                lfd_nr += 1

            # 13. Regler-Versorgung (nur eigener Regler)
            if not fremd:
                kt = get_kabel_info("EM-VD-SK")
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                    f"Regler {regler[:25] if regler else '–'} 230V Versorgung",
                    kt.get("typ","YMM-J"), "1,5", "3",
                    "Verteiler / SK", regler_bis,
                    kabel_laenge_regler, "ÖVE/ÖNORM E 8001", "Starkstrom"
                ))
                lfd_nr += 1

            # 14. Bus RS485 (wenn Bus-kompatibel oder eigener Regler)
            if not bus_nicht_komp:
                kt = get_kabel_info("ICK-RS485")
                bus_label = "RS485 Modbus Bus" if not fremd else "RS485 Bus (Fremdregler)"
                # Ziel: Monitoring-System
                bus_ziel = "Kiconex Gateway"
                if steuerung == "Wurm_Frigodata":
                    bus_ziel = "Frigodata Gateway"
                elif steuerung == "Carel_Boss":
                    bus_ziel = "Carel boss"
                elif steuerung == "Dixell_Xweb":
                    bus_ziel = "Xweb / Dixell"
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                    f"{bus_label} ({bus_proto.split()[0] if bus_proto else 'RS485'})",
                    kt.get("typ","LIYCY"), _qs(kt,0), _adern(kt),
                    regler_bis, bus_ziel,
                    laenge_router or laenge, kt.get("norm","EIA-485"), "Bus / Daten"
                ))
                lfd_nr += 1

            # 15. HACCP-Fühler (separat zu HACCP-Modul)
            haccp = komp.get("haccp_aufzeichnung", {})
            if haccp.get("aktiv"):
                haccp_p = haccp.get("parameter", {})
                anz_f = int(haccp_p.get("anzahl_fuehler", 1))
                tf_typ = haccp_p.get("fuehler_typ", "NTC (Standard)")
                aufz = haccp_p.get("aufzeichnung_system", "Regler-intern")
                kt = get_kabel_info("EM-VD-TF")

                # Ziel des HACCP-Fühlers
                if "intern" in aufz.lower():
                    haccp_ziel = regler_bis
                    haccp_laenge = kabel_laenge_regler
                elif "Xweb" in aufz:
                    haccp_ziel = "Xweb / Dixell"
                    haccp_laenge = laenge_router or laenge
                elif "Kiconex" in aufz:
                    haccp_ziel = "Kiconex Gateway"
                    haccp_laenge = laenge_router or laenge
                elif "Modul" in aufz:
                    haccp_ziel = "HACCP-Modul"
                    # HACCP-Modul suchen
                    for hm in haccp_module:
                        if hm.get("kreis") == kreis_nr or not hm.get("kreis"):
                            haccp_ziel = f"HACCP-Modul {hm.get('bezeichnung','')}"
                            haccp_laenge = hm.get("laenge_zur_ks", laenge)
                            break
                    else:
                        haccp_laenge = laenge
                else:
                    haccp_ziel = "HACCP-Modul / Regler"
                    haccp_laenge = laenge

                for f_i in range(anz_f):
                    f_suffix = f" F{f_i+1}" if anz_f > 1 else ""
                    kabelliste.append(_zeile(
                        lfd_nr, kreis_nr, kreis_label, ks_label, lieferumfang,
                        f"HACCP-Fühler{f_suffix} {tf_typ}",
                        kt.get("typ","LIYCY"), _qs(kt,0), _adern(kt),
                        ks_name, haccp_ziel, haccp_laenge,
                        kt.get("norm","DIN 44081"), "HACCP"
                    ))
                    lfd_nr += 1

        # HACCP-Modul Bus zum Monitoring (pro Kreis einmal)
        for hm in haccp_module:
            if hm.get("kreis") == kreis_nr or (not hm.get("kreis") and kreis_nr == 1):
                kt = get_kabel_info("ICK-RS485")
                hm_label = f"HACCP-Modul {hm.get('bezeichnung','')}"
                kabelliste.append(_zeile(
                    lfd_nr, kreis_nr, kreis_label, hm_label, "direkt",
                    "HACCP-Modul Bus zum Monitoring-System",
                    kt.get("typ","LIYCY"), _qs(kt,0), _adern(kt),
                    hm_label, hm.get("monitoring_ziel","Xweb / Dixell"),
                    hm.get("laenge_zum_monitoring", 20),
                    kt.get("norm","EIA-485"), "Bus / Daten"
                ))
                lfd_nr += 1

    return kabelliste


def _zeile(nr, kreis_nr, kreis_label, ks_label, lieferumfang,
           bezeichnung, kabeltyp, querschnitt, adern,
           von, bis, laenge_m, norm, kategorie) -> dict:
    """Erstellt eine Kabelzeile."""
    return {
        "_id": f"K{nr:04d}",
        "Kreis Nr.": kreis_nr,
        "Kreis": kreis_label,
        "Kühlstelle / Ort": ks_label,
        "Lieferumfang": "Direkt" if lieferumfang == "direkt" else "Extern",
        "Bezeichnung / Verbraucher": bezeichnung,
        "Kategorie": kategorie,
        "Kabeltyp": kabeltyp,
        "Querschnitt [mm²]": querschnitt,
        "Adern": adern,
        "Von": von,
        "Bis": bis,
        "Länge [m]": float(laenge_m) if laenge_m else 0.0,
        "Norm": norm,
        "Bemerkung": "",
    }


def _qs(kt: dict, idx: int = 0) -> str:
    qs = kt.get("querschnitt_mm2", [1.5])
    return str(qs[idx]) if qs else "1,5"


def _adern(kt: dict) -> str:
    return str(kt.get("aderzahl", 3))


def kabelliste_zusammenfassung(kabelliste: list) -> list:
    """
    Summiert Kabellängen nach Kabeltyp + Querschnitt.
    Gibt sortierte Liste mit Gesamtmetern zurück.
    """
    summen = {}
    for zeile in kabelliste:
        key = f"{zeile['Kabeltyp']} {zeile['Querschnitt [mm²]']}mm² {zeile['Adern']}-adrig"
        if key not in summen:
            summen[key] = {
                "Kabeltyp": zeile["Kabeltyp"],
                "Querschnitt [mm²]": zeile["Querschnitt [mm²]"],
                "Adern": zeile["Adern"],
                "Kategorie": zeile["Kategorie"],
                "Anzahl Leitungen": 0,
                "Gesamt [m]": 0.0,
                "Direkt [m]": 0.0,
                "Extern [m]": 0.0,
            }
        summen[key]["Anzahl Leitungen"] += 1
        l = float(zeile.get("Länge [m]", 0) or 0)
        summen[key]["Gesamt [m]"] += l
        if zeile.get("Lieferumfang") == "Direkt":
            summen[key]["Direkt [m]"] += l
        else:
            summen[key]["Extern [m]"] += l

    result = list(summen.values())
    for r in result:
        r["Gesamt [m]"] = round(r["Gesamt [m]"], 1)
        r["Direkt [m]"] = round(r["Direkt [m]"], 1)
        r["Extern [m]"] = round(r["Extern [m]"], 1)

    return sorted(result, key=lambda x: x["Gesamt [m]"], reverse=True)
