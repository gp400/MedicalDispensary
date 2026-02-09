import type { DrugType } from '@/dto/DrugType'
import apiClient from '@/utils/apiClient'
import { ref } from 'vue'

const route: String = "drug_type";

export function useDrugType() {
  const drugTypes = ref<DrugType[]>([])
  // const loading = ref(false)
  // const error = ref<string | null>(null)

  // const call = async (callback: () => {}) => {
  //   loading.value = true
  //   error.value = null

  //   try {
  //       return callback();
  //   } catch(err: any) {
  //       error.value = err.message;
  //   } finally {
  //     loading.value = false
  //   }
  // }

  const getAll = async (): Promise<DrugType[]> => {
    const { data } = await apiClient.get<DrugType[]>(`/${route}/get_all`);
    return data;
  } 

  const getById = async (id: number): Promise<DrugType> => {
    const { data } = await apiClient.get<DrugType>(`/${route}/get_by_id/${id}`);
    return data;
  }

  const create = async (drugType: DrugType): Promise<DrugType> => {
    const { data } = await apiClient.post<DrugType>(`/${route}/create`, { ...drugType });
    return data;
  }

  const update = async (drugType: DrugType): Promise<DrugType> => {
    const { data } = await apiClient.put<DrugType>(`/${route}/update`, { ...drugType });
    return data;
  }

  return { 
    drugTypes,
    // loading,
    // error,
    // call,
    getAll,
    getById,
    create,
    update
  }
}