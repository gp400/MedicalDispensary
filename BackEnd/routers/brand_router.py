from fastapi import APIRouter, Depends
from db.database import get_db
from repositories.brand_repository import BrandRepository
from schemas.brand_schema import BrandSchema
from services.brand_service import BrandService

router = APIRouter()

def get_service(db = Depends(get_db)):
    repository = BrandRepository(db)
    service = BrandService(repository)
    return service

@router.get("/get_all")
def get_all_brand(service: BrandService = Depends(get_service)):
    return service.get_all()

@router.get("/get_by_id/{id}")
def get_by_id_brand(id: int, service: BrandService = Depends(get_service)):
    return service.get_by_id(id)

@router.post("/create", status_code=201)
def create_brand(brand: BrandSchema, service: BrandService = Depends(get_service)):
    return service.create(brand)

@router.put("/update")
def update_brand(brand: BrandSchema, service: BrandService = Depends(get_service)):
    return service.update(brand)