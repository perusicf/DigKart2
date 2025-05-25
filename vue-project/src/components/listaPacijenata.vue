<template>
  <div class="patients-list">
    <h2>Popis pacijenata</h2>
    <table v-if="patients.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>OIB</th>
          <th>Ime</th>
          <th>Prezime</th>
          <th>Kontakt</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in patients" :key="p.pacijent_id">
          <td>{{ p.pacijent_id }}</td>
          <td>{{ p.oib }}</td>
          <td>{{ p.ime }}</td>
          <td>{{ p.prezime }}</td>
          <td>{{ p.kontakt }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Nema dostupnih pacijenata.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      patients: [],
      error: ''
    };
  },
  async created() {
    try {
      const response = await fetch('http://127.0.0.1:8000/patients/');
      if (!response.ok) throw new Error('Failed to fetch');
      this.patients = await response.json();
    } catch (err) {
      this.error = err.message;
      console.error(err);
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1em;
}
th, td {
  padding: 0.5em;
  border: 1px solid #ccc;
}
</style>
