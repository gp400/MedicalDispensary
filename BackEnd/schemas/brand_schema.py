from pydantic import BaseModel

class BrandSchema(BaseModel):

    Id: int | None
    Name: str
    Description: str
    State: bool