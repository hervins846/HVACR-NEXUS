# HVACR NEXUS

Plateforme de laboratoire jumeau numérique (Digital Twin Lab) dédiée à la simulation, au pilotage et au diagnostic des systèmes HVACR, reliant un backend **FastAPI / Uvicorn** (`http://localhost:8000`) à un frontend **React / Vite / TypeScript / Tailwind CSS** (`http://localhost:5173`).

---

## Architecture du projet

```text
HVACR-NEXUS/
├── backend/
│   └── app/
│       ├── main.py
│       ├── api/routes/simulation.py
│       ├── diagnostics/recommendation.py
│       └── engine/simulation_engine.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   └── postcss.config.js
├── docker-compose.yml
├── requirements.txt
└── README.md