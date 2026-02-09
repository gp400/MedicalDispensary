import datetime
from typing import Optional

from fastapi import APIRouter, Depends

from db.database import get_db
from repositories.visit_repository import VisitRepository
from schemas.visit_schema import VisitSchema
from services.visit_service import VisitService

router = APIRouter()

def get_service(db = Depends(get_db)):
    repository = VisitRepository(db)
    service = VisitService(repository)
    return service

@router.get("/get_all")
def get_all_visit(
        doctor_id: Optional[int] = None,
        patient_id: Optional[int] = None,
        initial_date: Optional[datetime.date] = None,
        end_date: Optional[datetime.date] = None,
        service: VisitService = Depends(get_service)
):
    return service.get_all(doctor_id, patient_id, initial_date, end_date)

@router.get("/get_by_id/{id}")
def get_by_id_visit(id: int, service: VisitService = Depends(get_service)):
    return service.get_by_id(id)

@router.post("/create", status_code=201)
def create_visit(visit: VisitSchema, service: VisitService = Depends(get_service)):
    return service.create(visit)

@router.put("/update")
def update_visit(visit: VisitSchema, service: VisitService = Depends(get_service)):
    return service.update(visit)