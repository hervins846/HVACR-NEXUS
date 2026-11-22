from CoolProp.CoolProp import PropsSI
from app.thermodynamics.temperature import saturation_temperature_c


def calculate_subcooling_k(actual_temp_c: float, pressure_pa: float, fluid: str) -> float:
    t_sat_c = saturation_temperature_c(pressure_pa, fluid, quality=0.0)
    return t_sat_c - actual_temp_c


def subcooled_liquid_temp_c(pressure_pa: float, subcooling_k: float, fluid: str) -> float:
    t_sat_c = saturation_temperature_c(pressure_pa, fluid, quality=0.0)
    return t_sat_c - subcooling_k


def subcooled_liquid_enthalpy_j_kg(pressure_pa: float, subcooling_k: float, fluid: str) -> float:
    t_sat_k = float(PropsSI("T", "P", pressure_pa, "Q", 0.0, fluid))
    t_actual_k = t_sat_k - subcooling_k
    return float(PropsSI("H", "P", pressure_pa, "T", t_actual_k, fluid))


def subcooled_liquid_entropy_j_kgk(pressure_pa: float, subcooling_k: float, fluid: str) -> float:
    t_sat_k = float(PropsSI("T", "P", pressure_pa, "Q", 0.0, fluid))
    t_actual_k = t_sat_k - subcooling_k
    return float(PropsSI("S", "P", pressure_pa, "T", t_actual_k, fluid))