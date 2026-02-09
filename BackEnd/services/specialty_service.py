from repositories.specialty_repository import SpecialtyRepository
from schemas.specialty_schema import SpecialtySchema

class SpecialtyService:
    def __init__(self, repository: SpecialtyRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, item: SpecialtySchema) -> SpecialtySchema:
        return self.repository.create(item)

    def update(self, item: SpecialtySchema) -> SpecialtySchema:
        return self.repository.update(item)