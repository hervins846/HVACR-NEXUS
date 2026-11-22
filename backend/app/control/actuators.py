from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ActuatorBank:
    compressor_speed_ratio: float = 1.0  # 0.25 a 1.20
    valve_opening_pct: float = 65.0  # 5.0 a 100.0 %
    condenser_fan_speed_ratio: float = 1.0  # 0.20 a 1.20
    compressor_enabled: bool = True

    def apply_commands(
        self,
        compressor_speed_ratio: float | None = None,
        valve_opening_pct: float | None = None,
        condenser_fan_speed_ratio: float | None = None,
        compressor_enabled: bool | None = None,
    ) -> dict:
        if compressor_enabled is not None:
            self.compressor_enabled = bool(compressor_enabled)

        if compressor_speed_ratio is not None:
            self.compressor_speed_ratio = round(
                max(0.25, min(1.20, float(compressor_speed_ratio))), 3
            )

        if valve_opening_pct is not None:
            self.valve_opening_pct = round(
                max(5.0, min(100.0, float(valve_opening_pct))), 2
            )

        if condenser_fan_speed_ratio is not None:
            self.condenser_fan_speed_ratio = round(
                max(0.20, min(1.20, float(condenser_fan_speed_ratio))), 3
            )

        effective_comp_speed = self.compressor_speed_ratio if self.compressor_enabled else 0.0
        return {
            "compressor_enabled": self.compressor_enabled,
            "compressor_speed_ratio": round(effective_comp_speed, 3),
            "valve_opening_pct": self.valve_opening_pct,
            "condenser_fan_speed_ratio": self.condenser_fan_speed_ratio,
        }