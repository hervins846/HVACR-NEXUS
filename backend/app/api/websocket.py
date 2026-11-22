from __future__ import annotations

import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.logging import logger
from app.engine.simulation_engine import simulation_engine

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("Client WebSocket connecte (%d actif(s)).", len(self.active_connections))

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info("Client WebSocket deconnecte (%d actif(s)).", len(self.active_connections))

    async def broadcast_json(self, payload: dict) -> None:
        stale: list[WebSocket] = []
        for connection in list(self.active_connections):
            try:
                await connection.send_json(payload)
            except Exception:
                stale.append(connection)
        for ws in stale:
            self.disconnect(ws)


manager = ConnectionManager()


@router.websocket("/ws/simulation")
async def simulation_websocket(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            snapshot = simulation_engine.step(dt=1.0)
            await websocket.send_json({
                "type": "simulation_snapshot",
                "data": snapshot,
            })
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as exc:
        logger.warning("Erreur sur le flux WebSocket : %s", exc)
        manager.disconnect(websocket)