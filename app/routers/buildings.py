from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.database import get_db
from app.dependencies import api_key_auth

router = APIRouter(dependencies=[Depends(api_key_auth)])


@router.post("/", response_model=schemas.BuildingRead)
def create_building(data: schemas.BuildingCreate, db: Session = Depends(get_db)):
    building = models.Building(**data.dict())
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


@router.get("/", response_model=List[schemas.BuildingRead])
def get_all_buildings(db: Session = Depends(get_db)):
    return db.query(models.Building).all()


@router.get("/{building_id}", response_model=schemas.BuildingRead)
def get_building(building_id: int, db: Session = Depends(get_db)):
    building = db.query(models.Building).filter(models.Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building
