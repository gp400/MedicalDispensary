from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Doctor, Specialty
from enums.doctor_batch_work import DoctorBatchWork
from schemas.doctor_schema import DoctorSchema
from schemas.specialty_schema import SpecialtySchema


class DoctorRepository:

    __not_found_message = "Paciente no encontrado."

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[DoctorSchema]:
        doctors: list[type[Doctor]] = self.db.query(Doctor).filter(Doctor.State).all()
        doctors_mapped = list(map(lambda doctor: DoctorSchema(
            Id=doctor.Id,
            Name=doctor.Name,
            Identification=doctor.Identification,
            BatchWork=DoctorBatchWork(doctor.BatchWork),
            SpecialtyId=doctor.SpecialtyId,
            State=doctor.State,
            Specialty=SpecialtySchema(Id=doctor.Specialty.Id, Name=doctor.Specialty.Name, Description=doctor.Specialty.Description, State=doctor.Specialty.State)
        ), doctors))
        return doctors_mapped

    def get_by_id(self, id: int) -> DoctorSchema:
        doctor: type[Doctor] = self.db.query(Doctor).filter(Doctor.Id == id and Doctor.State).first()
        if doctor is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        doctor_mapped = DoctorSchema(
            Id=doctor.Id,
            Name=doctor.Name,
            Identification=doctor.Identification,
            BatchWork=DoctorBatchWork(doctor.BatchWork),
            SpecialtyId=doctor.SpecialtyId,
            State=doctor.State,
            Specialty=SpecialtySchema(Id=doctor.Specialty.Id, Name=doctor.Specialty.Name, Description=doctor.Specialty.Description, State=doctor.Specialty.State)
        )
        return doctor_mapped

    def create(self, doctor_model: DoctorSchema) -> DoctorSchema:
        doctor = Doctor(doctor_model)
        doctor.Id = None
        doctor.State = True
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        return DoctorSchema(
            Id=doctor.Id,
            Name=doctor.Name,
            Identification=doctor.Identification,
            BatchWork=DoctorBatchWork(doctor.BatchWork),
            SpecialtyId=doctor.SpecialtyId,
            State=doctor.State,
            Specialty=SpecialtySchema(Id=doctor.Specialty.Id, Name=doctor.Specialty.Name, Description=doctor.Specialty.Description, State=doctor.Specialty.State)
        )

    def update(self, doctor_model: DoctorSchema) -> DoctorSchema:
        doctor: type[Doctor] = self.db.query(Doctor).filter(Doctor.Id == doctor_model.Id and Doctor.State).first()

        if doctor.Visits and doctor_model.State == False:
            raise HTTPException(status_code=400, detail='El Doctor posee Visitas relacionadas.')

        if doctor is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        doctor.Id = doctor_model.Id
        doctor.Name = doctor_model.Name
        doctor.Identification = doctor_model.Identification
        doctor.BatchWork = doctor_model.BatchWork.value
        doctor.SpecialtyId = doctor_model.SpecialtyId
        doctor.State = doctor_model.State
        self.db.commit()
        self.db.refresh(doctor)
        return DoctorSchema(
            Id=doctor.Id,
            Name=doctor.Name,
            Identification=doctor.Identification,
            BatchWork=DoctorBatchWork(doctor.BatchWork),
            SpecialtyId=doctor.SpecialtyId,
            State=doctor.State,
            Specialty=SpecialtySchema(Id=doctor.Specialty.Id, Name=doctor.Specialty.Name, Description=doctor.Specialty.Description, State=doctor.Specialty.State)
        )