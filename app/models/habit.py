from pydantic import BaseModel


class HabitCreate(BaseModel):
    title: str
    text_body: str
    reminder_interval_days: int


class HabitResponse(HabitCreate):
    id: int
