import type { Brand } from '@/dto/Brand';
import apiClient from '@/utils/apiClient';

const route: String = "brand";

export function useBrand() {
  
  const getAll = async (): Promise<Brand[]> => {
    const { data } = await apiClient.get<Brand[]>(`/${route}/get_all`);
    return data;
  } 

  const getById = async (id: number): Promise<Brand> => {
    const { data } = await apiClient.get<Brand>(`/${route}/get_by_id/${id}`);
    return data;
  }

  const create = async (brand: Brand): Promise<Brand> => {
    const { data } = await apiClient.post<Brand>(`/${route}/create`, { ...brand });
    return data;
  }

  const update = async (brand: Brand): Promise<Brand> => {
    const { data } = await apiClient.put<Brand>(`/${route}/update`, { ...brand });
    return data;
  }

  return {
    getAll,
    getById,
    create,
    update
  }
}