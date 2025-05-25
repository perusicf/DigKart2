<template>
  <div class="dashboard">
    <h2>Liječnik - Popis pacijenata</h2>

    <table v-if="patients.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>OIB</th>
          <th>Ime</th>
          <th>Prezime</th>
          <th>Kontakt</th>
          <th>Akcija</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in patients" :key="p.pacijent_id">
          <td>{{ p.pacijent_id }}</td>
          <td>{{ p.oib }}</td>
          <td>{{ p.ime }}</td>
          <td>{{ p.prezime }}</td>
          <td>{{ p.kontakt }}</td>
          <td><button @click="selectedPatient = p.pacijent_id">Pregled kartona</button></td>
        </tr>
      </tbody>
    </table>

    <p v-else>Nema pacijenata za prikaz.</p>

    <listaKartona v-if="selectedPatient" :pacijent-id="selectedPatient" />
  </div>
</template>

<script>
import listaKartona from './listaKartona.vue'

export default {
  components: {
    listaKartona
  },
  data() {
    return {
      patients: [],
      selectedPatient: null,
      error: ''
    }
  },
  async mounted() {
    try {
      const res = await fetch('http://127.0.0.1:8000/patients/')
      if (!res.ok) throw new Error('Greška pri dohvaćanju pacijenata')
      this.patients = await res.json()
    } catch (err) {
      this.error = err.message
    }
  }
}
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  padding: 0.5rem;
  border: 1px solid #ddd;
}
button {
  padding: 0.4rem 0.7rem;
  cursor: pointer;
}
</style>
