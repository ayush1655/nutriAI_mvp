# NutriAI

AI-powered nutrition assistant built with **FastAPI**, **SQLite**, **Cactus Needle**, and **React + shadcn/ui**.

Ask natural language questions about food and get instant nutritional analysis powered by the Cactus Needle on-device AI agent.

---

## Project Structure

```
nutriai/
├── backend/          # FastAPI + SQLite + Cactus Needle
│   ├── app/
│   │   ├── main.py        # App entry point, AI agent, routes
│   │   ├── database.py    # SQLAlchemy + SQLite setup
│   │   ├── models.py      # User & FoodItem models
│   │   ├── schemas.py     # Pydantic request/response schemas
│   │   ├── crud.py        # CRUD operations
│   │   └── routers/
│   │       └── items.py   # Food item endpoints
│   ├── requirements.txt
│   └── .env
├── frontend/         # React + Vite + Tailwind + shadcn/ui
│   ├── src/
│   │   ├── App.tsx        # Main UI (connected to backend)
│   │   ├── lib/api.ts     # API client
│   │   └── components/ui/ # shadcn components (button, card, input)
│   ├── vite.config.ts     # Dev proxy to backend
│   └── package.json
└── README.md
```

---

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **npm**

---

## Getting Started

### 1. Backend

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the server (starts on http://127.0.0.1:8000)
python app/main.py
```

### 2. Frontend

Open a **second terminal**:

```bash
cd frontend

# Install Node dependencies
npm install

# Start the dev server (starts on http://localhost:5173)
npm run dev
```

### 3. Open the App

Go to **http://localhost:5173** in your browser.

Type a food query like _"How much protein is in chicken breast?"_ and hit **Analyze Nutrition**.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API info |
| `POST` | `/ai/query` | Query the Cactus Needle nutrition AI |
| `GET` | `/items` | List food items |
| `POST` | `/items` | Create a food item |
| `GET` | `/items/{id}` | Get a food item |
| `PUT` | `/items/{id}` | Update a food item |
| `DELETE` | `/items/{id}` | Delete a food item |
| `GET` | `/users` | List users |
| `POST` | `/users` | Create a user |
| `GET` | `/users/{id}` | Get a user |

Interactive API docs available at **http://127.0.0.1:8000/docs** when the backend is running.

---

## How It Works

```
Browser (:5173)  →  Vite proxy (/api/*)  →  FastAPI (:8000)  →  Cactus Needle Agent
```

- The **Vite dev server** proxies all `/api/*` requests to the FastAPI backend (stripping the `/api` prefix).
- The **FastAPI backend** initializes a Cactus Needle agent with two nutrition tools: `analyze_food` and `get_nutrition_info`.
- The **AI endpoint** (`POST /ai/query`) takes a natural language query, routes it through Needle, and returns structured nutritional data.

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | React, TypeScript, Vite, Tailwind CSS v4, shadcn/ui |
| Backend | FastAPI, SQLAlchemy, SQLite |
| AI | Cactus Needle (on-device function-calling model) |