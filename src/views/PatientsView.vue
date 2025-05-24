<template>
  <div>
    <v-card>
      <v-card-title>
        Patients
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
        :items="patients"
        :search="search"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.actions="{ item }">
          <v-icon
            small
            class="mr-2"
            @click="viewPatient(item.raw)"
          >
            mdi-eye
          </v-icon>
          <v-icon
            small
            class="mr-2"
            @click="editPatient(item.raw)"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            small
            @click="archivePatient(item.raw)"
          >
            mdi-archive
          </v-icon>
        </template>
      </v-data-table>
    </v-card>

    <!-- Add/Edit Patient Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="editedItem.name"
                  label="Name"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="editedItem.dob"
                  label="Date of Birth"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="editedItem.phone"
                  label="Phone"
                ></v-text-field>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const search = ref('')
const loading = ref(false)
const dialog = ref(false)
const editedIndex = ref(-1)
const editedItem = ref({
  id: '',
  name: '',
  dob: '',
  phone: ''
})

const defaultItem = {
  id: '',
  name: '',
  dob: '',
  phone: ''
}

const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Date of Birth', key: 'dob' },
  { title: 'Phone', key: 'phone' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const patients = ref([
  // Sample data - replace with API call
  {
    id: '1',
    name: 'John Doe',
    dob: '1990-01-01',
    phone: '123-456-7890'
  }
])

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'New Patient' : 'Edit Patient'
})

const viewPatient = (item: any) => {
  router.push(`/patients/${item.id}`)
}

const editPatient = (item: any) => {
  editedIndex.value = patients.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialog.value = true
}

const archivePatient = async (item: any) => {
  if (confirm('Are you sure you want to archive this patient?')) {
    try {
      // Replace with actual API call
      await fetch(`/api/patients/${item.id}`, {
        method: 'DELETE'
      })
      const index = patients.value.indexOf(item)
      patients.value.splice(index, 1)
    } catch (error) {
      console.error('Error archiving patient:', error)
    }
  }
}

const close = () => {
  dialog.value = false
  editedItem.value = Object.assign({}, defaultItem)
  editedIndex.value = -1
}

const save = async () => {
  try {
    if (editedIndex.value > -1) {
      // Update existing patient
      await fetch(`/api/patients/${editedItem.value.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editedItem.value)
      })
      Object.assign(patients.value[editedIndex.value], editedItem.value)
    } else {
      // Create new patient
      const response = await fetch('/api/patients', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editedItem.value)
      })
      const newPatient = await response.json()
      patients.value.push(newPatient)
    }
    close()
  } catch (error) {
    console.error('Error saving patient:', error)
  }
}
</script> 