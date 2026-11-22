from __future__ import annotations


def physical_to_current_ma(
    value: float,
    range_min: float,
    range_max: float,
    clamp: bool = True,
) -> float:
    """Convertit une grandeur physique vers une boucle de courant 4-20 mA."""
    if range_max <= range_min:
        raise ValueError("range_max doit etre strictement superieur a range_min.")
    ratio = (value - range_min) / (range_max - range_min)
    if clamp:
        ratio = max(0.0, min(1.0, ratio))
    current_ma = 4.0 + ratio * 16.0
    return round(current_ma, 3)


def current_ma_to_physical(
    current_ma: float,
    range_min: float,
    range_max: float,
    clamp: bool = True,
) -> float:
    """Convertit un signal 4-20 mA vers sa grandeur physique correspondante."""
    if range_max <= range_min:
        raise ValueError("range_max doit etre strictement superieur a range_min.")
    ratio = (current_ma - 4.0) / 16.0
    if clamp:
        ratio = max(0.0, min(1.0, ratio))
    physical_value = range_min + ratio * (range_max - range_min)
    return round(physical_value, 4)


def detect_loop_fault(current_ma: float) -> str | None:
    """Detecte un defaut classique de boucle 4-20 mA (fil coupe ou court-circuit)."""
    if current_ma < 3.6:
        return "OPEN_LOOP_OR_WIRE_BREAK"
    if current_ma > 21.0:
        return "OVER_RANGE_OR_SHORT_CIRCUIT"
    return None