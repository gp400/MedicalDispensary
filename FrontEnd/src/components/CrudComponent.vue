<template>
  <h3 class="text-h3 text-center">{{ title }}</h3>

  <v-row justify="space-between" class="align-center mt-0">
    <v-col cols="6">
      <v-row>
        <v-col cols="12">
          <v-btn color="primary" class="text-none" @click="dialog = true">{{btnText}}</v-btn>
        </v-col>
        <v-col cols="12" v-if="showPrint">
          <v-btn color="green" class="text-none" @click="downloadPdf">Imprimir reporte</v-btn
          >
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="6">
      <v-row justify="end">
        <v-col cols="12" md="6">
          <v-text-field
            class="text-field"
            v-model="search"
            label="Filtro"
            clearable
            hide-details
          />
        </v-col>
        <v-col cols="12" v-if="setDoctorId || setPatientId">
          <v-row justify="end">
            <v-col cols="12" md="6" v-if="setDoctorId">
              <v-select
                :items="doctorOptions"
                item-title="Name"
                item-value="Id"
                label="Doctor"
                @update:model-value="setDoctorId"
                clearable
                hide-details
              />
            </v-col>
            <v-col cols="12" md="6" v-if="setPatientId">
              <v-select
                :items="patientOptions"
                item-title="Name"
                item-value="Id"
                label="Paciente"
                @update:model-value="setPatientId"
                clearable
                hide-details
              />
            </v-col>
          </v-row>
        </v-col>
        <v-col cols="12" v-if="setInitialDate || setEndDate">
          <v-row justify="end">
            <v-col cols="12" md="6" v-if="setInitialDate">
              <v-text-field
                type="date"
                label="Fecha Inicio"
                @input="(event: InputEvent) => setInitialDate((event.target as HTMLInputElement).value)"
                @click:clear="() => setInitialDate(null)"
                clearable
                hide-details
              />
            </v-col>
            <v-col cols="12" md="6" v-if="setEndDate">
              <v-text-field
                type="date"
                label="Fecha Fin"
                @input="(event: InputEvent) => setEndDate((event.target as HTMLInputElement).value)"
                @click:clear="() => setEndDate(null)"
                clearable
                hide-details
              />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-col>
  </v-row>

  <v-dialog v-model="dialog" max-width="500px" persistent>
    <v-card>
      <v-card-title> Complete los campos </v-card-title>

      <slot></slot>
      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn class="text-none" @click="onCancel" color="red"> Cancelar </v-btn>

        <v-btn class="text-none" color="primary" @click="handleSubmit"> Guardar </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <div ref="pdfContent">
      
      <DataTableComponent
        :headers
        :child-headers="childHeaders"
        :items
        :show-expand
        :search
        :on-edit="handleEdit"
        :on-delete="handleDelete"
        :items-per-page-text
        :items-per-page
        :hide-default-footer
      />

  </div>
</template>

<script setup lang="ts">
    import DataTableComponent from "@/components/DataTableComponent.vue";
    import { DataTableHeader } from "vuetify";
    import { ref } from "vue";
    import { Doctor } from "@/dto/Doctor";
    import { Patient } from "@/dto/Patient";
    import html2pdf from "html2pdf.js";

    const props = defineProps<{
        title: String;
        btnText: String;
        itemsPerPageText: String;
        headers: DataTableHeader[];
        childHeaders: DataTableHeader[];
        items: T[];
        showExpand: boolean;
        showPrint: boolean;
        doctorOptions: Doctor[];
        patientOptions: Patient[];
        reset: Function;
        submit: Function;
        onEdit: Function;
        onDelete: Function;
        setDoctorId: Function;
        setPatientId: Function;
        setInitialDate: Function;
        setEndDate: Function;
    }>();
    
    const search = ref<string>("");
    const dialog = ref<boolean>(false);
    const isPrint = ref<boolean>(false);
    const itemsPerPage = ref<number>(10);
    const hideDefaultFooter = ref<boolean>(false);
    const showExpand = ref<boolean>(props.showExpand);
    const pdfContent = ref<HTMLDivElement | null>(null);
    const headers = ref<DataTableHeader[]>(props.headers);

    const handleSubmit = async () => {
        const stayOpen: boolean = !(await props.submit());
        dialog.value = stayOpen;
    };

    const handleEdit = (id: number) => {
        dialog.value = true;
        props.onEdit(id);
    };

    const handleDelete = (item: T) => {
        props.onDelete(item);
    };

    const onCancel = () => {
        props.reset();
        dialog.value = false;
    };

    const downloadPdf = async () => {

        const invalidHeaders: string[] = ['actions']

        const showExpandOriginal = showExpand.value;

        isPrint.value = true;
        itemsPerPage.value = 0;
        hideDefaultFooter.value = true;
        showExpand.value = false
        headers.value = props.headers.filter(header => !invalidHeaders.includes(header.key!.toLocaleLowerCase()));

        const opt: Html2PdfOptions = {
          margin:       [20,10,10,10],
          filename:     `Reporte ${props.title}.pdf`,
          html2canvas:  { scale: 2 },
          jsPDF:        { unit: "mm", format: "a4", orientation: "portrait" }
        };

        await html2pdf().set(opt).from(pdfContent.value!)
          .toPdf()
          .get("pdf")
          .then(pdf => {
            const pageWidth = pdf.internal.pageSize.getWidth();

            const headerText = `Reporte de ${ props.title }`;

            pdf.setFont("helvetica", "bold");
            pdf.setFontSize(18);
            pdf.setTextColor(40);

            const textWidth = pdf.getTextWidth(headerText);

            const x = (pageWidth - textWidth) / 2;

            pdf.setPage(1);
            pdf.text(headerText, x, 15);
          })
          .save();

        isPrint.value = false;
        itemsPerPage.value = 10;
        hideDefaultFooter.value = false;
        showExpand.value = showExpandOriginal
        headers.value = props.headers
    };
</script>
