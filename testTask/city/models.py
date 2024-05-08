from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

from testTask.db import Base


class City(Base):
    __tablename__ = 'cities'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(255), unique=True)
    country: str = Column(String(255))
    geom: Geometry = Column(Geometry('POLYGON'))

    def __init__(self, name, country, geom):
        self.name = name
        self.country = country
        self.geom = geom
