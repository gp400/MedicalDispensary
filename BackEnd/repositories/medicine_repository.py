from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from db.models import Medicine
from schemas.brand_schema import BrandSchema
from schemas.drug_type_schema import DrugTypeSchema
from schemas.location_schema import LocationSchema
from schemas.medicine_schema import MedicineSchema


class MedicineRepository:

    __not_found_message = "Medicina no encontrada."

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[MedicineSchema]:
        medicines: list[type[Medicine]] = self.db.query(Medicine).filter(Medicine.State).all()
        medicines_mapped = list(map(lambda medicine: MedicineSchema(
            Id=medicine.Id,
            Description=medicine.Description,
            DrugTypeId=medicine.DrugTypeId,
            BrandId=medicine.BrandId,
            LocationId=medicine.LocationId,
            Dose=medicine.Dose,
            State=medicine.State,
            DrugTypeModel=DrugTypeSchema(Id=medicine.DrugType.Id, Name=medicine.DrugType.Name, Description=medicine.DrugType.Description, State=medicine.DrugType.State),
            BrandModel=BrandSchema(Id=medicine.Brand.Id, Name=medicine.Brand.Name, Description=medicine.Brand.Description, State=medicine.Brand.State),
            LocationModel=LocationSchema(Id=medicine.Location.Id, Description=medicine.Location.Description, Shelf=medicine.Location.Shelf, Section=medicine.Location.Section, Cell=medicine.Location.Cell, State=medicine.Location.State)
        ), medicines))
        return medicines_mapped

    def get_by_id(self, id: int) -> MedicineSchema:
        medicine: type[Medicine] = self.db.query(Medicine).filter(Medicine.Id == id and Medicine.State).first()
        if medicine is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        medicine_mapped = MedicineSchema(
            Id=medicine.Id,
            Description=medicine.Description,
            DrugTypeId=medicine.DrugTypeId,
            BrandId=medicine.BrandId,
            LocationId=medicine.LocationId,
            Dose=medicine.Dose,
            State=medicine.State,
            DrugTypeModel=DrugTypeSchema(Id=medicine.DrugType.Id, Name=medicine.DrugType.Name, Description=medicine.DrugType.Description, State=medicine.DrugType.State),
            BrandModel=BrandSchema(Id=medicine.Brand.Id, Name=medicine.Brand.Name, Description=medicine.Brand.Description, State=medicine.Brand.State),
            LocationModel=LocationSchema(Id=medicine.Location.Id, Description=medicine.Location.Description, Shelf=medicine.Location.Shelf, Section=medicine.Location.Section, Cell=medicine.Location.Cell, State=medicine.Location.State)
        )
        return medicine_mapped

    def create(self, medicine_model: MedicineSchema) -> MedicineSchema:
        medicine = Medicine(medicine_model)
        medicine.Id = None
        medicine.State = True
        self.db.add(medicine)
        self.db.commit()
        self.db.refresh(medicine)
        return MedicineSchema(
            Id=medicine.Id,
            Description=medicine.Description,
            DrugTypeId=medicine.DrugTypeId,
            BrandId=medicine.BrandId,
            LocationId=medicine.LocationId,
            Dose=medicine.Dose,
            State=medicine.State,
            DrugTypeModel=DrugTypeSchema(Id=medicine.DrugType.Id, Name=medicine.DrugType.Name, Description=medicine.DrugType.Description, State=medicine.DrugType.State),
            BrandModel=BrandSchema(Id=medicine.Brand.Id, Name=medicine.Brand.Name, Description=medicine.Brand.Description, State=medicine.Brand.State),
            LocationModel=LocationSchema(Id=medicine.Location.Id, Description=medicine.Location.Description, Shelf=medicine.Location.Shelf, Section=medicine.Location.Section, Cell=medicine.Location.Cell, State=medicine.Location.State)
        )

    def update(self, medicine_model: MedicineSchema) -> MedicineSchema:
        medicine: type[Medicine] = self.db.query(Medicine).filter(Medicine.Id == medicine_model.Id and Medicine.State).first()

        if medicine is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        if len(medicine.MedicineVisits) > 0 and medicine_model.State == False:
            raise HTTPException(status_code=400, detail='La Medicina posee Visitas relacionadas.')

        medicine.Id = medicine_model.Id
        medicine.Description = medicine_model.Description
        medicine.DrugTypeId = medicine_model.DrugTypeId
        medicine.BrandId = medicine_model.BrandId
        medicine.LocationId = medicine_model.LocationId
        medicine.Dose = medicine_model.Dose
        medicine.State = medicine_model.State
        self.db.commit()
        self.db.refresh(medicine)
        return MedicineSchema(
            Id=medicine.Id,
            Description=medicine.Description,
            DrugTypeId=medicine.DrugTypeId,
            BrandId=medicine.BrandId,
            LocationId=medicine.LocationId,
            Dose=medicine.Dose,
            State=medicine.State,
            DrugTypeModel=DrugTypeSchema(Id=medicine.DrugType.Id, Name=medicine.DrugType.Name, Description=medicine.DrugType.Description, State=medicine.DrugType.State),
            BrandModel=BrandSchema(Id=medicine.Brand.Id, Name=medicine.Brand.Name, Description=medicine.Brand.Description, State=medicine.Brand.State),
            LocationModel=LocationSchema(Id=medicine.Location.Id, Description=medicine.Location.Description, Shelf=medicine.Location.Shelf, Section=medicine.Location.Section, Cell=medicine.Location.Cell, State=medicine.Location.State)
        )