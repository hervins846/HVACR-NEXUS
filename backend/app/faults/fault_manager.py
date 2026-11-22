from __future__ import annotations

from dataclasses import dataclass, field
from app.faults.compressor_fault import CompressorFault
from app.faults.condenser_fouling import CondenserFoulingFault
from app.faults.evaporator_frost import EvaporatorFrostFault
from app.faults.leak import RefrigerantLeakFault
from app.faults.valve_fault import ExpansionValveFault


@dataclass
class FaultManager:
    compressor_fault: CompressorFault = field(default_factory=CompressorFault)
    condenser_fouling: CondenserFoulingFault = field(default_factory=CondenserFoulingFault)
    evaporator_frost: EvaporatorFrostFault = field(default_factory=EvaporatorFrostFault)
    refrigerant_leak: RefrigerantLeakFault = field(default_factory=RefrigerantLeakFault)
    valve_fault: ExpansionValveFault = field(default_factory=ExpansionValveFault)

    def apply_all(self, base_inputs: dict) -> dict:
        """Applique sequentiellement tous les defauts actifs aux parametres d'entree."""
        current = dict(base_inputs)
        current = self.compressor_fault.apply(current)
        current = self.condenser_fouling.apply(current)
        current = self.evaporator_frost.apply(current)
        current = self.refrigerant_leak.apply(current)
        current = self.valve_fault.apply(current)
        return current

    def active_faults(self) -> list[str]:
        active: list[str] = []
        if self.compressor_fault.active and self.compressor_fault.severity > 0:
            active.append("COMPRESSOR_FAULT")
        if self.condenser_fouling.active and self.condenser_fouling.fouling_factor > 0:
            active.append("CONDENSER_FOULING")
        if self.evaporator_frost.active and self.evaporator_frost.frost_level > 0:
            active.append("EVAPORATOR_FROST")
        if self.refrigerant_leak.active and self.refrigerant_leak.charge_loss_ratio > 0:
            active.append("REFRIGERANT_LEAK")
        if self.valve_fault.active and self.valve_fault.severity > 0:
            active.append(f"VALVE_{self.valve_fault.mode}")
        return active

    def clear_all(self) -> None:
        self.compressor_fault.active = False
        self.condenser_fouling.active = False
        self.evaporator_frost.active = False
        self.refrigerant_leak.active = False
        self.valve_fault.active = False