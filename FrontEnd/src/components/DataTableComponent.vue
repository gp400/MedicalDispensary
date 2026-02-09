<template>
  <v-data-table
    :headers
    :items
    :show-expand
    :search
    v-model:expanded="expanded"
    item-value="Id"
    class="elevation-1 mt-3"
    :items-per-page-text="`${itemsPerPageText}:`"
    :items-per-page
    :hide-default-footer
    :no-data-text="'No existen registros'"
  >
    <template #expanded-row="{ item, columns }">
      <td :colspan="columns.length">
        <v-data-table
          :headers="childHeaders"
          :items="item.MedicineVisits"
          class="w-90 ml-auto nested-table"
          hide-default-footer
        />
      </td>
    </template>
    <template #item.Actions="{ item }">
      <div class="d-flex flex-wrap">
        <div class="pa-2">
          <v-btn icon color="yellow" @click="onEdit(item.Id!)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </div>
        <div class="pa-2">
          <v-btn icon color="red" @click="onDelete(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </div>
      </div>
    </template>
  </v-data-table>
</template>

<style>
  .nested-table {
    border-left: 1px solid #D4D4D4;
    border-bottom: 1px solid #D4D4D4
  }
</style>

<script setup lang="ts">
  
  import { ref } from 'vue';
  import { DataTableHeader } from 'vuetify';

  const props = defineProps<{
    childHeaders: DataTableHeader[],
    itemsPerPageText: String,
    itemsPerPage: number,
    hideDefaultFooter: boolean,
    onEdit: Function,
    onDelete: Function
  }>()

  const expanded = ref([]);
</script>