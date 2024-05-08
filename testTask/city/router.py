from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from testTask import db

from . import schema
from . import services

router = APIRouter(prefix="/city", tags=["city"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_city(request: schema.Feature, database: Session = Depends(db.get_db)):
    return await services.create_city(request, database)


@router.get('/{city_id}', status_code=status.HTTP_200_OK)
async def get_city_by_id(city_id: int, database: Session = Depends(db.get_db)):
    return await services.get_city_by_id(city_id, database)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_cities(database: Session = Depends(db.get_db)):
    return await services.get_all_cities(database)


@router.delete('/{city_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_city_by_id(city_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_city_by_id(city_id, database)


@router.put("/{city_id}")
async def update_city(request: schema.Feature, city_id: int, database: Session = Depends(db.get_db)):
    return await services.update_city(request, city_id, database)
