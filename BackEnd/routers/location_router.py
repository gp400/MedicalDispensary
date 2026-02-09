from fastapi import APIRouter, Depends

from db.database import get_db
from repositories.location_repository import LocationRepository
from schemas.location_schema import LocationSchema
from services.location_service import LocationService

router = APIRouter()

def get_service(db = Depends(get_db)):
    repository = LocationRepository(db)
    service = LocationService(repository)
    return service

@router.get("/get_all")
def get_all_brand(service: LocationService = Depends(get_service)):
    return service.get_all()

@router.get("/get_by_id/{id}")
def get_by_id_brand(id: int, service: LocationService = Depends(get_service)):
    return service.get_by_id(id)

@router.post("/create", status_code=201)
def create_brand(location: LocationSchema, service: LocationService = Depends(get_service)):
    return service.create(location)

@router.put("/update")
def update_brand(location: LocationSchema, service: LocationService = Depends(get_service)):
    return service.update(location)