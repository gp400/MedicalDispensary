import { createRouter, createWebHistory } from 'vue-router'
import DrugView from '../views/DrugView.vue'
import LayoutComponent from '@/components/LayoutComponent.vue'
import BrandView from '@/views/BrandView.vue'
import LocationView from '@/views/LocationView.vue'
import MedicineView from '@/views/MedicineView.vue'
import PatientView from '@/views/PatientView.vue'
import SpecialtyView from '@/views/SpecialtyView.vue'
import DoctorView from '@/views/DoctorView.vue'
import VisitView from '@/views/VisitView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      component: LayoutComponent,
      children: [
        { path: "drug", name: 'drug', component: DrugView },
        { path: "brand", name: 'brand', component: BrandView },
        { path: "location", name: 'location', component: LocationView },
        { path: "medicine", name: 'medicine', component: MedicineView },
        { path: "specialty", name: 'specialty', component: SpecialtyView },
        { path: "patient", name: 'patient', component: PatientView },
        { path: "doctor", name: 'doctor', component: DoctorView },
        { path: "visit", name: 'visit', component: VisitView },
        { path: "", redirect: "drug" }
      ]
    }
  ],
})

export default router
