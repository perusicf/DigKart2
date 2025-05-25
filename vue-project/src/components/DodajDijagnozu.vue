<template>
  <form @submit.prevent="submit">
    <div>
      <label>Opis dijagnoze:</label>
      <textarea v-model="opis_dijagnoze" required></textarea>
    </div>
    <div>
      <label>Datum:</label>
      <input type="date" v-model="datum_dijagnoze" required />
    </div>
    <button type="submit">Spremi</button>
  </form>
</template>

<script>
export default {
  props: ['kartonId'],
  data() {
    return {
      opis_dijagnoze: '',
      datum_dijagnoze: ''
    }
  },
  methods: {
    async submit() {
      const user = JSON.parse(localStorage.getItem('user'))
      const payload = {
        karton_id: this.kartonId,
        lijecnik_id: user.user_id,
        opis_dijagnoze: this.opis_dijagnoze,
        datum_dijagnoze: this.datum_dijagnoze
      }

      const res = await fetch('http://127.0.0.1:8000/dijagnoze/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!res.ok) {
        alert('Greška pri dodavanju dijagnoze')
        return
      }

      this.$emit('saved')
    }
  }
}
</script>
