from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from testTask import db
from testTask.city.models import City
from . import schema
from . import services

router = APIRouter(prefix="/city", tags=["city"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_city(request: schema.Feature, database: Session = Depends(db.get_db)):
    new_city = await services.create_city(request, database)
    return new_city


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_cities(database: Session = Depends(db.get_db)):
    return await services.get_all_cities(database)
