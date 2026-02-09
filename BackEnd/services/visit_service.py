import datetime
from typing import Optional

from repositories.visit_repository import VisitRepository
from schemas.visit_schema import VisitSchema

class VisitService:
    def __init__(self, repository: VisitRepository):
        self.repository = repository

    def get_all(
            self,
            doctor_id: Optional[int] = None,
            patient_id: Optional[int] = None,
            initial_date: Optional[datetime.date] = None,
            end_date: Optional[datetime.date] = None
    ):
        return self.repository.get_all(initial_date, end_date, doctor_id, patient_id)

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, item: VisitSchema) -> VisitSchema:
        return self.repository.create(item)

    def update(self, item: VisitSchema) -> VisitSchema:
        return self.repository.update(item)