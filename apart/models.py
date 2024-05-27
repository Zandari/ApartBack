import uuid
from datetime import datetime
from typing import Optional, List, Tuple
from pydantic import BaseModel, Field, HttpUrl, Field


class Location(BaseModel):
    type: str
    coordinates: Tuple[float, float]


class Additional(BaseModel):
    author: str
    deal_type: str
    floor: int
    floors_count: int
    rooms_count: int


class Apartment(BaseModel):
    rent: int = Field()
    currency: str = Field(max_length=3, min_length=3)
    address: str
    metro_station: str
    location: Location = Field()
    area: Optional[int] = Field()
    cover_image: HttpUrl = Field()
    images: Optional[List[HttpUrl]] = Field()
    provider: str
    url: str
    additional: Additional


class ApartmentRecord(Apartment):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Place(BaseModel):
    address: str
    latitude: float
    longitude: float
    attendance: int