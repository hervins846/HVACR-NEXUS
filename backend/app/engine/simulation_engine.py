from __future__ import annotations

from typing import Any


class SimulationEngine:
    """Moteur de simulation thermodynamique et de charges HVACR."""

    def __init__(self) -> None:
        self.state: dict[str, Any] = {
            "running": False,
            "step": 0,
        }

    def step_simulation(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        self.state["step"] = int(self.state.get("step", 0)) + 1
        self.state["running"] = True
        if payload:
            self.state["last_input"] = payload
        return dict(self.state)

    def get_status(self) -> dict[str, Any]:
        return dict(self.state)


simulation_engine = SimulationEngine()
