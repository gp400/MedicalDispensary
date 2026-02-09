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
                  <v-select
                    v-model="formData.DrugTypeId"
                    :items="drugOptions"
                    item-title="Name"
                    item-value="Id"
                    label="Farmaco"
                    :rules="requiredRule"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-select
                    v-model="formData.BrandId"
                    :items="brandOptions"
                    item-title="Name"
                    item-value="Id"
                    label="Marca"
                    :rules="requiredRule"
                  />
                </v-col>

                <v-col cols="12" md="6">
                  <v-select
                    v-model="formData.LocationId"
                    :items="locationOptions"
                    :item-title="location => `${ location.Shelf }-${ location.Section }-${ location.Cell }`"
                    item-value="Id"
                    label="Ubicacion"
                    :rules="requiredRule"
                  />
                </v-col>

                <v-col cols="12" md="6">
                    <v-text-field
                        v-model="formData.Dose"
                        label="Dosis"
                        :rules="requiredRule"
                        type="number"
                    />
                </v-col>
            </v-row>
        </v-container>

      <v-textarea
        v-model="formData.Description"
        label="Descripcion"
      />
    </v-form>
  </CrudComponent>
</template>
<script setup lang="ts">
  import CrudComponent from '@/components/CrudComponent.vue';
  import { useBrand } from '@/composables/useBrand';
  import { useDrugType } from '@/composables/useDrugType';
  import { useLocation } from '@/composables/useLocation';
  import { useMedicine } from '@/composables/useMedicine';
  import { Brand } from '@/dto/Brand';
  import { DrugType } from '@/dto/DrugType';
  import { Location } from '@/dto/Location';
  import { Medicine } from '@/dto/Medicine';
  import { requiredRule } from '@/utils/Validations';
  import { AxiosError } from 'axios';
  import { onMounted, ref } from 'vue';
  import { VForm } from 'vuetify/components';

  const { getAll: getAllDrugType } = useDrugType()
  const { getAll: getAllBrand } = useBrand()
  const { getAll: getAllLocation } = useLocation()

  const { 
    getAll,
    getById,
    create,
    update
  } = useMedicine()

  const title = 'Medicamentos';
  const btnText = 'Crear Medicamento';
  const itemsPerPageText = 'Medicamentos por pagina'

  const formRef = ref<InstanceType<typeof VForm> | null>(null);
  const formData = ref(new Medicine());

  const items = ref<Medicine[]>([]);
  const drugOptions = ref<DrugType[]>([]);
  const brandOptions = ref<Brand[]>([]);
  const locationOptions = ref<Location[]>([]);

  const showSnackbar = ref<boolean>(false);
  const snackbarText = ref<string>('');

  onMounted(async() => {
      items.value = await getAll();
      drugOptions.value = await getAllDrugType();
      brandOptions.value = await getAllBrand();
      locationOptions.value = await getAllLocation();
  })

  const headers: DataTableHeader[] = [
      { title: 'Farmaco', key: "DrugTypeModel.Name" },
      { title: 'Marca', key: "BrandModel.Name" },
      { title: 'Ubicacion', key: "LocationText" },
      { title: 'Dosis', key: "Dose" },
      { title: 'Descripcion', key: "Description" },
      { title: 'Acciones', key: "Actions", sortable: false },
  ]

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

  const onDelete = async (values: Medicine) => {
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
      formData.value = new Medicine();
  }
</script>