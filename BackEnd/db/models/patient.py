from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.patient_schema import PatientSchema


class Patient(Base):
    __tablename__ = "Patient"

    def __init__(self, patient: PatientSchema):
        self.Id = patient.Id
        self.Name = patient.Name
        self.Identification = patient.Identification
        self.LicenseNumber = patient.LicenseNumber
        self.Type = patient.Type.value
        self.State = patient.State

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Identification = Column(String)
    LicenseNumber = Column(String)
    Type = Column(Integer) # Enum Estudiante, Empleado, Profesor, Otros
    State = Column(Boolean)

    Visits = relationship("Visit", back_populates="Patient")