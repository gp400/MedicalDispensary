from fastapi import APIRouter, Depends
from db.database import get_db
from repositories.drug_type_repository import DrugTypeRepository
from schemas.drug_type_schema import DrugTypeSchema
from services.drug_type_service import DrugTypeService

router = APIRouter()

def get_service(db = Depends(get_db)):
    repository = DrugTypeRepository(db)
    service = DrugTypeService(repository)
    return service

@router.get("/get_all")
def get_all_brand(service: DrugTypeService = Depends(get_service)):
    return service.get_all()

@router.get("/get_by_id/{id}")
def get_by_id_brand(id: int, service: DrugTypeService = Depends(get_service)):
    return service.get_by_id(id)

@router.post("/create", status_code=201)
def create_brand(drup_type: DrugTypeSchema, service: DrugTypeService = Depends(get_service)):
    return service.create(drup_type)

@router.put("/update")
def update_brand(drup_type: DrugTypeSchema, service: DrugTypeService = Depends(get_service)):
    return service.update(drup_type)