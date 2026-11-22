from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SystemDynamicState:
    t_evap_c: float = 5.0
    t_cond_c: float = 40.0
    chamber_temp_c: float = 20.0
    mass_flow_kg_s: float = 0.05
    stabilized: bool = True

    def evaluate_stability(
        self,
        target_t_evap_c: float,
        target_t_cond_c: float,
        target_chamber_temp_c: float,
        target_mass_flow_kg_s: float,
        temp_tol_c: float = 0.25,
        flow_tol_kg_s: float = 0.001,
    ) -> bool:
        delta_evap = abs(self.t_evap_c - target_t_evap_c)
        delta_cond = abs(self.t_cond_c - target_t_cond_c)
        delta_chamber = abs(self.chamber_temp_c - target_chamber_temp_c)
        delta_flow = abs(self.mass_flow_kg_s - target_mass_flow_kg_s)

        self.stabilized = (
            delta_evap <= temp_tol_c
            and delta_cond <= temp_tol_c
            and delta_chamber <= temp_tol_c
            and delta_flow <= flow_tol_kg_s
        )
        return self.stabilized