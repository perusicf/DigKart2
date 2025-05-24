<template>
  <div>
    <v-row>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Total Patients</v-card-title>
          <v-card-text class="text-h4">{{ stats.totalPatients }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Active Cases</v-card-title>
          <v-card-text class="text-h4">{{ stats.activeCases }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Today's Appointments</v-card-title>
          <v-card-text class="text-h4">{{ stats.todayAppointments }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Recent Patients</v-card-title>
          <v-list>
            <v-list-item
              v-for="patient in recentPatients"
              :key="patient.id"
              :to="`/patients/${patient.id}`"
            >
              <v-list-item-title>{{ patient.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ patient.lastVisit }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Upcoming Appointments</v-card-title>
          <v-list>
            <v-list-item
              v-for="appointment in upcomingAppointments"
              :key="appointment.id"
            >
              <v-list-item-title>{{ appointment.patientName }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ appointment.time }} - {{ appointment.doctor }}
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const stats = ref({
  totalPatients: 0,
  activeCases: 0,
  todayAppointments: 0
})

const recentPatients = ref([
  // Sample data - replace with API call
  {
    id: '1',
    name: 'John Doe',
    lastVisit: '2024-03-15'
  }
])

const upcomingAppointments = ref([
  // Sample data - replace with API call
  {
    id: '1',
    patientName: 'Jane Smith',
    time: '10:00 AM',
    doctor: 'Dr. Johnson'
  }
])

onMounted(async () => {
  try {
    // Fetch dashboard data
    const response = await fetch('/api/dashboard')
    const data = await response.json()
    stats.value = data.stats
    recentPatients.value = data.recentPatients
    upcomingAppointments.value = data.upcomingAppointments
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
})
</script> 