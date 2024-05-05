from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

from testTask.db import Base


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    country = Column(String(255))
    geom = Column(Geometry('POLYGON', srid=4326))

    def __init__(self, name, country, geom):
        self.name = name
        self.country = country
        self.geom = geom
