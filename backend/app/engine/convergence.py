from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConvergenceConfig:
    tolerance: float = 1e-4
    max_iterations: int = 50
    relaxation_factor: float = 0.7


@dataclass
class ConvergenceStatus:
    converged: bool
    iterations: int
    residual: float


def check_residual(current_value: float, previous_value: float, tolerance: float = 1e-4) -> tuple[bool, float]:
    residual = abs(current_value - previous_value)
    return residual <= tolerance, round(residual, 8)


def relax_value(previous_value: float, new_value: float, alpha: float = 0.7) -> float:
    clamped_alpha = max(0.05, min(1.0, alpha))
    return previous_value + clamped_alpha * (new_value - previous_value)