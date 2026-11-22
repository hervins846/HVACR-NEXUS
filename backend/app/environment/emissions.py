from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EmissionsReport:
    annual_energy_kwh: float
    grid_emission_factor_kg_co2_per_kwh: float
    annual_indirect_co2_kg: float
    annual_direct_co2e_kg: float
    total_annual_co2e_kg: float


def indirect_emissions_kg(
    power_kw: float,
    annual_operating_hours: float,
    emission_factor_kg_per_kwh: float = 0.45,
) -> float:
    """Calcule les emissions indirectes (en kg CO2) liees a la consommation electrique."""
    if power_kw < 0 or annual_operating_hours < 0 or emission_factor_kg_per_kwh < 0:
        raise ValueError("Les parametres d'emissions doivent etre positifs ou nuls.")
    kwh = power_kw * annual_operating_hours
    return round(kwh * emission_factor_kg_per_kwh, 2)


def evaluate_annual_emissions(
    power_kw: float,
    annual_operating_hours: float = 4000.0,
    emission_factor_kg_per_kwh: float = 0.45,
    direct_leak_co2e_kg: float = 0.0,
) -> EmissionsReport:
    annual_kwh = max(0.0, power_kw) * max(0.0, annual_operating_hours)
    indirect_kg = indirect_emissions_kg(
        power_kw=power_kw,
        annual_operating_hours=annual_operating_hours,
        emission_factor_kg_per_kwh=emission_factor_kg_per_kwh,
    )
    direct_kg = max(0.0, direct_leak_co2e_kg)
    return EmissionsReport(
        annual_energy_kwh=round(annual_kwh, 2),
        grid_emission_factor_kg_co2_per_kwh=emission_factor_kg_per_kwh,
        annual_indirect_co2_kg=indirect_kg,
        annual_direct_co2e_kg=round(direct_kg, 2),
        total_annual_co2e_kg=round(indirect_kg + direct_kg, 2),
    )