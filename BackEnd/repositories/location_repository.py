from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Location
from schemas.location_schema import LocationSchema


class LocationRepository:

    __not_found_message = "Ubicacion no encontrada."

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[LocationSchema]:
        locations: list[type[Location]] = self.db.query(Location).filter(Location.State).all()
        locations_mapped = list(map(lambda location: LocationSchema(Id=location.Id, Description=location.Description, Shelf=location.Shelf, Section=location.Section, Cell=location.Cell, State=location.State), locations))
        return locations_mapped

    def get_by_id(self, id: int) -> LocationSchema:
        location: type[Location] = self.db.query(Location).filter(Location.Id == id and Location.State).first()
        if location is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        location_mapped = LocationSchema(Id=location.Id, Description=location.Description, Shelf=location.Shelf, Section=location.Section, Cell=location.Cell, State=location.State)
        return location_mapped

    def create(self, location_model: LocationSchema) -> LocationSchema:
        location = Location(location_model)
        location.Id = None
        location.State = True
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return LocationSchema(Id=location.Id, Description=location.Description, Shelf=location.Shelf, Section=location.Section, Cell=location.Cell, State=location.State)

    def update(self, location_model: LocationSchema) -> LocationSchema:
        location: type[Location] = self.db.query(Location).filter(Location.Id == location_model.Id and Location.State).first()

        if location.Medicines and location_model.State == False:
            raise HTTPException(status_code=400, detail='La Ubicacion posee Medicamentos relacionados.')

        if location is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        location.Id = location_model.Id
        location.Description = location_model.Description
        location.Shelf = location_model.Shelf
        location.Section = location_model.Section
        location.Cell = location_model.Cell
        location.State = location_model.State
        self.db.commit()
        self.db.refresh(location)
        return LocationSchema(Id=location.Id, Description=location.Description, Shelf=location.Shelf, Section=location.Section, Cell=location.Cell, State=location.State)