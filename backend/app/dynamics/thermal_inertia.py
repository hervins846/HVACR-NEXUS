from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ThermalMass:
    mass_kg: float
    specific_heat_j_kg_k: float

    @property
    def capacitance_j_k(self) -> float:
        """Capacite calorifique C = m * cp (en J/K)."""
        return max(1e-3, self.mass_kg) * max(1.0, self.specific_heat_j_kg_k)


def time_constant_seconds(capacitance_j_k: float, heat_transfer_ua_w_k: float) -> float:
    """Calcule la constante de temps thermique tau = C / UA (en secondes)."""
    ua = max(1e-6, heat_transfer_ua_w_k)
    return round(max(0.0, capacitance_j_k) / ua, 3)


def step_temperature_first_order(
    current_temp_c: float,
    target_temp_c: float,
    dt_seconds: float,
    tau_seconds: float,
) -> float:
    """Fait avancer une temperature selon un modele du 1er ordre discretise."""
    if dt_seconds <= 0.0:
        return round(current_temp_c, 3)
    if tau_seconds <= 1e-6:
        return round(target_temp_c, 3)
    alpha = 1.0 - (2.718281828459045 ** (-dt_seconds / tau_seconds))
    next_temp = current_temp_c + alpha * (target_temp_c - current_temp_c)
    return round(next_temp, 3)