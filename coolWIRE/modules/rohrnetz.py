# ==============================================================================
# modules/rohrnetz.py  –  Kältemittel-Rohrdimensionierung für °coolWIRE
# Basiert auf coolROHR v2.0 | °coolsulting e.U. | Michael Schäpers
# ==============================================================================

import math
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# CU-ROHR TABELLE
# ─────────────────────────────────────────────────────────────────────────────
CU_PIPES = [
    {"od": 10.0,  "wall": 1.0, "id": 8.0,   "label": "10 × 1,0"},
    {"od": 12.0,  "wall": 1.0, "id": 10.0,  "label": "12 × 1,0"},
    {"od": 15.0,  "wall": 1.0, "id": 13.0,  "label": "15 × 1,0"},
    {"od": 18.0,  "wall": 1.0, "id": 16.0,  "label": "18 × 1,0"},
    {"od": 22.0,  "wall": 1.0, "id": 20.0,  "label": "22 × 1,0"},
    {"od": 28.0,  "wall": 1.5, "id": 25.0,  "label": "28 × 1,5"},
    {"od": 35.0,  "wall": 1.5, "id": 32.0,  "label": "35 × 1,5"},
    {"od": 42.0,  "wall": 1.5, "id": 39.0,  "label": "42 × 1,5"},
    {"od": 54.0,  "wall": 2.0, "id": 50.0,  "label": "54 × 2,0"},
    {"od": 64.0,  "wall": 2.0, "id": 60.0,  "label": "64 × 2,0"},
    {"od": 76.1,  "wall": 2.0, "id": 72.1,  "label": "76,1 × 2,0"},
    {"od": 88.9,  "wall": 2.5, "id": 83.9,  "label": "88,9 × 2,5"},
    {"od": 108.0, "wall": 2.5, "id": 103.0, "label": "108 × 2,5"},
]

# ─────────────────────────────────────────────────────────────────────────────
# KÄLTEMITTEL-DATENTABELLEN
# ─────────────────────────────────────────────────────────────────────────────
REFRIGERANTS = {
    "R32": {
        "name": "R32", "color": "#2196F3",
        "warning": "A2L-Kältemittel – Zündschutz nach EN 378 / EN 60335-2-40 erforderlich.",
        "a2l": True, "co2": False,
        "temps":  [-50,  -40,  -35,  -30,  -25,  -20,  -15,  -10,  0,    10,   20,   30,   40,   50],
        "p_bar":  [1.45, 2.18, 2.66, 3.22, 3.87, 4.62, 5.48, 6.47, 8.85, 11.84,15.53,20.05,25.49,31.99],
        "rho_v":  [8.5,  12.8, 15.8, 19.4, 23.7, 28.7, 34.6, 41.4, 58.8, 82.2, 113.0,153.0,205.0,273.0],
        "rho_l":  [1157, 1117, 1096, 1074, 1052, 1028, 1004, 978,  923,  862,  793,  714,  620,  503],
        "h_fg":   [390,  375,  367,  358,  348,  337,  325,  311,  281,  246,  205,  157,  99,   24],
        "mu_v":   [9.2,  9.6,  9.9,  10.2, 10.5, 10.9, 11.3, 11.8, 12.8, 14.0, 15.5, 17.5, 20.3, 24.8],
    },
    "R134a": {
        "name": "R134a", "color": "#607D8B",
        "warning": "HFC-Kältemittel – GWP 1430, Phase-Out beachten (F-Gas-VO).",
        "a2l": False, "co2": False,
        "temps":  [-50,  -40,  -35,  -30,  -25,  -20,  -15,  -10,  0,    10,   20,   30,   40,   50],
        "p_bar":  [0.29, 0.51, 0.66, 0.84, 1.06, 1.33, 1.65, 2.01, 2.93, 4.15, 5.72, 7.70, 10.17,13.18],
        "rho_v":  [1.7,  3.0,  3.8,  4.8,  6.1,  7.6,  9.5,  11.7, 17.1, 24.6, 34.7, 48.2, 66.2, 90.2],
        "rho_l":  [1418, 1378, 1357, 1336, 1314, 1291, 1267, 1243, 1191, 1135, 1074, 1007, 931,  845],
        "h_fg":   [218,  213,  210,  207,  203,  199,  195,  191,  182,  171,  159,  145,  128,  107],
        "mu_v":   [8.5,  8.9,  9.1,  9.4,  9.7,  10.0, 10.4, 10.8, 11.6, 12.6, 13.8, 15.2, 16.9, 19.1],
    },
    "R513A": {
        "name": "R513A", "color": "#00BCD4",
        "warning": "HFO-Blend (R1234yf/R134a) – Sicherheitsklasse A1.",
        "a2l": False, "co2": False,
        "temps":  [-50,  -40,  -35,  -30,  -25,  -20,  -15,  -10,  0,    10,   20,   30,   40,   50],
        "p_bar":  [0.64, 0.99, 1.24, 1.54, 1.89, 2.32, 2.82, 3.41, 4.88, 6.80, 9.26, 12.34,16.15,20.80],
        "rho_v":  [3.5,  5.5,  6.9,  8.6,  10.7, 13.2, 16.3, 19.9, 28.8, 41.0, 57.5, 79.5, 109.0,149.0],
        "rho_l":  [1288, 1254, 1237, 1219, 1201, 1182, 1162, 1141, 1097, 1049, 995,  933,  860,  770],
        "h_fg":   [208,  203,  200,  197,  193,  189,  185,  181,  172,  161,  148,  131,  110,  83],
        "mu_v":   [9.0,  9.4,  9.7,  10.0, 10.3, 10.7, 11.1, 11.5, 12.4, 13.4, 14.7, 16.3, 18.5, 21.5],
    },
    "R449A": {
        "name": "R449A", "color": "#E91E63",
        "warning": "HFO-Blend (R32/R125/R1234yf/R134a) – Sicherheitsklasse A1.",
        "a2l": False, "co2": False,
        "temps":  [-50,  -40,  -35,  -30,  -25,  -20,  -15,  -10,  0,    10,   20,   30,   40,   50],
        "p_bar":  [1.10, 1.68, 2.07, 2.52, 3.05, 3.66, 4.37, 5.20, 7.20, 9.70, 12.85,16.75,21.50,27.20],
        "rho_v":  [6.5,  9.9,  12.3, 15.3, 18.9, 23.2, 28.2, 34.2, 48.5, 67.5, 92.5, 125.0,168.0,224.0],
        "rho_l":  [1315, 1280, 1262, 1243, 1224, 1203, 1182, 1160, 1113, 1060, 1000, 932,  852,  756],
        "h_fg":   [260,  255,  252,  248,  243,  238,  232,  225,  211,  194,  175,  152,  124,  90],
        "mu_v":   [9.8,  10.2, 10.6, 11.0, 11.4, 11.8, 12.3, 12.8, 13.9, 15.2, 16.8, 18.8, 21.5, 25.0],
    },
    "R744": {
        "name": "R744 (CO₂)", "color": "#FF6B35",
        "warning": "CO₂-Hochdruckanlage! K65-Armaturen erforderlich.",
        "a2l": False, "co2": True,
        "temps":  [-50,   -40,   -35,   -30,   -25,   -20,   -15,   -10,   0,     10,    20,    30],
        "p_bar":  [6.83,  10.05, 12.05, 14.34, 16.96, 19.94, 23.31, 27.12, 34.85, 45.01, 57.34, 72.13],
        "rho_v":  [14.5,  21.3,  25.9,  31.2,  37.5,  44.9,  53.7,  64.1,  92.0,  134.0, 202.0, 316.0],
        "rho_l":  [1153,  1119,  1101,  1082,  1062,  1039,  1015,  989,   929,   858,   771,   655],
        "h_fg":   [322,   312,   306,   299,   292,   283,   273,   261,   231,   193,   143,   72],
        "mu_v":   [11.0,  11.5,  11.8,  12.1,  12.4,  12.8,  13.2,  13.6,  14.7,  16.1,  18.0,  21.5],
    },
    "R455A": {
        "name": "R455A", "color": "#9C27B0",
        "warning": "A2L-Kältemittel – Zündschutz beachten.",
        "a2l": True, "co2": False,
        "temps":  [-50,  -40,  -35,  -30,  -25,  -20,  -15,  -10,  0,    10,   20,   30,   40,   50],
        "p_bar":  [0.75, 1.15, 1.45, 1.80, 2.20, 2.70, 3.25, 3.90, 5.45, 7.50, 10.10,13.35,17.30,22.10],
        "rho_v":  [4.5,  6.9,  8.7,  10.8, 13.4, 16.5, 20.2, 24.5, 34.8, 48.8, 67.5, 92.0, 124.0,166.0],
        "rho_l":  [1220, 1185, 1167, 1148, 1129, 1109, 1088, 1067, 1022, 972,  915,  850,  773,  680],
        "h_fg":   [300,  295,  290,  285,  280,  274,  268,  261,  247,  230,  210,  186,  158,  122],
        "mu_v":   [9.0,  9.4,  9.7,  10.0, 10.3, 10.7, 11.1, 11.5, 12.4, 13.4, 14.6, 16.2, 18.2, 21.0],
    },
    "R452A": {
        "name": "R452A", "color": "#FF9800",
        "warning": "A2L-Kältemittel – Zündschutz beachten.",
        "a2l": True, "co2": False,
        "temps":  [-50,  -40,  -35,  -30,  -25,  -20,  -15,  -10,  0,    10,   20,   30,   40,   50],
        "p_bar":  [1.05, 1.60, 1.97, 2.40, 2.90, 3.50, 4.20, 5.00, 6.90, 9.30, 12.30,16.00,20.50,25.90],
        "rho_v":  [6.2,  9.4,  11.7, 14.5, 17.8, 21.8, 26.5, 32.0, 45.0, 62.5, 85.5, 115.0,154.0,205.0],
        "rho_l":  [1330, 1295, 1277, 1258, 1238, 1218, 1197, 1175, 1129, 1079, 1023, 958,  882,  790],
        "h_fg":   [238,  233,  230,  226,  222,  218,  213,  208,  197,  184,  168,  149,  125,  96],
        "mu_v":   [9.5,  9.9,  10.2, 10.6, 11.0, 11.4, 11.8, 12.3, 13.3, 14.5, 15.9, 17.8, 20.2, 23.5],
    },
    "R1234yf": {
        "name": "R1234yf", "color": "#4CAF50",
        "warning": "A2L-Kältemittel – Zündschutz nach EN 378 erforderlich.",
        "a2l": True, "co2": False,
        "temps":  [-50,  -40,  -35,  -30,  -25,  -20,  -15,  -10,  0,    10,   20,   30,   40,   50],
        "p_bar":  [0.51, 0.80, 1.00, 1.25, 1.55, 1.91, 2.34, 2.84, 4.07, 5.72, 7.86, 10.57,13.97,18.17],
        "rho_v":  [2.8,  4.4,  5.5,  6.9,  8.6,  10.6, 13.1, 16.1, 23.1, 33.2, 46.9, 65.7, 91.7, 128.0],
        "rho_l":  [1237, 1200, 1181, 1162, 1143, 1123, 1102, 1081, 1036, 988,  934,  874,  803,  716],
        "h_fg":   [211,  206,  203,  200,  197,  194,  190,  186,  178,  168,  155,  139,  119,  93],
        "mu_v":   [8.5,  9.0,  9.2,  9.5,  9.8,  10.1, 10.4, 10.8, 11.5, 12.3, 13.3, 14.6, 16.2, 18.5],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# PHYSIKFUNKTIONEN
# ─────────────────────────────────────────────────────────────────────────────
def interp_prop(ref_key, T_C, prop):
    d = REFRIGERANTS[ref_key]
    return float(np.interp(T_C, d["temps"], d[prop]))

def get_sat_props(ref_key, T_C):
    return {
        "p_bar":  interp_prop(ref_key, T_C, "p_bar"),
        "rho_v":  interp_prop(ref_key, T_C, "rho_v"),
        "rho_l":  interp_prop(ref_key, T_C, "rho_l"),
        "h_fg":   interp_prop(ref_key, T_C, "h_fg"),
        "mu_v":   interp_prop(ref_key, T_C, "mu_v") * 1e-6,
    }

def darcy_f(Re):
    if Re < 1:    return 1.0
    if Re < 2300: return 64.0 / Re
    return 0.316 / (Re ** 0.25)  # Blasius (glatte Cu-Rohre)

def calc_pipe(pipe, m_dot_kg_s, rho_kg_m3, mu_Pa_s, L_eq_m, T_sat_C, h_fg_kJ, rho_v_kg_m3):
    d_m = pipe["id"] / 1000.0
    A   = math.pi * (d_m / 2.0) ** 2
    v   = m_dot_kg_s / (rho_kg_m3 * A) if A > 0 else 999.0
    Re  = rho_kg_m3 * abs(v) * d_m / mu_Pa_s if mu_Pa_s > 0 else 1e6
    f   = darcy_f(Re)
    dp_Pa  = f * (L_eq_m / d_m) * rho_kg_m3 * v**2 / 2.0
    dp_bar = dp_Pa / 1e5
    T_sat_K = T_sat_C + 273.15
    dp_dT   = (h_fg_kJ * 1000.0 * rho_v_kg_m3) / T_sat_K
    dp_K    = dp_Pa / dp_dT if dp_dT > 0 else 0.0
    return {"v": v, "Re": Re, "dp_Pa": dp_Pa, "dp_bar": dp_bar, "dp_K": dp_K}

def select_pipe(m_dot_kg_s, rho_kg_m3, mu_Pa_s, L_eq_m,
                v_min, v_max, dp_K_max, T_sat_C, h_fg_kJ, rho_v_kg_m3):
    best = {"prio": 99, "idx": len(CU_PIPES)-1,
            "warns": ["⚠️ Kein ideales Rohr gefunden – größtes Rohr gewählt"]}
    for i, pipe in enumerate(CU_PIPES):
        r = calc_pipe(pipe, m_dot_kg_s, rho_kg_m3, mu_Pa_s, L_eq_m, T_sat_C, h_fg_kJ, rho_v_kg_m3)
        v_ok  = v_min <= r["v"] <= v_max
        dp_ok = r["dp_K"] <= dp_K_max
        if v_ok and dp_ok:
            return i, []
        elif r["v"] <= v_max and dp_ok and best["prio"] > 2:
            best = {"prio": 2, "idx": i,
                    "warns": [f"⚠️ v = {r['v']:.1f} m/s < v_min {v_min:.1f} m/s – Ölrückführung prüfen!"]}
        elif v_ok and not dp_ok and best["prio"] > 3:
            best = {"prio": 3, "idx": i,
                    "warns": [f"⚠️ Δp = {r['dp_K']:.2f} K > Grenzwert {dp_K_max:.1f} K"]}
        elif r["v"] <= v_max and best["prio"] > 4:
            best = {"prio": 4, "idx": i,
                    "warns": [f"⚠️ v = {r['v']:.1f} m/s < v_min, Δp = {r['dp_K']:.2f} K – Kompromiss"]}
    return best["idx"], best["warns"]

def dp_limit_K(line_type, L_total_m, app_type):
    if app_type == "NK":
        if line_type == "SL":
            return 1.5 if L_total_m <= 25 else (1.2 if L_total_m <= 50 else 1.0)
        elif line_type == "DL": return 2.0
        elif line_type == "FL": return 0.5
        else:                   return 1.5
    else:  # TK
        if line_type == "SL":
            return 1.0 if L_total_m <= 25 else (0.8 if L_total_m <= 50 else 0.6)
        elif line_type == "DL": return 1.5
        elif line_type == "FL": return 0.4
        else:                   return 1.0

def equiv_length(L_m, n_elbows, n_ball_valves, n_solenoid, d_od_mm):
    L_eq  = L_m
    L_eq += n_elbows      * 1.2 * (d_od_mm/1000) * 30
    L_eq += n_ball_valves * 1.2 * (d_od_mm/1000) * 6
    L_eq += n_solenoid    * 1.2 * (d_od_mm/1000) * 75
    return L_eq

def hydrostatic_dp(rho, h_m):
    return rho * 9.81 * h_m

def insulation_thickness_mm(T_pipe_C, T_amb_C, phi_pct, d_od_mm):
    a, b = 17.625, 243.04
    phi = phi_pct / 100.0
    if phi <= 0: return 0
    gamma = (a * T_amb_C / (b + T_amb_C)) + math.log(phi)
    T_dew = b * gamma / (a - gamma)
    if T_pipe_C >= T_dew: return 0
    dT = T_dew - T_pipe_C
    raw = max(dT * 2.5, 9.0)
    for std in [9, 13, 19, 25, 32, 40]:
        if std >= raw: return std
    return 40

def berechne_leitung(ref_key, t0_C, tc_C, Q_kW, L_h_m, L_v_m,
                     n_elbows=4, n_ball_valves=1, n_solenoid=1,
                     h_SL_m=0.0, h_FL_m=0.0,
                     T_amb_C=25.0, phi_pct=70.0,
                     app_code="NK"):
    """
    Hauptfunktion: berechnet alle 4 Leitungen für einen Kreis.
    Gibt dict mit Ergebnissen zurück.
    """
    props0 = get_sat_props(ref_key, t0_C)
    propsc = get_sat_props(ref_key, tc_C)

    rho_v0 = props0["rho_v"]
    rho_vc = propsc["rho_v"]
    rho_l  = propsc["rho_l"]
    h_fg0  = props0["h_fg"]
    mu_v0  = props0["mu_v"]
    mu_vc  = propsc["mu_v"]

    m_dot = Q_kW / h_fg0  # kg/s

    L_SL_total = L_h_m + abs(L_v_m)
    L_FL = L_SL_total
    L_DL = max(L_v_m, 2.0)

    L_SL_eq = equiv_length(L_SL_total, n_elbows, n_ball_valves, n_solenoid, 42)
    L_DL_eq = equiv_length(L_DL, n_elbows, n_ball_valves, 0, 42)
    L_FL_eq = equiv_length(L_FL, n_elbows, n_ball_valves, n_solenoid, 28)

    # v-Grenzen
    if app_code == "NK":
        vmin_sl = 7.6 if L_v_m > 0.5 else 3.8
        vmax_sl = 18.0
        vmin_dl = 8.0 if L_DL > 1 else 5.0
        vmax_dl = 15.0
    else:
        vmin_sl = 9.0 if L_v_m > 0.5 else 4.5
        vmax_sl = 18.0
        vmin_dl = 10.0 if L_DL > 1 else 5.0
        vmax_dl = 15.0

    dp_max_SL = dp_limit_K("SL", L_SL_total, app_code)
    dp_max_DL = dp_limit_K("DL", L_DL, app_code)
    dp_max_FL = dp_limit_K("FL", L_FL, app_code)

    dp_hydro_SL = hydrostatic_dp(rho_v0, h_SL_m)
    dp_hydro_FL = hydrostatic_dp(rho_l, h_FL_m)

    auto_SL, warns_SL = select_pipe(m_dot, rho_v0, mu_v0, L_SL_eq, vmin_sl, vmax_sl, dp_max_SL, t0_C, h_fg0, rho_v0)
    auto_DL, warns_DL = select_pipe(m_dot, rho_vc, mu_vc, L_DL_eq, vmin_dl, vmax_dl, dp_max_DL, tc_C, propsc["h_fg"], rho_vc)
    auto_FL, warns_FL = select_pipe(m_dot, rho_l, mu_vc, L_FL_eq, 0.5, 1.5, dp_max_FL, tc_C, propsc["h_fg"], rho_vc)

    def get_result(pipe_idx, m, rho, mu, L_eq, T_sat, h_fg_val, rho_v_val, dp_hydro=0):
        pipe = CU_PIPES[pipe_idx]
        r = calc_pipe(pipe, m, rho, mu, L_eq, T_sat, h_fg_val, rho_v_val)
        dp_total_Pa = r["dp_Pa"] + dp_hydro
        T_K = T_sat + 273.15
        dp_dT = (h_fg_val * 1000 * rho_v_val) / T_K
        dp_K_total = dp_total_Pa / dp_dT if dp_dT > 0 else r["dp_K"]
        insul = insulation_thickness_mm(T_sat, T_amb_C, phi_pct, pipe["od"])
        return {
            "pipe": pipe,
            "pipe_idx": pipe_idx,
            "v": r["v"],
            "Re": r["Re"],
            "dp_K": dp_K_total,
            "dp_bar": dp_total_Pa / 1e5,
            "insul_mm": insul,
        }

    return {
        "ref_key": ref_key,
        "ref_name": REFRIGERANTS[ref_key]["name"],
        "t0_C": t0_C,
        "tc_C": tc_C,
        "Q_kW": Q_kW,
        "m_dot_kgh": round(m_dot * 3600, 2),
        "p0_bar": round(props0["p_bar"], 2),
        "pc_bar": round(propsc["p_bar"], 2),
        "SL": {**get_result(auto_SL, m_dot, rho_v0, mu_v0, L_SL_eq, t0_C, h_fg0, rho_v0, dp_hydro_SL),
               "auto_idx": auto_SL, "warns": warns_SL, "L_eq": L_SL_eq,
               "vmin": vmin_sl, "vmax": vmax_sl, "dp_max_K": dp_max_SL},
        "DL": {**get_result(auto_DL, m_dot, rho_vc, mu_vc, L_DL_eq, tc_C, propsc["h_fg"], rho_vc),
               "auto_idx": auto_DL, "warns": warns_DL, "L_eq": L_DL_eq,
               "vmin": vmin_dl, "vmax": vmax_dl, "dp_max_K": dp_max_DL},
        "FL": {**get_result(auto_FL, m_dot, rho_l, mu_vc, L_FL_eq, tc_C, propsc["h_fg"], rho_vc, dp_hydro_FL),
               "auto_idx": auto_FL, "warns": warns_FL, "L_eq": L_FL_eq,
               "vmin": 0.5, "vmax": 1.5, "dp_max_K": dp_max_FL},
    }
