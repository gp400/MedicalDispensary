import type { Medicine } from "@/dto/Medicine";
import apiClient from "@/utils/apiClient";

const route: String = "medicine";

export function useMedicine() {
    
  const getAll = async (): Promise<Medicine[]> => {
    const { data } = await apiClient.get<Medicine[]>(`/${route}/get_all`);
    data.forEach(item => item.LocationText = `${ item.LocationModel!.Shelf }-${ item.LocationModel!.Section }-${ item.LocationModel!.Cell }`)

    return data;
  } 

  const getById = async (id: number): Promise<Medicine> => {
    const { data } = await apiClient.get<Medicine>(`/${route}/get_by_id/${id}`);
    data.LocationText = `${ data.LocationModel!.Shelf }-${ data.LocationModel!.Section }-${ data.LocationModel!.Cell }`
    return data;
  }

  const create = async (medicine: Medicine): Promise<Medicine> => {
    const { data } = await apiClient.post<Medicine>(`/${route}/create`, { ...medicine });
    return data;
  }

  const update = async (medicine: Medicine): Promise<Medicine> => {
    const { data } = await apiClient.put<Medicine>(`/${route}/update`, { ...medicine });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}