from __future__ import annotations

from dataclasses import dataclass
from CoolProp.CoolProp import PropsSI
from app.equipment.base_equipment import BaseEquipment


@dataclass
class CompressorEquipment(BaseEquipment):
    compressor_type: str = "SCROLL"  # "SCROLL", "RECIPROCATING", "SCREW"
    displacement_m3_h: float = 18.0
    volumetric_efficiency: float = 0.85
    isentropic_efficiency: float = 0.78
    motor_efficiency: float = 0.92
    category: str = "COMPRESSOR"

    def evaluate(
        self,
        fluid: str,
        p_evap_pa: float,
        p_cond_pa: float,
        t_suction_c: float,
        mass_flow_kg_s: float | None = None,
    ) -> dict:
        self.clear_alarms()
        if not self.running:
            return {
                "equipment_id": self.equipment_id,
                "name": self.name,
                "running": False,
                "power_kw": 0.0,
                "discharge_temp_c": None,
                "pressure_ratio": 0.0,
                "mass_flow_kg_s": 0.0,
                "alarms": self.alarms,
            }

        t_suc_k = t_suction_c + 273.15
        rho_suc = float(PropsSI("D", "P", p_evap_pa, "T", t_suc_k, fluid))
        h1 = float(PropsSI("H", "P", p_evap_pa, "T", t_suc_k, fluid))
        s1 = float(PropsSI("S", "P", p_evap_pa, "T", t_suc_k, fluid))

        eta_is = max(0.15, min(0.98, self.isentropic_efficiency))
        eta_vol = max(0.20, min(0.99, self.volumetric_efficiency))
        eta_mot = max(0.40, min(0.99, self.motor_efficiency))

        if mass_flow_kg_s is None:
            m_dot = (self.displacement_m3_h / 3600.0) * eta_vol * rho_suc
        else:
            m_dot = max(0.0, mass_flow_kg_s)

        h2s = float(PropsSI("H", "P", p_cond_pa, "S", s1, fluid))
        h2 = h1 + (h2s - h1) / eta_is
        t2_c = float(PropsSI("T", "P", p_cond_pa, "H", h2, fluid)) - 273.15

        shaft_power_kw = (m_dot * (h2 - h1)) / 1000.0
        electrical_power_kw = shaft_power_kw / eta_mot
        pressure_ratio = p_cond_pa / p_evap_pa if p_evap_pa > 0 else 0.0

        if t2_c > 110.0:
            self.add_alarm("HIGH_DISCHARGE_TEMP")
        if pressure_ratio > 6.5:
            self.add_alarm("HIGH_COMPRESSION_RATIO")

        return {
            "equipment_id": self.equipment_id,
            "name": self.name,
            "compressor_type": self.compressor_type,
            "running": True,
            "mass_flow_kg_s": round(m_dot, 5),
            "pressure_ratio": round(pressure_ratio, 2),
            "suction_temp_c": round(t_suction_c, 2),
            "discharge_temp_c": round(t2_c, 2),
            "h_in_kj_kg": round(h1 / 1000.0, 2),
            "h_out_kj_kg": round(h2 / 1000.0, 2),
            "shaft_power_kw": round(shaft_power_kw, 3),
            "power_kw": round(electrical_power_kw, 3),
            "alarms": list(self.alarms),
        }