from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CondenserFoulingFault:
    fouling_factor: float = 0.0  # 0.0 (propre) a 1.0 (encrassement severe / mauvais echange air ou eau)
    active: bool = False

    def apply(self, inputs: dict) -> dict:
        if not self.active or self.fouling_factor <= 0.0:
            return inputs
        sev = max(0.0, min(1.0, self.fouling_factor))
        updated = dict(inputs)
        base_t_cond = float(updated.get("t_cond_c", 40.0))
        base_subcooling = float(updated.get("subcooling_k", 4.0))
        updated["t_cond_c"] = round(base_t_cond + 18.0 * sev, 2)
        updated["subcooling_k"] = round(max(0.5, base_subcooling * (1.0 - 0.5 * sev)), 2)
        return updated