from typing import Optional, List
from sqlalchemy.orm import Session
from app import models, schemas


# ==========================================
# User CRUD Operations
# ==========================================

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Retrieve a single user by primary key ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Retrieve a single user by email address."""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Retrieve a paginated list of users."""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user record."""
    db_user = models.User(
        name=user.name,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ==========================================
# FoodItem CRUD Operations
# ==========================================

def get_food_item(db: Session, item_id: int) -> Optional[models.FoodItem]:
    """Retrieve a single food item by ID."""
    return db.query(models.FoodItem).filter(models.FoodItem.id == item_id).first()


def get_food_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
) -> List[models.FoodItem]:
    """Retrieve food items with optional pagination and user_id filtering."""
    query = db.query(models.FoodItem)
    if user_id is not None:
        query = query.filter(models.FoodItem.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def create_food_item(db: Session, item: schemas.FoodItemCreate) -> models.FoodItem:
    """Create a new food item record."""
    db_item = models.FoodItem(
        name=item.name,
        calories=item.calories,
        protein=item.protein,
        carbs=item.carbs,
        fat=item.fat,
        user_id=item.user_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_food_item(
    db: Session,
    item_id: int,
    item_update: schemas.FoodItemUpdate,
) -> Optional[models.FoodItem]:
    """Update an existing food item record with partial or full attributes."""
    db_item = get_food_item(db, item_id)
    if not db_item:
        return None

    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_food_item(db: Session, item_id: int) -> Optional[models.FoodItem]:
    """Delete a food item record by ID."""
    db_item = get_food_item(db, item_id)
    if not db_item:
        return None

    db.delete(db_item)
    db.commit()
    return db_item
