from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


MaintenanceTrigger = Literal["CALENDAR_DAYS", "RUNNING_HOURS", "THERMAL_ALERT"]


@dataclass
class PreventiveTask:
    task_id: str
    equipment_id: str
    title: str
    trigger: MaintenanceTrigger
    interval_value: float
    elapsed_value: float
    estimated_duration_h: float

    @property
    def is_due(self) -> bool:
        return self.elapsed_value >= self.interval_value

    @property
    def remaining_before_due(self) -> float:
        return round(self.interval_value - self.elapsed_value, 2)


def build_hvacr_preventive_plan(equipment_id: str, running_hours: float, has_thermal_alert: bool) -> list[PreventiveTask]:
    """Genere un plan de maintenance preventive standard pour equipement HVAC/R."""
    return [
        PreventiveTask(
            task_id="PM-COMP-01",
            equipment_id=equipment_id,
            title="Controle isolement moteur compresseur, intensite et vibrations",
            trigger="RUNNING_HOURS",
            interval_value=2000.0,
            elapsed_value=running_hours,
            estimated_duration_h=2.5,
        ),
        PreventiveTask(
            task_id="PM-COND-02",
            equipment_id=equipment_id,
            title="Nettoyage batterie condenseur, verification sous-refroidissement et HP",
            trigger="RUNNING_HOURS",
            interval_value=1500.0,
            elapsed_value=running_hours,
            estimated_duration_h=3.0,
        ),
        PreventiveTask(
            task_id="PM-EVAP-03",
            equipment_id=equipment_id,
            title="Verification surchauffe, detendeur, givrage et ecoulement condensats",
            trigger="THERMAL_ALERT" if has_thermal_alert else "RUNNING_HOURS",
            interval_value=1.0 if has_thermal_alert else 1000.0,
            elapsed_value=1.0 if has_thermal_alert else running_hours,
            estimated_duration_h=1.5,
        ),
    ]