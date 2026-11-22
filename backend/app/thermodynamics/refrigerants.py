SUPPORTED_REFRIGERANTS = {
    "R134a": {"name": "R134a", "gwp": 1430, "safety": "A1"},
    "R410A": {"name": "R410A", "gwp": 2088, "safety": "A1"},
    "R32": {"name": "R32", "gwp": 675, "safety": "A2L"},
    "R290": {"name": "R290 (Propane)", "gwp": 3, "safety": "A3"},
    "R744": {"name": "R744 (CO2)", "gwp": 1, "safety": "A1"},
}


def get_refrigerant_info(fluid: str) -> dict:
    key = fluid.strip()
    if key not in SUPPORTED_REFRIGERANTS:
        raise ValueError(f"Fluide frigorigene non supporte : {fluid}")
    return SUPPORTED_REFRIGERANTS[key]