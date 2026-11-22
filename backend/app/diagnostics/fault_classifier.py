from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ClassifiedFault:
    fault_code: str
    subsystem: str  # "COMPRESSOR", "CONDENSER", "EVAPORATOR", "EXPANSION_VALVE", "REFRIGERANT_CIRCUIT", "EFFICIENCY"
    severity: str
    confidence: float  # 0.0 a 1.0


FAULT_SUBSYSTEM_MAP: dict[str, tuple[str, float]] = {
    "HIGH_DISCHARGE_TEMP": ("COMPRESSOR", 0.90),
    "CONDENSER_FOULING_HIGH_HEAD": ("CONDENSER", 0.85),
    "EVAPORATOR_FROST_OR_LOW_EVAP": ("EVAPORATOR", 0.82),
    "REFRIGERANT_LEAK_SUSPECTED": ("REFRIGERANT_CIRCUIT", 0.80),
    "LIQUID_SLUGGING_LOW_SUPERHEAT": ("EXPANSION_VALVE", 0.88),
    "LOW_COP_EFFICIENCY": ("EFFICIENCY", 0.75),
}


def classify_triggered_rules(triggered_rules: list[dict]) -> list[ClassifiedFault]:
    classified: list[ClassifiedFault] = []
    for item in triggered_rules:
        code = str(item.get("fault_code", "UNKNOWN_FAULT"))
        severity = str(item.get("severity", "WARNING"))
        subsystem, base_conf = FAULT_SUBSYSTEM_MAP.get(code, ("GENERAL", 0.65))
        classified.append(
            ClassifiedFault(
                fault_code=code,
                subsystem=subsystem,
                severity=severity,
                confidence=base_conf,
            )
        )
    return classified