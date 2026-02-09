import type { Location } from '@/dto/Location';
import apiClient from '@/utils/apiClient';
import { ref } from "vue";

const route: String = "location";

export function useLocation() {
    
  const getAll = async (): Promise<Location[]> => {
    const { data } = await apiClient.get<Location[]>(`/${route}/get_all`);
    return data;
  } 

  const getById = async (id: number): Promise<Location> => {
    const { data } = await apiClient.get<Location>(`/${route}/get_by_id/${id}`);
    return data;
  }

  const create = async (location: Location): Promise<Location> => {
    const { data } = await apiClient.post<Location>(`/${route}/create`, { ...location });
    return data;
  }

  const update = async (location: Location): Promise<Location> => {
    const { data } = await apiClient.put<Location>(`/${route}/update`, { ...location });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}