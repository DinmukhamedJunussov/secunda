from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas, models
from app.database import get_db
from app.dependencies import api_key_auth

router = APIRouter(dependencies=[Depends(api_key_auth)])


@router.post("/", response_model=schemas.ActivityRead)
def create_activity(data: schemas.ActivityCreate, db: Session = Depends(get_db)):
    activity = models.Activity(**data.dict())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.get("/", response_model=List[schemas.ActivityRead])
def get_all_activities(db: Session = Depends(get_db)):
    return db.query(models.Activity).filter(models.Activity.parent_id == None).all()


@router.get("/{activity_id}", response_model=schemas.ActivityRead)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity
