from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MTBFResult:
    equipment_id: str
    operating_hours: float
    failure_count: int
    mtbf_hours: float
    failure_rate_per_hour: float


def calculate_mtbf_hours(operating_hours: float, failure_count: int) -> float:
    """Calcule le Mean Time Between Failures (MTBF) en heures."""
    if operating_hours < 0:
        raise ValueError("Le temps de fonctionnement doit etre positif ou nul.")
    if failure_count < 0:
        raise ValueError("Le nombre de defaillances doit etre positif ou nul.")
    if failure_count == 0:
        return float(operating_hours)
    return round(operating_hours / failure_count, 2)


def evaluate_mtbf(equipment_id: str, operating_hours: float, failure_count: int) -> MTBFResult:
    """Retourne le MTBF et le taux de defaillance lambda (1/h)."""
    mtbf = calculate_mtbf_hours(operating_hours, failure_count)
    failure_rate = (failure_count / operating_hours) if operating_hours > 0 and failure_count > 0 else 0.0
    return MTBFResult(
        equipment_id=equipment_id,
        operating_hours=operating_hours,
        failure_count=failure_count,
        mtbf_hours=mtbf,
        failure_rate_per_hour=round(failure_rate, 6),
    )