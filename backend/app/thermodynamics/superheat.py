from CoolProp.CoolProp import PropsSI
from app.thermodynamics.temperature import k_to_c, saturation_temperature_c


def calculate_superheat_k(actual_temp_c: float, pressure_pa: float, fluid: str) -> float:
    t_sat_c = saturation_temperature_c(pressure_pa, fluid, quality=1.0)
    return actual_temp_c - t_sat_c


def superheated_vapor_temp_c(pressure_pa: float, superheat_k: float, fluid: str) -> float:
    t_sat_c = saturation_temperature_c(pressure_pa, fluid, quality=1.0)
    return t_sat_c + superheat_k


def superheated_vapor_enthalpy_j_kg(pressure_pa: float, superheat_k: float, fluid: str) -> float:
    t_sat_k = float(PropsSI("T", "P", pressure_pa, "Q", 1.0, fluid))
    t_actual_k = t_sat_k + superheat_k
    return float(PropsSI("H", "P", pressure_pa, "T", t_actual_k, fluid))


def superheated_vapor_entropy_j_kgk(pressure_pa: float, superheat_k: float, fluid: str) -> float:
    t_sat_k = float(PropsSI("T", "P", pressure_pa, "Q", 1.0, fluid))
    t_actual_k = t_sat_k + superheat_k
    return float(PropsSI("S", "P", pressure_pa, "T", t_actual_k, fluid))