from __future__ import annotations

from dataclasses import dataclass
from app.energy.cop import calculate_carnot_cop_cooling, calculate_cop_cooling


@dataclass
class OptimizationRecommendation:
    current_cop: float
    target_cop: float
    potential_cop_gain_pct: float
    recommended_t_cond_c: float
    recommended_t_evap_c: float
    recommended_superheat_k: float
    actions: list[str]


def suggest_cycle_optimization(
    t_evap_c: float,
    t_cond_c: float,
    superheat_k: float,
    subcooling_k: float,
    cooling_capacity_kw: float,
    electrical_power_kw: float,
    ambient_temp_c: float = 32.0,
) -> OptimizationRecommendation:
    """Propose des ajustements pragmatiques pour maximiser le COP sans compromettre la fiabilite."""
    current_cop = calculate_cop_cooling(cooling_capacity_kw, electrical_power_kw)
    carnot_cop = calculate_carnot_cop_cooling(t_evap_c, t_cond_c)

    actions: list[str] = []
    rec_t_cond = t_cond_c
    rec_t_evap = t_evap_c
    rec_sh = superheat_k

    # Abaisser la condensation vers une approche raisonnable (~8 K au-dessus de l'ambiant)
    min_achievable_cond = ambient_temp_c + 8.0
    if t_cond_c > min_achievable_cond + 1.5:
        rec_t_cond = round(max(min_achievable_cond, t_cond_c - 3.0), 1)
        actions.append("Reduire la temperature de condensation (nettoyage condenseur / debit air ou eau)")

    # Relever legerement l'evaporation si possible pour reduire le taux de compression
    if t_evap_c < 8.0:
        rec_t_evap = round(min(10.0, t_evap_c + 2.0), 1)
        actions.append("Relever la consigne d'evaporation selon la charge thermique admissible")

    # Ajuster la surchauffe vers la zone optimale 4 K - 6 K
    if superheat_k > 6.5:
        rec_sh = 5.0
        actions.append("Reduire l'exces de surchauffe vers ~5 K via le reglage du detendeur")
    elif superheat_k < 3.0:
        rec_sh = 4.5
        actions.append("Augmenter la surchauffe au-dessus de 4 K pour proteger le compresseur contre le coup de liquide")

    if subcooling_k < 2.0:
        actions.append("Verifier la charge en fluide frigorigene et le sous-refroidissement liquide")

    estimated_new_carnot = calculate_carnot_cop_cooling(rec_t_evap, rec_t_cond)
    gain_ratio = (estimated_new_carnot / carnot_cop) if carnot_cop > 0 else 1.0
    target_cop = round(max(current_cop, current_cop * min(1.35, max(1.0, gain_ratio))), 3)
    gain_pct = ((target_cop - current_cop) / current_cop * 100.0) if current_cop > 0 else 0.0

    if not actions:
        actions.append("Point de fonctionnement deja proche de l'optimum operationnel")

    return OptimizationRecommendation(
        current_cop=current_cop,
        target_cop=target_cop,
        potential_cop_gain_pct=round(max(0.0, gain_pct), 1),
        recommended_t_cond_c=rec_t_cond,
        recommended_t_evap_c=rec_t_evap,
        recommended_superheat_k=rec_sh,
        actions=actions,
    )