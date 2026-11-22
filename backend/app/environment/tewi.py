from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TEWIResult:
    fluid: str
    lifetime_years: float
    direct_emissions_kg_co2e: float
    indirect_emissions_kg_co2e: float
    total_tewi_kg_co2e: float
    total_tewi_t_co2e: float
    direct_share_pct: float
    indirect_share_pct: float


def calculate_tewi(
    fluid: str,
    gwp_100yr: float,
    charge_kg: float,
    annual_leak_rate: float,
    end_of_life_recovery_loss_rate: float,
    lifetime_years: float,
    annual_energy_kwh: float,
    emission_factor_kg_per_kwh: float = 0.45,
) -> TEWIResult:
    """
    Calcule le Total Equivalent Warming Impact (TEWI) sur la duree de vie :
    TEWI = Direct (fuites annuelles + pertes fin de vie) + Indirect (consommation electrique).
    """
    if lifetime_years <= 0 or charge_kg < 0 or annual_energy_kwh < 0:
        raise ValueError("Duree de vie (> 0), charge (>= 0) et energie (>= 0) invalides.")

    leak_loss = charge_kg * max(0.0, annual_leak_rate) * lifetime_years
    eol_loss = charge_kg * max(0.0, min(1.0, end_of_life_recovery_loss_rate))
    direct_kg = (leak_loss + eol_loss) * max(0.0, gwp_100yr)

    indirect_kg = annual_energy_kwh * lifetime_years * max(0.0, emission_factor_kg_per_kwh)
    total_kg = direct_kg + indirect_kg

    direct_pct = (direct_kg / total_kg * 100.0) if total_kg > 0 else 0.0
    indirect_pct = (indirect_kg / total_kg * 100.0) if total_kg > 0 else 0.0

    return TEWIResult(
        fluid=fluid,
        lifetime_years=lifetime_years,
        direct_emissions_kg_co2e=round(direct_kg, 2),
        indirect_emissions_kg_co2e=round(indirect_kg, 2),
        total_tewi_kg_co2e=round(total_kg, 2),
        total_tewi_t_co2e=round(total_kg / 1000.0, 3),
        direct_share_pct=round(direct_pct, 1),
        indirect_share_pct=round(indirect_pct, 1),
    )