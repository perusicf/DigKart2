<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <label for="username">Username:</label>
      <input v-model="username" required />

      <label for="password">Password:</label>
      <input type="password" v-model="password" required />

      <button type="submit">Login</button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      try {
        const response = await fetch('http://127.0.0.1:8000/korisnici/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password })
        });

        if (!response.ok) throw new Error('Login failed');

        const data = await response.json();
        localStorage.setItem('user', JSON.stringify(data));

        // redirect by role
        switch (data.role) {
          case 'lijecnik':
            this.$router.push('/lijecnik');
            break;
          case 'administrator':
            this.$router.push('/admin');
            break;
          case 'medicinski_djelatnik':
            this.$router.push('/medicinski_djelatnik');
            break;
          default:
            throw new Error('Unknown role');
        }
      } catch (err) {
        this.error = err.message;
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: auto;
  padding: 2rem;
  border: 1px solid #ccc;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
