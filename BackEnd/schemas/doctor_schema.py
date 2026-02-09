from pydantic import BaseModel
from enums.doctor_batch_work import DoctorBatchWork
from schemas.specialty_schema import SpecialtySchema


class DoctorSchema(BaseModel):

    Id: int | None
    Name: str
    Identification: str
    BatchWork: DoctorBatchWork
    SpecialtyId: int
    State: bool

    Specialty: SpecialtySchema | None = None