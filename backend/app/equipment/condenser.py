from __future__ import annotations

from dataclasses import dataclass
from CoolProp.CoolProp import PropsSI
from app.equipment.base_equipment import BaseEquipment


@dataclass
class CondenserEquipment(BaseEquipment):
    condenser_type: str = "AIR_COOLED"  # "AIR_COOLED", "WATER_COOLED", "EVAPORATIVE"
    t_cond_c: float = 40.0
    subcooling_k: float = 4.0
    approach_k: float = 6.0
    category: str = "CONDENSER"

    def evaluate(
        self,
        fluid: str,
        h_in_j_kg: float,
        mass_flow_kg_s: float,
        ambient_temp_c: float = 34.0,
    ) -> dict:
        self.clear_alarms()
        effective_t_cond_c = max(self.t_cond_c, ambient_temp_c + self.approach_k)
        t_cond_k = effective_t_cond_c + 273.15
        p_cond_pa = float(PropsSI("P", "T", t_cond_k, "Q", 0.0, fluid))

        t_out_k = max(274.15, t_cond_k - max(0.0, self.subcooling_k))
        h_out_j_kg = float(PropsSI("H", "P", p_cond_pa, "T", t_out_k, fluid))

        q_cond_kw = max(0.0, mass_flow_kg_s) * (h_in_j_kg - h_out_j_kg) / 1000.0

        if effective_t_cond_c > 52.0:
            self.add_alarm("HIGH_CONDENSING_TEMP")
        if self.subcooling_k < 1.5:
            self.add_alarm("LOW_SUBCOOLING_CHARGE_RISK")

        return {
            "equipment_id": self.equipment_id,
            "name": self.name,
            "condenser_type": self.condenser_type,
            "running": self.running,
            "t_cond_c": round(effective_t_cond_c, 2),
            "p_cond_bar": round(p_cond_pa / 1e5, 3),
            "p_cond_pa": round(p_cond_pa, 1),
            "outlet_temp_c": round(t_out_k - 273.15, 2),
            "subcooling_k": round(self.subcooling_k, 2),
            "h_in_kj_kg": round(h_in_j_kg / 1000.0, 2),
            "h_out_kj_kg": round(h_out_j_kg / 1000.0, 2),
            "heat_rejection_kw": round(q_cond_kw, 3),
            "alarms": list(self.alarms),
        }