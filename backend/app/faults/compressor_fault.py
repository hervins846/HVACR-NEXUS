from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CompressorFault:
    severity: float = 0.0  # 0.0 (aucun defaut) a 1.0 (defaut severe : clapets, usure, manque huile)
    active: bool = False

    def apply(self, inputs: dict) -> dict:
        if not self.active or self.severity <= 0.0:
            return inputs
        sev = max(0.0, min(1.0, self.severity))
        updated = dict(inputs)
        base_eta = float(updated.get("eta_isentropic", 0.78))
        base_flow = float(updated.get("mass_flow_kg_s", 0.05))
        updated["eta_isentropic"] = round(max(0.30, base_eta * (1.0 - 0.35 * sev)), 4)
        updated["mass_flow_kg_s"] = round(max(0.005, base_flow * (1.0 - 0.25 * sev)), 5)
        return updated