from __future__ import annotations

from datetime import datetime, timezone
import json
from app.database.connection import get_db_connection


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS simulation_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    sim_time_s REAL NOT NULL,
    fluid TEXT NOT NULL,
    t_evap_c REAL NOT NULL,
    t_cond_c REAL NOT NULL,
    cop REAL NOT NULL,
    q_evap_kw REAL NOT NULL,
    w_comp_kw REAL NOT NULL,
    health_score REAL NOT NULL DEFAULT 100.0,
    alarms_json TEXT NOT NULL DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS maintenance_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    equipment_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    downtime_hours REAL NOT NULL DEFAULT 0.0,
    notes TEXT NOT NULL DEFAULT ''
);
"""


def init_database() -> None:
    with get_db_connection() as conn:
        conn.executescript(SCHEMA_SQL)


def save_simulation_snapshot(
    sim_time_s: float,
    fluid: str,
    t_evap_c: float,
    t_cond_c: float,
    cop: float,
    q_evap_kw: float,
    w_comp_kw: float,
    health_score: float = 100.0,
    alarms: list[str] | None = None,
) -> int:
    now_iso = datetime.now(timezone.utc).isoformat()
    payload = json.dumps(alarms or [])
    with get_db_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO simulation_snapshots (
                created_at, sim_time_s, fluid, t_evap_c, t_cond_c,
                cop, q_evap_kw, w_comp_kw, health_score, alarms_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                now_iso,
                sim_time_s,
                fluid,
                t_evap_c,
                t_cond_c,
                cop,
                q_evap_kw,
                w_comp_kw,
                health_score,
                payload,
            ),
        )
        return int(cursor.lastrowid)