from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.brand_schema import BrandSchema


class Brand(Base):
    __tablename__ = "Brand"

    def __init__(self, brand: BrandSchema):
        self.Id = brand.Id
        self.Name = brand.Name
        self.Description = brand.Description
        self.State = brand.State

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Description = Column(String)
    State = Column(Boolean)

    Medicines = relationship("Medicine", back_populates="Brand")