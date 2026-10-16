# NutriAI Backend API

A high-performance FastAPI backend for nutrition tracking and AI-powered dietary insights, built with SQLite, SQLAlchemy, Pydantic, and the Cactus Needle AI tool-calling agent.

---

## Features

- **FastAPI Framework**: Modern, asynchronous, and OpenAPI/Swagger documented.
- **SQLAlchemy ORM & SQLite**: Relational database schema with models for `User` and `FoodItem`, automatically initialized on startup.
- **Cactus Needle Integration**: Natural language nutrition queries with automated function calling via `needle.Needle(tools=[analyze_food, get_nutrition_info])`.
- **Complete CRUD Operations**: Full management of food item entries and user accounts.
- **CORS Configured**: Ready for frontend integration.

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI app, Needle agent, and endpoints
│   ├── database.py          # SQLite engine, SessionLocal, Base, and get_db dependency
│   ├── models.py            # SQLAlchemy models (User, FoodItem)
│   ├── schemas.py           # Pydantic validation schemas
│   ├── crud.py              # CRUD database helper functions
│   └── routers/
│       ├── __init__.py      # Routers package initialization
│       └── items.py         # Food items CRUD router
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables
└── README.md                # Documentation and setup instructions
```

---

## Getting Started

### 1. Prerequisites

- Python 3.10+ (tested on Python 3.11)
- `pip` or virtualenv

### 2. Setup Virtual Environment (Recommended)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (cmd/PowerShell):
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configuration

The application loads configuration from `.env`. A default `.env` is provided:

```ini
DATABASE_URL=sqlite:///./nutriai.db
```

### 5. Run the Application

Start the development server with Uvicorn:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Once running:
- **Interactive OpenAPI Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **API Status Root**: [http://localhost:8000/](http://localhost:8000/)

---

## API Endpoints

### General
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API status and endpoint directory |
| `GET` | `/docs` | Interactive Swagger UI documentation |

### AI Nutrition Agent
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ai/query` | Submit natural language queries to the Needle agent |

**Example Request:**
```bash
curl -X POST "http://localhost:8000/ai/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the calories and macros for chicken breast?"}'
```

**Example Response:**
```json
{
  "query": "What are the calories and macros for chicken breast?",
  "success": true,
  "response": {
    "food": "chicken breast",
    "calories": 165.0,
    "protein": 31.0,
    "carbs": 0.0,
    "fat": 3.6,
    "fiber": 0.0,
    "serving": "100g cooked",
    "found_in_database": true
  },
  "reasoning": "User asked for calorie and macronutrient details; responded with food lookup.",
  "confidence": 0.95
}
```

### Food Items (`/items`)
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/items/` | List food items (supports `skip`, `limit`, `user_id` query params) |
| `POST` | `/items/` | Create a new food item |
| `GET` | `/items/{item_id}` | Get food item details by ID |
| `PUT` | `/items/{item_id}` | Update an existing food item |
| `DELETE` | `/items/{item_id}` | Delete a food item by ID |

**Example Create Food Item:**
```bash
curl -X POST "http://localhost:8000/items/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Grilled Chicken Salad",
       "calories": 320.0,
       "protein": 35.0,
       "carbs": 12.0,
       "fat": 14.0
     }'
```

### Users (`/users`)
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users` | Create a new user |
| `GET` | `/users` | List users |
| `GET` | `/users/{user_id}` | Get user by ID including their logged food items |
