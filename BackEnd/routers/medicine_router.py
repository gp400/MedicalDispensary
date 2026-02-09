from fastapi import APIRouter, Depends

from db.database import get_db
from repositories.medicine_repository import MedicineRepository
from schemas.medicine_schema import MedicineSchema
from services.medicine_service import MedicineService

router = APIRouter()

def get_service(db = Depends(get_db)):
    repository = MedicineRepository(db)
    service = MedicineService(repository)
    return service

@router.get("/get_all")
def get_all_brand(service: MedicineService = Depends(get_service)):
    return service.get_all()

@router.get("/get_by_id/{id}")
def get_by_id_brand(id: int, service: MedicineService = Depends(get_service)):
    return service.get_by_id(id)

@router.post("/create", status_code=201)
def create_brand(medicine: MedicineSchema, service: MedicineService = Depends(get_service)):
    return service.create(medicine)

@router.put("/update")
def update_brand(medicine: MedicineSchema, service: MedicineService = Depends(get_service)):
    return service.update(medicine)