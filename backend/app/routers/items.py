from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/items",
    tags=["Food Items"],
)


@router.get(
    "/",
    response_model=List[schemas.FoodItemResponse],
    summary="List food items",
    description="Retrieve a paginated list of food items, optionally filtered by user ID.",
)
def read_food_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of items to return"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db),
):
    """Retrieve food items."""
    return crud.get_food_items(db, skip=skip, limit=limit, user_id=user_id)


@router.get(
    "/{item_id}",
    response_model=schemas.FoodItemResponse,
    summary="Get food item by ID",
    description="Retrieve the nutritional details of a specific food item.",
)
def read_food_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """Retrieve a single food item by ID."""
    db_item = crud.get_food_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with id {item_id} not found",
        )
    return db_item


@router.post(
    "/",
    response_model=schemas.FoodItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create food item",
    description="Add a new food item with nutritional values (calories, protein, carbs, fat).",
)
def create_food_item(
    item: schemas.FoodItemCreate,
    db: Session = Depends(get_db),
):
    """Create a new food item."""
    if item.user_id is not None:
        user = crud.get_user(db, user_id=item.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {item.user_id} not found",
            )
    return crud.create_food_item(db=db, item=item)


@router.put(
    "/{item_id}",
    response_model=schemas.FoodItemResponse,
    summary="Update food item",
    description="Update an existing food item by ID with partial or full fields.",
)
def update_food_item(
    item_id: int,
    item_update: schemas.FoodItemUpdate,
    db: Session = Depends(get_db),
):
    """Update a food item."""
    if item_update.user_id is not None:
        user = crud.get_user(db, user_id=item_update.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {item_update.user_id} not found",
            )

    updated_item = crud.update_food_item(db=db, item_id=item_id, item_update=item_update)
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with id {item_id} not found",
        )
    return updated_item


@router.delete(
    "/{item_id}",
    response_model=schemas.FoodItemResponse,
    summary="Delete food item",
    description="Delete a food item by ID.",
)
def delete_food_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """Delete a food item."""
    deleted_item = crud.delete_food_item(db=db, item_id=item_id)
    if not deleted_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with id {item_id} not found",
        )
    return deleted_item
