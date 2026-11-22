import { useEffect, useState } from "react";

export default function App() {
  const [apiStatus, setApiStatus] = useState<string>("Verification en cours...");

  useEffect(() => {
    fetch("http://localhost:8000/")
      .then((res) => res.json())
      .then((data) => setApiStatus(`${data.service ?? "API"} : ${data.status ?? "ok"}`))
      .catch(() => setApiStatus("API locale inaccessible sur http://localhost:8000"));
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
      <h1 style={{ color: "#28EBFF", fontSize: "2rem", marginBottom: "0.75rem" }}>
        HVACR NEXUS
      </h1>
      <p style={{ marginBottom: "1rem" }}>
        Interface frontend active sur <strong>http://localhost:5173/</strong>
      </p>
      <p style={{ color: "#CE701A", fontWeight: 600 }}>Backend : {apiStatus}</p>
    </div>
  );
}