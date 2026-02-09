from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

from db.database import Base
from schemas.specialty_schema import SpecialtySchema

class Specialty(Base):
    __tablename__ = "Specialty"

    def __init__(self, specialty: SpecialtySchema):
        self.Id = specialty.Id
        self.Name = specialty.Name
        self.Description = specialty.Description
        self.State = specialty.State

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Description = Column(String)
    State = Column(Boolean)

    Doctors = relationship("Doctor", back_populates="Specialty")