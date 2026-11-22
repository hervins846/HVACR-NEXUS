from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class BaseEquipment(ABC):
    equipment_id: str
    name: str
    category: str
    running: bool = True
    operating_hours: float = 0.0
    health_index: float = 100.0  # 0.0 a 100.0 %
    alarms: list[str] = field(default_factory=list)

    def clear_alarms(self) -> None:
        self.alarms.clear()

    def add_alarm(self, alarm_code: str) -> None:
        if alarm_code not in self.alarms:
            self.alarms.append(alarm_code)

    def advance_hours(self, dt_seconds: float) -> None:
        if self.running and dt_seconds > 0:
            self.operating_hours = round(self.operating_hours + dt_seconds / 3600.0, 4)

    @abstractmethod
    def evaluate(self, *args, **kwargs) -> dict:
        """Calcule l'etat physique, les performances et les alertes de l'equipement."""