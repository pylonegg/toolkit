from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Person(Base):
    __tablename__ = "Person"

    person_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    nickname = Column(String(100))
    date_of_birth = Column(Date)
    notes = Column(Text)

class Event(Base):
    __tablename__ = "Event"

    event_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_type = Column(String(50))
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    location = Column(String(255))
    emotional_impact = Column(Integer)

class MoodLog(Base):
    __tablename__ = "Mood_Log"

    log_id = Column(Integer, primary_key=True)
    log_date = Column(Date, nullable=False)
    mood_level = Column(Integer)
    energy_level = Column(Integer)
    notes = Column(Text)

class Habit(Base):
    __tablename__ = "Habit"

    habit_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    category = Column(String(50))

class HabitLog(Base):
    __tablename__ = "Habit_Log"

    habit_id = Column(Integer, ForeignKey("Habit.habit_id"), primary_key=True)
    log_date = Column(Date, primary_key=True)
    completed = Column(Boolean)