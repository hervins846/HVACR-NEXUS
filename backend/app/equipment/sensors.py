from __future__ import annotations

from dataclasses import dataclass, field
from app.instrumentation.calibration import CalibrationProfile
from app.instrumentation.flow_meter import FlowMeter
from app.instrumentation.pressure_transmitter import PressureTransmitter
from app.instrumentation.temperature_sensor import TemperatureSensor


@dataclass
class EquipmentSensorSuite:
    equipment_id: str
    suction_pressure: PressureTransmitter = field(
        default_factory=lambda: PressureTransmitter(tag="PT-LP-01", p_min_bar=0.0, p_max_bar=20.0)
    )
    discharge_pressure: PressureTransmitter = field(
        default_factory=lambda: PressureTransmitter(tag="PT-HP-01", p_min_bar=0.0, p_max_bar=40.0)
    )
    suction_temp: TemperatureSensor = field(
        default_factory=lambda: TemperatureSensor(tag="TT-SUC-01", sensor_type="PT100", t_min_c=-40.0, t_max_c=120.0)
    )
    discharge_temp: TemperatureSensor = field(
        default_factory=lambda: TemperatureSensor(tag="TT-DIS-01", sensor_type="PT100", t_min_c=-20.0, t_max_c=180.0)
    )
    refrigerant_flow: FlowMeter = field(
        default_factory=lambda: FlowMeter(tag="FT-REF-01", flow_min_kg_s=0.0, flow_max_kg_s=0.5)
    )

    def apply_calibration(self, sensor_name: str, profile: CalibrationProfile) -> None:
        target = getattr(self, sensor_name, None)
        if target is None or not hasattr(target, "calibration"):
            raise ValueError(f"Capteur inconnu : {sensor_name}")
        target.calibration = profile

    def poll_cycle_telemetry(
        self,
        p_evap_bar: float,
        p_cond_bar: float,
        t_suction_c: float,
        t_discharge_c: float,
        mass_flow_kg_s: float,
    ) -> dict:
        readings = {
            "suction_pressure": self.suction_pressure.read_bar(p_evap_bar),
            "discharge_pressure": self.discharge_pressure.read_bar(p_cond_bar),
            "suction_temp": self.suction_temp.read_celsius(t_suction_c),
            "discharge_temp": self.discharge_temp.read_celsius(t_discharge_c),
            "refrigerant_flow": self.refrigerant_flow.read_mass_flow(mass_flow_kg_s),
        }
        faults = [
            f"{key}:{val['fault']}"
            for key, val in readings.items()
            if val.get("fault") is not None
        ]
        return {
            "equipment_id": self.equipment_id,
            "readings": readings,
            "sensor_faults": faults,
        }