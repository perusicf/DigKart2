<template>
  <div>
    <v-card>
      <v-card-title>
        Patient Details
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="printRecord">
          <v-icon left>mdi-printer</v-icon>
          Print Record
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="patient.name"
              label="Name"
              readonly
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="patient.dob"
              label="Date of Birth"
              readonly
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="patient.phone"
              label="Phone"
              readonly
            ></v-text-field>
          </v-col>
        </v-row>

        <v-divider class="my-4"></v-divider>

        <h3 class="text-h6 mb-4">Medical History</h3>
        
        <v-timeline>
          <v-timeline-item
            v-for="record in medicalRecords"
            :key="record.id"
            :dot-color="record.type === 'diagnosis' ? 'primary' : 'success'"
            size="small"
          >
            <template v-slot:opposite>
              {{ formatDate(record.date) }}
            </template>
            <v-card>
              <v-card-title class="text-h6">
                {{ record.type === 'diagnosis' ? 'Diagnosis' : 'Treatment' }}
              </v-card-title>
              <v-card-text>
                <p><strong>Description:</strong> {{ record.description }}</p>
                <p v-if="record.notes"><strong>Notes:</strong> {{ record.notes }}</p>
                <p v-if="record.doctor"><strong>Doctor:</strong> {{ record.doctor }}</p>
              </v-card-text>
              <v-card-actions v-if="canEdit">
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  variant="text"
                  @click="editRecord(record)"
                >
                  Edit
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-timeline-item>
        </v-timeline>

        <v-btn
          v-if="canEdit"
          color="primary"
          class="mt-4"
          @click="addNewRecord"
        >
          Add New Record
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- Add/Edit Record Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-select
                  v-model="editedItem.type"
                  :items="['diagnosis', 'treatment']"
                  label="Record Type"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.description"
                  label="Description"
                  rows="3"
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.notes"
                  label="Notes"
                  rows="2"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="close">
            Cancel
          </v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="save">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const dialog = ref(false)
const editedIndex = ref(-1)
const editedItem = ref({
  id: '',
  type: 'diagnosis',
  description: '',
  notes: '',
  date: new Date().toISOString().split('T')[0],
  doctor: 'Dr. Smith' // This should come from the logged-in user
})

const defaultItem = {
  id: '',
  type: 'diagnosis',
  description: '',
  notes: '',
  date: new Date().toISOString().split('T')[0],
  doctor: 'Dr. Smith'
}

const patient = ref({
  id: '',
  name: '',
  dob: '',
  phone: ''
})

const medicalRecords = ref([
  // Sample data - replace with API call
  {
    id: '1',
    type: 'diagnosis',
    description: 'Common cold',
    notes: 'Patient reported symptoms for 3 days',
    date: '2024-03-15',
    doctor: 'Dr. Smith'
  }
])

const canEdit = computed(() => {
  const userRole = localStorage.getItem('userRole')
  return userRole === 'doctor' || userRole === 'admin'
})

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'New Record' : 'Edit Record'
})

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString()
}

const printRecord = () => {
  window.print()
}

const editRecord = (item: any) => {
  editedIndex.value = medicalRecords.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialog.value = true
}

const addNewRecord = () => {
  editedIndex.value = -1
  editedItem.value = Object.assign({}, defaultItem)
  dialog.value = true
}

const close = () => {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem)
  editedIndex.value = -1
}

const save = async () => {
  try {
    if (editedIndex.value > -1) {
      // Update existing record
      await fetch(`/api/records/${editedItem.value.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editedItem.value)
      })
      Object.assign(medicalRecords.value[editedIndex.value], editedItem.value)
    } else {
      // Create new record
      const response = await fetch('/api/records', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ...editedItem.value,
          patientId: route.params.id
        })
      })
      const newRecord = await response.json()
      medicalRecords.value.push(newRecord)
    }
    close()
  } catch (error) {
    console.error('Error saving record:', error)
  }
}

onMounted(async () => {
  try {
    // Fetch patient details
    const response = await fetch(`/api/patients/${route.params.id}`)
    const data = await response.json()
    patient.value = data

    // Fetch medical records
    const recordsResponse = await fetch(`/api/patients/${route.params.id}/records`)
    const recordsData = await recordsResponse.json()
    medicalRecords.value = recordsData
  } catch (error) {
    console.error('Error fetching patient data:', error)
  }
})
</script>

<style>
@media print {
  .v-btn {
    display: none !important;
  }
}
</style> 