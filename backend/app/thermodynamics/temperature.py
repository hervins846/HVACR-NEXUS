from CoolProp.CoolProp import PropsSI


def c_to_k(temp_c: float) -> float:
    return temp_c + 273.15


def k_to_c(temp_k: float) -> float:
    return temp_k - 273.15


def saturation_temperature_c(pressure_pa: float, fluid: str, quality: float = 0.0) -> float:
    t_k = float(PropsSI("T", "P", pressure_pa, "Q", quality, fluid))
    return k_to_c(t_k)


def temperature_from_ph_c(pressure_pa: float, enthalpy_j_kg: float, fluid: str) -> float:
    t_k = float(PropsSI("T", "P", pressure_pa, "H", enthalpy_j_kg, fluid))
    return k_to_c(t_k)


def temperature_from_ps_c(pressure_pa: float, entropy_j_kgk: float, fluid: str) -> float:
    t_k = float(PropsSI("T", "P", pressure_pa, "S", entropy_j_kgk, fluid))
    return k_to_c(t_k)