from __future__ import annotations

from dataclasses import dataclass
from app.instrumentation.calibration import CalibrationProfile
from app.instrumentation.signal_4_20ma import current_ma_to_physical, detect_loop_fault, physical_to_current_ma


@dataclass
class TemperatureSensor:
    tag: str
    sensor_type: str = "PT100"
    t_min_c: float = -40.0
    t_max_c: float = 150.0
    calibration: CalibrationProfile | None = None

    def read_celsius(self, true_temp_c: float) -> dict:
        calibrated = self.calibration.apply(true_temp_c) if self.calibration else round(true_temp_c, 3)
        current_ma = physical_to_current_ma(calibrated, self.t_min_c, self.t_max_c)
        reconstructed_c = current_ma_to_physical(current_ma, self.t_min_c, self.t_max_c)
        fault = detect_loop_fault(current_ma)
        return {
            "tag": self.tag,
            "sensor_type": self.sensor_type,
            "temperature_c": round(reconstructed_c, 3),
            "temperature_k": round(reconstructed_c + 273.15, 3),
            "signal_ma": current_ma,
            "fault": fault,
        }