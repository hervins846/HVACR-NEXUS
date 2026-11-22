from __future__ import annotations

from dataclasses import dataclass, field
import os


@dataclass
class Settings:
    app_name: str = "HVACR NEXUS"
    app_version: str = "1.0.0"
    environment: str = field(default_factory=lambda: os.getenv("HVACR_ENV", "development"))
    debug: bool = field(default_factory=lambda: os.getenv("HVACR_DEBUG", "true").lower() == "true")
    host: str = field(default_factory=lambda: os.getenv("HVACR_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("HVACR_PORT", "8000")))
    default_fluid: str = field(default_factory=lambda: os.getenv("HVACR_DEFAULT_FLUID", "R134a"))
    default_ambient_temp_c: float = field(default_factory=lambda: float(os.getenv("HVACR_AMBIENT_TEMP_C", "32.0")))
    grid_emission_factor_kg_per_kwh: float = field(
        default_factory=lambda: float(os.getenv("HVACR_GRID_EMISSION_FACTOR", "0.45"))
    )
    cors_origins: list[str] = field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv(
                "HVACR_CORS_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
            ).split(",")
            if origin.strip()
        ]
    )


settings = Settings()