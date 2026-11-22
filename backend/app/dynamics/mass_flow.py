from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MassFlowDynamics:
    current_mass_flow_kg_s: float = 0.05
    valve_response_tau_s: float = 4.0

    def step(
        self,
        target_mass_flow_kg_s: float,
        dt_seconds: float,
        compressor_speed_ratio: float = 1.0,
        valve_opening_pct: float = 65.0,
    ) -> float:
        """Fait evoluer dynamiquement le debit massique selon la vitesse compresseur et l'ouverture detendeur."""
        speed_factor = max(0.1, min(1.25, compressor_speed_ratio))
        valve_factor = max(0.15, min(1.2, valve_opening_pct / 65.0))
        effective_target = max(0.0, target_mass_flow_kg_s) * speed_factor * valve_factor

        if dt_seconds <= 0.0 or self.valve_response_tau_s <= 1e-6:
            self.current_mass_flow_kg_s = round(effective_target, 5)
            return self.current_mass_flow_kg_s

        alpha = 1.0 - (2.718281828459045 ** (-dt_seconds / self.valve_response_tau_s))
        self.current_mass_flow_kg_s = round(
            self.current_mass_flow_kg_s + alpha * (effective_target - self.current_mass_flow_kg_s),
            5,
        )
        return self.current_mass_flow_kg_s