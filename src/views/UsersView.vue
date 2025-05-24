<template>
  <div>
    <v-card>
      <v-card-title>
        Users Management
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="addUser">
          <v-icon left>mdi-account-plus</v-icon>
          Add User
        </v-btn>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="users"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.role="{ item }">
          <v-chip
            :color="getRoleColor(item.raw.role)"
            text-color="white"
          >
            {{ item.raw.role }}
          </v-chip>
        </template>

        <template v-slot:item.status="{ item }">
          <v-chip
            :color="item.raw.status === 'active' ? 'success' : 'error'"
            text-color="white"
          >
            {{ item.raw.status }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-icon
            small
            class="mr-2"
            @click="editUser(item.raw)"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            small
            @click="toggleUserStatus(item.raw)"
          >
            {{ item.raw.status === 'active' ? 'mdi-account-off' : 'mdi-account-check' }}
          </v-icon>
        </template>
      </v-data-table>
    </v-card>

    <!-- Add/Edit User Dialog -->
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
                  v-model="editedItem.name"
                  label="Name"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.email"
                  label="Email"
                  type="email"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="editedItem.role"
                  :items="roles"
                  label="Role"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" v-if="editedIndex === -1">
                <v-text-field
                  v-model="editedItem.password"
                  label="Password"
                  type="password"
                  required
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

const loading = ref(false)
const dialog = ref(false)
const editedIndex = ref(-1)
const editedItem = ref({
  id: '',
  name: '',
  email: '',
  role: '',
  password: '',
  status: 'active'
})

const defaultItem = {
  id: '',
  name: '',
  email: '',
  role: '',
  password: '',
  status: 'active'
}

const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Email', key: 'email' },
  { title: 'Role', key: 'role' },
  { title: 'Status', key: 'status' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const roles = ['admin', 'doctor', 'medical_staff']

const users = ref([
  // Sample data - replace with API call
  {
    id: '1',
    name: 'Dr. Smith',
    email: 'smith@hospital.com',
    role: 'doctor',
    status: 'active'
  }
])

const formTitle = computed(() => {
  return editedIndex.value === -1 ? 'New User' : 'Edit User'
})

const getRoleColor = (role: string) => {
  switch (role) {
    case 'admin':
      return 'error'
    case 'doctor':
      return 'primary'
    case 'medical_staff':
      return 'success'
    default:
      return 'grey'
  }
}

const addUser = () => {
  editedIndex.value = -1
  editedItem.value = Object.assign({}, defaultItem)
  dialog.value = true
}

const editUser = (item: any) => {
  editedIndex.value = users.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialog.value = true
}

const toggleUserStatus = async (item: any) => {
  try {
    const newStatus = item.status === 'active' ? 'inactive' : 'active'
    await fetch(`/api/users/${item.id}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: newStatus })
    })
    item.status = newStatus
  } catch (error) {
    console.error('Error toggling user status:', error)
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
      // Update existing user
      await fetch(`/api/users/${editedItem.value.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editedItem.value)
      })
      Object.assign(users.value[editedIndex.value], editedItem.value)
    } else {
      // Create new user
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(editedItem.value)
      })
      const newUser = await response.json()
      users.value.push(newUser)
    }
    close()
  } catch (error) {
    console.error('Error saving user:', error)
  }
}
</script> 