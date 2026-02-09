import type { Medicine } from "./Medicine"

export class MedicineVisit {
    Id: number | null = null
    MedicineId: number | null = null
    VisitId: number | null = null
    State: boolean = false

    MedicineModel: Medicine | null = null
} 