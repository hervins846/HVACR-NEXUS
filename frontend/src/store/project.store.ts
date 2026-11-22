export interface ProjectConfig {
  projectName: string;
  siteName: string;
  fluid: string;
  ambientTempC: number;
  lifetimeYears: number;
  annualOperatingHours: number;
  tariffPerKwh: number;
  currency: string;
}

export interface ProjectStoreState {
  activeTab: "cycle" | "equipment" | "dynamics" | "energy" | "diagnostics";
  config: ProjectConfig;
  lastSavedAt: string | null;
}

export function createInitialProjectState(): ProjectStoreState {
  return {
    activeTab: "cycle",
    config: {
      projectName: "HVACR NEXUS — Digital Twin Lab",
      siteName: "Unite Pilote Industrielle",
      fluid: "R134a",
      ambientTempC: 32.0,
      lifetimeYears: 15,
      annualOperatingHours: 4000,
      tariffPerKwh: 0.15,
      currency: "USD",
    },
    lastSavedAt: null,
  };
}

export function setActiveProjectTab(
  state: ProjectStoreState,
  activeTab: ProjectStoreState["activeTab"]
): ProjectStoreState {
  return { ...state, activeTab };
}

export function updateProjectConfig(
  state: ProjectStoreState,
  updates: Partial<ProjectConfig>
): ProjectStoreState {
  return {
    ...state,
    config: { ...state.config, ...updates },
    lastSavedAt: new Date().toISOString(),
  };
}