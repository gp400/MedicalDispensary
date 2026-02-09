from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from db.models import MedicineVisit
from schemas.visit_schema import VisitSchema


class Visit(Base):
    __tablename__ = "Visit"

    def __init__(self, visit: VisitSchema):
        self.Id = visit.Id
        self.DoctorId = visit.DoctorId
        self.PatientId = visit.PatientId
        self.Date = visit.Date
        self.Time = datetime.strptime(visit.Time, "%H:%M").time()
        self.Symptoms = visit.Symptoms
        self.Recommendations = visit.Recommendations
        self.State = visit.State
        self.MedicineVisits = list(map(lambda mv: MedicineVisit(mv), visit.MedicineVisits))

    Id = Column(Integer, primary_key=True, index=True)
    DoctorId = Column(Integer, ForeignKey("Doctor.Id"))
    PatientId = Column(Integer, ForeignKey("Patient.Id"))
    Date = Column(Date)
    Time = Column(Time)
    Symptoms = Column(String)
    Recommendations = Column(String)
    State = Column(Boolean)

    Doctor = relationship("Doctor", back_populates="Visits")
    Patient = relationship("Patient", back_populates="Visits")

    MedicineVisits = relationship("MedicineVisit", back_populates="Visit")