import React from "react";
import ReactDOM from "react-dom/client";

function App() {
  return (
    <main className="min-h-screen bg-[#06212E] text-slate-100 p-6">
      <div className="max-w-6xl mx-auto rounded-xl border border-[#11606B] bg-[#092C3C] p-6 shadow-lg">
        <div className="flex items-center justify-between border-b border-[#11606B]/60 pb-4">
          <div>
            <p className="text-xs uppercase tracking-widest text-[#28EBFF]">
              Digital Twin Engineering Lab
            </p>
            <h1 className="text-2xl font-bold text-white mt-1">HVACR NEXUS</h1>
          </div>
          <span className="rounded-full bg-[#CE701A]/20 border border-[#CE701A] px-3 py-1 text-xs font-semibold text-[#CE701A]">
            BACKEND READY
          </span>
        </div>
        <p className="mt-4 text-sm text-slate-300">
          Interface React connectee au moteur thermodynamique, a la boucle de
          regulation et au flux temps reel.
        </p>
      </div>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
