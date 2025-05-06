from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    parent = relationship("Activity", remote_side=[id], backref="children")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")
    phones = relationship("PhoneNumber", back_populates="organization", cascade="all, delete-orphan")
    activities = relationship("Activity", secondary=organization_activities, backref="organizations")


class PhoneNumber(Base):
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="phones")
