from repositories.medicine_repository import MedicineRepository
from schemas.medicine_schema import MedicineSchema


class MedicineService:
    def __init__(self, repository: MedicineRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, item: MedicineSchema) -> MedicineSchema:
        return self.repository.create(item)

    def update(self, item: MedicineSchema) -> MedicineSchema:
        return self.repository.update(item)