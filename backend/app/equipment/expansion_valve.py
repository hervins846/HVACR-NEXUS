from __future__ import annotations

from dataclasses import dataclass
from CoolProp.CoolProp import PropsSI
from app.equipment.base_equipment import BaseEquipment


@dataclass
class ExpansionValveEquipment(BaseEquipment):
    valve_type: str = "TEV"  # "TEV", "EEV", "CAPILLARY"
    opening_pct: float = 65.0  # 0.0 a 100.0 %
    target_superheat_k: float = 5.0
    category: str = "EXPANSION_VALVE"

    def evaluate(
        self,
        fluid: str,
        p_cond_pa: float,
        p_evap_pa: float,
        h_in_j_kg: float,
    ) -> dict:
        self.clear_alarms()
        # Detente isenthalpique ideale : h_out = h_in
        h_out_j_kg = h_in_j_kg
        t_out_c = float(PropsSI("T", "P", p_evap_pa, "H", h_out_j_kg, fluid)) - 273.15
        vapor_quality = float(PropsSI("Q", "P", p_evap_pa, "H", h_out_j_kg, fluid))

        if self.opening_pct <= 10.0:
            self.add_alarm("VALVE_NEAR_CLOSED_STARVATION")
        elif self.opening_pct >= 98.0:
            self.add_alarm("VALVE_FULLY_OPEN_FLOODING_RISK")

        return {
            "equipment_id": self.equipment_id,
            "name": self.name,
            "valve_type": self.valve_type,
            "opening_pct": round(max(0.0, min(100.0, self.opening_pct)), 1),
            "target_superheat_k": round(self.target_superheat_k, 2),
            "p_in_bar": round(p_cond_pa / 1e5, 3),
            "p_out_bar": round(p_evap_pa / 1e5, 3),
            "h_in_kj_kg": round(h_in_j_kg / 1000.0, 2),
            "h_out_kj_kg": round(h_out_j_kg / 1000.0, 2),
            "outlet_temp_c": round(t_out_c, 2),
            "vapor_quality": round(max(0.0, min(1.0, vapor_quality)), 3),
            "alarms": list(self.alarms),
        }