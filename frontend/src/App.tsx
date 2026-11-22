import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000";

type CyclePoint = {
  name: string;
  t_c: number;
  p_bar: number;
};

type SimulationState = {
  running?: boolean;
  step?: number;
  sim_time_s?: number;
  inputs?: {
    fluid?: string;
    t_evap_c?: number;
    t_cond_c?: number;
    superheat_k?: number;
    subcooling_k?: number;
    eta_isentropic?: number;
    mass_flow_kg_s?: number;
  };
  cycle?: {
    performance?: {
      cop?: number;
      cooling_capacity_kw?: number;
      compressor_power_kw?: number;
    };
    points?: CyclePoint[];
  };
  last_input?: Record<string, unknown>;
};

type DiagnosisPayload = {
  health_score?: number;
  overall_status?: string;
  triggered_rules?: Array<Record<string, unknown>>;
  classified_faults?: Array<Record<string, unknown>>;
  recommendations?: Array<Record<string, unknown>>;
};

type ScenarioPreset = {
  id: string;
  label: string;
  params: Record<string, number>;
};

const SCENARIOS: ScenarioPreset[] = [
  {
    id: "nominal",
    label: "Nominal (R410A)",
    params: { t_evap_c: 5.0, t_cond_c: 40.0, superheat_k: 5.0, subcooling_k: 4.0 },
  },
  {
    id: "high_cond",
    label: "Encrassement Condenseur (75 C)",
    params: { t_cond_c: 75.0, superheat_k: 5.0, subcooling_k: 4.0 },
  },
  {
    id: "low_sh",
    label: "Coup de Liquide (SH 1.2 K)",
    params: { t_cond_c: 40.0, superheat_k: 1.2, subcooling_k: 4.0 },
  },
  {
    id: "leak",
    label: "Fuite Fluide (SH 12 K / SC 1 K)",
    params: { t_cond_c: 40.0, superheat_k: 12.0, subcooling_k: 1.0 },
  },
];

export default function App() {
  const [backendOk, setBackendOk] = useState<string>("Verification...");
  const [banner, setBanner] = useState<string>("Pret.");
  const [dt, setDt] = useState<string>("1.0");
  const [paramName, setParamName] = useState<string>("t_cond_c");
  const [paramValue, setParamValue] = useState<string>("42.0");
  const [selectedScenario, setSelectedScenario] = useState<string>("nominal");
  const [stateData, setStateData] = useState<SimulationState | null>(null);
  const [diagData, setDiagData] = useState<DiagnosisPayload | null>(null);

  async function syncAll(message = "Etat et diagnostic synchronises avec le backend.") {
    try {
      const [rootRes, stateRes, diagRes] = await Promise.all([
        fetch(`${API_BASE}/`),
        fetch(`${API_BASE}/simulation/state`),
        fetch(`${API_BASE}/simulation/diagnosis`),
      ]);
      if (rootRes.ok) {
        const rootJson = await rootRes.json();
        setBackendOk(`${rootJson.service ?? "HVACR NEXUS"} : ${rootJson.status ?? "ok"}`);
      } else {
        setBackendOk(`Erreur HTTP ${rootRes.status}`);
      }
      if (stateRes.ok) {
        setStateData(await stateRes.json());
      }
      if (diagRes.ok) {
        setDiagData(await diagRes.json());
      }
      setBanner(message);
    } catch (err) {
      setBackendOk("Hors ligne");
      setBanner(`Erreur de synchronisation : ${String(err)}`);
    }
  }

  async function handleStep() {
    const parsedDt = Number(dt);
    const safeDt = Number.isFinite(parsedDt) && parsedDt >= 0 ? parsedDt : 1.0;
    await fetch(`${API_BASE}/simulation/step?dt=${encodeURIComponent(String(safeDt))}`, {
      method: "POST",
    });
    await syncAll(`Pas de simulation execute (dt = ${safeDt} s).`);
  }

  async function handlePatchSingle() {
    const numVal = Number(paramValue);
    if (!paramName.trim() || !Number.isFinite(numVal)) return;
    await fetch(`${API_BASE}/simulation/parameters`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ [paramName.trim()]: numVal }),
    });
    await syncAll(`Parametre ${paramName.trim()} mis a jour (${numVal}).`);
  }

  async function handleApplyScenario(scenarioId: string) {
    setSelectedScenario(scenarioId);
    const preset = SCENARIOS.find((s) => s.id === scenarioId);
    if (!preset) return;
    await fetch(`${API_BASE}/simulation/parameters`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(preset.params),
    });
    await syncAll(`Scenario applique : ${preset.label}.`);
  }

  useEffect(() => {
    syncAll();
  }, []);

  const perf = stateData?.cycle?.performance;
  const points = stateData?.cycle?.points ?? [];
  const status = diagData?.overall_status ?? "INCONNU";
  const score = diagData?.health_score ?? "--";

  return (
    <div style={{ minHeight: "100vh", background: "#03131b", color: "#e6f7ff", padding: "24px", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ maxWidth: "1360px", margin: "0 auto" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "12px", marginBottom: "16px" }}>
          <div>
            <h1 style={{ margin: 0, fontSize: "32px", color: "#28ebff" }}>HVACR NEXUS</h1>
            <div style={{ color: "#9ec2d4", fontSize: "14px" }}>
              Digital Twin Lab — Frontend http://localhost:5173/ &lt;-&gt; API http://localhost:8000
            </div>
          </div>
          <div style={{ background: "#083c47", color: "#4ce89b", padding: "10px 16px", borderRadius: "8px", fontWeight: 700 }}>
            Backend : {backendOk}
          </div>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "10px", alignItems: "center", marginBottom: "14px" }}>
          <button onClick={() => syncAll()} style={{ background: "#0b6e7a", color: "#fff", border: "none", padding: "10px 14px", borderRadius: "6px", cursor: "pointer", fontWeight: 600 }}>
            Actualiser State &amp; Diagnosis
          </button>

          <label style={{ fontSize: "13px", color: "#9ec2d4" }}>dt:</label>
          <input
            value={dt}
            onChange={(e) => setDt(e.target.value)}
            style={{ width: "68px", padding: "9px", borderRadius: "6px", border: "1px solid #1b4b5c", background: "#07222e", color: "#fff" }}
          />
          <button onClick={handleStep} style={{ background: "#14b8e6", color: "#03131b", border: "none", padding: "10px 14px", borderRadius: "6px", cursor: "pointer", fontWeight: 700 }}>
            Executer 1 Pas (POST /simulation/step)
          </button>

          <input
            value={paramName}
            onChange={(e) => setParamName(e.target.value)}
            style={{ width: "130px", padding: "9px", borderRadius: "6px", border: "1px solid #1b4b5c", background: "#07222e", color: "#fff" }}
          />
          <input
            value={paramValue}
            onChange={(e) => setParamValue(e.target.value)}
            style={{ width: "86px", padding: "9px", borderRadius: "6px", border: "1px solid #1b4b5c", background: "#07222e", color: "#fff" }}
          />
          <button onClick={handlePatchSingle} style={{ background: "#ce701a", color: "#fff", border: "none", padding: "10px 14px", borderRadius: "6px", cursor: "pointer", fontWeight: 700 }}>
            PATCH Parameters
          </button>

          <select
            value={selectedScenario}
            onChange={(e) => handleApplyScenario(e.target.value)}
            style={{ padding: "9px 12px", borderRadius: "6px", border: "1px solid #28ebff", background: "#07222e", color: "#e6f7ff", fontWeight: 600 }}
          >
            {SCENARIOS.map((s) => (
              <option key={s.id} value={s.id}>
                {s.label}
              </option>
            ))}
          </select>
        </div>

        <div style={{ background: "#06212e", border: "1px solid #124859", borderRadius: "8px", padding: "12px 16px", marginBottom: "18px", color: "#bfe8f7" }}>
          {banner}
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "12px", marginBottom: "18px" }}>
          <div style={{ background: "#06212e", border: "1px solid #11606b", borderRadius: "8px", padding: "12px" }}>
            <div style={{ fontSize: "12px", color: "#8cb8c9" }}>COP / Puissances</div>
            <div style={{ fontSize: "20px", fontWeight: 700, color: "#28ebff", marginTop: "4px" }}>
              COP {perf?.cop ?? "--"}
            </div>
            <div style={{ fontSize: "13px", color: "#cce9f4", marginTop: "4px" }}>
              Froid : {perf?.cooling_capacity_kw ?? "--"} kW | Comp : {perf?.compressor_power_kw ?? "--"} kW
            </div>
          </div>

          {points.map((pt) => (
            <div key={pt.name} style={{ background: "#06212e", border: "1px solid #11606b", borderRadius: "8px", padding: "12px" }}>
              <div style={{ fontSize: "12px", color: "#ce701a", fontWeight: 700 }}>{pt.name}</div>
              <div style={{ fontSize: "18px", fontWeight: 700, color: "#e6f7ff", marginTop: "4px" }}>
                {pt.t_c} °C
              </div>
              <div style={{ fontSize: "13px", color: "#9ec2d4", marginTop: "2px" }}>
                {pt.p_bar} bar
              </div>
            </div>
          ))}
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(460px, 1fr))", gap: "18px" }}>
          <div style={{ background: "#06212e", border: "1px solid #11606b", borderRadius: "10px", padding: "16px" }}>
            <h2 style={{ marginTop: 0, color: "#28ebff", fontSize: "18px" }}>GET /simulation/state</h2>
            <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-word", fontSize: "13px", lineHeight: 1.45 }}>
              {JSON.stringify(stateData, null, 2)}
            </pre>
          </div>

          <div style={{ background: "#06212e", border: "1px solid #11606b", borderRadius: "10px", padding: "16px" }}>
            <h2 style={{ marginTop: 0, color: "#ce701a", fontSize: "18px" }}>GET /simulation/diagnosis</h2>
            <div style={{ marginBottom: "10px", fontWeight: 700, color: status === "CRITICAL" ? "#ff6b6b" : status === "DEGRADED" ? "#ffb84d" : "#4ce89b" }}>
              Score : {score} &nbsp; Statut : {status}
            </div>
            <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-word", fontSize: "13px", lineHeight: 1.45 }}>
              {JSON.stringify(diagData, null, 2)}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}