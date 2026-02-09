src/layouts/Default.vue
<template>
  <v-app>

    <v-app-bar flat color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>Dispensario Medico</v-toolbar-title>
    </v-app-bar>

    <!-- Drawer -->
    <v-navigation-drawer
      v-model="drawer"
      app
      color="grey lighten-4"
    >
      <v-list nav>
        <v-list-item link v-for="drawerRoute in drawerRoutes" :key="drawerRoute.title" :to="drawerRoute.route">
          <div class="d-flex align-end">
            <v-list-item-icon>
              <v-icon size="18">{{ drawerRoute.icon }}</v-icon> 
            </v-list-item-icon>
            <v-list-item-title class="text-body-1 list-item-title">{{ drawerRoute.title }}</v-list-item-title>
          </div>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <div class="pa-3">
        <router-view />
      </div>
    </v-main>
  </v-app>
</template>

<style>
  .list-item-title {
    margin-bottom: 2.2px;
    margin-left: 5px
  }
</style>

<script setup lang="ts">
  import { ref } from 'vue'

  class DrawerRoutes {
    route: String;
    icon: String;
    title: String;
  }

  const drawer = ref(true);

  const drawerRoutes = ref<DrawerRoutes[]>([
    {
      route: '/drug',
      icon: 'mdi-pill',
      title: 'Farmacos'
    },
    {
      route: '/brand',
      icon: 'mdi-watermark',
      title: 'Marcas'
    },
    {
      route: '/location',
      icon: 'mdi-hospital-marker',
      title: 'Ubicaciones'
    },
    {
      route: '/medicine',
      icon: 'mdi-medication-outline',
      title: 'Medicamentos'
    },
    {
      route: '/specialty',
      icon: 'mdi-needle',
      title: 'Especialidades'
    },
    {
      route: '/patient',
      icon: 'mdi-account-injury-outline',
      title: 'Pacientes'
    },
    {
      route: '/doctor',
      icon: 'mdi-doctor',
      title: 'Doctores'
    },
    {
      route: '/visit',
      icon: 'mdi-calendar-clock',
      title: 'Visitas'
    },
  ])
</script>
