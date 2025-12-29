from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class PersonCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    nickname: Optional[str] = None
    date_of_birth: Optional[date] = None
    notes: Optional[str] = None

class PersonOut(PersonCreate):
    person_id: int
    class Config:
        orm_mode = True

class EventCreate(BaseModel):
    title: str
    description: Optional[str]
    event_type: str
    start_datetime: datetime
    end_datetime: Optional[datetime]
    location: Optional[str]

class MoodLogCreate(BaseModel):
    log_date: date
    mood_level: int
    energy_level: int
    notes: Optional[str]