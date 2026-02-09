from repositories.drug_type_repository import DrugTypeRepository
from schemas.drug_type_schema import DrugTypeSchema

class DrugTypeService:
    def __init__(self, repository: DrugTypeRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, item: DrugTypeSchema) -> DrugTypeSchema:
        return self.repository.create(item)

    def update(self, item: DrugTypeSchema) -> DrugTypeSchema:
        return self.repository.update(item)