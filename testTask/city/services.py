from typing import List
from binascii import unhexlify

from fastapi import HTTPException, status
from shapely import wkb, from_wkt, to_wkb

from . import models
from . import schema
from . import validator


def generate_geometry(coordinates: List[List[List[float]]]) -> str:
    res = []
    for pair in coordinates[0]:
        res.append(f'{pair[0]} {pair[1]}')
    return ','.join(res)


def generate_geojson(city: models.City):
    binary = unhexlify(str(city.geom))
    polygon = wkb.loads(binary)
    coords_tuple = list(polygon.exterior.coords)
    coords = [list(c) for c in coords_tuple]
    return {
        'type': 'Feature',
        'properties': {
            'id': city.id,
            'name': city.name,
            'country': city.country,
        },
        'geometry': {
            'coordinates': [coords],
            'type': 'Polygon',
        }
    }


async def create_city(request: schema.Feature, db):
    city = await validator.city_validator(db, request.properties.name)
    if city:
        raise HTTPException(status_code=400, detail="City already exists")
    geometry = f'{request.geometry.type}(({generate_geometry(request.geometry.coordinates)}))'
    new_city = models.City(name=request.properties.name, country=request.properties.country, geom=geometry)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    geojson = generate_geojson(new_city)
    return geojson


async def get_city_by_id(city_id, db):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    city_geojson = generate_geojson(city)
    return city_geojson


async def get_all_cities(db):
    res_geojson = {
        'type': 'FeatureCollection',
        'features': [
        ]
    }
    cities = db.query(models.City).all()
    for city in cities:
        res_geojson['features'].append(generate_geojson(city))
    return res_geojson


async def delete_city_by_id(city_id, database):
    database.query(models.City).filter(models.City.id == city_id).delete()
    database.commit()


async def update_city(request, city_id, database):
    city = database.query(models.City).filter(models.City.id == city_id).first()
    city.name = request.properties.name
    city.country = request.properties.country
    geometry = from_wkt(f'{request.geometry.type}(({generate_geometry(request.geometry.coordinates)}))')
    city.geom = to_wkb(geometry, hex=True)
    database.add(city)
    database.commit()
    database.refresh(city)
    return city
