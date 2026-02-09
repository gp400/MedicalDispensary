from pydantic import BaseModel
from schemas.brand_schema import BrandSchema
from schemas.drug_type_schema import DrugTypeSchema
from schemas.location_schema import LocationSchema


class MedicineSchema(BaseModel):

    Id: int | None
    Description: str
    DrugTypeId: int
    BrandId: int
    LocationId: int
    Dose: int
    State: bool

    DrugTypeModel: DrugTypeSchema | None = None
    BrandModel: BrandSchema | None = None
    LocationModel: LocationSchema | None = None