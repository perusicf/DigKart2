<template>
  <div class="terapije">
    <h5>Terapije za dijagnozu {{ dijagnozaId }}</h5>

    <ul>
      <li v-for="t in terapije" :key="t.terapija_id">
        {{ t.opis_terapije }}
        <button @click="urediTerapiju(t)">Uredi</button>
        <button @click="obrisi(t.terapija_id)">Obriši</button>
      </li>
    </ul>

    <form @submit.prevent="dodajTerapiju">
      <input v-model="opis_terapije" placeholder="Unesi terapiju" required />
      <button type="submit">Dodaj</button>
    </form>
  </div>
</template>

<script>
export default {
  props: ['dijagnozaId'],
  data() {
    return {
      terapije: [],
      opis_terapije: ''
    }
  },
  mounted() {
    this.ucitajTerapije()
  },
  methods: {
    async ucitajTerapije() {
      try {
        const res = await fetch(`http://127.0.0.1:8000/terapije/dijagnoza/${this.dijagnozaId}`)
        if (!res.ok) throw new Error('Greška pri dohvaćanju terapija')
        this.terapije = await res.json()
      } catch (err) {
        console.error(err)
        alert('Neuspješno učitavanje terapija')
      }
    },
    async dodajTerapiju() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        const payload = {
          opis_terapije: this.opis_terapije,
          dijagnoza_id: this.dijagnozaId,
          lijecnik_id: user.user_id
        }

        const res = await fetch(`http://127.0.0.1:8000/terapije/?role=${user.role}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })

        if (!res.ok) throw new Error('Greška pri dodavanju terapije')

        this.opis_terapije = ''
        await this.ucitajTerapije()
      } catch (err) {
        console.error(err)
        alert('Greška pri dodavanju terapije')
      }
    },
    async obrisi(id) {
      if (!confirm('Jeste li sigurni da želite obrisati terapiju?')) return
      try {
        const res = await fetch(`http://127.0.0.1:8000/terapije/${id}`, { method: 'DELETE' })
        if (!res.ok) throw new Error('Greška pri brisanju')
        await this.ucitajTerapije()
      } catch (err) {
        console.error(err)
        alert('Greška pri brisanju terapije')
      }
    },
    async urediTerapiju(terapija) {
      const noviOpis = prompt("Unesi novi opis terapije:", terapija.opis_terapije)
      if (noviOpis === null || noviOpis.trim() === '') return

      try {
        const res = await fetch(`http://127.0.0.1:8000/terapije/${terapija.terapija_id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ opis_terapije: noviOpis })
        })
        if (!res.ok) throw new Error('Greška pri ažuriranju terapije')
        await this.ucitajTerapije()
      } catch (err) {
        console.error(err)
        alert('Greška pri ažuriranju terapije')
      }
    }
  }
}
</script>
