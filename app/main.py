from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.routers import organizations, buildings, activities


app = FastAPI(title="Organization Directory API")

# CORS (на всякий случай)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
app.include_router(buildings.router, prefix="/buildings", tags=["Buildings"])
app.include_router(activities.router, prefix="/activities", tags=["Activities"])
