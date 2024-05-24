from fastapi import APIRouter, Request
from typing import List

from ..models import ApartmentRecord, Place

router = APIRouter()


@router.get(
    path="get_aparts",
    response_description="Returns recomended aparts",
    response_model=List[ApartmentRecord],
)
def get_aparts(request: Request, places: List[Place]) -> List[ApartmentRecord]:
    aparts = list(request.app.database["aparts"].find(limit=10))
    return aparts
