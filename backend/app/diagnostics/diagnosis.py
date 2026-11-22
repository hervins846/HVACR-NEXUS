from __future__ import annotations

from dataclasses import asdict, dataclass
from app.diagnostics.fault_classifier import classify_triggered_rules
from app.diagnostics.recommendation import build_recommendations
from app.diagnostics.rule_engine import RuleEngine


@dataclass
class DiagnosisReport:
    health_score: float  # 0.0 a 100.0
    overall_status: str  # "NOMINAL", "DEGRADED", "CRITICAL"
    triggered_rules: list[dict]
    classified_faults: list[dict]
    recommendations: list[dict]


class SystemDiagnostician:
    def __init__(self, rule_engine: RuleEngine | None = None) -> None:
        self.rule_engine = rule_engine or RuleEngine()

    def diagnose(self, telemetry: dict) -> DiagnosisReport:
        triggered = self.rule_engine.evaluate(telemetry)
        classified = classify_triggered_rules(triggered)
        fault_codes = [f.fault_code for f in classified]
        recommendations = build_recommendations(fault_codes)

        penalty = 0.0
        for fault in classified:
            if fault.severity == "CRITICAL":
                penalty += 25.0
            elif fault.severity == "WARNING":
                penalty += 12.0
            else:
                penalty += 5.0

        health_score = round(max(0.0, min(100.0, 100.0 - penalty)), 1)

        if any(f.severity == "CRITICAL" for f in classified) or health_score < 50.0:
            overall_status = "CRITICAL"
        elif classified:
            overall_status = "DEGRADED"
        else:
            overall_status = "NOMINAL"

        return DiagnosisReport(
            health_score=health_score,
            overall_status=overall_status,
            triggered_rules=triggered,
            classified_faults=[asdict(f) for f in classified],
            recommendations=[asdict(r) for r in recommendations],
        )