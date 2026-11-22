from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BuildingEnvelope:
    wall_area_m2: float = 120.0
    wall_u_value_w_m2_k: float = 1.4
    window_area_m2: float = 18.0
    window_u_value_w_m2_k: float = 2.8
    solar_heat_gain_coeff: float = 0.55
    roof_area_m2: float = 80.0
    roof_u_value_w_m2_k: float = 0.9

    @property
    def total_ua_w_per_k(self) -> float:
        ua = (
            max(0.0, self.wall_area_m2) * max(0.0, self.wall_u_value_w_m2_k)
            + max(0.0, self.window_area_m2) * max(0.0, self.window_u_value_w_m2_k)
            + max(0.0, self.roof_area_m2) * max(0.0, self.roof_u_value_w_m2_k)
        )
        return round(ua, 2)

    def conduction_heat_gain_kw(self, indoor_temp_c: float, outdoor_temp_c: float) -> float:
        """Calcule les gains ou pertes thermiques par conduction (en kW)."""
        delta_t = outdoor_temp_c - indoor_temp_c
        return round((self.total_ua_w_per_k * delta_t) / 1000.0, 3)

    def solar_heat_gain_kw(self, solar_irradiance_w_m2: float = 350.0) -> float:
        """Calcule les apports solaires transmis a travers les vitrages (en kW)."""
        q_solar_w = (
            max(0.0, self.window_area_m2)
            * max(0.0, self.solar_heat_gain_coeff)
            * max(0.0, solar_irradiance_w_m2)
        )
        return round(q_solar_w / 1000.0, 3)