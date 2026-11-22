from __future__ import annotations

from dataclasses import dataclass
from app.instrumentation.calibration import CalibrationProfile
from app.instrumentation.signal_4_20ma import current_ma_to_physical, detect_loop_fault, physical_to_current_ma


@dataclass
class FlowMeter:
    tag: str
    flow_min_kg_s: float = 0.0
    flow_max_kg_s: float = 1.0
    calibration: CalibrationProfile | None = None

    def read_mass_flow(self, true_mass_flow_kg_s: float, density_kg_m3: float | None = None) -> dict:
        calibrated = (
            self.calibration.apply(true_mass_flow_kg_s)
            if self.calibration
            else round(true_mass_flow_kg_s, 5)
        )
        current_ma = physical_to_current_ma(calibrated, self.flow_min_kg_s, self.flow_max_kg_s)
        mass_flow = current_ma_to_physical(current_ma, self.flow_min_kg_s, self.flow_max_kg_s)
        volumetric_m3_h = (
            round((mass_flow / density_kg_m3) * 3600.0, 4)
            if density_kg_m3 and density_kg_m3 > 0
            else None
        )
        fault = detect_loop_fault(current_ma)
        return {
            "tag": self.tag,
            "mass_flow_kg_s": round(mass_flow, 5),
            "volumetric_flow_m3_h": volumetric_m3_h,
            "signal_ma": current_ma,
            "fault": fault,
        }