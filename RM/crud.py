from sqlalchemy.orm import Session
import models, schemas

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_people(db: Session):
    return db.query(models.Person).all()

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def create_mood_log(db: Session, log: schemas.MoodLogCreate):
    db_log = models.MoodLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log