import type { Doctor } from "@/dto/Doctor";
import apiClient from "@/utils/apiClient";
import { parseDoctorBatchWork } from "@/utils/parseDoctorBatchWork";

const route: String = "doctor";

export function useDoctor() {
    
  const getAll = async (): Promise<Doctor[]> => {
    const { data } = await apiClient.get<Doctor[]>(`/${route}/get_all`);
    data.forEach(item => item.BatchWorkText = parseDoctorBatchWork(item.BatchWork!) );
    return data;
  } 

  const getById = async (id: number): Promise<Doctor> => {
    const { data } = await apiClient.get<Doctor>(`/${route}/get_by_id/${id}`);
    data.BatchWorkText = parseDoctorBatchWork(data.BatchWork!);
    return data;
  }

  const create = async (doctor: Doctor): Promise<Doctor> => {
    const { data } = await apiClient.post<Doctor>(`/${route}/create`, { ...doctor });
    return data;
  }

  const update = async (doctor: Doctor): Promise<Doctor> => {
    const { data } = await apiClient.put<Doctor>(`/${route}/update`, { ...doctor });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}