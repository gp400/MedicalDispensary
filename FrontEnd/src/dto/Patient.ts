import type { PatientType } from "@/enum/patientType"

export class Patient {
    Id: number | null = null
    Name: string = ''
    Identification: string = ''
    LicenseNumber: string = ''
    Type: PatientType | null = null
    TypeText: string = ''
    State: boolean = false
}