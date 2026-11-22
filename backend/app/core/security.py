from __future__ import annotations

import os
from fastapi import Header, HTTPException, status


def get_api_key_required() -> str | None:
    """Retourne une cle API optionnelle si HVACR_API_KEY est definie dans l'environnement."""
    key = os.getenv("HVACR_API_KEY", "").strip()
    return key if key else None


async def verify_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    """Verifie la cle API uniquement lorsqu'une cle est configuree sur le serveur."""
    expected_key = get_api_key_required()
    if not expected_key:
        return
    if not x_api_key or x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cle API invalide ou manquante (en-tete X-API-Key).",
        )