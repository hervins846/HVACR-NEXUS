from __future__ import annotations

import logging
import sys


def setup_logging(level_name: str = "INFO") -> logging.Logger:
    """Configure un logger unifie pour l'API FastAPI et le moteur de simulation."""
    level = getattr(logging, level_name.upper(), logging.INFO)
    logger = logging.getLogger("hvacr_nexus")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s.%(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger


logger = setup_logging()