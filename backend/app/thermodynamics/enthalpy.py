from CoolProp.CoolProp import PropsSI


def enthalpy_from_pt(pressure_pa: float, temp_c: float, fluid: str) -> float:
    return float(PropsSI("H", "P", pressure_pa, "T", temp_c + 273.15, fluid))


def enthalpy_from_ps(pressure_pa: float, entropy_j_kgk: float, fluid: str) -> float:
    return float(PropsSI("H", "P", pressure_pa, "S", entropy_j_kgk, fluid))


def enthalpy_from_pq(pressure_pa: float, quality: float, fluid: str) -> float:
    return float(PropsSI("H", "P", pressure_pa, "Q", quality, fluid))


def saturated_vapor_enthalpy(pressure_pa: float, fluid: str) -> float:
    return enthalpy_from_pq(pressure_pa, 1.0, fluid)


def saturated_liquid_enthalpy(pressure_pa: float, fluid: str) -> float:
    return enthalpy_from_pq(pressure_pa, 0.0, fluid)


def isentropic_discharge_enthalpy(h_in_j_kg: float, s_in_j_kgk: float, p_cond_pa: float, eta_is: float, fluid: str) -> float:
    h_2s = enthalpy_from_ps(p_cond_pa, s_in_j_kgk, fluid)
    eta = max(0.05, min(0.99, eta_is))
    return h_in_j_kg + (h_2s - h_in_j_kg) / eta