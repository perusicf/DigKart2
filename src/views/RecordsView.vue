<template>
  <div>
    <v-card>
      <v-card-title>
        Medical Records
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="records"
        :search="search"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.type="{ item }">
          <v-chip
            :color="item.raw.type === 'diagnosis' ? 'primary' : 'success'"
            text-color="white"
          >
            {{ item.raw.type }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-icon
            small
            class="mr-2"
            @click="viewRecord(item.raw)"
          >
            mdi-eye
          </v-icon>
          <v-icon
            v-if="canEdit"
            small
            class="mr-2"
            @click="editRecord(item.raw)"
          >
            mdi-pencil
          </v-icon>
        </template>
      </v-data-table>
    </v-card>

    <!-- View/Edit Record Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.patientName"
                  label="Patient Name"
                  readonly
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="editedItem.type"
                  :items="['diagnosis', 'treatment']"
                  label="Record Type"
                  :disabled="!canEdit"
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.description"
                  label="Description"
                  rows="3"
                  :readonly="!canEdit"
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="editedItem.notes"
                  label="Notes"
                  rows="2"
                  :readonly="!canEdit"
                ></v-textarea>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.doctor"
                  label="Doctor"
                  readonly
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.date"
                  label="Date"
                  readonly
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="close">
            {{ canEdit ? 'Cancel' : 'Close' }}
          </v-btn>
          <v-btn
            v-if="canEdit"
            color="blue-darken-1"
            variant="text"
            @click="save"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const search = ref('')
const loading = ref(false)
const dialog = ref(false)
const editedIndex = ref(-1)
const editedItem = ref({
  id: '',
  patientId: '',
  patientName: '',
  type: '',
  description: '',
  notes: '',
  doctor: '',
  date: ''
})

const defaultItem = {
  id: '',
  patientId: '',
  patientName: '',
  type: '',
  description: '',
  notes: '',
  doctor: '',
  date: ''
}

const headers = [
  { title: 'Patient', key: 'patientName' },
  { title: 'Type', key: 'type' },
  { title: 'Description', key: 'description' },
  { title: 'Doctor', key: 'doctor' },
  { title: 'Date', key: 'date' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const records = ref([
  // Sample data - replace with API call
  {
    id: '1',
    patientId: '1',
    patientName: 'John Doe',
    type: 'diagnosis',
    description: 'Common cold',
    notes: 'Patient reported symptoms for 3 days',
    doctor: 'Dr. Smith',
    date: '2024-03-15'
  }
])

const canEdit = computed(() => {
  const userRole = localStorage.getItem('userRole')
  return userRole === 'doctor' || userRole === 'admin'
})

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'View Record' : 'Edit Record'
})

const viewRecord = (item: any) => {
  editedIndex.value = records.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialog.value = true
}

const editRecord = (item: any) => {
  editedIndex.value = records.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialog.value = true
}

const close = () => {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem)
  editedIndex.value = -1
}

const save = async () => {
  try {
    // Update existing record
    await fetch(`/api/records/${editedItem.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(editedItem.value)
    })
    Object.assign(records.value[editedIndex.value], editedItem.value)
    close()
  } catch (error) {
    console.error('Error saving record:', error)
  }
}

// Fetch records on component mount
const fetchRecords = async () => {
  try {
    loading.value = true
    const response = await fetch('/api/records')
    const data = await response.json()
    records.value = data
  } catch (error) {
    console.error('Error fetching records:', error)
  } finally {
    loading.value = false
  }
}

fetchRecords()
</script> 