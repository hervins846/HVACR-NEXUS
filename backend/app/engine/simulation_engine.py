from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StateManager:
    state: dict[str, Any]

    def get_state(self) -> dict[str, Any]:
        return self.state


@dataclass
class SimulationEngine:
    """Moteur de simulation thermodynamique et de charges HVACR."""

    state: dict[str, Any] = field(init=False)
    state_manager: StateManager = field(init=False)

    def __post_init__(self) -> None:
        self.state = {
            "running": False,
            "step": 0,
            "sim_time_s": 0.0,
            "inputs": {
                "fluid": "R410A",
                "t_evap_c": 5.0,
                "t_cond_c": 40.0,
                "superheat_k": 5.0,
                "subcooling_k": 4.0,
                "eta_isentropic": 0.78,
                "mass_flow_kg_s": 0.15,
            },
            "cycle": {
                "performance": {
                    "cop": 3.5,
                    "cooling_capacity_kw": 24.5,
                    "compressor_power_kw": 7.0,
                },
                "points": [
                    {"name": "evap_out", "t_c": 10.0, "p_bar": 9.3},
                    {"name": "comp_out", "t_c": 68.0, "p_bar": 24.2},
                    {"name": "cond_out", "t_c": 36.0, "p_bar": 24.2},
                    {"name": "exp_out", "t_c": 5.0, "p_bar": 9.3},
                ],
            },
        }
        self.state_manager = StateManager(self.state)

    def _recompute_cycle(self) -> None:
        inputs = self.state["inputs"]
        t_evap = float(inputs.get("t_evap_c", 5.0))
        t_cond = float(inputs.get("t_cond_c", 40.0))
        sh = float(inputs.get("superheat_k", 5.0))
        sc = float(inputs.get("subcooling_k", 4.0))
        eta = float(inputs.get("eta_isentropic", 0.78))
        mdot = float(inputs.get("mass_flow_kg_s", 0.15))

        delta_t = max(1.0, t_cond - t_evap)
        cop = max(0.8, round((273.15 + t_evap) / delta_t * eta * 0.65, 2))
        cooling_kw = max(0.5, round(mdot * (145.0 + 1.4 * sc), 2))
        power_kw = max(0.2, round(cooling_kw / cop, 2))
        discharge_t = round(t_cond + 18.0 + 0.6 * sh + 0.35 * delta_t, 1)

        self.state["cycle"] = {
            "performance": {
                "cop": cop,
                "cooling_capacity_kw": cooling_kw,
                "compressor_power_kw": power_kw,
            },
            "points": [
                {"name": "evap_out", "t_c": round(t_evap + sh, 1), "p_bar": 9.3},
                {"name": "comp_out", "t_c": discharge_t, "p_bar": 24.2},
                {"name": "cond_out", "t_c": round(t_cond - sc, 1), "p_bar": 24.2},
                {"name": "exp_out", "t_c": round(t_evap, 1), "p_bar": 9.3},
            ],
        }

    def step(self, dt: float = 1.0, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        safe_dt = max(0.0, float(dt))
        self.state["step"] = int(self.state.get("step", 0)) + 1
        self.state["sim_time_s"] = round(float(self.state.get("sim_time_s", 0.0)) + safe_dt, 2)
        self.state["running"] = True
        if payload:
            self.update_parameters(payload)
        else:
            self._recompute_cycle()
        return dict(self.state)

    def step_simulation(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.step(dt=1.0, payload=payload)

    def update_parameters(self, updates: dict[str, Any]) -> dict[str, Any]:
        if updates:
            self.state["inputs"].update(updates)
            self.state["last_input"] = dict(updates)
        self._recompute_cycle()
        return dict(self.state)

    def get_status(self) -> dict[str, Any]:
        return dict(self.state)


simulation_engine = SimulationEngine()