from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvaporatorFrostFault:
    frost_level: float = 0.0  # 0.0 (sans givre) a 1.0 (givrage fort / debit d'air reduit)
    active: bool = False

    def apply(self, inputs: dict) -> dict:
        if not self.active or self.frost_level <= 0.0:
            return inputs
        sev = max(0.0, min(1.0, self.frost_level))
        updated = dict(inputs)
        base_t_evap = float(updated.get("t_evap_c", 5.0))
        base_superheat = float(updated.get("superheat_k", 5.0))
        updated["t_evap_c"] = round(base_t_evap - 12.0 * sev, 2)
        updated["superheat_k"] = round(max(1.0, base_superheat * (1.0 - 0.45 * sev)), 2)
        return updated