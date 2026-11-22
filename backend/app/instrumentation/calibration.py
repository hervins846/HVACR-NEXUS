from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CalibrationProfile:
    sensor_id: str
    offset: float = 0.0
    gain: float = 1.0
    uncertainty: float = 0.0

    def apply(self, raw_value: float) -> float:
        """Applique la correction lineaire y_corr = gain * y_raw + offset."""
        return round(self.gain * raw_value + self.offset, 4)


def fit_two_point_calibration(
    sensor_id: str,
    raw_low: float,
    ref_low: float,
    raw_high: float,
    ref_high: float,
    uncertainty: float = 0.0,
) -> CalibrationProfile:
    """Calcule gain et offset a partir d'un etalonnage deux points (bas / haut)."""
    if raw_high == raw_low:
        raise ValueError("Les deux mesures brutes d'etalonnage doivent etre distinctes.")
    gain = (ref_high - ref_low) / (raw_high - raw_low)
    offset = ref_low - gain * raw_low
    return CalibrationProfile(
        sensor_id=sensor_id,
        offset=round(offset, 6),
        gain=round(gain, 6),
        uncertainty=round(uncertainty, 4),
    )