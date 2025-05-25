<template>
  <div>
    <h3>Kartoni za pacijenta ID {{ pacijentId }}</h3>

    <p v-if="error" class="error">{{ error }}</p>

    <table v-if="kartoni.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Datum otvaranja</th>
          <th>Status aktivnosti</th>
          <th>Akcija</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="k in kartoni" :key="k.karton_id">
          <tr>
            <td>{{ k.karton_id }}</td>
            <td>{{ k.datum_otvaranja }}</td>
            <td>{{ k.status_aktivnosti }}</td>
            <td>
              <button @click="toggleDijagnoze(k.karton_id)">
                {{ prikazaneDijagnoze.includes(k.karton_id) ? 'Sakrij dijagnoze' : 'Prikaži dijagnoze' }}
              </button>
            </td>
          </tr>

          <tr v-if="prikazaneDijagnoze.includes(k.karton_id)">
            <td colspan="4">
              <table v-if="dijagnoze[k.karton_id] && dijagnoze[k.karton_id].length">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Opis</th>
                    <th>Datum</th>
                    <th>Akcije</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="d in dijagnoze[k.karton_id]" :key="d.dijagnoza_id">
                    <td>{{ d.dijagnoza_id }}</td>
                    <td v-if="editingDijagnoza !== d.dijagnoza_id">{{ d.opis_dijagnoze }}</td>
                    <td v-else colspan="2">
                      <UrediDijagnozu
                        :dijagnoza="d"
                        @updated="refreshDijagnoze(k.karton_id); editingDijagnoza = null"
                        @cancel="editingDijagnoza = null"
                      />
                    </td>
                    <td v-if="editingDijagnoza !== d.dijagnoza_id">{{ d.datum_dijagnoze }}</td>
                    <td v-if="editingDijagnoza !== d.dijagnoza_id">
                      <button @click="editingDijagnoza = d.dijagnoza_id">Uredi</button>
                      <button @click="obrisiDijagnozu(d.dijagnoza_id, k.karton_id)" style="margin-left: 0.5rem;">Obriši</button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <p v-else>Nema dijagnoza za ovaj karton.</p>

              <DodajDijagnozu :karton-id="k.karton_id" @saved="refreshDijagnoze(k.karton_id)" />

              <div
                v-for="d in dijagnoze[k.karton_id]"
                :key="'t_' + d.dijagnoza_id"
                style="margin-top: 1rem"
              >
                <TerapijePoDijagnozi :dijagnoza-id="d.dijagnoza_id" />
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>

    <p v-else>Nema dostupnih kartona.</p>
  </div>
</template>

<script>
import DodajDijagnozu from './DodajDijagnozu.vue'
import UrediDijagnozu from './UrediDijagnozu.vue'
import TerapijePoDijagnozi from './TerapijePoDijagnozi.vue'

export default {
  props: ['pacijentId'],
  components: {
    DodajDijagnozu,
    UrediDijagnozu,
    TerapijePoDijagnozi
  },
  data() {
    return {
      kartoni: [],
      dijagnoze: {},
      prikazaneDijagnoze: [],
      editingDijagnoza: null,
      error: ''
    }
  },
  watch: {
    pacijentId: {
      immediate: true,
      handler() {
        this.kartoni = []
        this.dijagnoze = {}
        this.prikazaneDijagnoze = []
        this.fetchKartoni()
      }
    }
  },
  methods: {
    async fetchKartoni() {
      try {
        const res = await fetch(`http://127.0.0.1:8000/kartoni/pacijent/${this.pacijentId}`)
        if (!res.ok) throw new Error('Greška pri dohvaćanju kartona')
        this.kartoni = await res.json()
      } catch (err) {
        console.error(err)
        this.error = 'Neuspješno dohvaćanje kartona.'
      }
    },
    async toggleDijagnoze(kartonId) {
      const index = this.prikazaneDijagnoze.indexOf(kartonId)
      if (index >= 0) {
        this.prikazaneDijagnoze.splice(index, 1)
      } else {
        if (!this.dijagnoze[kartonId]) {
          await this.fetchDijagnoze(kartonId)
        }
        this.prikazaneDijagnoze.push(kartonId)
      }
    },
    async fetchDijagnoze(kartonId) {
      try {
        const res = await fetch(`http://127.0.0.1:8000/dijagnoze/karton/${kartonId}`)
        if (!res.ok) throw new Error('Greška pri dohvaćanju dijagnoza')
        const data = await res.json()
        this.dijagnoze = { ...this.dijagnoze, [kartonId]: data }
      } catch (err) {
        console.error(err)
        this.dijagnoze = { ...this.dijagnoze, [kartonId]: [] }
      }
    },
    async refreshDijagnoze(kartonId) {
      await this.fetchDijagnoze(kartonId)
    },
    async obrisiDijagnozu(dijagnozaId, kartonId) {
      if (!confirm('Jeste li sigurni da želite obrisati dijagnozu?')) return

      try {
        const res = await fetch(`http://127.0.0.1:8000/dijagnoze/${dijagnozaId}`, {
          method: 'DELETE'
        })
        if (!res.ok) throw new Error('Brisanje nije uspjelo')
        await this.refreshDijagnoze(kartonId)
      } catch (err) {
        alert('Greška pri brisanju dijagnoze')
        console.error(err)
      }
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
th,
td {
  padding: 0.5rem;
  border: 1px solid #ccc;
}
button {
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}
.error {
  color: red;
  margin: 1rem 0;
}
</style>
