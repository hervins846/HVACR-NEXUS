from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FanEquipment:
    tag: str
    nominal_airflow_m3_h: float = 5000.0
    nominal_static_pressure_pa: float = 350.0
    nominal_power_kw: float = 1.5
    efficiency: float = 0.72
    speed_ratio: float = 1.0  # 0.0 a 1.2 (variateur VFD)
    fouling_factor: float = 0.0  # 0.0 (propre) a 1.0 (encrassement pales / grille)
    running: bool = True

    def evaluate(self) -> dict:
        if not self.running or self.speed_ratio <= 0.0:
            return {
                "tag": self.tag,
                "running": False,
                "speed_ratio": 0.0,
                "airflow_m3_h": 0.0,
                "static_pressure_pa": 0.0,
                "power_kw": 0.0,
                "effective_efficiency": 0.0,
            }

        n = max(0.1, min(1.2, self.speed_ratio))
        foul = max(0.0, min(0.8, self.fouling_factor))
        eff_factor = max(0.35, 1.0 - 0.30 * foul)

        # Lois de similitude ventilateur (affinite) + impact encrassement
        airflow = self.nominal_airflow_m3_h * n * (1.0 - 0.15 * foul)
        static_pressure = self.nominal_static_pressure_pa * (n**2) * (1.0 + 0.20 * foul)
        power_kw = (self.nominal_power_kw * (n**3)) / eff_factor

        return {
            "tag": self.tag,
            "running": True,
            "speed_ratio": round(n, 3),
            "airflow_m3_h": round(airflow, 2),
            "static_pressure_pa": round(static_pressure, 1),
            "power_kw": round(power_kw, 3),
            "effective_efficiency": round(self.efficiency * eff_factor, 3),
        }