from __future__ import annotations

from app.engine.convergence import ConvergenceConfig, ConvergenceStatus, check_residual, relax_value
from app.thermodynamics.cycle_calculator import calculate_vapor_compression_cycle


def solve_cycle_steady(inputs: dict, config: ConvergenceConfig | None = None) -> tuple[dict, ConvergenceStatus]:
    """Resout le cycle frigorifique en iterant sur la puissance frigorifique pour verifier la convergence."""
    cfg = config or ConvergenceConfig()
    prev_q = None
    relaxed_q = None
    last_cycle: dict = {}
    residual = 0.0
    converged = False
    iterations = 0

    for iteration in range(1, cfg.max_iterations + 1):
        iterations = iteration
        cycle = calculate_vapor_compression_cycle(
            fluid=inputs["fluid"],
            t_evap_c=inputs["t_evap_c"],
            t_cond_c=inputs["t_cond_c"],
            superheat_k=inputs["superheat_k"],
            subcooling_k=inputs["subcooling_k"],
            eta_isentropic=inputs["eta_isentropic"],
            mass_flow_kg_s=inputs["mass_flow_kg_s"],
        )
        raw_q = float(cycle["performance"]["q_evap_kw"])
        relaxed_q = raw_q if relaxed_q is None else relax_value(relaxed_q, raw_q, cfg.relaxation_factor)

        if prev_q is not None:
            converged, residual = check_residual(relaxed_q, prev_q, cfg.tolerance)
            if converged:
                last_cycle = cycle
                break

        prev_q = relaxed_q
        last_cycle = cycle

    return last_cycle, ConvergenceStatus(
        converged=converged or iterations == 1,
        iterations=iterations,
        residual=residual,
    )