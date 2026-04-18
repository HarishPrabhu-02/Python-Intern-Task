from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, auth, database

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user) # Protects the route
):
    # Create the task and assign the owner_id to the currently logged-in user
    new_task = models.Task(**task.model_dump(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(
    completed: Optional[bool] = None, # Optional filter
    skip: int = 0,                    # Pagination start
    limit: int = 10,                  # Pagination limit
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    # Start the query, strictly filtering by the current user's ID
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)
    
    # Apply completion filter if provided
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
        
    # Apply pagination and execute
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    # Ensure the task exists AND belongs to the user
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")
    return task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int, 
    task_update: schemas.TaskUpdate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")

    # Update only the fields that were provided in the request
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")

    db.delete(task)
    db.commit()
    return None