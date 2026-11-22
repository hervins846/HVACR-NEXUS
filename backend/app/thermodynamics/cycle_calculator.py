from CoolProp.CoolProp import PropsSI


def calculate_vapor_compression_cycle(
    fluid: str = "R134a",
    t_evap_c: float = 5.0,
    t_cond_c: float = 40.0,
    superheat_k: float = 5.0,
    subcooling_k: float = 4.0,
    eta_isentropic: float = 0.78,
    mass_flow_kg_s: float = 0.05,
) -> dict:
    t_evap_k = t_evap_c + 273.15
    t_cond_k = t_cond_c + 273.15

    p_evap = float(PropsSI("P", "T", t_evap_k, "Q", 1.0, fluid))
    p_cond = float(PropsSI("P", "T", t_cond_k, "Q", 0.0, fluid))

    # Point 1 : Sortie evaporateur (vapeur surchauffee)
    t1_k = t_evap_k + superheat_k
    h1 = float(PropsSI("H", "P", p_evap, "T", t1_k, fluid))
    s1 = float(PropsSI("S", "P", p_evap, "T", t1_k, fluid))

    # Point 2s & 2 : Fin de compression
    h2s = float(PropsSI("H", "P", p_cond, "S", s1, fluid))
    eta = max(0.1, min(0.99, eta_isentropic))
    h2 = h1 + (h2s - h1) / eta
    t2_k = float(PropsSI("T", "P", p_cond, "H", h2, fluid))
    s2 = float(PropsSI("S", "P", p_cond, "H", h2, fluid))

    # Point 3 : Sortie condenseur (liquide sous-refroidi)
    t3_k = t_cond_k - subcooling_k
    h3 = float(PropsSI("H", "P", p_cond, "T", t3_k, fluid))
    s3 = float(PropsSI("S", "P", p_cond, "T", t3_k, fluid))

    # Point 4 : Sortie detendeur (detente isenthalpique h4 = h3)
    h4 = h3
    t4_k = float(PropsSI("T", "P", p_evap, "H", h4, fluid))
    s4 = float(PropsSI("S", "P", p_evap, "H", h4, fluid))
    q4 = float(PropsSI("Q", "P", p_evap, "H", h4, fluid))

    # Puissances (en kW, enthalpies en J/kg)
    q_evap_kw = mass_flow_kg_s * (h1 - h4) / 1000.0
    w_comp_kw = mass_flow_kg_s * (h2 - h1) / 1000.0
    q_cond_kw = mass_flow_kg_s * (h2 - h3) / 1000.0
    cop = q_evap_kw / w_comp_kw if w_comp_kw > 1e-9 else 0.0
    pressure_ratio = p_cond / p_evap if p_evap > 0 else 0.0

    return {
        "fluid": fluid,
        "pressures_bar": {
            "p_evap": round(p_evap / 1e5, 3),
            "p_cond": round(p_cond / 1e5, 3),
            "pressure_ratio": round(pressure_ratio, 2),
        },
        "points": [
            {"id": 1, "label": "Evap Out", "t_c": round(t1_k - 273.15, 2), "p_bar": round(p_evap / 1e5, 3), "h_kj_kg": round(h1 / 1000.0, 2), "s_kj_kgk": round(s1 / 1000.0, 4)},
            {"id": 2, "label": "Comp Out", "t_c": round(t2_k - 273.15, 2), "p_bar": round(p_cond / 1e5, 3), "h_kj_kg": round(h2 / 1000.0, 2), "s_kj_kgk": round(s2 / 1000.0, 4)},
            {"id": 3, "label": "Cond Out", "t_c": round(t3_k - 273.15, 2), "p_bar": round(p_cond / 1e5, 3), "h_kj_kg": round(h3 / 1000.0, 2), "s_kj_kgk": round(s3 / 1000.0, 4)},
            {"id": 4, "label": "Exp Out", "t_c": round(t4_k - 273.15, 2), "p_bar": round(p_evap / 1e5, 3), "h_kj_kg": round(h4 / 1000.0, 2), "s_kj_kgk": round(s4 / 1000.0, 4), "vapor_quality": round(q4, 3)},
        ],
        "performance": {
            "q_evap_kw": round(q_evap_kw, 3),
            "w_comp_kw": round(w_comp_kw, 3),
            "q_cond_kw": round(q_cond_kw, 3),
            "cop": round(cop, 3),
            "mass_flow_kg_s": mass_flow_kg_s,
        },
    }