from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass
class ReliabilityReport:
    equipment_id: str
    mission_time_hours: float
    mtbf_hours: float
    mttr_hours: float
    failure_rate_per_hour: float
    reliability_r_t: float
    inherent_availability: float
    operational_availability: float
    risk_level: str


def failure_rate_from_mtbf(mtbf_hours: float) -> float:
    """Calcule le taux de defaillance constant lambda = 1 / MTBF (en h^-1)."""
    if mtbf_hours <= 0:
        return 0.0
    return 1.0 / mtbf_hours


def reliability_at_time(mission_time_hours: float, mtbf_hours: float) -> float:
    """Calcule la fiabilite R(t) = exp(-t / MTBF) pour une loi exponentielle."""
    if mission_time_hours < 0:
        raise ValueError("Le temps de mission t doit etre positif ou nul.")
    if mtbf_hours <= 0:
        return 0.0 if mission_time_hours > 0 else 1.0
    r_t = math.exp(-mission_time_hours / mtbf_hours)
    return round(max(0.0, min(1.0, r_t)), 4)


def reliability_curve(
    mtbf_hours: float,
    max_hours: float = 8760.0,
    steps: int = 25,
) -> list[dict[str, float]]:
    """Genere une serie temporelle (t, R(t)) pour tracer la courbe de fiabilite."""
    if max_hours <= 0 or steps < 2:
        raise ValueError("max_hours doit etre > 0 et steps >= 2.")
    interval = max_hours / (steps - 1)
    points: list[dict[str, float]] = []
    for i in range(steps):
        t_h = round(i * interval, 2)
        points.append({
            "time_h": t_h,
            "reliability": reliability_at_time(t_h, mtbf_hours),
        })
    return points


def inherent_availability(mtbf_hours: float, mttr_hours: float) -> float:
    """Calcule la disponibilite intrinseque Ai = MTBF / (MTBF + MTTR)."""
    total = mtbf_hours + mttr_hours
    if total <= 0:
        return 0.0
    return round(mtbf_hours / total, 4)


def operational_availability(
    operating_hours: float,
    downtime_corrective_h: float,
    downtime_preventive_h: float = 0.0,
    downtime_logistics_h: float = 0.0,
) -> float:
    """Calcule la disponibilite operationnelle Ao = Uptime / (Uptime + Total Downtime)."""
    if operating_hours < 0:
        raise ValueError("Les heures de fonctionnement doivent etre positives ou nulles.")
    total_downtime = (
        max(0.0, downtime_corrective_h)
        + max(0.0, downtime_preventive_h)
        + max(0.0, downtime_logistics_h)
    )
    total_time = operating_hours + total_downtime
    if total_time <= 0:
        return 0.0
    return round(operating_hours / total_time, 4)


def evaluate_reliability(
    equipment_id: str,
    mission_time_hours: float,
    mtbf_hours: float,
    mttr_hours: float,
    downtime_preventive_h: float = 0.0,
    downtime_logistics_h: float = 0.0,
) -> ReliabilityReport:
    """Compile R(t), disponibilite intrinseque, disponibilite operationnelle et niveau de risque."""
    lam = failure_rate_from_mtbf(mtbf_hours)
    r_t = reliability_at_time(mission_time_hours, mtbf_hours)
    a_i = inherent_availability(mtbf_hours, mttr_hours)
    a_o = operational_availability(
        operating_hours=mission_time_hours,
        downtime_corrective_h=mttr_hours,
        downtime_preventive_h=downtime_preventive_h,
        downtime_logistics_h=downtime_logistics_h,
    )

    if r_t >= 0.85:
        risk_level = "LOW"
    elif r_t >= 0.65:
        risk_level = "MODERATE"
    else:
        risk_level = "HIGH"

    return ReliabilityReport(
        equipment_id=equipment_id,
        mission_time_hours=mission_time_hours,
        mtbf_hours=mtbf_hours,
        mttr_hours=mttr_hours,
        failure_rate_per_hour=round(lam, 6),
        reliability_r_t=r_t,
        inherent_availability=a_i,
        operational_availability=a_o,
        risk_level=risk_level,
    )