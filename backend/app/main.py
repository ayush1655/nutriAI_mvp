import os
import sys

# Ensure the backend/ directory is on sys.path so `app` resolves as a package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import needle

from app import crud, models, schemas
from app.database import engine, get_db
from app.routers import items

# Load environment configuration
load_dotenv()


# ==========================================
# Cactus Needle Nutrition Agent & Tools
# ==========================================

NUTRITION_DATABASE: Dict[str, Dict[str, Any]] = {
    "apple": {
        "calories": 52.0,
        "protein": 0.3,
        "carbs": 14.0,
        "fat": 0.2,
        "fiber": 2.4,
        "serving": "100g",
    },
    "banana": {
        "calories": 89.0,
        "protein": 1.1,
        "carbs": 23.0,
        "fat": 0.3,
        "fiber": 2.6,
        "serving": "100g",
    },
    "chicken breast": {
        "calories": 165.0,
        "protein": 31.0,
        "carbs": 0.0,
        "fat": 3.6,
        "fiber": 0.0,
        "serving": "100g cooked",
    },
    "salmon": {
        "calories": 208.0,
        "protein": 20.0,
        "carbs": 0.0,
        "fat": 13.0,
        "fiber": 0.0,
        "serving": "100g fillet",
    },
    "egg": {
        "calories": 78.0,
        "protein": 6.3,
        "carbs": 0.6,
        "fat": 5.3,
        "fiber": 0.0,
        "serving": "1 large (50g)",
    },
    "oats": {
        "calories": 150.0,
        "protein": 5.0,
        "carbs": 27.0,
        "fat": 2.5,
        "fiber": 4.0,
        "serving": "40g dry",
    },
    "brown rice": {
        "calories": 111.0,
        "protein": 2.6,
        "carbs": 23.0,
        "fat": 0.9,
        "fiber": 1.8,
        "serving": "100g cooked",
    },
    "broccoli": {
        "calories": 34.0,
        "protein": 2.8,
        "carbs": 7.0,
        "fat": 0.4,
        "fiber": 2.6,
        "serving": "100g raw",
    },
    "spinach": {
        "calories": 23.0,
        "protein": 2.9,
        "carbs": 3.6,
        "fat": 0.4,
        "fiber": 2.2,
        "serving": "100g raw",
    },
    "greek yogurt": {
        "calories": 100.0,
        "protein": 17.0,
        "carbs": 6.0,
        "fat": 0.7,
        "fiber": 0.0,
        "serving": "170g non-fat",
    },
    "almonds": {
        "calories": 579.0,
        "protein": 21.0,
        "carbs": 22.0,
        "fat": 50.0,
        "fiber": 12.5,
        "serving": "100g",
    },
    "avocado": {
        "calories": 160.0,
        "protein": 2.0,
        "carbs": 8.5,
        "fat": 14.7,
        "fiber": 6.7,
        "serving": "100g",
    },
}


def analyze_food(food_name: str) -> dict:
    """Analyze the nutritional composition, health score, and dietary advice for a given food.

    Args:
        food_name: Name of the food item to analyze.
    """
    clean_name = food_name.lower().strip()

    # Search for match in database
    matched_entry = None
    for key, data in NUTRITION_DATABASE.items():
        if key in clean_name or clean_name in key:
            matched_entry = data
            break

    if matched_entry:
        calories = matched_entry["calories"]
        protein = matched_entry["protein"]
        carbs = matched_entry["carbs"]
        fat = matched_entry["fat"]
        is_estimate = False
    else:
        # Default baseline estimation for unknown foods
        calories, protein, carbs, fat = 150.0, 5.0, 20.0, 5.0
        is_estimate = True

    # Calculate health metrics
    protein_ratio = (protein * 4) / max(calories, 1.0)
    is_high_protein = protein_ratio >= 0.25 or protein >= 15.0
    is_low_carb = carbs <= 5.0
    is_low_calorie = calories <= 100.0

    score = 70
    if is_high_protein:
        score += 15
    if is_low_calorie:
        score += 10
    if not is_estimate:
        score = min(score, 100)

    dietary_tags = []
    if is_high_protein:
        dietary_tags.append("High Protein")
    if is_low_carb:
        dietary_tags.append("Keto-Friendly / Low Carb")
    if is_low_calorie:
        dietary_tags.append("Low Calorie Density")

    return {
        "food": food_name,
        "health_score": score,
        "is_estimate": is_estimate,
        "dietary_tags": dietary_tags,
        "summary": (
            f"{food_name.title()} is a great source of lean protein."
            if is_high_protein
            else f"{food_name.title()} provides energy and essential nutrients."
        ),
    }


def get_nutrition_info(food_name: str) -> dict:
    """Retrieve macronutrient details including calories, protein, carbohydrates, and fat for a specific food.

    Args:
        food_name: Name of the food item to retrieve nutrition info for.
    """
    clean_name = food_name.lower().strip()

    matched_key = None
    for key in NUTRITION_DATABASE:
        if key in clean_name or clean_name in key:
            matched_key = key
            break

    if matched_key:
        info = dict(NUTRITION_DATABASE[matched_key])
        info["food"] = food_name
        info["found_in_database"] = True
        return info

    # Fallback nutritional estimate
    return {
        "food": food_name,
        "calories": 150.0,
        "protein": 5.0,
        "carbs": 20.0,
        "fat": 5.0,
        "fiber": 2.0,
        "serving": "100g standard portion",
        "found_in_database": False,
        "note": "Nutritional values are estimated based on general food category standards.",
    }


# Initialize Cactus Needle Agent with nutrition tools
agent = needle.Needle(tools=[analyze_food, get_nutrition_info])

# Create database tables
models.Base.metadata.create_all(bind=engine)


# ==========================================
# FastAPI Application Setup
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event to ensure database tables exist on application startup."""
    models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(

    title="NutriAI API",
    description="NutriAI backend with SQLite database, Food Item logging, and Cactus Needle AI Nutrition Agent.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration allowing all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(items.router)


# ==========================================
# User Endpoints
# ==========================================

@app.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Create user",
    description="Register a new user in the system.",
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    existing_user = crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    return crud.create_user(db=db, user=user)


@app.get(
    "/users",
    response_model=List[schemas.UserResponse],
    tags=["Users"],
    summary="List users",
    description="Retrieve a paginated list of registered users.",
)
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Retrieve all users."""
    return crud.get_users(db, skip=skip, limit=limit)


@app.get(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
    tags=["Users"],
    summary="Get user by ID",
    description="Retrieve a specific user along with their logged food items.",
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a single user by ID."""
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return db_user


# ==========================================
# AI Agent Endpoint
# ==========================================

@app.post(
    "/ai/query",
    response_model=schemas.AIQueryResponse,
    tags=["AI Agent"],
    summary="Query Nutrition AI Agent",
    description="Run a natural language query through the Cactus Needle agent with nutrition tools.",
)
def query_ai(request: schemas.AIQueryRequest):
    """Processes a natural language query using the Cactus Needle agent."""
    try:
        agent_result = agent.run(request.query)
        tool_results = agent_result.get("results", [])

        # Format user-friendly response payload
        if tool_results and len(tool_results) == 1:
            response_data = tool_results[0]
        elif tool_results:
            response_data = tool_results
        else:
            response_data = agent_result.get("reasoning") or "No specific tool execution result returned."

        return schemas.AIQueryResponse(
            query=request.query,
            success=agent_result.get("success", True),
            response=response_data,
            reasoning=agent_result.get("reasoning"),
            confidence=agent_result.get("confidence"),
            raw=agent_result,
        )
    except Exception as exc:
        return schemas.AIQueryResponse(
            query=request.query,
            success=False,
            response={"error": str(exc)},
            reasoning="An error occurred while executing the agent.",
            confidence=0.0,
            raw={"error": str(exc)},
        )


# ==========================================
# Root Endpoint
# ==========================================

@app.get(
    "/",
    tags=["General"],
    summary="Root API Info",
    description="Returns basic information and available endpoints.",
)
def read_root():
    """Root endpoint returning API details."""
    return {
        "title": "NutriAI API",
        "version": "1.0.0",
        "status": "online",
        "documentation": "/docs",
        "endpoints": {
            "root": "/",
            "items": "/items",
            "users": "/users",
            "ai_query": "/ai/query",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
