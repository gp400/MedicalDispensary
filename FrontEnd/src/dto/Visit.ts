import type { Doctor } from "./Doctor"
import type { MedicineVisit } from "./MedicineVisit"
import type { Patient } from "./Patient"

export class Visit {
    Id: number | null = null
    DoctorId: number | null = null
    PatientId: number | null = null
    Date: Date | null = null
    Time: string = ""
    Symptoms: string = ""
    Recommendations: string = ""
    State: boolean = false

    DoctorModel: Doctor | null = null
    PatientModel: Patient | null = null

    MedicineVisits: MedicineVisit[] = []

    DateText: string = '';
}