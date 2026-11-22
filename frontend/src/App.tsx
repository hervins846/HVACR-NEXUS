import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000";

type JsonRecord = Record<string, unknown>;

async function parseJsonSafe(res: Response): Promise<unknown> {
  const text = await res.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return { raw: text };
  }
}

export default function App() {
  const [health, setHealth] = useState<string>("Verification en cours...");
  const [simState, setSimState] = useState<unknown>(null);
  const [diagnosis, setDiagnosis] = useState<unknown>(null);
  const [paramKey, setParamKey] = useState<string>("ambient_temp");
  const [paramValue, setParamValue] = useState<string>("32.5");
  const [actionLog, setActionLog] = useState<string>("Pret pour le pilotage HVACR NEXUS.");
  const [busy, setBusy] = useState<boolean>(false);

  async function refreshAll() {
    setBusy(true);
    try {
      const [rootRes, stateRes, diagRes] = await Promise.allSettled([
        fetch(`${API_BASE}/`),
        fetch(`${API_BASE}/simulation/state`),
        fetch(`${API_BASE}/simulation/diagnosis`),
      ]);

      if (rootRes.status === "fulfilled" && rootRes.value.ok) {
        const rootData = (await parseJsonSafe(rootRes.value)) as JsonRecord | null;
        setHealth(`${String(rootData?.service ?? "HVACR NEXUS")} : ${String(rootData?.status ?? "ok")}`);
      } else {
        setHealth("API locale inaccessible sur http://localhost:8000");
      }

      if (stateRes.status === "fulfilled") {
        setSimState(await parseJsonSafe(stateRes.value));
      }

      if (diagRes.status === "fulfilled") {
        setDiagnosis(await parseJsonSafe(diagRes.value));
      }

      setActionLog("Etat et diagnostic synchronises avec le backend.");
    } catch (err) {
      setActionLog(`Erreur de synchronisation : ${String(err)}`);
    } finally {
      setBusy(false);
    }
  }

  async function handleStep() {
    setBusy(true);
    try {
      const res = await fetch(`${API_BASE}/simulation/step`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      const data = await parseJsonSafe(res);
      setSimState(data);
      setActionLog(`POST /simulation/step -> HTTP ${res.status}`);

      const diagRes = await fetch(`${API_BASE}/simulation/diagnosis`);
      if (diagRes.ok) {
        setDiagnosis(await parseJsonSafe(diagRes));
      }
    } catch (err) {
      setActionLog(`Erreur POST /simulation/step : ${String(err)}`);
    } finally {
      setBusy(false);
    }
  }

  async function handlePatchParams(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    const trimmedKey = paramKey.trim();
    const numericVal = Number(paramValue);
    const parsedVal: unknown =
      paramValue.trim() === ""
        ? ""
        : !Number.isNaN(numericVal) && paramValue.trim() !== ""
        ? numericVal
        : paramValue;

    const payload = trimmedKey ? { [trimmedKey]: parsedVal } : {};

    try {
      const res = await fetch(`${API_BASE}/simulation/parameters`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await parseJsonSafe(res);
      setActionLog(`PATCH /simulation/parameters (${JSON.stringify(payload)}) -> HTTP ${res.status}`);
      if (typeof data === "object" && data !== null) {
        setSimState(data);
      }
      await refreshAll();
    } catch (err) {
      setActionLog(`Erreur PATCH /simulation/parameters : ${String(err)}`);
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    refreshAll();
  }, []);

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#06212E",
        color: "#E6F7FF",
        padding: "2rem",
        fontFamily: "system-ui, -apple-system, sans-serif",
      }}
    >
      <header
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "space-between",
          alignItems: "center",
          gap: "1rem",
          borderBottom: "1px solid #11606B",
          paddingBottom: "1rem",
          marginBottom: "1.5rem",
        }}
      >
        <div>
          <h1 style={{ color: "#28EBFF", fontSize: "2rem", margin: 0 }}>HVACR NEXUS</h1>
          <p style={{ margin: "0.35rem 0 0", color: "#9AD8E6" }}>
            Digital Twin Lab — Frontend <strong>http://localhost:5173/</strong> &lt;-&gt; API{" "}
            <strong>http://localhost:8000</strong>
          </p>
        </div>
        <div
          style={{
            backgroundColor: "#11606B",
            padding: "0.55rem 1rem",
            borderRadius: "0.5rem",
            color: "#CE701A",
            fontWeight: 700,
          }}
        >
          Backend : {health}
        </div>
      </header>

      <section
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "0.75rem",
          alignItems: "center",
          marginBottom: "1.5rem",
        }}
      >
        <button
          type="button"
          disabled={busy}
          onClick={refreshAll}
          style={{
            backgroundColor: "#11606B",
            color: "#E6F7FF",
            border: "1px solid #28EBFF",
            padding: "0.6rem 1rem",
            borderRadius: "0.4rem",
            cursor: "pointer",
            fontWeight: 600,
          }}
        >
          Actualiser State &amp; Diagnosis
        </button>

        <button
          type="button"
          disabled={busy}
          onClick={handleStep}
          style={{
            backgroundColor: "#28EBFF",
            color: "#06212E",
            border: "none",
            padding: "0.6rem 1.1rem",
            borderRadius: "0.4rem",
            cursor: "pointer",
            fontWeight: 700,
          }}
        >
          Executer 1 Pas (POST /simulation/step)
        </button>

        <form onSubmit={handlePatchParams} style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          <input
            type="text"
            value={paramKey}
            onChange={(e) => setParamKey(e.target.value)}
            placeholder="Parametre (ex: ambient_temp)"
            style={{
              backgroundColor: "#0A2E3F",
              color: "#E6F7FF",
              border: "1px solid #11606B",
              padding: "0.55rem 0.75rem",
              borderRadius: "0.4rem",
            }}
          />
          <input
            type="text"
            value={paramValue}
            onChange={(e) => setParamValue(e.target.value)}
            placeholder="Valeur (ex: 32.5)"
            style={{
              backgroundColor: "#0A2E3F",
              color: "#E6F7FF",
              border: "1px solid #11606B",
              padding: "0.55rem 0.75rem",
              borderRadius: "0.4rem",
              width: "120px",
            }}
          />
          <button
            type="submit"
            disabled={busy}
            style={{
              backgroundColor: "#CE701A",
              color: "#06212E",
              border: "none",
              padding: "0.6rem 1rem",
              borderRadius: "0.4rem",
              cursor: "pointer",
              fontWeight: 700,
            }}
          >
            PATCH Parameters
          </button>
        </form>
      </section>

      <p
        style={{
          backgroundColor: "#0A2E3F",
          borderLeft: "4px solid #28EBFF",
          padding: "0.65rem 0.9rem",
          borderRadius: "0.25rem",
          marginBottom: "1.5rem",
          fontSize: "0.95rem",
        }}
      >
        {actionLog}
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
          gap: "1.25rem",
        }}
      >
        <div
          style={{
            backgroundColor: "#0A2E3F",
            border: "1px solid #11606B",
            borderRadius: "0.5rem",
            padding: "1rem",
          }}
        >
          <h2 style={{ color: "#28EBFF", fontSize: "1.1rem", marginTop: 0 }}>
            GET /simulation/state
          </h2>
          <pre
            style={{
              margin: 0,
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
              fontSize: "0.85rem",
              color: "#D8F3FA",
            }}
          >
            {JSON.stringify(simState, null, 2)}
          </pre>
        </div>

        <div
          style={{
            backgroundColor: "#0A2E3F",
            border: "1px solid #11606B",
            borderRadius: "0.5rem",
            padding: "1rem",
          }}
        >
          <h2 style={{ color: "#CE701A", fontSize: "1.1rem", marginTop: 0 }}>
            GET /simulation/diagnosis
          </h2>
          <pre
            style={{
              margin: 0,
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
              fontSize: "0.85rem",
              color: "#D8F3FA",
            }}
          >
            {JSON.stringify(diagnosis, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}