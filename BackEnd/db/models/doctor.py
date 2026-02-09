from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.doctor_schema import DoctorSchema


class Doctor(Base):
    __tablename__ = "Doctor"

    def __init__(self, doctor: DoctorSchema):
        self.Id = doctor.Id
        self.Name = doctor.Name
        self.Identification = doctor.Identification
        self.BatchWork = doctor.BatchWork.value
        self.SpecialtyId = doctor.SpecialtyId
        self.State = doctor.State

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Identification = Column(String)
    BatchWork = Column(Integer) # Enum Moring, tarde, noche
    SpecialtyId = Column(Integer, ForeignKey('Specialty.Id', name='fk_doctor_specialty_id'))
    State = Column(Boolean)

    Visits = relationship("Visit", back_populates="Doctor")
    Specialty = relationship("Specialty", back_populates="Doctors")