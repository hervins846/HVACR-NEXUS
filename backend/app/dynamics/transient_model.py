from __future__ import annotations

from dataclasses import dataclass, field
from app.dynamics.heat_transfer import HeatExchangerDynamics
from app.dynamics.mass_flow import MassFlowDynamics
from app.dynamics.system_response import SystemDynamicState
from app.dynamics.thermal_inertia import ThermalMass, step_temperature_first_order, time_constant_seconds


@dataclass
class TransientModel:
    state: SystemDynamicState = field(default_factory=SystemDynamicState)
    mass_flow_dyn: MassFlowDynamics = field(default_factory=MassFlowDynamics)
    condenser_hx: HeatExchangerDynamics = field(default_factory=lambda: HeatExchangerDynamics(ua_w_per_k=1800.0))
    evaporator_hx: HeatExchangerDynamics = field(default_factory=lambda: HeatExchangerDynamics(ua_w_per_k=1400.0))
    chamber_thermal_mass: ThermalMass = field(default_factory=lambda: ThermalMass(mass_kg=450.0, specific_heat_j_kg_k=1005.0))
    evap_tau_s: float = 15.0
    cond_tau_s: float = 20.0

    def step(
        self,
        dt_seconds: float,
        target_t_evap_c: float,
        target_t_cond_c: float,
        target_mass_flow_kg_s: float,
        cooling_capacity_kw: float,
        ambient_temp_c: float = 32.0,
        heat_load_kw: float = 10.0,
        compressor_speed_ratio: float = 1.0,
        valve_opening_pct: float = 65.0,
    ) -> dict:
        m_dot = self.mass_flow_dyn.step(
            target_mass_flow_kg_s=target_mass_flow_kg_s,
            dt_seconds=dt_seconds,
            compressor_speed_ratio=compressor_speed_ratio,
            valve_opening_pct=valve_opening_pct,
        )

        self.state.t_evap_c = step_temperature_first_order(
            current_temp_c=self.state.t_evap_c,
            target_temp_c=target_t_evap_c,
            dt_seconds=dt_seconds,
            tau_seconds=self.evap_tau_s,
        )
        self.state.t_cond_c = step_temperature_first_order(
            current_temp_c=self.state.t_cond_c,
            target_temp_c=target_t_cond_c,
            dt_seconds=dt_seconds,
            tau_seconds=self.cond_tau_s,
        )

        chamber_tau_s = time_constant_seconds(
            capacitance_j_k=self.chamber_thermal_mass.capacitance_j_k,
            heat_transfer_ua_w_k=self.evaporator_hx.effective_ua_w_per_k,
        )
        net_load_delta_k = (heat_load_kw - cooling_capacity_kw) * 1000.0 / max(
            1.0, self.evaporator_hx.effective_ua_w_per_k
        )
        target_chamber_c = max(self.state.t_evap_c + 2.0, ambient_temp_c + net_load_delta_k)
        self.state.chamber_temp_c = step_temperature_first_order(
            current_temp_c=self.state.chamber_temp_c,
            target_temp_c=target_chamber_c,
            dt_seconds=dt_seconds,
            tau_seconds=chamber_tau_s,
        )
        self.state.mass_flow_kg_s = m_dot

        stabilized = self.state.evaluate_stability(
            target_t_evap_c=target_t_evap_c,
            target_t_cond_c=target_t_cond_c,
            target_chamber_temp_c=target_chamber_c,
            target_mass_flow_kg_s=target_mass_flow_kg_s,
        )

        return {
            "t_evap_c": self.state.t_evap_c,
            "t_cond_c": self.state.t_cond_c,
            "chamber_temp_c": self.state.chamber_temp_c,
            "mass_flow_kg_s": self.state.mass_flow_kg_s,
            "stabilized": stabilized,
        }