from pydantic import BaseModel
from enums.patient_type import PatientType

class PatientSchema(BaseModel):

    Id: int | None
    Name: str
    Identification: str
    LicenseNumber: str
    Type: PatientType
    State: bool