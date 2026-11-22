from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MTTRResult:
    equipment_id: str
    total_repair_hours: float
    repair_count: int
    mttr_hours: float
    maintainability_index: float


def calculate_mttr_hours(total_repair_hours: float, repair_count: int) -> float:
    """Calcule le Mean Time To Repair (MTTR) en heures."""
    if total_repair_hours < 0:
        raise ValueError("La duree totale de reparation doit etre positive ou nulle.")
    if repair_count < 0:
        raise ValueError("Le nombre d'interventions correctives doit etre positif ou nul.")
    if repair_count == 0:
        return 0.0
    return round(total_repair_hours / repair_count, 2)


def evaluate_mttr(
    equipment_id: str,
    total_repair_hours: float,
    repair_count: int,
    target_mttr_hours: float = 4.0,
) -> MTTRResult:
    """Evalue le MTTR et un indicateur de maintenabilite relatif a une cible (0 a 100 %)."""
    mttr = calculate_mttr_hours(total_repair_hours, repair_count)
    if mttr == 0.0:
        index = 100.0
    elif target_mttr_hours > 0:
        index = max(0.0, min(100.0, (target_mttr_hours / mttr) * 100.0))
    else:
        index = 0.0

    return MTTRResult(
        equipment_id=equipment_id,
        total_repair_hours=total_repair_hours,
        repair_count=repair_count,
        mttr_hours=mttr,
        maintainability_index=round(index, 1),
    )