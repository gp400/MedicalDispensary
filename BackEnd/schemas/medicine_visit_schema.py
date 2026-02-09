from pydantic import BaseModel
from schemas.medicine_schema import MedicineSchema

class MedicineVisitSchema(BaseModel):

    Id: int | None
    MedicineId: int
    VisitId: int | None
    State: bool

    MedicineModel: MedicineSchema | None = None