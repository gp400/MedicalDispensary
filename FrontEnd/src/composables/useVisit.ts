import type { Visit } from "@/dto/Visit";
import apiClient from "@/utils/apiClient";

const route: String = "visit";

export function useVisit() {
  
  const getAll = async (doctorId: number | null, patientId: number | null, initialDate: Date | null, endDate: Date | null): Promise<Visit[]> => {
    const { data } = await apiClient.get<Visit[]>(`/${route}/get_all`, {
      params: {
        doctor_id: doctorId,
        patient_id: patientId,
        initial_date: initialDate,
        end_date: endDate
      }
    });
    data.forEach(visit => {
      const date = new Date(`${visit.Date} 12:00`);
      visit.DateText = date.toLocaleDateString();
    });
    return data;
  } 

  const getById = async (id: number): Promise<Visit> => {
    const { data } = await apiClient.get<Visit>(`/${route}/get_by_id/${id}`);
    return data;
  }

  const create = async (visit: Visit): Promise<Visit> => {
    const { data } = await apiClient.post<Visit>(`/${route}/create`, { ...visit });
    return data;
  }

  const update = async (visit: Visit): Promise<Visit> => {
    const { data } = await apiClient.put<Visit>(`/${route}/update`, { ...visit });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}