from repositories.doctor_repository import DoctorRepository
from schemas.doctor_schema import DoctorSchema

class DoctorService:
    def __init__(self, repository: DoctorRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, item: DoctorSchema) -> DoctorSchema:
        return self.repository.create(item)

    def update(self, item: DoctorSchema) -> DoctorSchema:
        return self.repository.update(item)