from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# FoodItem Schemas
# ==========================================

class FoodItemBase(BaseModel):
    """Base schema for food item attributes."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the food item")
    calories: float = Field(..., ge=0, description="Total calories (kcal)")
    protein: float = Field(..., ge=0, description="Protein in grams")
    carbs: float = Field(..., ge=0, description="Carbohydrates in grams")
    fat: float = Field(..., ge=0, description="Fat in grams")
    user_id: Optional[int] = Field(None, description="Optional ID of the user logging this item")


class FoodItemCreate(FoodItemBase):
    """Schema for creating a new food item."""
    pass


class FoodItemUpdate(BaseModel):
    """Schema for updating an existing food item."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    calories: Optional[float] = Field(None, ge=0)
    protein: Optional[float] = Field(None, ge=0)
    carbs: Optional[float] = Field(None, ge=0)
    fat: Optional[float] = Field(None, ge=0)
    user_id: Optional[int] = None


class FoodItemResponse(FoodItemBase):
    """Schema for returning food item data."""
    id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# User Schemas
# ==========================================

class UserBase(BaseModel):
    """Base schema for user attributes."""
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the user")
    email: str = Field(..., min_length=3, max_length=255, description="Unique email address")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass


class UserResponse(UserBase):
    """Schema for returning user data."""
    id: int
    created_at: datetime
    food_items: List[FoodItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# AI Query Schemas
# ==========================================

class AIQueryRequest(BaseModel):
    """Schema for natural language AI nutrition query request."""
    query: str = Field(..., min_length=1, description="Natural language query for the nutrition assistant")


class AIQueryResponse(BaseModel):
    """Schema for the AI assistant response."""
    query: str
    success: bool
    response: Any = Field(..., description="Structured tool output, response text, or result dictionary")
    reasoning: Optional[str] = Field(None, description="Model reasoning behind the tool choice or response")
    confidence: Optional[float] = Field(None, description="Model confidence score")
    raw: Optional[dict] = Field(None, description="Complete raw response from the agent")
