from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.location_schema import LocationSchema


class Location(Base):
    __tablename__ = "Location"

    def __init__(self, location: LocationSchema):
        self.Id = location.Id
        self.Description = location.Description
        self.Shelf = location.Shelf
        self.Section = location.Section
        self.Cell = location.Cell
        self.State = location.State

    Id = Column(Integer, primary_key=True, index=True)
    Description = Column(String)
    Shelf = Column(String)
    Section = Column(String)
    Cell = Column(String)
    State = Column(Boolean)

    Medicines = relationship("Medicine", back_populates="Location")