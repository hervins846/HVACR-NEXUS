from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EnergyConsumptionReport:
    duration_hours: float
    electrical_energy_kwh: float
    cooling_energy_kwh_th: float
    estimated_cost: float
    currency: str


def calculate_energy_kwh(power_kw: float, duration_hours: float) -> float:
    """Calcule l'energie consommee ou produite en kWh : E(kWh) = P(kW) * t(h)."""
    if power_kw < 0 or duration_hours < 0:
        raise ValueError("La puissance et la duree doivent etre positives ou nulles.")
    return round(power_kw * duration_hours, 3)


def evaluate_energy_consumption(
    total_power_kw: float,
    cooling_capacity_kw: float,
    duration_hours: float = 24.0,
    tariff_per_kwh: float = 0.15,
    currency: str = "USD",
) -> EnergyConsumptionReport:
    elec_kwh = calculate_energy_kwh(total_power_kw, duration_hours)
    cool_kwh = calculate_energy_kwh(cooling_capacity_kw, duration_hours)
    cost = elec_kwh * max(0.0, tariff_per_kwh)
    return EnergyConsumptionReport(
        duration_hours=duration_hours,
        electrical_energy_kwh=elec_kwh,
        cooling_energy_kwh_th=cool_kwh,
        estimated_cost=round(cost, 2),
        currency=currency,
    )