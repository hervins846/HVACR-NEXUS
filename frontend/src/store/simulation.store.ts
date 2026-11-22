export interface SimulationInputs {
  fluid: string;
  t_evap_c: number;
  t_cond_c: number;
  superheat_k: number;
  subcooling_k: number;
  eta_isentropic: number;
  mass_flow_kg_s: number;
}

export interface CyclePerformance {
  q_evap_kw: number;
  w_comp_kw: number;
  q_cond_kw: number;
  cop: number;
}

export interface SimulationSnapshot {
  time_s: number;
  inputs: SimulationInputs;
  cycle: {
    performance?: CyclePerformance;
    pressures_bar?: { p_evap: number; p_cond: number };
    points?: Array<{ state: number; t_c: number; p_bar: number; h_kj_kg: number; s_kj_kg_k: number }>;
  };
  convergence: {
    converged: boolean;
    iterations: number;
    residual: number;
  };
  alarms: string[];
}

export interface SimulationHistoryPoint {
  time_s: number;
  cop: number;
  q_evap_kw: number;
  w_comp_kw: number;
  t_evap_c: number;
  t_cond_c: number;
}

export interface SimulationStoreState {
  connected: boolean;
  running: boolean;
  snapshot: SimulationSnapshot | null;
  history: SimulationHistoryPoint[];
}

export function createInitialSimulationState(): SimulationStoreState {
  return {
    connected: false,
    running: true,
    snapshot: null,
    history: [],
  };
}

export function applySimulationSnapshot(
  state: SimulationStoreState,
  snapshot: SimulationSnapshot,
  maxHistoryPoints: number = 120
): SimulationStoreState {
  const perf = snapshot.cycle?.performance;
  const nextPoint: SimulationHistoryPoint = {
    time_s: snapshot.time_s,
    cop: perf?.cop ?? 0,
    q_evap_kw: perf?.q_evap_kw ?? 0,
    w_comp_kw: perf?.w_comp_kw ?? 0,
    t_evap_c: snapshot.inputs.t_evap_c,
    t_cond_c: snapshot.inputs.t_cond_c,
  };

  const nextHistory = [...state.history, nextPoint].slice(-maxHistoryPoints);

  return {
    ...state,
    snapshot,
    history: nextHistory,
  };
}