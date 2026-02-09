import { DoctorBatchWork } from "@/enum/doctorBatchWork";

export const parseDoctorBatchWork = (batchWork: DoctorBatchWork): string => {
    switch (batchWork) {
        case DoctorBatchWork.Morning:
            return "Mañana"; 
        case DoctorBatchWork.Afternoon:
            return "Tarde"; 
        case DoctorBatchWork.Night:
            return "Noche"; 
        default:
            throw new Error("Tanda labor desconocida");
    }
}