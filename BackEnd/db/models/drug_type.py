from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.drug_type_schema import DrugTypeSchema

class DrugType(Base):
    __tablename__ = "DrugType"

    def __init__(self, drug_type: DrugTypeSchema):
        self.Id = drug_type.Id
        self.Name = drug_type.Name
        self.Description = drug_type.Description
        self.State = drug_type.State

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Description = Column(String)
    State = Column(Boolean)

    Medicines = relationship("Medicine", back_populates="DrugType")