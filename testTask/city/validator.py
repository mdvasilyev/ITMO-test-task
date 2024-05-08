from typing import Optional

from sqlalchemy.orm import Session

from .models import City


async def city_validator(db_session: Session, name: City.name) -> Optional[City]:
    return db_session.query(City).filter(City.name == name).first()
