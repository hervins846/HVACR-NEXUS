from CoolProp.CoolProp import PropsSI


def get_prop(output: str, input1_name: str, input1_val: float, input2_name: str, input2_val: float, fluid: str) -> float:
    return float(PropsSI(output, input1_name, input1_val, input2_name, input2_val, fluid))


def t_sat_from_p(pressure_pa: float, fluid: str) -> float:
    return get_prop("T", "P", pressure_pa, "Q", 0.0, fluid) - 273.15


def p_sat_from_t(temp_c: float, fluid: str) -> float:
    return get_prop("P", "T", temp_c + 273.15, "Q", 0.0, fluid)