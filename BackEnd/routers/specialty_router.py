from fastapi import APIRouter, Depends

from db.database import get_db
from repositories.specialty_repository import SpecialtyRepository
from schemas.specialty_schema import SpecialtySchema
from services.specialty_service import SpecialtyService

router = APIRouter()

def get_service(db = Depends(get_db)):
    repository = SpecialtyRepository(db)
    service = SpecialtyService(repository)
    return service

@router.get("/get_all")
def get_all_specialty(service: SpecialtyService = Depends(get_service)):
    return service.get_all()

@router.get("/get_by_id/{id}")
def get_by_id_specialty(id: int, service: SpecialtyService = Depends(get_service)):
    return service.get_by_id(id)

@router.post("/create", status_code=201)
def create_specialty(specialty: SpecialtySchema, service: SpecialtyService = Depends(get_service)):
    return service.create(specialty)

@router.put("/update")
def update_specialty(specialty: SpecialtySchema, service: SpecialtyService = Depends(get_service)):
    return service.update(specialty)