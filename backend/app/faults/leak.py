from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RefrigerantLeakFault:
    charge_loss_ratio: float = 0.0  # 0.0 (charge nominale) a 1.0 (fuite importante de fluide frigorigene)
    active: bool = False

    def apply(self, inputs: dict) -> dict:
        if not self.active or self.charge_loss_ratio <= 0.0:
            return inputs
        sev = max(0.0, min(1.0, self.charge_loss_ratio))
        updated = dict(inputs)
        base_flow = float(updated.get("mass_flow_kg_s", 0.05))
        base_subcooling = float(updated.get("subcooling_k", 4.0))
        base_superheat = float(updated.get("superheat_k", 5.0))
        updated["mass_flow_kg_s"] = round(max(0.005, base_flow * (1.0 - 0.55 * sev)), 5)
        updated["subcooling_k"] = round(max(0.0, base_subcooling * (1.0 - 0.85 * sev)), 2)
        updated["superheat_k"] = round(base_superheat + 9.0 * sev, 2)
        return updated