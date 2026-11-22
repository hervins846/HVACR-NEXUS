from __future__ import annotations

from dataclasses import dataclass, field
from app.building.envelope import BuildingEnvelope
from app.building.occupancy import OccupancyProfile


@dataclass
class RoomZoneModel:
    zone_id: str
    name: str
    floor_area_m2: float = 80.0
    ceiling_height_m: float = 3.0
    air_density_kg_m3: float = 1.2
    air_cp_j_kg_k: float = 1005.0
    indoor_temp_c: float = 24.0
    relative_humidity_pct: float = 55.0
    envelope: BuildingEnvelope = field(default_factory=BuildingEnvelope)
    occupancy: OccupancyProfile = field(default_factory=OccupancyProfile)

    @property
    def volume_m3(self) -> float:
        return round(max(1.0, self.floor_area_m2) * max(1.0, self.ceiling_height_m), 2)

    @property
    def air_thermal_capacitance_j_k(self) -> float:
        air_mass_kg = self.volume_m3 * max(0.5, self.air_density_kg_m3)
        return round(air_mass_kg * max(500.0, self.air_cp_j_kg_k), 1)

    def step_temperature(
        self,
        net_heat_gain_kw: float,
        dt_seconds: float,
    ) -> float:
        """Met a jour la temperature interieure selon le bilan thermique net (en kW)."""
        if dt_seconds <= 0.0:
            return round(self.indoor_temp_c, 3)
        c_total = self.air_thermal_capacitance_j_k * 3.0  # facteur d'inertie mobilier/parois legères
        delta_t_c = (net_heat_gain_kw * 1000.0 * dt_seconds) / max(1.0, c_total)
        self.indoor_temp_c = round(max(2.0, min(48.0, self.indoor_temp_c + delta_t_c)), 3)
        return self.indoor_temp_c