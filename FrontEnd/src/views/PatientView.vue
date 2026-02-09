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
                        :rules="[...requiredRule, ...numberRule, ...maxLengthRule(indentificationCounter)]"
                        @input="(e: InputEvent) => filterNumbers(e, 'Identification')"
                        :counter="indentificationCounter"
                    />
                </v-col>
                
                <v-col cols="12" md="6">
                    <v-text-field
                        v-model="formData.LicenseNumber"
                        label="No. Carnet"
                        :rules="[...requiredRule, ...numberRule]"
                        @input="(e: InputEvent) => filterNumbers(e, 'LicenseNumber')"
                    />
                </v-col>

                <v-col cols="12" md="6">
                  <v-select
                    v-model="formData.Type"
                    :items="typeOptions"
                    item-title="Name"
                    item-value="Id"
                    label="Tipo"
                    :rules="requiredRule"
                  />
                </v-col>
            </v-row>
        </v-container>
    </v-form>
  </CrudComponent>
</template>
<script lang="ts" setup>

    import CrudComponent from '@/components/CrudComponent.vue';
    import { usePatient } from '@/composables/usePatient';
    import { Patient } from '@/dto/Patient';
    import { AxiosError } from 'axios';
    import { onMounted, ref } from 'vue';
    import { VForm } from 'vuetify/components';
    import { requiredRule, numberRule, maxLengthRule } from '@/utils/Validations';
    import { PatientType } from '@/enum/patientType';
    import { parsePatientType } from '@/utils/parsePatientType';

    const { 
        getAll,
        getById,
        create,
        update
    } = usePatient()

    const title = 'Pacientes';
    const btnText = 'Crear Paciente';
    const itemsPerPageText = 'Pacientes por pagina'

    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Patient());

    const indentificationCounter = ref<number>(11);
    const items = ref<Patient[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');
    const typeOptions = ref([
      { Id: PatientType.Student, Name: parsePatientType(PatientType.Student) },
      { Id: PatientType.Employee, Name: parsePatientType(PatientType.Employee) },
      { Id: PatientType.Teacher, Name: parsePatientType(PatientType.Teacher) },
      { Id: PatientType.Other, Name: parsePatientType(PatientType.Other) }
    ]);

    onMounted(async() => {
        items.value = await getAll();
    })

    const headers: DataTableHeader[] = [
        { title: 'Nombre', key: "Name" },
        { title: 'Cédula', key: "Identification" },
        { title: 'No. Carnet', key: "LicenseNumber" },
        { title: 'Tipo', key: "TypeText" },
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

    const onDelete = async (values: Patient) => {
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
      formData.value = new Patient();
    }
</script>
  