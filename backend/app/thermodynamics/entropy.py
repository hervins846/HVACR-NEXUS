from CoolProp.CoolProp import PropsSI


def entropy_from_pt(pressure_pa: float, temp_c: float, fluid: str) -> float:
    return float(PropsSI("S", "P", pressure_pa, "T", temp_c + 273.15, fluid))


def entropy_from_ph(pressure_pa: float, enthalpy_j_kg: float, fluid: str) -> float:
    return float(PropsSI("S", "P", pressure_pa, "H", enthalpy_j_kg, fluid))


def saturated_vapor_entropy(pressure_pa: float, fluid: str) -> float:
    return float(PropsSI("S", "P", pressure_pa, "Q", 1.0, fluid))


def saturated_liquid_entropy(pressure_pa: float, fluid: str) -> float:
    return float(PropsSI("S", "P", pressure_pa, "Q", 0.0, fluid))


def entropy_generation_j_kgk(s_out: float, s_in: float, q_dot_w: float = 0.0, t_source_k: float = 298.15) -> float:
    heat_term = (q_dot_w / t_source_k) if t_source_k > 0 else 0.0
    return (s_out - s_in) - heat_term