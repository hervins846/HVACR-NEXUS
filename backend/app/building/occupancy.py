from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OccupancyProfile:
    num_occupants: int = 10
    sensible_per_person_w: float = 75.0
    latent_per_person_w: float = 55.0
    lighting_power_kw: float = 1.2
    equipment_power_kw: float = 2.5
    occupancy_factor: float = 1.0  # 0.0 (inoccupé) a 1.2 (pic)

    def evaluate_internal_loads(self) -> dict:
        factor = max(0.0, min(1.5, self.occupancy_factor))
        people = max(0, self.num_occupants) * factor

        sensible_people_kw = (people * max(0.0, self.sensible_per_person_w)) / 1000.0
        latent_people_kw = (people * max(0.0, self.latent_per_person_w)) / 1000.0
        lighting_kw = max(0.0, self.lighting_power_kw) * factor
        equipment_kw = max(0.0, self.equipment_power_kw) * factor

        sensible_total_kw = sensible_people_kw + lighting_kw + equipment_kw
        latent_total_kw = latent_people_kw

        return {
            "effective_occupants": round(people, 1),
            "sensible_load_kw": round(sensible_total_kw, 3),
            "latent_load_kw": round(latent_total_kw, 3),
            "total_internal_load_kw": round(sensible_total_kw + latent_total_kw, 3),
        }