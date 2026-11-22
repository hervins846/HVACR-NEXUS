export type EquipmentCategory = "COMPRESSOR" | "CONDENSER" | "EVAPORATOR" | "EXPANSION_VALVE" | "PUMP" | "FAN";

export interface EquipmentItem {
  id: string;
  tag: string;
  name: string;
  category: EquipmentCategory;
  running: boolean;
  healthIndex: number;
  operatingHours: number;
  metrics: Record<string, number | string | boolean | null>;
}

export interface EquipmentStoreState {
  items: EquipmentItem[];
  selectedEquipmentId: string | null;
}

export function createInitialEquipmentState(): EquipmentStoreState {
  const items: EquipmentItem[] = [
    {
      id: "comp-01",
      tag: "CP-101",
      name: "Compresseur Principal",
      category: "COMPRESSOR",
      running: true,
      healthIndex: 96.5,
      operatingHours: 1240,
      metrics: { power_kw: 4.2, discharge_temp_c: 74.5, pressure_ratio: 3.4 },
    },
    {
      id: "cond-01",
      tag: "CD-101",
      name: "Condenseur",
      category: "CONDENSER",
      running: true,
      healthIndex: 94.0,
      operatingHours: 1240,
      metrics: { t_cond_c: 40.0, subcooling_k: 4.0, heat_rejection_kw: 18.5 },
    },
    {
      id: "evap-01",
      tag: "EV-101",
      name: "Evaporateur",
      category: "EVAPORATOR",
      running: true,
      healthIndex: 95.2,
      operatingHours: 1240,
      metrics: { t_evap_c: 5.0, superheat_k: 5.0, cooling_capacity_kw: 14.3 },
    },
    {
      id: "txv-01",
      tag: "EEV-101",
      name: "Detendeur Electronique",
      category: "EXPANSION_VALVE",
      running: true,
      healthIndex: 98.0,
      operatingHours: 1240,
      metrics: { opening_pct: 65.0, vapor_quality: 0.24 },
    },
  ];

  return {
    items,
    selectedEquipmentId: items[0]?.id ?? null,
  };
}

export function selectEquipment(state: EquipmentStoreState, equipmentId: string): EquipmentStoreState {
  return {
    ...state,
    selectedEquipmentId: equipmentId,
  };
}

export function updateEquipmentMetrics(
  state: EquipmentStoreState,
  equipmentId: string,
  metrics: Record<string, number | string | boolean | null>,
  healthIndex?: number
): EquipmentStoreState {
  return {
    ...state,
    items: state.items.map((item) =>
      item.id === equipmentId
        ? {
            ...item,
            metrics: { ...item.metrics, ...metrics },
            healthIndex: healthIndex !== undefined ? healthIndex : item.healthIndex,
          }
        : item
    ),
  };
}