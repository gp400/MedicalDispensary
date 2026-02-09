from fastapi import APIRouter, Depends

from db.database import get_db
from repositories.patient_repository import PatientRepository
from schemas.patient_schema import PatientSchema
from services.patient_service import PatientService

router = APIRouter()

def get_service(db = Depends(get_db)):
    repository = PatientRepository(db)
    service = PatientService(repository)
    return service

@router.get("/get_all")
def get_all_brand(service: PatientService = Depends(get_service)):
    return service.get_all()

@router.get("/get_by_id/{id}")
def get_by_id_brand(id: int, service: PatientService = Depends(get_service)):
    return service.get_by_id(id)

@router.post("/create", status_code=201)
def create_brand(patient: PatientSchema, service: PatientService = Depends(get_service)):
    return service.create(patient)

@router.put("/update")
def update_brand(patient: PatientSchema, service: PatientService = Depends(get_service)):
    return service.update(patient)