import { PatientType } from "@/enum/patientType";

export const parsePatientType = (type: PatientType): string => {
    switch (type) {
        case PatientType.Student:
            return "Estudiante"; 
        case PatientType.Employee:
            return "Empleado"; 
        case PatientType.Teacher:
            return "Profesor"; 
        case PatientType.Other:
            return "Otros"; 
        default:
            throw new Error("Tipo de paciente desconocido");
    }
}