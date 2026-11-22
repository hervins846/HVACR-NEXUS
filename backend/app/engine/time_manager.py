from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TimeManager:
    current_time_s: float = 0.0
    dt_s: float = 1.0
    paused: bool = False
    speed_multiplier: float = 1.0

    def advance(self, dt_override: float | None = None) -> float:
        if self.paused:
            return round(self.current_time_s, 3)
        step_dt = self.dt_s if dt_override is None else max(0.0, dt_override)
        effective_dt = step_dt * max(0.1, self.speed_multiplier)
        self.current_time_s = round(self.current_time_s + effective_dt, 3)
        return self.current_time_s

    def reset(self) -> float:
        self.current_time_s = 0.0
        return self.current_time_s

    @property
    def elapsed_hours(self) -> float:
        return round(self.current_time_s / 3600.0, 5)