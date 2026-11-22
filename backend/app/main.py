from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.simulation import router as simulation_router
from app.api.websocket import router as websocket_router
from app.core.logging import logger

app = FastAPI(
    title="HVACR NEXUS API",
    description="Digital Twin Engineering Lab — Thermodynamic Simulation, Controls & Diagnostics",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation_router)
app.include_router(websocket_router)


@app.get("/")
def root() -> dict:
    logger.info("Verification de l'etat de l'API HVACR NEXUS")
    return {"status": "ok", "service": "HVACR NEXUS"}