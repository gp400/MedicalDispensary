from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import database
from exceptions.global_exception_handler import global_exception_handler
from routers import drug_type_router, brand_router, location_router, medicine_router, patient_router, specialty_router, \
    doctor_router, visit_router

app = FastAPI()

origins = [
    'http://localhost:5173',
    'http://localhost:5174'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.Base.metadata.create_all(bind=database.engine)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(drug_type_router.router, prefix="/drug_type", tags=["drug_type"])
app.include_router(brand_router.router, prefix="/brand", tags=["brand"])
app.include_router(location_router.router, prefix="/location", tags=["location"])
app.include_router(medicine_router.router, prefix="/medicine", tags=["medicine"])
app.include_router(specialty_router.router, prefix="/specialty", tags=["specialty"])
app.include_router(patient_router.router, prefix="/patient", tags=["patient"])
app.include_router(doctor_router.router, prefix="/doctor", tags=["doctor"])
app.include_router(visit_router.router, prefix="/visit", tags=["visit"])