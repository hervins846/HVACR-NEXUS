from copy import deepcopy


class StateManager:
    def __init__(self) -> None:
        self._state: dict = {
            "time_s": 0.0,
            "inputs": {
                "fluid": "R134a",
                "t_evap_c": 5.0,
                "t_cond_c": 40.0,
                "superheat_k": 5.0,
                "subcooling_k": 4.0,
                "eta_isentropic": 0.78,
                "mass_flow_kg_s": 0.05,
            },
            "cycle": {},
            "alarms": [],
        }

    def get_state(self) -> dict:
        return deepcopy(self._state)

    def update_inputs(self, updates: dict) -> dict:
        for key, value in updates.items():
            if value is not None and key in self._state["inputs"]:
                self._state["inputs"][key] = value
        return deepcopy(self._state["inputs"])

    def set_cycle_result(self, cycle_data: dict, time_s: float, alarms: list[str]) -> dict:
        self._state["cycle"] = cycle_data
        self._state["time_s"] = round(time_s, 2)
        self._state["alarms"] = alarms
        return self.get_state()
    