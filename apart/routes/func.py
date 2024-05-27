from fastapi import APIRouter, Request
from typing import List, Optional, Literal
from pydantic import PositiveInt

from ..models import ApartmentRecord, Place

router = APIRouter()


@router.post(
    path="/get_aparts",
    response_description="Returns recommended aparts",
    response_model=List[ApartmentRecord],
)
def get_aparts(
        request: Request,
        places: List[Place],
        rent_min: Optional[PositiveInt] = None,
        rent_max: Optional[PositiveInt] = None,
        area_min: Optional[PositiveInt] = None,
        area_max: Optional[PositiveInt] = None,
        rooms: Optional[List[PositiveInt]] = None,
        deal_type: Optional[Literal["rent", "sale"]] = None,
        limit: int = 20,
        radius: int = 10,
    ) -> List[ApartmentRecord]:

    center = [0, 0]
    total_attendance = 0
    for place in places:
        total_attendance += place.attendance
        center[0] += place.latitude * place.attendance
        center[1] += place.longitude * place.attendance
    center[0] /= total_attendance
    center[1] /= total_attendance

    query = {
        "location": {
            "$geoWithin": {
                "$centerSphere": [center, radius / 6378.1]
            }
        }
    }

    rent_query = dict()
    if rent_min is not None:
        rent_query["$gt"] = rent_min
    if rent_max is not None:
        rent_query["$lt"] = rent_max
    query["rent"] = rent_query

    area_query = dict()
    if area_min is not None:
        area_query["$gt"] = area_min
    if area_max is not None:
        area_query["$lt"] = area_max
    query["area"] = area_query

    if rooms is not None:
        query["$additional.rooms_count"] = {"$in": rooms}

    if deal_type is not None:
        query["$additional.deal_type"] = deal_type

    result = request.app.database["aparts"].find(query, limit=limit)

    return list(result)
