from __future__ import annotations

from dataclasses import dataclass
from app.instrumentation.calibration import CalibrationProfile
from app.instrumentation.signal_4_20ma import current_ma_to_physical, detect_loop_fault, physical_to_current_ma


@dataclass
class PressureTransmitter:
    tag: str
    p_min_bar: float = 0.0
    p_max_bar: float = 35.0
    calibration: CalibrationProfile | None = None

    def read_bar(self, true_pressure_bar: float) -> dict:
        calibrated = self.calibration.apply(true_pressure_bar) if self.calibration else round(true_pressure_bar, 4)
        current_ma = physical_to_current_ma(calibrated, self.p_min_bar, self.p_max_bar)
        reconstructed_bar = current_ma_to_physical(current_ma, self.p_min_bar, self.p_max_bar)
        fault = detect_loop_fault(current_ma)
        return {
            "tag": self.tag,
            "pressure_bar": reconstructed_bar,
            "pressure_pa": round(reconstructed_bar * 1e5, 1),
            "signal_ma": current_ma,
            "fault": fault,
        }