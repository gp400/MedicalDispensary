from repositories.location_repository import LocationRepository
from schemas.location_schema import LocationSchema

class LocationService:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, item: LocationSchema) -> LocationSchema:
        return self.repository.create(item)

    def update(self, item: LocationSchema) -> LocationSchema:
        return self.repository.update(item)