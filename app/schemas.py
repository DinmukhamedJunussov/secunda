from typing import List, Optional
from pydantic import BaseModel


# === PhoneNumber ===
class PhoneNumberBase(BaseModel):
    phone: str

class PhoneNumberCreate(PhoneNumberBase):
    pass

class PhoneNumberRead(PhoneNumberBase):
    id: int

    class Config:
        orm_mode = True


# === Activity ===
class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityRead(ActivityBase):
    id: int
    children: List["ActivityRead"] = []

    class Config:
        orm_mode = True


# === Building ===
class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float

class BuildingCreate(BuildingBase):
    pass

class BuildingRead(BuildingBase):
    id: int

    class Config:
        orm_mode = True


# === Organization ===
class OrganizationBase(BaseModel):
    name: str
    building_id: int

class OrganizationCreate(OrganizationBase):
    phones: List[PhoneNumberCreate]
    activity_ids: List[int]

class OrganizationRead(OrganizationBase):
    id: int
    phones: List[PhoneNumberRead]
    activities: List[ActivityRead]
    building: BuildingRead

    class Config:
        orm_mode = True


# Для рекурсивной модели ActivityRead
ActivityRead.update_forward_refs()
