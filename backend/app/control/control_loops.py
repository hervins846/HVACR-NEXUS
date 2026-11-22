from __future__ import annotations

from dataclasses import dataclass, field
from app.control.actuators import ActuatorBank
from app.control.pid_controller import PIDController
from app.control.setpoints import SystemSetpoints


@dataclass
class ControlLoopSystem:
    setpoints: SystemSetpoints = field(default_factory=SystemSetpoints)
    actuators: ActuatorBank = field(default_factory=ActuatorBank)
    capacity_pid: PIDController = field(
        default_factory=lambda: PIDController(
            kp=0.08, ki=0.015, kd=0.01, output_min=0.35, output_max=1.15, reverse_acting=True
        )
    )
    superheat_pid: PIDController = field(
        default_factory=lambda: PIDController(
            kp=3.5, ki=0.6, kd=0.2, output_min=10.0, output_max=95.0, reverse_acting=False
        )
    )
    condenser_pid: PIDController = field(
        default_factory=lambda: PIDController(
            kp=0.06, ki=0.01, kd=0.005, output_min=0.30, output_max=1.20, reverse_acting=True
        )
    )

    def step(
        self,
        chamber_temp_c: float,
        superheat_k: float,
        t_cond_c: float,
        dt_seconds: float = 1.0,
    ) -> dict:
        if not self.setpoints.auto_mode:
            return {
                "auto_mode": False,
                "setpoints": self.setpoints.as_dict(),
                "actuators": self.actuators.apply_commands(),
            }

        comp_speed = self.capacity_pid.step(
            setpoint=self.setpoints.target_chamber_temp_c,
            measurement=chamber_temp_c,
            dt_seconds=dt_seconds,
        )
        valve_pct = self.superheat_pid.step(
            setpoint=self.setpoints.target_superheat_k,
            measurement=superheat_k,
            dt_seconds=dt_seconds,
        )
        fan_speed = self.condenser_pid.step(
            setpoint=self.setpoints.target_t_cond_c,
            measurement=t_cond_c,
            dt_seconds=dt_seconds,
        )

        act_state = self.actuators.apply_commands(
            compressor_speed_ratio=comp_speed,
            valve_opening_pct=valve_pct,
            condenser_fan_speed_ratio=fan_speed,
            compressor_enabled=True,
        )
        return {
            "auto_mode": True,
            "setpoints": self.setpoints.as_dict(),
            "actuators": act_state,
        }