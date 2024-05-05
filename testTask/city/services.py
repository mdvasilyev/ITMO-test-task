from typing import List

from fastapi import HTTPException, status
from geoalchemy2 import Geometry

from . import models
from . import schema


def generate_geometry(coordinates: List[List[List[float]]]) -> str:
    res = []
    for pair in coordinates[0]:
        res.append(f'{pair[0]} {pair[1]}')
    return ','.join(res)


async def create_city(request: schema.Feature, db) -> models.City:
    geometry = f'SRID=4326;{request.geometry.type}(({generate_geometry(request.geometry.coordinates)}))'
    new_city = models.City(name=request.properties.name, country=request.properties.country, geom=geometry)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city


def get_all_cities(database):
    return None
