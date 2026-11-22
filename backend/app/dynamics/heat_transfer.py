from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HeatExchangerDynamics:
    ua_w_per_k: float = 1200.0
    fouling_resistance_factor: float = 0.0  # 0.0 (propre) a 1.0 (encrasse)

    @property
    def effective_ua_w_per_k(self) -> float:
        factor = max(0.2, 1.0 - 0.55 * max(0.0, min(1.0, self.fouling_resistance_factor)))
        return round(self.ua_w_per_k * factor, 2)

    def sensible_heat_kw(self, mass_flow_kg_s: float, cp_j_kg_k: float, delta_t_k: float) -> float:
        """Flux thermique sensible Q_dot = m_dot * cp * dT (en kW)."""
        q_w = max(0.0, mass_flow_kg_s) * max(0.0, cp_j_kg_k) * delta_t_k
        return round(q_w / 1000.0, 3)

    def conductance_heat_kw(self, temp_hot_c: float, temp_cold_c: float) -> float:
        """Flux thermique par conductance Q_dot = UA_eff * (T_chaud - T_froid) (en kW)."""
        q_w = self.effective_ua_w_per_k * (temp_hot_c - temp_cold_c)
        return round(q_w / 1000.0, 3)