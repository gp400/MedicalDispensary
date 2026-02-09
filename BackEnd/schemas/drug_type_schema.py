from pydantic import BaseModel

class DrugTypeSchema(BaseModel):

    Id: int | None
    Name: str
    Description: str
    State: bool