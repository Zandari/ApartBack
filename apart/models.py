import uuid
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, Field


class Location(BaseModel):
    address: str
    longitude: float
    latitude: float
    metro_station: str


class Apartment(BaseModel):
    rent: int = Field()
    currency: str = Field(max_length=3, min_length=3)
    location: Location = Field()
    area: Optional[int] = Field()
    cover_image: HttpUrl = Field()
    images: Optional[List[HttpUrl]] = Field()


class ApartmentRecord(Apartment):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
