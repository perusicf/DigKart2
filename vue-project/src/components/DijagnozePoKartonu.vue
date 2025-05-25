<template>
  <div class="dijagnoze">
    <h4>Dijagnoze za karton {{ kartonId }}</h4>

    <button @click="showForm = !showForm">
      {{ showForm ? 'Odustani' : 'Dodaj dijagnozu' }}
    </button>

    <DodajDijagnozu v-if="showForm" :karton-id="kartonId" @saved="refresh" />

    <div v-if="dijagnoze.length">
      <div v-for="d in dijagnoze" :key="d.dijagnoza_id" class="dijagnoza-box">
        <p><strong>ID:</strong> {{ d.dijagnoza_id }}</p>
        <p><strong>Opis:</strong> {{ d.opis_dijagnoze }}</p>
        <p><strong>Datum:</strong> {{ d.datum_dijagnoze }}</p>

        <div class="akcije">
          <button @click="edit(d)">Uredi</button>
          <button @click="obrisiDijagnozu(d.dijagnoza_id)">Obriši</button>
        </div>

        <UrediDijagnozu
          v-if="dijagnozaEdit && dijagnozaEdit.dijagnoza_id === d.dijagnoza_id"
          :dijagnoza="dijagnozaEdit"
          @cancel="dijagnozaEdit = null"
          @updated="refresh"
        />

        <TerapijePoDijagnozi :dijagnoza-id="d.dijagnoza_id" />
      </div>
    </div>
    <p v-else>Nema dijagnoza za ovaj karton.</p>
  </div>
</template>

<script>
import DodajDijagnozu from './DodajDijagnozu.vue'
import UrediDijagnozu from './UrediDijagnozu.vue'
import TerapijePoDijagnozi from './TerapijePoDijagnozi.vue'

export default {
  props: ['kartonId'],
  components: {
    DodajDijagnozu,
    UrediDijagnozu,
    TerapijePoDijagnozi
  },
  data() {
    return {
      dijagnoze: [],
      showForm: false,
      dijagnozaEdit: null
    }
  },
  async mounted() {
    await this.loadDijagnoze()
  },
  methods: {
    async loadDijagnoze() {
      try {
        const res = await fetch(`http://127.0.0.1:8000/dijagnoze/karton/${this.kartonId}`)
        this.dijagnoze = await res.json()
      } catch (err) {
        console.error(err)
        this.dijagnoze = []
      }
    },
    async obrisiDijagnozu(dijagnoza_id) {
      if (!confirm("Jeste li sigurni da želite obrisati ovu dijagnozu?")) return;

      try {
        const res = await fetch(`http://127.0.0.1:8000/dijagnoze/${dijagnoza_id}`, {
          method: 'DELETE'
        });
        if (!res.ok) throw new Error('Greška pri brisanju dijagnoze');
        await this.loadDijagnoze();
      } catch (err) {
        alert('Greška: ' + err.message);
      }
    },
    edit(dijagnoza) {
      this.dijagnozaEdit = { ...dijagnoza }
    },
    async refresh() {
      this.dijagnozaEdit = null
      this.showForm = false
      await this.loadDijagnoze()
    }
  }
}
</script>

<style scoped>
.dijagnoza-box {
  border: 1px solid #ccc;
  margin: 1rem 0;
  padding: 1rem;
}

.akcije {
  margin-top: 0.5rem;
}
.akcije button {
  margin-right: 0.5rem;
}
</style>
