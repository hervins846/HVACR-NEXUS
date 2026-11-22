import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000";

type JsonRecord = Record<string, unknown>;

async function fetchJsonWithStatus(url: string, init?: RequestInit): Promise<{ ok: boolean; status: number; data: unknown }> {
  const res = await fetch(url, init);
  const text = await res.text();
  let data: unknown = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { raw: text };
    }
  }
  return { ok: res.ok, status: res.status, data };
}

export default function App() {
  const [health, setHealth] = useState<string>("Verification en cours...");
  const [simState, setSimState] = useState<unknown>(null);
  const [diagnosis, setDiagnosis] = useState<JsonRecord | null>(null);
  const [dtValue, setDtValue] = useState<string>("1.0");
  const [paramKey, setParamKey] = useState<string>("t_cond_c");
  const [paramValue, setParamValue] = useState<string>("42.0");
  const [actionLog, setActionLog] = useState<string>("Pret pour le pilotage HVACR NEXUS.");
  const [busy, setBusy] = useState<boolean>(false);

  async function refreshAll() {
    setBusy(true);
    try {
      const [rootRes, stateRes, diagRes] = await Promise.allSettled([
        fetchJsonWithStatus(`${API_BASE}/`),
        fetchJsonWithStatus(`${API_BASE}/simulation/state`),
        fetchJsonWithStatus(`${API_BASE}/simulation/diagnosis`),
      ]);

      if (rootRes.status === "fulfilled" && rootRes.value.ok) {
        const rootData = (rootRes.value.data ?? {}) as JsonRecord;
        setHealth(`${String(rootData.service ?? "HVACR NEXUS")} : ${String(rootData.status ?? "ok")}`);
      } else {
        setHealth("API locale inaccessible sur http://localhost:8000");
      }

      if (stateRes.status === "fulfilled") {
        setSimState(
          stateRes.value.ok
            ? stateRes.value.data
            : { http_status: stateRes.value.status, detail: stateRes.value.data }
        );
      }

      if (diagRes.status === "fulfilled") {
        setDiagnosis(
          diagRes.value.ok && typeof diagRes.value.data === "object" && diagRes.value.data !== null
            ? (diagRes.value.data as JsonRecord)
            : { http_status: diagRes.value.status, detail: diagRes.value.data }
        );
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
    const parsedDt = Number(dtValue);
    const safeDt = Number.isFinite(parsedDt) && parsedDt >= 0 ? parsedDt : 1.0;

    try {
      const stepRes = await fetchJsonWithStatus(`${API_BASE}/simulation/step?dt=${encodeURIComponent(String(safeDt))}`, {
        method: "POST",
      });
      setSimState(stepRes.ok ? stepRes.data : { http_status: stepRes.status, detail: stepRes.data });

      const diagRes = await fetchJsonWithStatus(`${API_BASE}/simulation/diagnosis`);
      if (diagRes.ok && typeof diagRes.data === "object" && diagRes.data !== null) {
        setDiagnosis(diagRes.data as JsonRecord);
      }

      setActionLog(`POST /simulation/step?dt=${safeDt} -> HTTP ${stepRes.status}`);
    } catch (err) {
      setActionLog(`Erreur POST /simulation/step : ${String(err)}`);
    } finally {
      setBusy(false);
    }
  }

  async function handlePatchParams(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    const key = paramKey.trim();
    const trimmedVal = paramValue.trim();
    const numVal = Number(trimmedVal);
    const val: unknown = trimmedVal !== "" && !Number.isNaN(numVal) ? numVal : trimmedVal;
    const payload = key ? { [key]: val } : {};

    try {
      const patchRes = await fetchJsonWithStatus(`${API_BASE}/simulation/parameters`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!patchRes.ok) {
        setActionLog(`PATCH /simulation/parameters -> HTTP ${patchRes.status} (${JSON.stringify(patchRes.data)})`);
        return;
      }

      if (typeof patchRes.data === "object" && patchRes.data !== null) {
        setSimState(patchRes.data);
      }

      const diagRes = await fetchJsonWithStatus(`${API_BASE}/simulation/diagnosis`);
      if (diagRes.ok && typeof diagRes.data === "object" && diagRes.data !== null) {
        setDiagnosis(diagRes.data as JsonRecord);
      }

      setActionLog(`PATCH /simulation/parameters (${JSON.stringify(payload)}) -> HTTP ${patchRes.status}`);
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

        <label style={{ display: "flex", alignItems: "center", gap: "0.35rem", fontSize: "0.9rem" }}>
          <span>dt:</span>
          <input
            type="text"
            value={dtValue}
            onChange={(e) => setDtValue(e.target.value)}
            style={{
              backgroundColor: "#0A2E3F",
              color: "#E6F7FF",
              border: "1px solid #11606B",
              padding: "0.55rem 0.6rem",
              borderRadius: "0.4rem",
              width: "68px",
            }}
          />
        </label>

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
            placeholder="t_cond_c / superheat_k / subcooling_k"
            style={{
              backgroundColor: "#0A2E3F",
              color: "#E6F7FF",
              border: "1px solid #11606B",
              padding: "0.55rem 0.75rem",
              borderRadius: "0.4rem",
              width: "180px",
            }}
          />
          <input
            type="text"
            value={paramValue}
            onChange={(e) => setParamValue(e.target.value)}
            placeholder="Valeur"
            style={{
              backgroundColor: "#0A2E3F",
              color: "#E6F7FF",
              border: "1px solid #11606B",
              padding: "0.55rem 0.75rem",
              borderRadius: "0.4rem",
              width: "100px",
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
          {diagnosis && "health_score" in diagnosis && (
            <div
              style={{
                display: "flex",
                gap: "1rem",
                marginBottom: "0.75rem",
                fontSize: "0.9rem",
                color: "#28EBFF",
                fontWeight: 600,
              }}
            >
              <span>Score : {String(diagnosis.health_score ?? "-")}</span>
              <span>Statut : {String(diagnosis.overall_status ?? "-")}</span>
            </div>
          )}
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