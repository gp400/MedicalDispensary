<template>
  <v-snackbar
    v-model="showSnackbar"
    :timeout="5000"
    color="yellow"
    location="top right"
  >
    <div class="d-flex">
        <v-icon
        color="black"
        icon="mdi-alert-circle"
        ></v-icon>
        <div style="margin-left: 5px;">
        {{ snackbarText }}
        </div>
    </div>
  </v-snackbar>
  <CrudComponent
    :title
    :btn-text
    :reset
    :submit
    :headers
    :items
    :on-edit
    :on-delete
    :items-per-page-text
  >
    <v-form ref="formRef" @submit.prevent class="px-3">
        <v-container class="px-0 pb-0">
            <v-row>
                <v-col cols="12" md="6">
                    <v-text-field
                        v-model="formData.Name"
                        label="Nombre"
                        :rules="requiredRule"
                    />
                </v-col>
                
                <v-col cols="12" md="6">
                    <v-text-field
                        v-model="formData.Identification"
                        label="Cédula (Sin guiones)"
                        :rules="[...requiredRule, ...numberRule, ...maxLengthRule(indentificationCounter), ...identificacionRule]"
                        @input="(e: InputEvent) => filterNumbers(e, 'Identification')"
                        :counter="indentificationCounter"
                    />
                </v-col>
                
                <v-col cols="12" md="6">
                    <v-select
                        v-model="formData.BatchWork"
                        :items="batchWorkOptions"
                        item-title="Name"
                        item-value="Id"
                        label="Tanda labor"
                        :rules="requiredRule"
                    />
                </v-col>

                <v-col cols="12" md="6">
                    <v-select
                        v-model="formData.SpecialtyId"
                        :items="specialtyOptions"
                        item-title="Name"
                        item-value="Id"
                        label="Especialidad"
                        :rules="requiredRule"
                    />
                </v-col>
            </v-row>
        </v-container>
    </v-form>
  </CrudComponent>
</template>

<script setup lang="ts">

    import CrudComponent from '@/components/CrudComponent.vue';
    import { useDoctor } from '@/composables/useDoctor';
    import { useSpecialty } from '@/composables/useSpecialty';
    import { Doctor } from '@/dto/Doctor';
    import { DoctorBatchWork } from '@/enum/doctorBatchWork';
    import { parseDoctorBatchWork } from '@/utils/parseDoctorBatchWork';
    import { maxLengthRule, numberRule, requiredRule, identificacionRule } from '@/utils/Validations';
    import { AxiosError } from 'axios';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';
    import { Specialty } from '../dto/Specialty';

    const { getAll: getAllSpecialties } = useSpecialty();

    const { 
        getAll,
        getById,
        create,
        update
    } = useDoctor()

    const title = 'Doctores';
    const btnText = 'Crear Doctor';
    const itemsPerPageText = 'Doctores por pagina'

    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Doctor());

    const items = ref<Doctor[]>([]);
    const specialtyOptions = ref<Specialty[]>([]);

    const indentificationCounter = ref<number>(11);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');
    const batchWorkOptions = ref([
      { Id: DoctorBatchWork.Morning, Name: parseDoctorBatchWork(DoctorBatchWork.Morning) },
      { Id: DoctorBatchWork.Afternoon, Name: parseDoctorBatchWork(DoctorBatchWork.Afternoon) },
      { Id: DoctorBatchWork.Night, Name: parseDoctorBatchWork(DoctorBatchWork.Night) },
    ]);

    onMounted(async() => {
        items.value = await getAll();
        specialtyOptions.value = await getAllSpecialties();
    })

    const headers: DataTableHeader[] = [
        { title: 'Nombre', key: "Name" },
        { title: 'Cédula', key: "Identification" },
        { title: 'Tanda labor', key: "BatchWorkText" },
        { title: 'Especialidad', key: "Specialty.Name" },
        { title: 'Acciones', key: "Actions", sortable: false },
    ]

    const filterNumbers = (value: InputEvent, prop: string) => {
        const validator = numberRule[0]!;
        if (validator(value.data as string) !== true && value.data) {
            formData.value[prop] = (formData.value[prop] as string).replace(value.data, '');
        }
    }

    const submit = async (): Promise<boolean> => {
        let { valid } = await formRef.value!.validate();

        if (valid) {
            const values = {...formData.value}
            if (values.Id){
                await update(values);
            } else {
                await create(values);
            }
            reset();
            items.value = await getAll();
        }

        return valid
    };

    const onEdit = async (id: number) => {
        formData.value = await getById(id);
    }

    const onDelete = async (values: Doctor) => {
        try {
            await update({ ...values, State: false })
            items.value = await getAll();
        } catch({ response: { data: { detail } } }: AxiosError) {
            showSnackbar.value = true;
            snackbarText.value = detail
        }
    }

    const reset = () => {
      formRef.value!.reset();
      formData.value = new Doctor();
    }
</script>