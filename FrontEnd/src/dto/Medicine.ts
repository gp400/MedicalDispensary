import type { Brand } from "./Brand"
import type { DrugType } from "./DrugType"
import type { Location } from "./Location"

export class Medicine {
    Id: number | null = null
    Description: string = ''
    DrugTypeId?: number
    BrandId?: number
    LocationId?: number
    Dose?: number
    State: boolean = true
    LocationText: string = ''

    DrugTypeModel: DrugType | null = null
    BrandModel: Brand | null = null
    LocationModel: Location | null = null
}