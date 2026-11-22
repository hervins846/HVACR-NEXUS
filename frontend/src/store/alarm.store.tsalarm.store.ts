export type AlarmSeverity = "INFO" | "WARNING" | "CRITICAL";

export interface SystemAlarm {
  id: string;
  code: string;
  severity: AlarmSeverity;
  message: string;
  timestamp: string;
  acknowledged: boolean;
}

export interface AlarmStoreState {
  alarms: SystemAlarm[];
  unreadCount: number;
}

const ALARM_MESSAGES: Record<string, { severity: AlarmSeverity; message: string }> = {
  HIGH_CONDENSING_PRESSURE: {
    severity: "WARNING",
    message: "Pression de condensation elevee (> 16 bar) : verifier l'echangeur condenseur.",
  },
  HIGH_DISCHARGE_TEMPERATURE: {
    severity: "CRITICAL",
    message: "Temperature de refoulement critique (> 110 C) : risque d'usure compresseur.",
  },
  LOW_COP_EFFICIENCY: {
    severity: "WARNING",
    message: "COP frigorifique faible (< 2.2) : verifier les consignes et l'encrassement.",
  },
  LOW_SUPERHEAT_LIQUID_SLUG_RISK: {
    severity: "CRITICAL",
    message: "Surchauffe trop basse (< 2.0 K) : risque de retour de liquide au compresseur.",
  },
};

export function createInitialAlarmState(): AlarmStoreState {
  return {
    alarms: [],
    unreadCount: 0,
  };
}

export function syncAlarmsFromCodes(
  state: AlarmStoreState,
  alarmCodes: string[],
  simTimeS: number
): AlarmStoreState {
  const nowLabel = `t=${simTimeS.toFixed(1)}s`;
  const existingCodes = new Set(state.alarms.map((a) => a.code));
  const nextAlarms = [...state.alarms];

  for (const code of alarmCodes) {
    if (!existingCodes.has(code)) {
      const meta = ALARM_MESSAGES[code] ?? {
        severity: "WARNING" as AlarmSeverity,
        message: `Alarme systeme detectee : ${code}`,
      };
      nextAlarms.unshift({
        id: `${code}-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
        code,
        severity: meta.severity,
        message: meta.message,
        timestamp: nowLabel,
        acknowledged: false,
      });
    }
  }

  return {
    alarms: nextAlarms.slice(0, 100),
    unreadCount: nextAlarms.filter((a) => !a.acknowledged).length,
  };
}

export function acknowledgeAlarm(state: AlarmStoreState, alarmId: string): AlarmStoreState {
  const updated = state.alarms.map((item) =>
    item.id === alarmId ? { ...item, acknowledged: true } : item
  );
  return {
    alarms: updated,
    unreadCount: updated.filter((a) => !a.acknowledged).length,
  };
}

export function clearAllAlarms(): AlarmStoreState {
  return createInitialAlarmState();
}