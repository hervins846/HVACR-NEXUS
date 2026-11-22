from __future__ import annotations

from dataclasses import dataclass
from CoolProp.CoolProp import PropsSI
from app.equipment.base_equipment import BaseEquipment


@dataclass
class EvaporatorEquipment(BaseEquipment):
    evaporator_type: str = "DIRECT_EXPANSION"  # "DIRECT_EXPANSION", "CHILLER_SHELL_TUBE", "AIR_COIL"
    t_evap_c: float = 5.0
    superheat_k: float = 5.0
    category: str = "EVAPORATOR"

    def evaluate(
        self,
        fluid: str,
        h_in_j_kg: float,
        mass_flow_kg_s: float,
    ) -> dict:
        self.clear_alarms()
        t_evap_k = self.t_evap_c + 273.15
        p_evap_pa = float(PropsSI("P", "T", t_evap_k, "Q", 1.0, fluid))

        t_out_k = t_evap_k + max(0.0, self.superheat_k)
        h_out_j_kg = float(PropsSI("H", "P", p_evap_pa, "T", t_out_k, fluid))

        q_evap_kw = max(0.0, mass_flow_kg_s) * (h_out_j_kg - h_in_j_kg) / 1000.0

        if self.superheat_k < 2.0:
            self.add_alarm("LOW_SUPERHEAT_LIQUID_SLUG_RISK")
        elif self.superheat_k > 12.0:
            self.add_alarm("HIGH_SUPERHEAT_STARVATION")

        if self.t_evap_c < -15.0:
            self.add_alarm("LOW_EVAPORATING_TEMP_FROST_RISK")

        return {
            "equipment_id": self.equipment_id,
            "name": self.name,
            "evaporator_type": self.evaporator_type,
            "running": self.running,
            "t_evap_c": round(self.t_evap_c, 2),
            "p_evap_bar": round(p_evap_pa / 1e5, 3),
            "p_evap_pa": round(p_evap_pa, 1),
            "outlet_temp_c": round(t_out_k - 273.15, 2),
            "superheat_k": round(self.superheat_k, 2),
            "h_in_kj_kg": round(h_in_j_kg / 1000.0, 2),
            "h_out_kj_kg": round(h_out_j_kg / 1000.0, 2),
            "cooling_capacity_kw": round(q_evap_kw, 3),
            "alarms": list(self.alarms),
        }