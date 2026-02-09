from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.medicine_schema import MedicineSchema


class Medicine(Base):
    __tablename__ = "Medicine"

    def __init__(self, medicine: MedicineSchema):
        self.Id = medicine.Id
        self.Description = medicine.Description
        self.DrugTypeId = medicine.DrugTypeId
        self.BrandId = medicine.BrandId
        self.LocationId = medicine.LocationId
        self.Dose = medicine.Dose
        self.State = medicine.State

    Id = Column(Integer, primary_key=True, index=True)
    Description = Column(String)
    DrugTypeId = Column(Integer, ForeignKey("DrugType.Id"))
    BrandId = Column(Integer, ForeignKey("Brand.Id"))
    LocationId = Column(Integer, ForeignKey("Location.Id"))
    Dose = Column(Integer)
    State = Column(Boolean)

    DrugType = relationship("DrugType", back_populates="Medicines")
    Brand = relationship("Brand", back_populates="Medicines")
    Location = relationship("Location", back_populates="Medicines")

    MedicineVisits = relationship("MedicineVisit", back_populates="Medicine")