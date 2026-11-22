from __future__ import annotations

from dataclasses import dataclass


@dataclass
class COPReport:
    cop_cooling: float
    cop_heating: float
    cop_carnot_cooling: float
    exergetic_efficiency: float


def calculate_cop_cooling(cooling_capacity_kw: float, electrical_power_kw: float) -> float:
    """Calcule le Coefficient de Performance frigorifique COP_f = Q_evap / W_elec."""
    if electrical_power_kw <= 0:
        return 0.0
    return round(max(0.0, cooling_capacity_kw) / electrical_power_kw, 3)


def calculate_cop_heating(heating_capacity_kw: float, electrical_power_kw: float) -> float:
    """Calcule le Coefficient de Performance calorifique COP_c = Q_cond / W_elec."""
    if electrical_power_kw <= 0:
        return 0.0
    return round(max(0.0, heating_capacity_kw) / electrical_power_kw, 3)


def calculate_carnot_cop_cooling(t_evap_c: float, t_cond_c: float) -> float:
    """Calcule le COP ideal de Carnot en froid : T_evap(K) / (T_cond(K) - T_evap(K))."""
    t_evap_k = t_evap_c + 273.15
    t_cond_k = t_cond_c + 273.15
    delta_t = t_cond_k - t_evap_k
    if delta_t <= 0 or t_evap_k <= 0:
        return 0.0
    return round(t_evap_k / delta_t, 3)


def evaluate_cop_metrics(
    cooling_capacity_kw: float,
    heating_capacity_kw: float,
    electrical_power_kw: float,
    t_evap_c: float,
    t_cond_c: float,
) -> COPReport:
    cop_c = calculate_cop_cooling(cooling_capacity_kw, electrical_power_kw)
    cop_h = calculate_cop_heating(heating_capacity_kw, electrical_power_kw)
    cop_carnot = calculate_carnot_cop_cooling(t_evap_c, t_cond_c)
    exergy_eff = (cop_c / cop_carnot * 100.0) if cop_carnot > 0 else 0.0
    return COPReport(
        cop_cooling=cop_c,
        cop_heating=cop_h,
        cop_carnot_cooling=cop_carnot,
        exergetic_efficiency=round(max(0.0, min(100.0, exergy_eff)), 1),
    )