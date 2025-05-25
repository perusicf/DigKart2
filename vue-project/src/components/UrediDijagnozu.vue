<template>
  <form @submit.prevent="submit">
    <div>
      <label>Opis:</label>
      <textarea v-model="form.opis_dijagnoze" required></textarea>
    </div>
    <div>
      <label>Datum:</label>
      <input type="date" v-model="form.datum_dijagnoze" required />
    </div>
    <button type="submit">Ažuriraj</button>
    <button type="button" @click="$emit('cancel')">Odustani</button>
  </form>
</template>

<script>
export default {
  props: ['dijagnoza'],
  data() {
    return {
      form: {
        opis_dijagnoze: this.dijagnoza.opis_dijagnoze,
        datum_dijagnoze: this.dijagnoza.datum_dijagnoze
      }
    }
  },
  methods: {
    async submit() {
      const res = await fetch(`http://127.0.0.1:8000/dijagnoze/${this.dijagnoza.dijagnoza_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.form)
      })

      if (!res.ok) {
        alert('Greška pri ažuriranju dijagnoze')
        return
      }

      this.$emit('updated')
    }
  }
}
</script>
