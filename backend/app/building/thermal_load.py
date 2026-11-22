from dataclasses import dataclass
from app.building.room_model import RoomZoneModel


@dataclass
class ThermalLoadSummary:
    zone_id: str
    conduction_kw: float
    solar_kw: float
    infiltration_kw: float
    internal_sensible_kw: float
    internal_latent_kw: float
    total_sensible_load_kw: float
    total_latent_load_kw: float
    total_cooling_load_kw: float


def calculate_infiltration_load_kw(
    volume_m3: float,
    air_changes_per_hour: float,
    indoor_temp_c: float,
    outdoor_temp_c: float,
    air_density_kg_m3: float = 1.2,
    air_cp_j_kg_k: float = 1005.0,
) -> float:
    """Calcule la charge sensible d'infiltration d'air (en kW)."""
    vol_flow_m3_s = (max(0.0, volume_m3) * max(0.0, air_changes_per_hour)) / 3600.0
    mass_flow_kg_s = vol_flow_m3_s * max(0.5, air_density_kg_m3)
    q_w = mass_flow_kg_s * max(500.0, air_cp_j_kg_k) * (outdoor_temp_c - indoor_temp_c)
    return round(q_w / 1000.0, 3)


def evaluate_zone_thermal_load(
    zone: RoomZoneModel,
    outdoor_temp_c: float = 33.0,
    solar_irradiance_w_m2: float = 350.0,
    air_changes_per_hour: float = 0.8,
) -> ThermalLoadSummary:
    conduction_kw = zone.envelope.conduction_heat_gain_kw(
        indoor_temp_c=zone.indoor_temp_c,
        outdoor_temp_c=outdoor_temp_c,
    )
    solar_kw = zone.envelope.solar_heat_gain_kw(solar_irradiance_w_m2=solar_irradiance_w_m2)
    infiltration_kw = calculate_infiltration_load_kw(
        volume_m3=zone.volume_m3,
        air_changes_per_hour=air_changes_per_hour,
        indoor_temp_c=zone.indoor_temp_c,
        outdoor_temp_c=outdoor_temp_c,
        air_density_kg_m3=zone.air_density_kg_m3,
        air_cp_j_kg_k=zone.air_cp_j_kg_k,
    )
    internal = zone.occupancy.evaluate_internal_loads()
    sensible_total = conduction_kw + solar_kw + infiltration_kw + internal["sensible_load_kw"]
    latent_total = internal["latent_load_kw"]
    total_load = max(0.0, sensible_total + latent_total)

    return ThermalLoadSummary(
        zone_id=zone.zone_id,
        conduction_kw=conduction_kw,
        solar_kw=solar_kw,
        infiltration_kw=infiltration_kw,
        internal_sensible_kw=internal["sensible_load_kw"],
        internal_latent_kw=latent_total,
        total_sensible_load_kw=round(sensible_total, 3),
        total_latent_load_kw=round(latent_total, 3),
        total_cooling_load_kw=round(total_load, 3),
    )