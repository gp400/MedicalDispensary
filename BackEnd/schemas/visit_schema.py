import datetime
from pydantic import BaseModel

from schemas.doctor_schema import DoctorSchema
from schemas.medicine_visit_schema import MedicineVisitSchema
from schemas.patient_schema import PatientSchema


class VisitSchema(BaseModel):

    Id: int | None
    DoctorId: int
    PatientId: int
    Date: datetime.date
    Time: str
    Symptoms: str
    Recommendations: str
    State: bool

    DoctorModel: DoctorSchema | None = None
    PatientModel: PatientSchema | None = None

    MedicineVisits: list[MedicineVisitSchema] = []