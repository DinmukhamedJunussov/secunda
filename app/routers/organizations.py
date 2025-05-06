from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List

from app import schemas, models
from app.database import get_db
from app.dependencies import api_key_auth

router = APIRouter(dependencies=[Depends(api_key_auth)])


@router.get("/", response_model=List[schemas.OrganizationRead])
def get_all_organizations(db: Session = Depends(get_db)):
    return db.query(models.Organization).all()


@router.get("/{org_id}", response_model=schemas.OrganizationRead)
def get_organization(org_id: int, db: Session = Depends(get_db)):
    org = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.post("/", response_model=schemas.OrganizationRead)
def create_organization(org_data: schemas.OrganizationCreate, db: Session = Depends(get_db)):
    org = models.Organization(name=org_data.name, building_id=org_data.building_id)

    # Add phones
    for phone in org_data.phones:
        org.phones.append(models.PhoneNumber(phone=phone.phone))

    # Add activities
    activities = db.query(models.Activity).filter(models.Activity.id.in_(org_data.activity_ids)).all()
    org.activities.extend(activities)

    db.add(org)
    db.commit()
    db.refresh(org)
    return org


@router.get("/by-building/{building_id}", response_model=List[schemas.OrganizationRead])
def get_organizations_by_building(building_id: int, db: Session = Depends(get_db)):
    return db.query(models.Organization).filter(models.Organization.building_id == building_id).all()


@router.get("/by-activity/{activity_id}", response_model=List[schemas.OrganizationRead])
def get_organizations_by_activity(activity_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Organization)
        .join(models.Organization.activities)
        .filter(models.Activity.id == activity_id)
        .all()
    )


@router.get("/search", response_model=List[schemas.OrganizationRead])
def search_organizations(
    name: str = Query(None),
    activity: str = Query(None),
    lat: float = Query(None),
    lon: float = Query(None),
    radius_km: float = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Organization)

    if name:
        query = query.filter(models.Organization.name.ilike(f"%{name}%"))

    if activity:
        activity_ids = get_nested_activity_ids(activity_name=activity, db=db)
        query = query.join(models.Organization.activities).filter(models.Activity.id.in_(activity_ids))

    if lat is not None and lon is not None and radius_km is not None:
        # гео фильтрация через Haversine формулу (упрощённая версия)
        radius_deg = radius_km / 111  # Примерно 1 градус ≈ 111 км
        query = query.join(models.Organization.building).filter(
            models.Building.latitude.between(lat - radius_deg, lat + radius_deg),
            models.Building.longitude.between(lon - radius_deg, lon + radius_deg),
        )

    return query.all()


# рекурсивный поиск всех вложенных под-видов деятельности
def get_nested_activity_ids(activity_name: str, db: Session, max_depth: int = 3) -> List[int]:
    root = db.query(models.Activity).filter(models.Activity.name == activity_name).first()
    if not root:
        return []
    ids = set()

    def collect_children(act, current_depth=0):
        if current_depth > max_depth:
            return
        ids.add(act.id)
        for child in act.children:
            collect_children(child, current_depth + 1)

    collect_children(root)
    return list(ids)
