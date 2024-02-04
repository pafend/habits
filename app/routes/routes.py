from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.habit import HabitCreate, HabitResponse
from app.db_models.habit import Habit

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/habits/", response_model=HabitResponse)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = Habit(**habit.dict())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


@router.get("/habits/{habit_id}", response_model=HabitResponse)
def read_habit(habit_id: int, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return db_habit


@router.get("/habits/", response_model=list[HabitResponse])
def read_habits(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    habits = db.query(Habit).offset(skip).limit(limit).all()
    return habits


@router.put("/habits/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    for key, value in habit.dict().items():
        setattr(db_habit, key, value)

    db.commit()
    db.refresh(db_habit)
    return db_habit


@router.delete("/habits/{habit_id}", response_model=HabitResponse)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if db_habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    db.delete(db_habit)
    db.commit()
    return db_habit
