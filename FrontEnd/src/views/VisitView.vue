<template>
  <CrudComponent
    :title
    :btn-text
    :reset
    :submit
    :headers
    :child-headers
    :items
    :show-expand
    :show-print="true"
    :doctor-options
    :patient-options
    :on-edit
    :on-delete
    :items-per-page-text
    :set-doctor-id
    :set-patient-id
    :set-initial-date
    :set-end-date
  >
    <v-form ref="formRef" @submit.prevent class="pt-3 px-3">
      <v-container class="px-0 pb-0">
          <v-row>
              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.DoctorId"
                  :items="doctorOptions"
                  item-title="Name"
                  item-value="Id"
                  label="Doctor"
                  :rules="requiredRule"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="formData.PatientId"
                  :items="patientOptions"
                  item-title="Name"
                  item-value="Id"
                  label="Paciente"
                  :rules="requiredRule"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.Date"
                  type="date"
                  label="Fecha"
                  :rules="requiredRule"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="formData.Time"
                  type="time"
                  label="Hora"
                  :rules="requiredRule"
                />
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="formData.Symptoms"
                  label="Síntomas"
                  :rules="requiredRule"
                />
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="formData.Recommendations"
                  label="Recomendaciones"
                  :rules="requiredRule"
                />
              </v-col>

              <v-col cols="12">
                <div class="d-flex">
                  <v-select
                    v-model="medicineId"
                    :items="medicineOptions.filter(med => 
                      !formData.MedicineVisits.some(mv => mv.MedicineId === med.Id)
                    )"
                    :item-title="item => `${item.DrugTypeModel.Name} - ${item.BrandModel.Name}`"
                    item-value="Id"
                    label="Medicamento Suministrado"
                    :rules="shouldValidate ? validateList(formData.MedicineVisits) : []"
                    ref="medicineSelect"
                  />
                  <div class="ps-2">
                    <v-btn icon color="blue add-btn" @click="addBtn">
                      <v-icon>mdi-plus</v-icon>
                    </v-btn>
                  </div>
                </div>
                <v-data-table
                  v-if="formData.MedicineVisits.length > 0"
                  :headers="medicineHeaders"
                  :items="formData.MedicineVisits"
                  class="elevation-1 mt-2"
                  hide-default-footer
                  hide-actions
                >
                  <template #item.Delete="{ item }">
                    <v-btn icon color="red" class="delete-medicine-btn" @click="onDeleteMedicine(item)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
              </v-col>
          </v-row>
      </v-container>
    </v-form>
  </CrudComponent>
</template>

<style scoped>
  .add-btn {
    height: 55px;
    width: 55px;
  }

  .delete-medicine-btn {
    height: 40px;
    width: 40px;
  }
</style>

<script setup lang="ts">
  import CrudComponent from '@/components/CrudComponent.vue';
  import { useDoctor } from '@/composables/useDoctor';
  import { useMedicine } from '@/composables/useMedicine';
  import { usePatient } from '@/composables/usePatient';
  import { useVisit } from '@/composables/useVisit';
  import { Doctor } from '@/dto/Doctor';
  import { Medicine } from '@/dto/Medicine';
  import { MedicineVisit } from '@/dto/MedicineVisit';
  import { Patient } from '@/dto/Patient';
  import { Visit } from '@/dto/Visit';
  import { requiredRule, validateList } from '@/utils/Validations';
  import { onMounted, ref } from 'vue';
  import { DataTableHeader } from 'vuetify';
  import { VForm } from 'vuetify/components';

  const { getAll: getAllDoctor } = useDoctor();
  const { getAll: getAllPatient } = usePatient();
  const { getAll: getAllMedicine } = useMedicine();

  const { 
      getAll,
      getById,
      create,
      update
  } = useVisit()

  const showExpand = true;
  const title = 'Visitas';
  const btnText = 'Crear Visita';
  const itemsPerPageText = 'Visitas por pagina'
  const formRef = ref<InstanceType<typeof VForm> | null>(null);
  const medicineSelect = ref<any>(null);
  const formData = ref(new Visit());

  const doctorId = ref<number | null>(null);
  const patientId = ref<number | null>(null);
  const initialDate = ref<Date | null>(null);
  const endDate = ref<Date | null>(null);
  const shouldValidate = ref<boolean>(false);
  const medicineId = ref<number | null>(null);
  const items = ref<Visit[]>([]);
  const doctorOptions = ref<Doctor[]>([]);
  const patientOptions = ref<Patient[]>([]);
  const medicineOptions = ref<Medicine[]>([]);

  onMounted(async() => {
    items.value = await getAll();
    doctorOptions.value = await getAllDoctor();
    patientOptions.value = await getAllPatient();
    medicineOptions.value = await getAllMedicine();
  })

  const headers: DataTableHeader[] = [
      { title: 'Doctor', key: "DoctorModel.Name" },
      { title: 'Paciente', key: "PatientModel.Name" },
      { title: 'Fecha Visita', key: "DateText" },
      { title: 'Hora Visita', key: "Time" },
      { title: 'Síntomas', key: "Symptoms" },
      { title: 'Recomendaciones', key: "Recommendations" },
      { title: 'Acciones', key: "Actions", sortable: false },
  ]

  const childHeaders: DataTableHeader[] = [
    { title: 'Farmaco', key: "MedicineModel.DrugTypeModel.Name" },
    { title: 'Marca', key: "MedicineModel.BrandModel.Name" },
    { title: 'Descripcion', key: "MedicineModel.Description" }
  ]

  const submit = async (): Promise<boolean> => {

      shouldValidate.value = true;

      let { valid } = await formRef.value!.validate();

      if (valid) {
          const values = {...formData.value}
          if (values.Id){
              await update(values);
          } else {
              await create(values);
          }
          reset();
          items.value = await getAll( initialDate.value, endDate.value );
      }

      return valid
  };

  const onEdit = async (id: number) => {
      formData.value = await getById(id);
  }

  const onDelete = async (values: Visit) => {
    await update({ ...values, State: false })
    items.value = await getAll( initialDate.value, endDate.value );
  }

  const reset = () => {
    shouldValidate.value = false
    formRef.value!.reset();
    formData.value = new Visit();
    medicineId.value = null;
  }

  const setDoctorId = async (value: number | null) => {
    doctorId.value = value;
    items.value = await getAll( doctorId.value, patientId.value, initialDate.value, endDate.value )
  }
  const setPatientId = async (value: number | null) => {
    patientId.value = value;
    items.value = await getAll( doctorId.value, patientId.value, initialDate.value, endDate.value )
  }

  const setInitialDate = async (value: Date | null) => {
    initialDate.value = value;
    items.value = await getAll( doctorId.value, patientId.value, initialDate.value, endDate.value )
  }

  const setEndDate = async (value: Date | null) => {
    endDate.value = value;
    items.value = await getAll( doctorId.value, patientId.value, initialDate.value, endDate.value )
  }

  const medicineHeaders: DataTableHeader[] = [
    ...childHeaders.values(),
    { title: 'Acciones', key: "Delete", sortable: false },
  ]

  const addBtn = () => {
    shouldValidate.value = true
    formData.value.MedicineVisits.push({
      Id: null,
      MedicineId: medicineId.value!,
      VisitId: null,
      MedicineModel: medicineOptions.value.find(med => med.Id === medicineId.value)!,
      State: true
    });
    medicineId.value = null;
    medicineSelect.value.validate()
  }

  const onDeleteMedicine = async (values: MedicineVisit) => {
    shouldValidate.value = false
    formData.value.MedicineVisits = formData.value.MedicineVisits.filter(mv => mv.MedicineId !== values.MedicineId);
    medicineSelect.value.validate()
  }
</script>