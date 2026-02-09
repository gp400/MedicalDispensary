from pydantic import BaseModel

class SpecialtySchema(BaseModel):

    Id: int | None
    Name: str
    Description: str
    State: bool