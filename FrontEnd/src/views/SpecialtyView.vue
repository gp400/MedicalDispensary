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
    <v-form ref="formRef" @submit.prevent class="pt-3 px-3">
      <v-text-field
        class="mb-3"
        v-model="formData.Name"
        label="Nombre"
        :rules="requiredRule"
      />

      <v-textarea
        v-model="formData.Description"
        label="Descripcion"
      />
    </v-form>
  </CrudComponent>
</template>

<script setup lang="ts">
    import CrudComponent from '@/components/CrudComponent.vue';
    import { useSpecialty } from '@/composables/useSpecialty';
    import { Specialty } from '@/dto/Specialty';
    import type { AxiosError } from 'axios';
    import { onMounted, ref } from 'vue';
    import { DataTableHeader } from 'vuetify';
    import { VForm } from 'vuetify/components';

    const { 
        getAll,
        getById,
        create,
        update
    } = useSpecialty()

    const title = 'Especialidades';
    const btnText = 'Crear Especialidad';
    const itemsPerPageText = 'Especialidades por pagina'
    const formRef = ref<InstanceType<typeof VForm> | null>(null);
    const formData = ref(new Specialty());

    const items = ref<Specialty[]>([]);
    const showSnackbar = ref<boolean>(false);
    const snackbarText = ref<string>('');

    onMounted(async() => {
        items.value = await getAll();
    })

    const headers: DataTableHeader[] = [
        { title: 'Nombre', key: "Name" },
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

    const onDelete = async (values: Specialty) => {
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
      formData.value = new Specialty();
    }
</script>