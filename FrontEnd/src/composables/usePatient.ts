import type { Patient } from "@/dto/Patient";
import apiClient from "@/utils/apiClient";
import { parsePatientType } from "@/utils/parsePatientType";

const route: String = "patient";

export function usePatient() {
    
  const getAll = async (): Promise<Patient[]> => {
    const { data } = await apiClient.get<Patient[]>(`/${route}/get_all`);
    data.forEach(item => item.TypeText = parsePatientType(item.Type!) );
    return data;
  } 

  const getById = async (id: number): Promise<Patient> => {
    const { data } = await apiClient.get<Patient>(`/${route}/get_by_id/${id}`);
    data.TypeText = parsePatientType(data.Type!);
    return data;
  }

  const create = async (patient: Patient): Promise<Patient> => {
    const { data } = await apiClient.post<Patient>(`/${route}/create`, { ...patient });
    return data;
  }

  const update = async (patient: Patient): Promise<Patient> => {
    const { data } = await apiClient.put<Patient>(`/${route}/update`, { ...patient });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}