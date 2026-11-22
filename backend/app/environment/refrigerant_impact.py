from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RefrigerantImpactProfile:
    fluid: str
    gwp_100yr: float
    odp: float
    safety_class: str
    charge_kg: float
    annual_leak_rate: float  # ex. 0.05 pour 5 % / an

    @property
    def annual_leak_kg(self) -> float:
        return round(max(0.0, self.charge_kg) * max(0.0, self.annual_leak_rate), 4)

    @property
    def annual_direct_co2e_kg(self) -> float:
        return round(self.annual_leak_kg * self.gwp_100yr, 2)


DEFAULT_REFRIGERANT_IMPACTS: dict[str, dict[str, float | str]] = {
    "R134a": {"gwp_100yr": 1430.0, "odp": 0.0, "safety_class": "A1"},
    "R410A": {"gwp_100yr": 2088.0, "odp": 0.0, "safety_class": "A1"},
    "R32": {"gwp_100yr": 675.0, "odp": 0.0, "safety_class": "A2L"},
    "R290": {"gwp_100yr": 3.0, "odp": 0.0, "safety_class": "A3"},
    "R744": {"gwp_100yr": 1.0, "odp": 0.0, "safety_class": "A1"},
}


def get_refrigerant_impact(
    fluid: str,
    charge_kg: float = 10.0,
    annual_leak_rate: float = 0.05,
) -> RefrigerantImpactProfile:
    key = fluid.strip()
    meta = DEFAULT_REFRIGERANT_IMPACTS.get(
        key, {"gwp_100yr": 1000.0, "odp": 0.0, "safety_class": "A1"}
    )
    return RefrigerantImpactProfile(
        fluid=key,
        gwp_100yr=float(meta["gwp_100yr"]),
        odp=float(meta["odp"]),
        safety_class=str(meta["safety_class"]),
        charge_kg=charge_kg,
        annual_leak_rate=annual_leak_rate,
    )