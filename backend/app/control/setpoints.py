from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SystemSetpoints:
    target_chamber_temp_c: float = 4.0
    target_t_evap_c: float = 2.0
    target_t_cond_c: float = 38.0
    target_superheat_k: float = 5.0
    target_subcooling_k: float = 4.0
    deadband_c: float = 0.5
    auto_mode: bool = True

    def update(self, updates: dict) -> dict:
        for key, value in updates.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)
        return self.as_dict()

    def as_dict(self) -> dict:
        return {
            "target_chamber_temp_c": round(float(self.target_chamber_temp_c), 2),
            "target_t_evap_c": round(float(self.target_t_evap_c), 2),
            "target_t_cond_c": round(float(self.target_t_cond_c), 2),
            "target_superheat_k": round(float(self.target_superheat_k), 2),
            "target_subcooling_k": round(float(self.target_subcooling_k), 2),
            "deadband_c": round(float(self.deadband_c), 2),
            "auto_mode": bool(self.auto_mode),
        }