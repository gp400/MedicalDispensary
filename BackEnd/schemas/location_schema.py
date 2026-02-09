from pydantic import BaseModel

class LocationSchema(BaseModel):

    Id: int | None
    Description: str
    Shelf: str
    Section: str
    Cell: str
    State: bool