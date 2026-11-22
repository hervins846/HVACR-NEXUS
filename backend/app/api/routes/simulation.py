from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.diagnostics.diagnosis import SystemDiagnostician
from app.engine.simulation_engine import simulation_engine

router = APIRouter(prefix="/simulation", tags=["simulation"])
diagnostician = SystemDiagnostician()


class SimulationParametersUpdate(BaseModel):
    fluid: str | None = None
    t_evap_c: float | None = Field(default=None, ge=-60.0, le=35.0)
    t_cond_c: float | None = Field(default=None, ge=10.0, le=90.0)
    superheat_k: float | None = Field(default=None, ge=0.0, le=40.0)
    subcooling_k: float | None = Field(default=None, ge=0.0, le=30.0)
    eta_isentropic: float | None = Field(default=None, ge=0.2, le=0.98)
    mass_flow_kg_s: float | None = Field(default=None, ge=0.001, le=50.0)


@router.get("/state")
def get_simulation_state() -> dict:
    return simulation_engine.state_manager.get_state()


@router.post("/step")
def step_simulation(dt: float = 1.0) -> dict:
    return simulation_engine.step(dt=max(0.0, dt))


@router.patch("/parameters")
def update_simulation_parameters(payload: SimulationParametersUpdate) -> dict:
    updates = payload.model_dump(exclude_none=True)
    return simulation_engine.update_parameters(updates)


@router.get("/diagnosis")
def get_system_diagnosis() -> dict:
    state = simulation_engine.state_manager.get_state()
    cycle = state.get("cycle", {})
    inputs = state.get("inputs", {})
    perf = cycle.get("performance", {})
    points = cycle.get("points", [])

    telemetry = {
        "discharge_temp_c": points[1]["t_c"] if len(points) > 1 else 65.0,
        "t_cond_c": inputs.get("t_cond_c", 40.0),
        "ambient_temp_c": 32.0,
        "t_evap_c": inputs.get("t_evap_c", 5.0),
        "superheat_k": inputs.get("superheat_k", 5.0),
        "subcooling_k": inputs.get("subcooling_k", 4.0),
        "cop": perf.get("cop", 3.5),
    }
    report = diagnostician.diagnose(telemetry)
    return {
        "health_score": report.health_score,
        "overall_status": report.overall_status,
        "triggered_rules": report.triggered_rules,
        "classified_faults": report.classified_faults,
        "recommendations": report.recommendations,
    }