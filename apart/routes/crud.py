from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Optional

from ..models import ApartmentRecord, Apartment

router = APIRouter()


@router.post(
    path="/",
    response_description="Create new apart",
    status_code=status.HTTP_201_CREATED,
    response_model=ApartmentRecord,
)
def create_apartment(request: Request, apart: ApartmentRecord = Body(...)) -> ApartmentRecord:
    apart = jsonable_encoder(apart)
    new_apart = request.app.database["aparts"].insert_one(apart)
    created_apart = request.app.database["aparts"].find_one(
        {"_id": new_apart.inserted_id}
    )
    return created_apart


@router.get(
    path="/",
    response_description="List all aparts",
    response_model=List[ApartmentRecord],
)
def list_aparts(
        request: Request,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0) -> List[ApartmentRecord]:
    aparts = list(request.app.database["aparts"].find(limit=limit, skip=offset))
    return aparts


@router.get(
    path="/{id}",
    response_description="Get a single apart by id",
    response_model=ApartmentRecord,
)
def find_apart(id: str, request: Request) -> ApartmentRecord:
    if (apart := request.app.database["aparts"].apart({"_id": id})) is not None:
        return apart
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Apartment with ID {id} not found"
    )


@router.put(
    path="/{id}",
    response_description="Update a apartment",
    response_model=ApartmentRecord,
)
def update_apart(id: str, request: Request, apart: Apartment = Body(...)) -> ApartmentRecord:
    apart = {k: v for k, v in apart.dict().items() if v is not None}
    if len(apart) >= 1:
        update_result = request.app.database["aparts"].update_one(
            {"_id": id}, {"$set": apart}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Apart with ID {id} not found",
            )

    if (existing_book := request.app.database["aparts"].find_one({"_id": id})) is not None:
        return existing_book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Apart with ID {id} not found",
    )


@router.delete(
    path="/{id}",
    response_description="Delete a apartment",
)
def delete_apart(id: str, request: Request, response: Response):
    delete_result = request.app.database["aparts"].delete_one({"_id": id})

    if delete_result.delete_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Apart with ID {id} not found",
    )
