from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ValveFaultMode = Literal["OVERFEEDING", "STARVATION", "STUCK"]


@dataclass
class ExpansionValveFault:
    mode: ValveFaultMode = "STARVATION"
    severity: float = 0.0  # 0.0 a 1.0
    active: bool = False

    def apply(self, inputs: dict) -> dict:
        if not self.active or self.severity <= 0.0:
            return inputs
        sev = max(0.0, min(1.0, self.severity))
        updated = dict(inputs)
        base_superheat = float(updated.get("superheat_k", 5.0))
        base_flow = float(updated.get("mass_flow_kg_s", 0.05))

        if self.mode == "STARVATION":
            updated["superheat_k"] = round(base_superheat + 10.0 * sev, 2)
            updated["mass_flow_kg_s"] = round(max(0.005, base_flow * (1.0 - 0.30 * sev)), 5)
        elif self.mode == "OVERFEEDING":
            updated["superheat_k"] = round(max(0.5, base_superheat - 4.2 * sev), 2)
            updated["mass_flow_kg_s"] = round(base_flow * (1.0 + 0.15 * sev), 5)
        elif self.mode == "STUCK":
            updated["mass_flow_kg_s"] = round(max(0.005, base_flow * (1.0 - 0.20 * sev)), 5)

        return updated