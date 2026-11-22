from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PIDController:
    kp: float = 2.0
    ki: float = 0.25
    kd: float = 0.1
    output_min: float = 0.0
    output_max: float = 100.0
    integral_limit: float = 50.0
    reverse_acting: bool = False  # True si la sortie doit diminuer quand la mesure augmente (ex. refroidissement)
    _integral: float = 0.0
    _prev_error: float | None = None

    def reset(self) -> None:
        self._integral = 0.0
        self._prev_error = None

    def step(self, setpoint: float, measurement: float, dt_seconds: float = 1.0) -> float:
        dt = max(1e-3, float(dt_seconds))
        raw_error = setpoint - measurement
        error = -raw_error if self.reverse_acting else raw_error

        self._integral = max(
            -self.integral_limit,
            min(self.integral_limit, self._integral + error * dt),
        )

        derivative = 0.0
        if self._prev_error is not None:
            derivative = (error - self._prev_error) / dt
        self._prev_error = error

        output = self.kp * error + self.ki * self._integral + self.kd * derivative
        clamped = max(self.output_min, min(self.output_max, output))
        return round(clamped, 3)