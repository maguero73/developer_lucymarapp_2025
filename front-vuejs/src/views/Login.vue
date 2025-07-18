<template>
    <div class="login">
        <h2>Iniciar sesión</h2>
        <form @submit.prevent="login">
            <label>Usuario:</label>
            <input v-model="username" type="text" required />

            <label>Contraseña:</label>
            <input v-model="password" type="password" required />

            <button type="submit">Ingresar</button>

            <p v-if="error" class="error">{{ error }}</p>
        </form>
    </div>
</template>
  
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/helpers/api'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
    error.value = ''
    try {
        const response = await api.post(
            '/login',
            new URLSearchParams({
                username: username.value,
                password: password.value,
            }),
            {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            }
        )
        const token = response.data.access_token;
        if (!token) throw new Error('Token no recibido');
            localStorage.setItem('access_token', token);
            router.push('/inicio') // o donde quieras redirigir
    } catch (err) {
        error.value = 'Usuario o contraseña incorrectos'
        console.error('Error en login:', err)
    }
}
</script>
  
<style scoped>
.login {
    max-width: 400px;
    margin: 3rem auto;
    padding: 2rem;
    border: 1px solid #ccc;
    border-radius: 8px;
}

input {
    display: block;
    width: 100%;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
    padding: 0.5rem;
}

button {
    padding: 0.6rem 1.5rem;
}

.error {
    color: red;
    margin-top: 1rem;
}
</style>
  