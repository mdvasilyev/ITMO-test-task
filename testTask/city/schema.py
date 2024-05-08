from typing import List

from pydantic import BaseModel, Field
from geoalchemy2.types import WKBElement
from typing_extensions import Annotated


class City(BaseModel):
    name: str
    country: str
    geom: Annotated[str, WKBElement]


class Properties(BaseModel):
    id: int = Field(primary_key=True)
    name: str
    country: str


class Geometry(BaseModel):
    coordinates: List[List[List[float]]]
    type: str = Field(default="Polygon")


class Feature(BaseModel):
    type: str = Field(default="Feature")
    properties: Properties
    geometry: Geometry


class FeatureCollection(BaseModel):
    type: str = Field(default="FeatureCollection")
    features: List[Feature]
