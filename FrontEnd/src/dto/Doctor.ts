import type { DoctorBatchWork } from "@/enum/doctorBatchWork"
import type { Specialty } from "./Specialty"

export class Doctor {
    Id: number | null = null
    Name: string = ''
    Identification: string = ''
    BatchWork: DoctorBatchWork | null = null
    BatchWorkText: string = ''
    SpecialtyId?: number
    State: boolean = false

    Specialty: Specialty | null = null
}