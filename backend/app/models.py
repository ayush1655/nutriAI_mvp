from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """User model representing application users."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    food_items = relationship("FoodItem", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"


class FoodItem(Base):
    """FoodItem model storing nutritional information for food entries."""

    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    calories = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)  # in grams
    carbs = Column(Float, nullable=False)    # in grams
    fat = Column(Float, nullable=False)      # in grams
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="food_items")

    def __repr__(self) -> str:
        return f"<FoodItem(id={self.id}, name='{self.name}', calories={self.calories})>"
