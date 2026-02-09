from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models import DrugType
from schemas.drug_type_schema import DrugTypeSchema

class DrugTypeRepository:

    __not_found_message = "Farmaco no encontrado."

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[DrugTypeSchema]:
        drug_types: list[type[DrugType]] = self.db.query(DrugType).filter(DrugType.State).all()
        drug_types_mapped = list(map(lambda drug_type: DrugTypeSchema(Id=drug_type.Id, Name=drug_type.Name, Description=drug_type.Description, State=drug_type.State), drug_types))
        return drug_types_mapped

    def get_by_id(self, id: int) -> DrugTypeSchema:
        drug_type: type[DrugType] = self.db.query(DrugType).filter(DrugType.Id == id and DrugType.State).first()
        if drug_type is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        drug_type_mapped = DrugTypeSchema(Id=drug_type.Id, Name=drug_type.Name, Description=drug_type.Description, State=drug_type.State)
        return drug_type_mapped

    def create(self, drug_type_model: DrugTypeSchema) -> DrugTypeSchema:
        drug_type = DrugType(drug_type_model)
        drug_type.Id = None
        drug_type.State = True
        self.db.add(drug_type)
        self.db.commit()
        self.db.refresh(drug_type)
        return DrugTypeSchema(Id=drug_type.Id, Name=drug_type.Name, Description=drug_type.Description, State=drug_type.State)

    def update(self, drug_type_model: DrugTypeSchema) -> DrugTypeSchema:
        drug_type: type[DrugType] = self.db.query(DrugType).filter(DrugType.Id == drug_type_model.Id and DrugType.State).first()

        if drug_type.Medicines and drug_type_model.State == False:
            raise HTTPException(status_code=400, detail='El Farmaco posee Medicamentos relacionados.')

        if drug_type is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        drug_type.Name = drug_type_model.Name
        drug_type.Description = drug_type_model.Description
        drug_type.State = drug_type_model.State
        self.db.commit()
        self.db.refresh(drug_type)
        return DrugTypeSchema(Id=drug_type.Id, Name=drug_type.Name, Description=drug_type.Description,State=drug_type.State)