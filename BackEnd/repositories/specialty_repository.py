from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Specialty
from schemas.specialty_schema import SpecialtySchema


class SpecialtyRepository:

    __not_found_message = "Especialidad no encontrada."

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[SpecialtySchema]:
        specialties: list[type[Specialty]] = self.db.query(Specialty).filter(Specialty.State).all()
        specialties_mapped = list(map(lambda specialty: SpecialtySchema(Id=specialty.Id, Name=specialty.Name, Description=specialty.Description, State=specialty.State), specialties))
        return specialties_mapped

    def get_by_id(self, id: int) -> SpecialtySchema:
        specialty: type[Specialty] = self.db.query(Specialty).filter(Specialty.Id == id and Specialty.State).first()
        if specialty is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        specialty_mapped = SpecialtySchema(Id=specialty.Id, Name=specialty.Name, Description=specialty.Description, State=specialty.State)
        return specialty_mapped

    def create(self, specialty_model: SpecialtySchema) -> SpecialtySchema:
        specialty = Specialty(specialty_model)
        specialty.Id = None
        specialty.State = True
        self.db.add(specialty)
        self.db.commit()
        self.db.refresh(specialty)
        return SpecialtySchema(Id=specialty.Id, Name=specialty.Name, Description=specialty.Description, State=specialty.State)

    def update(self, specialty_model: SpecialtySchema) -> SpecialtySchema:
        specialty: type[Specialty] = self.db.query(Specialty).filter(Specialty.Id == specialty_model.Id and Specialty.State).first()

        if specialty.Doctors and specialty_model.State == False:
            raise HTTPException(status_code=400, detail='La Especialidad posee Doctores relacionados.')

        if specialty is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        specialty.Name = specialty_model.Name
        specialty.Description = specialty_model.Description
        specialty.State = specialty_model.State
        self.db.commit()
        self.db.refresh(specialty)
        return SpecialtySchema(Id=specialty.Id, Name=specialty.Name, Description=specialty.Description,State=specialty.State)