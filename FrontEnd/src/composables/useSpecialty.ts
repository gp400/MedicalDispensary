import type { Specialty } from "@/dto/Specialty";
import apiClient from "@/utils/apiClient";

const route: String = "specialty";

export function useSpecialty() {
  
  const getAll = async (): Promise<Specialty[]> => {
    const { data } = await apiClient.get<Specialty[]>(`/${route}/get_all`);
    return data;
  } 

  const getById = async (id: number): Promise<Specialty> => {
    const { data } = await apiClient.get<Specialty>(`/${route}/get_by_id/${id}`);
    return data;
  }

  const create = async (specialty: Specialty): Promise<Specialty> => {
    const { data } = await apiClient.post<Specialty>(`/${route}/create`, { ...specialty });
    return data;
  }

  const update = async (specialty: Specialty): Promise<Specialty> => {
    const { data } = await apiClient.put<Specialty>(`/${route}/update`, { ...specialty });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}