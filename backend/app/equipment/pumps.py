from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PumpEquipment:
    tag: str
    fluid_type: str = "WATER"  # "WATER", "BRINE", "GLYCOL_30"
    nominal_flow_m3_h: float = 12.0
    nominal_head_m: float = 18.0
    nominal_power_kw: float = 1.1
    fluid_density_kg_m3: float = 998.0
    efficiency: float = 0.75
    speed_ratio: float = 1.0  # 0.0 a 1.2
    cavitation_risk: float = 0.0  # 0.0 a 1.0
    running: bool = True

    def evaluate(self) -> dict:
        if not self.running or self.speed_ratio <= 0.0:
            return {
                "tag": self.tag,
                "fluid_type": self.fluid_type,
                "running": False,
                "speed_ratio": 0.0,
                "flow_m3_h": 0.0,
                "mass_flow_kg_s": 0.0,
                "head_m": 0.0,
                "power_kw": 0.0,
                "cavitation_alarm": False,
            }

        n = max(0.1, min(1.2, self.speed_ratio))
        cav = max(0.0, min(1.0, self.cavitation_risk))
        degradation = max(0.4, 1.0 - 0.35 * cav)

        flow_m3_h = self.nominal_flow_m3_h * n * degradation
        head_m = self.nominal_head_m * (n**2) * degradation
        mass_flow_kg_s = (flow_m3_h * self.fluid_density_kg_m3) / 3600.0
        power_kw = (self.nominal_power_kw * (n**3)) / max(0.45, self.efficiency * degradation)

        return {
            "tag": self.tag,
            "fluid_type": self.fluid_type,
            "running": True,
            "speed_ratio": round(n, 3),
            "flow_m3_h": round(flow_m3_h, 3),
            "mass_flow_kg_s": round(mass_flow_kg_s, 4),
            "head_m": round(head_m, 2),
            "power_kw": round(power_kw, 3),
            "cavitation_alarm": cav >= 0.65,
        }