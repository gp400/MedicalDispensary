from repositories.brand_repository import BrandRepository
from schemas.brand_schema import BrandSchema

class BrandService:
    def __init__(self, repository: BrandRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, item: BrandSchema) -> BrandSchema:
        return self.repository.create(item)

    def update(self, item: BrandSchema) -> BrandSchema:
        return self.repository.update(item)