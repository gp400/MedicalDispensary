from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Patient
from enums.patient_type import PatientType
from schemas.patient_schema import PatientSchema


class PatientRepository:

    __not_found_message = "Paciente no encontrado."

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[PatientSchema]:
        patients: list[type[Patient]] = self.db.query(Patient).filter(Patient.State).all()
        patients_mapped = list(map(lambda patient: PatientSchema(Id=patient.Id, Name=patient.Name, Identification=patient.Identification, LicenseNumber=patient.LicenseNumber, Type=PatientType(patient.Type), State=patient.State), patients))
        return patients_mapped

    def get_by_id(self, id: int) -> PatientSchema:
        patient: type[Patient] = self.db.query(Patient).filter(Patient.Id == id and Patient.State).first()
        if patient is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        patient_mapped = PatientSchema(Id=patient.Id, Name=patient.Name, Identification=patient.Identification, LicenseNumber=patient.LicenseNumber, Type=PatientType(patient.Type), State=patient.State)
        return patient_mapped

    def create(self, patient_model: PatientSchema) -> PatientSchema:
        patient = Patient(patient_model)
        patient.Id = None
        patient.State = True
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return PatientSchema(Id=patient.Id, Name=patient.Name, Identification=patient.Identification, LicenseNumber=patient.LicenseNumber, Type=PatientType(patient.Type), State=patient.State)

    def update(self, patient_model: PatientSchema) -> PatientSchema:
        patient: type[Patient] = self.db.query(Patient).filter(Patient.Id == patient_model.Id and Patient.State).first()

        if patient.Visits and patient_model.State == False:
            raise HTTPException(status_code=400, detail='El Paciente posee Visitas relacionadas.')

        if patient is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        patient.Id = patient_model.Id
        patient.Name = patient_model.Name
        patient.Identification = patient_model.Identification
        patient.LicenseNumber = patient_model.LicenseNumber
        patient.Type = patient_model.Type.value
        patient.State = patient_model.State
        self.db.commit()
        self.db.refresh(patient)
        return PatientSchema(Id=patient.Id, Name=patient.Name, Identification=patient.Identification, LicenseNumber=patient.LicenseNumber, Type=PatientType(patient.Type), State=patient.State)