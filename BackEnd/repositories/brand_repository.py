from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Brand
from schemas.brand_schema import BrandSchema


class BrandRepository:

    __not_found_message = "Marca no encontrada."

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[BrandSchema]:
        brands: list[type[Brand]] = self.db.query(Brand).filter(Brand.State).all()
        brands_mapped = list(map(lambda brand: BrandSchema(Id=brand.Id, Name=brand.Name, Description=brand.Description, State=brand.State), brands))
        return brands_mapped

    def get_by_id(self, id: int) -> BrandSchema:
        brand: type[Brand] = self.db.query(Brand).filter(Brand.Id == id and Brand.State).first()
        if brand is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        brand_mapped = BrandSchema(Id=brand.Id, Name=brand.Name, Description=brand.Description, State=brand.State)
        return brand_mapped

    def create(self, brand_model: BrandSchema) -> BrandSchema:
        brand = Brand(brand_model)
        brand.Id = None
        brand.State = True
        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)
        return BrandSchema(Id=brand.Id, Name=brand.Name, Description=brand.Description, State=brand.State)

    def update(self, brand_model: BrandSchema) -> BrandSchema:
        brand: type[Brand] = self.db.query(Brand).filter(Brand.Id == brand_model.Id and Brand.State).first()

        if brand.Medicines and brand_model.State == False:
            raise HTTPException(status_code=400, detail='La Marca posee Medicamentos relacionados.')

        if brand is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        brand.Name = brand_model.Name
        brand.Description = brand_model.Description
        brand.State = brand_model.State
        self.db.commit()
        self.db.refresh(brand)
        return BrandSchema(Id=brand.Id, Name=brand.Name, Description=brand.Description,State=brand.State)