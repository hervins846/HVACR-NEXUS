from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class DiagnosticRule:
    rule_id: str
    fault_code: str
    severity: str  # "INFO", "WARNING", "CRITICAL"
    description: str
    condition: Callable[[dict], bool]


class RuleEngine:
    def __init__(self, rules: list[DiagnosticRule] | None = None) -> None:
        self.rules: list[DiagnosticRule] = rules if rules is not None else default_hvacr_rules()

    def evaluate(self, telemetry: dict) -> list[dict]:
        triggered: list[dict] = []
        for rule in self.rules:
            try:
                if rule.condition(telemetry):
                    triggered.append({
                        "rule_id": rule.rule_id,
                        "fault_code": rule.fault_code,
                        "severity": rule.severity,
                        "description": rule.description,
                    })
            except (KeyError, TypeError, ZeroDivisionError):
                continue
        return triggered


def default_hvacr_rules() -> list[DiagnosticRule]:
    return [
        DiagnosticRule(
            rule_id="R-01",
            fault_code="HIGH_DISCHARGE_TEMP",
            severity="CRITICAL",
            description="Temperature de refoulement compresseur superieure au seuil de securite (110 C).",
            condition=lambda d: float(d.get("discharge_temp_c", 0.0)) > 110.0,
        ),
        DiagnosticRule(
            rule_id="R-02",
            fault_code="CONDENSER_FOULING_HIGH_HEAD",
            severity="WARNING",
            description="Condensation excessive par rapport a la temperature ambiante (approche > 18 K).",
            condition=lambda d: (float(d.get("t_cond_c", 40.0)) - float(d.get("ambient_temp_c", 32.0))) > 18.0,
        ),
        DiagnosticRule(
            rule_id="R-03",
            fault_code="EVAPORATOR_FROST_OR_LOW_EVAP",
            severity="WARNING",
            description="Temperature d'evaporation basse (< -8 C) avec risque de givrage ou baisse de debit d'air.",
            condition=lambda d: float(d.get("t_evap_c", 5.0)) < -8.0,
        ),
        DiagnosticRule(
            rule_id="R-04",
            fault_code="REFRIGERANT_LEAK_SUSPECTED",
            severity="WARNING",
            description="Surchauffe elevee (> 10 K) associee a un faible sous-refroidissement (< 1.5 K).",
            condition=lambda d: (
                float(d.get("superheat_k", 5.0)) > 10.0
                and float(d.get("subcooling_k", 4.0)) < 1.5
            ),
        ),
        DiagnosticRule(
            rule_id="R-05",
            fault_code="LIQUID_SLUGGING_LOW_SUPERHEAT",
            severity="CRITICAL",
            description="Surchauffe trop faible (< 2.0 K) : risque de retour de liquide au compresseur.",
            condition=lambda d: float(d.get("superheat_k", 5.0)) < 2.0,
        ),
        DiagnosticRule(
            rule_id="R-06",
            fault_code="LOW_COP_EFFICIENCY",
            severity="WARNING",
            description="Coefficient de performance frigorifique degrade (COP < 2.2).",
            condition=lambda d: float(d.get("cop", 3.5)) < 2.2,
        ),
    ]