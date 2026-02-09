from fastapi import APIRouter, Depends

from db.database import get_db
from repositories.doctor_repository import DoctorRepository
from schemas.doctor_schema import DoctorSchema
from services.doctor_service import DoctorService

router = APIRouter()

def get_service(db = Depends(get_db)):
    repository = DoctorRepository(db)
    service = DoctorService(repository)
    return service

@router.get("/get_all")
def get_all_brand(service: DoctorService = Depends(get_service)):
    return service.get_all()

@router.get("/get_by_id/{id}")
def get_by_id_brand(id: int, service: DoctorService = Depends(get_service)):
    return service.get_by_id(id)

@router.post("/create", status_code=201)
def create_brand(doctor: DoctorSchema, service: DoctorService = Depends(get_service)):
    return service.create(doctor)

@router.put("/update")
def update_brand(doctor: DoctorSchema, service: DoctorService = Depends(get_service)):
    return service.update(doctor)