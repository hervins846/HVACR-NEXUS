from __future__ import annotations

from app.engine.solver import solve_cycle_steady
from app.engine.state_manager import StateManager
from app.engine.time_manager import TimeManager


class SimulationEngine:
    def __init__(self) -> None:
        self.state_manager = StateManager()
        self.time_manager = TimeManager()
        self.step(dt=1.0)

    def _evaluate_alarms(self, cycle: dict, inputs: dict) -> list[str]:
        alarms: list[str] = []
        p_cond = cycle["pressures_bar"]["p_cond"]
        t_disch = cycle["points"][1]["t_c"]
        cop = cycle["performance"]["cop"]

        if p_cond > 16.0:
            alarms.append("HIGH_CONDENSING_PRESSURE")
        if t_disch > 110.0:
            alarms.append("HIGH_DISCHARGE_TEMPERATURE")
        if cop < 2.2:
            alarms.append("LOW_COP_EFFICIENCY")
        if inputs["superheat_k"] < 2.0:
            alarms.append("LOW_SUPERHEAT_LIQUID_SLUG_RISK")
        return alarms

    def update_parameters(self, updates: dict) -> dict:
        self.state_manager.update_inputs(updates)
        return self.step(dt=0.0)

    def step(self, dt: float = 1.0) -> dict:
        current = self.state_manager.get_state()
        inputs = current["inputs"]
        next_time = self.time_manager.advance(dt_override=dt)

        cycle, conv_status = solve_cycle_steady(inputs=inputs)
        alarms = self._evaluate_alarms(cycle, inputs)
        return self.state_manager.set_simulation_snapshot(
            cycle_data=cycle,
            time_s=next_time,
            alarms=alarms,
            convergence={
                "converged": conv_status.converged,
                "iterations": conv_status.iterations,
                "residual": conv_status.residual,
            },
        )


simulation_engine = SimulationEngine()