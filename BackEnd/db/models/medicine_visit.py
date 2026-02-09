from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.medicine_visit_schema import MedicineVisitSchema


class MedicineVisit(Base):
    __tablename__ = "MedicineVisit"

    def __init__(self, medicine_visit: MedicineVisitSchema):
        self.Id = medicine_visit.Id
        self.MedicineId = medicine_visit.MedicineId
        self.VisitId = medicine_visit.VisitId
        self.State = medicine_visit.State

    Id = Column(Integer, primary_key=True, index=True)
    MedicineId = Column(Integer, ForeignKey("Medicine.Id"))
    VisitId = Column(Integer, ForeignKey("Visit.Id"))
    State = Column(Boolean)

    Medicine = relationship("Medicine", back_populates="MedicineVisits")
    Visit = relationship("Visit", back_populates="MedicineVisits")