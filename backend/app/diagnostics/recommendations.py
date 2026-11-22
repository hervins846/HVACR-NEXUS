from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MaintenanceRecommendation:
    fault_code: str
    priority: str  # "IMMEDIATE", "URGENT", "PLANNED"
    action: str
    target_component: str


RECOMMENDATION_CATALOG: dict[str, tuple[str, str, str]] = {
    "HIGH_DISCHARGE_TEMP": (
        "IMMEDIATE",
        "Verifier la surchauffe, le taux de compression, la charge en fluide et l'etat des clapets compresseur.",
        "Compressor",
    ),
    "CONDENSER_FOULING_HIGH_HEAD": (
        "URGENT",
        "Nettoyer l'echangeur du condenseur et verifier le debit d'air ou d'eau de refroidissement.",
        "Condenser",
    ),
    "EVAPORATOR_FROST_OR_LOW_EVAP": (
        "URGENT",
        "Declencher un degivrage, verifier le ventilateur evaporateur et controler la pression basse.",
        "Evaporator",
    ),
    "REFRIGERANT_LEAK_SUSPECTED": (
        "URGENT",
        "Rechercher les fuites sur le circuit frigorifique, corriger l'etancheite et completer la charge.",
        "Refrigerant Circuit",
    ),
    "LIQUID_SLUGGING_LOW_SUPERHEAT": (
        "IMMEDIATE",
        "Fermer legerement le detendeur (TEV/EEV) pour retablir une surchauffe sure (>= 4 K) et proteger le compresseur.",
        "Expansion Valve",
    ),
    "LOW_COP_EFFICIENCY": (
        "PLANNED",
        "Optimiser les consignes d'evaporation/condensation et verifier l'etat global des echangeurs.",
        "System",
    ),
}


def build_recommendations(fault_codes: list[str]) -> list[MaintenanceRecommendation]:
    recommendations: list[MaintenanceRecommendation] = []
    seen: set[str] = set()
    for code in fault_codes:
        if code in seen:
            continue
        seen.add(code)
        priority, action, component = RECOMMENDATION_CATALOG.get(
            code,
            ("PLANNED", "Effectuer un controle technique complet de la boucle frigorifique.", "HVACR System"),
        )
        recommendations.append(
            MaintenanceRecommendation(
                fault_code=code,
                priority=priority,
                action=action,
                target_component=component,
            )
        )
    return recommendations