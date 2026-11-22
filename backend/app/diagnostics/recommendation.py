from __future__ import annotations

from typing import Any


def build_recommendations(context: dict[str, Any] | list[Any] | None = None) -> list[dict[str, Any]]:
    """Genere des recommandations de maintenance et d'optimisation HVACR."""
    items = context if isinstance(context, list) else []
    if items:
        return [
            {
                "id": f"rec-{idx + 1}",
                "priority": "medium",
                "action": "Verifier la surchauffe, le sous-refroidissement et les echanges thermiques",
                "detail": entry,
            }
            for idx, entry in enumerate(items)
        ]

    return [
        {
            "id": "rec-1",
            "priority": "normal",
            "action": "Surveiller le COP, les temperatures condenseur/evaporateur et la charge frigorifique",
            "detail": context or {},
        }
    ]