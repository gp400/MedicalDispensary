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
                <v-col cols="12" md="4">
                    <v-text-field
                        v-model="formData.Shelf"
                        label="Estante"
                        :rules="requiredRule"
                    />
                </v-col>

                <v-col cols="12" md="4">
                    <v-text-field
                        v-model="formData.Section"
                        label="Tramo"
                        :rules="requiredRule"
                    />
                </v-col>

                <v-col cols="12" md="4">
                    <v-text-field
                        v-model="formData.Cell"
                        label="Celda"
                        :rules="requiredRule"
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
    import { useLocation } from '@/composables/useLocation';
    import { onMounted, ref } from 'vue';
    import type { VForm } from 'vuetify/components';
    import { Location } from '@/dto/Location';
    import type { DataTableHeader } from 'vuetify';
    import { requiredRule } from '@/utils/Validations';

    const { 
        getAll,
        getById,
        create,
        update
    } = useLocation()

    const title = 'Ubicaciones';
    const btnText = 'Crear Ubicacion';
    const itemsPerPageText = 'Ubicaciones por pagina'

    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Location());

    const items = ref<Location[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');

    onMounted(async() => {
        items.value = await getAll();
    })

    const headers: DataTableHeader[] = [
        { title: 'Estante', key: "Shelf" },
        { title: 'Tramo', key: "Section" },
        { title: 'Celda', key: "Cell" },
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

    const onDelete = async (values: Location) => {
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
        formData.value = new Location();
    }
</script>