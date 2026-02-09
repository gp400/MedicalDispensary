from datetime import datetime, date
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Visit, visit, MedicineVisit
from enums.doctor_batch_work import DoctorBatchWork
from enums.patient_type import PatientType
from schemas.brand_schema import BrandSchema
from schemas.doctor_schema import DoctorSchema
from schemas.drug_type_schema import DrugTypeSchema
from schemas.location_schema import LocationSchema
from schemas.medicine_schema import MedicineSchema
from schemas.medicine_visit_schema import MedicineVisitSchema
from schemas.patient_schema import PatientSchema
from schemas.specialty_schema import SpecialtySchema
from schemas.visit_schema import VisitSchema

class VisitRepository:

    __not_found_message = "Visita no encontrada."
    __medicine_required_message = "Las Medicinas son requeridas."

    def __init__(self, db: Session):
        self.db = db

    def get_all(
            self,
            initial_date: Optional[date] = None,
            end_date: Optional[date] = None,
            doctor_id: Optional[int] = None,
            patient_id: Optional[int] = None,
    ) -> list[VisitSchema]:

        query = self.db.query(Visit).filter(Visit.State == True)

        if initial_date is not None:
            query = query.filter(Visit.Date >= initial_date)

        if end_date is not None:
            query = query.filter(Visit.Date <= end_date)

        if doctor_id is not None:
            query = query.filter(Visit.DoctorId == doctor_id)

        if patient_id is not None:
            query = query.filter(Visit.PatientId == patient_id)

        visits: list[type[Visit]] = query.all()
        visits_mapped = list(map(lambda visit: VisitSchema(
            Id=visit.Id,
            DoctorId=visit.DoctorId,
            PatientId=visit.PatientId,
            Date=visit.Date,
            Time=visit.Time.strftime("%H:%M"),
            Symptoms=visit.Symptoms,
            Recommendations=visit.Recommendations,
            State=visit.State,
            DoctorModel=DoctorSchema(
                Id=visit.Doctor.Id,
                Name=visit.Doctor.Name,
                Identification=visit.Doctor.Identification,
                BatchWork=DoctorBatchWork(visit.Doctor.BatchWork),
                SpecialtyId=visit.Doctor.SpecialtyId,
                State=visit.Doctor.State,
                Specialty=SpecialtySchema(Id=visit.Doctor.Specialty.Id, Name=visit.Doctor.Specialty.Name, Description=visit.Doctor.Specialty.Description, State=visit.Doctor.Specialty.State)
            ),
            PatientModel=PatientSchema(Id=visit.Patient.Id, Name=visit.Patient.Name, Identification=visit.Patient.Identification, LicenseNumber=visit.Patient.LicenseNumber, Type=PatientType(visit.Patient.Type), State=visit.Patient.State),
            MedicineVisits=list(map(lambda mv: MedicineVisitSchema(
                Id=mv.Id,
                MedicineId=mv.MedicineId,
                VisitId=mv.VisitId,
                State=mv.State,
                MedicineModel=MedicineSchema(
                    Id=mv.Medicine.Id,
                    Description=mv.Medicine.Description,
                    DrugTypeId=mv.Medicine.DrugTypeId,
                    BrandId=mv.Medicine.BrandId,
                    LocationId=mv.Medicine.LocationId,
                    Dose=mv.Medicine.Dose,
                    State=mv.Medicine.State,
                    DrugTypeModel=DrugTypeSchema(Id=mv.Medicine.DrugType.Id, Name=mv.Medicine.DrugType.Name, Description=mv.Medicine.DrugType.Description, State=mv.Medicine.DrugType.State),
                    BrandModel=BrandSchema(Id=mv.Medicine.Brand.Id, Name=mv.Medicine.Brand.Name, Description=mv.Medicine.Brand.Description, State=mv.Medicine.Brand.State),
                    LocationModel=LocationSchema(Id=mv.Medicine.Location.Id, Description=mv.Medicine.Location.Description, Shelf=mv.Medicine.Location.Shelf, Section=mv.Medicine.Location.Section, Cell=mv.Medicine.Location.Cell, State=mv.Medicine.Location.State)
                )), visit.MedicineVisits
            ))
        ), visits))
        return visits_mapped

    def get_by_id(self, id: int) -> VisitSchema:
        visit: type[Visit] = self.db.query(Visit).filter(Visit.Id == id and Visit.State).first()
        if visit is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        visit_mapped = VisitSchema(
            Id=visit.Id,
            DoctorId=visit.DoctorId,
            PatientId=visit.PatientId,
            Date=visit.Date,
            Time=visit.Time.strftime("%H:%M"),
            Symptoms=visit.Symptoms,
            Recommendations=visit.Recommendations,
            State=visit.State,
            DoctorModel=DoctorSchema(
                Id=visit.Doctor.Id,
                Name=visit.Doctor.Name,
                Identification=visit.Doctor.Identification,
                BatchWork=DoctorBatchWork(visit.Doctor.BatchWork),
                SpecialtyId=visit.Doctor.SpecialtyId,
                State=visit.Doctor.State,
                Specialty=SpecialtySchema(Id=visit.Doctor.Specialty.Id, Name=visit.Doctor.Specialty.Name, Description=visit.Doctor.Specialty.Description, State=visit.Doctor.Specialty.State)
            ),
            PatientModel=PatientSchema(Id=visit.Patient.Id, Name=visit.Patient.Name, Identification=visit.Patient.Identification, LicenseNumber=visit.Patient.LicenseNumber, Type=PatientType(visit.Patient.Type), State=visit.Patient.State),
            MedicineVisits=list(map(lambda mv: MedicineVisitSchema(
                Id=mv.Id,
                MedicineId=mv.MedicineId,
                VisitId=mv.VisitId,
                State=mv.State,
                MedicineModel=MedicineSchema(
                    Id=mv.Medicine.Id,
                    Description=mv.Medicine.Description,
                    DrugTypeId=mv.Medicine.DrugTypeId,
                    BrandId=mv.Medicine.BrandId,
                    LocationId=mv.Medicine.LocationId,
                    Dose=mv.Medicine.Dose,
                    State=mv.Medicine.State,
                    DrugTypeModel=DrugTypeSchema(Id=mv.Medicine.DrugType.Id, Name=mv.Medicine.DrugType.Name, Description=mv.Medicine.DrugType.Description, State=mv.Medicine.DrugType.State),
                    BrandModel=BrandSchema(Id=mv.Medicine.Brand.Id, Name=mv.Medicine.Brand.Name, Description=mv.Medicine.Brand.Description, State=mv.Medicine.Brand.State),
                    LocationModel=LocationSchema(Id=mv.Medicine.Location.Id, Description=mv.Medicine.Location.Description, Shelf=mv.Medicine.Location.Shelf, Section=mv.Medicine.Location.Section, Cell=mv.Medicine.Location.Cell, State=mv.Medicine.Location.State)
                )), visit.MedicineVisits
            ))
        )

        return visit_mapped

    def create(self, visit_model: VisitSchema) -> VisitSchema:

        if not visit_model.MedicineVisits:
            raise HTTPException(status_code=400, detail=self.__medicine_required_message)

        for mv in visit_model.MedicineVisits:
            mv.State = True

        for mv in visit_model.MedicineVisits:
            mv.Id = None

        visit = Visit(visit_model)
        visit.Id = None
        visit.State = True

        self.db.add(visit)
        self.db.commit()
        self.db.refresh(visit)

        return VisitSchema(
            Id=visit.Id,
            DoctorId=visit.DoctorId,
            PatientId=visit.PatientId,
            Date=visit.Date,
            Time=visit.Time.strftime("%H:%M"),
            Symptoms=visit.Symptoms,
            Recommendations=visit.Recommendations,
            State=visit.State,
            DoctorModel=DoctorSchema(
                Id=visit.Doctor.Id,
                Name=visit.Doctor.Name,
                Identification=visit.Doctor.Identification,
                BatchWork=DoctorBatchWork(visit.Doctor.BatchWork),
                SpecialtyId=visit.Doctor.SpecialtyId,
                State=visit.Doctor.State,
                Specialty=SpecialtySchema(Id=visit.Doctor.Specialty.Id, Name=visit.Doctor.Specialty.Name, Description=visit.Doctor.Specialty.Description, State=visit.Doctor.Specialty.State)
            ),
            PatientModel=PatientSchema(Id=visit.Patient.Id, Name=visit.Patient.Name, Identification=visit.Patient.Identification, LicenseNumber=visit.Patient.LicenseNumber, Type=PatientType(visit.Patient.Type), State=visit.Patient.State),
            MedicineVisits=list(map(lambda mv: MedicineVisitSchema(
                Id=mv.Id,
                MedicineId=mv.MedicineId,
                VisitId=mv.VisitId,
                State=mv.State,
                MedicineModel=MedicineSchema(
                    Id=mv.Medicine.Id,
                    Description=mv.Medicine.Description,
                    DrugTypeId=mv.Medicine.DrugTypeId,
                    BrandId=mv.Medicine.BrandId,
                    LocationId=mv.Medicine.LocationId,
                    Dose=mv.Medicine.Dose,
                    State=mv.Medicine.State,
                    DrugTypeModel=DrugTypeSchema(Id=mv.Medicine.DrugType.Id, Name=mv.Medicine.DrugType.Name, Description=mv.Medicine.DrugType.Description, State=mv.Medicine.DrugType.State),
                    BrandModel=BrandSchema(Id=mv.Medicine.Brand.Id, Name=mv.Medicine.Brand.Name, Description=mv.Medicine.Brand.Description, State=mv.Medicine.Brand.State),
                    LocationModel=LocationSchema(Id=mv.Medicine.Location.Id, Description=mv.Medicine.Location.Description, Shelf=mv.Medicine.Location.Shelf, Section=mv.Medicine.Location.Section, Cell=mv.Medicine.Location.Cell, State=mv.Medicine.Location.State)
                )), visit.MedicineVisits
            ))
        )

    def update(self, visit_model: VisitSchema) -> VisitSchema:

        visit: type[Visit] = self.db.query(Visit).filter(Visit.Id == visit_model.Id and Visit.State).first()

        if visit is None:
            raise HTTPException(status_code=404, detail=self.__not_found_message)

        if not visit_model.MedicineVisits:
            raise HTTPException(status_code=400, detail=self.__medicine_required_message)

        for mv in visit.MedicineVisits:
            mv.State = False

        for mv in visit_model.MedicineVisits:
            mv.Id = None

        if visit_model.State == False:
            for mv in visit_model.MedicineVisits:
                mv.State = False

        visit.Id = visit_model.Id
        visit.DoctorId = visit_model.DoctorId
        visit.PatientId = visit_model.PatientId
        visit.Date = visit_model.Date
        visit.Time = datetime.strptime(visit_model.Time, "%H:%M").time()
        visit.Symptoms = visit_model.Symptoms
        visit.Recommendations = visit_model.Recommendations
        visit.State = visit_model.State
        visit.MedicineVisits = list(map(lambda mv: MedicineVisit(mv), visit_model.MedicineVisits))

        self.db.commit()
        self.db.refresh(visit)
        return VisitSchema(
            Id=visit.Id,
            DoctorId=visit.DoctorId,
            PatientId=visit.PatientId,
            Date=visit.Date,
            Time=visit.Time.strftime("%H:%M"),
            Symptoms=visit.Symptoms,
            Recommendations=visit.Recommendations,
            State=visit.State,
            DoctorModel=DoctorSchema(
                Id=visit.Doctor.Id,
                Name=visit.Doctor.Name,
                Identification=visit.Doctor.Identification,
                BatchWork=DoctorBatchWork(visit.Doctor.BatchWork),
                SpecialtyId=visit.Doctor.SpecialtyId,
                State=visit.Doctor.State,
                Specialty=SpecialtySchema(Id=visit.Doctor.Specialty.Id, Name=visit.Doctor.Specialty.Name, Description=visit.Doctor.Specialty.Description, State=visit.Doctor.Specialty.State)
            ),
            PatientModel=PatientSchema(Id=visit.Patient.Id, Name=visit.Patient.Name, Identification=visit.Patient.Identification, LicenseNumber=visit.Patient.LicenseNumber, Type=PatientType(visit.Patient.Type), State=visit.Patient.State),
            MedicineVisits=list(map(lambda mv: MedicineVisitSchema(
                Id=mv.Id,
                MedicineId=mv.MedicineId,
                VisitId=mv.VisitId,
                State=mv.State,
                MedicineModel=MedicineSchema(
                    Id=mv.Medicine.Id,
                    Description=mv.Medicine.Description,
                    DrugTypeId=mv.Medicine.DrugTypeId,
                    BrandId=mv.Medicine.BrandId,
                    LocationId=mv.Medicine.LocationId,
                    Dose=mv.Medicine.Dose,
                    State=mv.Medicine.State,
                    DrugTypeModel=DrugTypeSchema(Id=mv.Medicine.DrugType.Id, Name=mv.Medicine.DrugType.Name, Description=mv.Medicine.DrugType.Description, State=mv.Medicine.DrugType.State),
                    BrandModel=BrandSchema(Id=mv.Medicine.Brand.Id, Name=mv.Medicine.Brand.Name, Description=mv.Medicine.Brand.Description, State=mv.Medicine.Brand.State),
                    LocationModel=LocationSchema(Id=mv.Medicine.Location.Id, Description=mv.Medicine.Location.Description, Shelf=mv.Medicine.Location.Shelf, Section=mv.Medicine.Location.Section, Cell=mv.Medicine.Location.Cell, State=mv.Medicine.Location.State)
                )), visit.MedicineVisits
            ))
        )