from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PowerBreakdown:
    compressor_power_kw: float
    auxiliaries_power_kw: float
    total_electrical_power_kw: float
    specific_power_kw_per_tr: float


def calculate_compressor_power_kw(
    mass_flow_kg_s: float,
    h_in_j_kg: float,
    h_out_j_kg: float,
    motor_efficiency: float = 0.92,
) -> float:
    """Calcule la puissance electrique compresseur (en kW)."""
    eta = max(0.35, min(0.99, motor_efficiency))
    shaft_kw = max(0.0, mass_flow_kg_s) * (h_out_j_kg - h_in_j_kg) / 1000.0
    return round(max(0.0, shaft_kw) / eta, 3)


def evaluate_power_breakdown(
    compressor_power_kw: float,
    cooling_capacity_kw: float,
    fan_power_kw: float = 0.0,
    pump_power_kw: float = 0.0,
) -> PowerBreakdown:
    comp_kw = max(0.0, compressor_power_kw)
    aux_kw = max(0.0, fan_power_kw) + max(0.0, pump_power_kw)
    total_kw = comp_kw + aux_kw
    tons_of_refrigeration = cooling_capacity_kw / 3.51685 if cooling_capacity_kw > 0 else 0.0
    kw_per_tr = (total_kw / tons_of_refrigeration) if tons_of_refrigeration > 0 else 0.0

    return PowerBreakdown(
        compressor_power_kw=round(comp_kw, 3),
        auxiliaries_power_kw=round(aux_kw, 3),
        total_electrical_power_kw=round(total_kw, 3),
        specific_power_kw_per_tr=round(kw_per_tr, 3),
    )