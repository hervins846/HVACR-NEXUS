from CoolProp.CoolProp import PropsSI


def bar_to_pa(pressure_bar: float) -> float:
    return pressure_bar * 1e5


def pa_to_bar(pressure_pa: float) -> float:
    return pressure_pa / 1e5


def saturation_pressure_pa(temp_c: float, fluid: str, quality: float = 0.0) -> float:
    temp_k = temp_c + 273.15
    return float(PropsSI("P", "T", temp_k, "Q", quality, fluid))


def saturation_pressure_bar(temp_c: float, fluid: str, quality: float = 0.0) -> float:
    return pa_to_bar(saturation_pressure_pa(temp_c, fluid, quality=quality))


def compression_ratio(p_cond_pa: float, p_evap_pa: float) -> float:
    if p_evap_pa <= 0:
        raise ValueError("La pression d'evaporation doit etre strictement positive.")
    return p_cond_pa / p_evap_pa