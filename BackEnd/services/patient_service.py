from repositories.patient_repository import PatientRepository
from schemas.patient_schema import PatientSchema

class PatientService:
    def __init__(self, repository: PatientRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, item: PatientSchema) -> PatientSchema:
        return self.repository.create(item)

    def update(self, item: PatientSchema) -> PatientSchema:
        return self.repository.update(item)