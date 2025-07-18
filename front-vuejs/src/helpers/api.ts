import axios from 'axios';
import router from '../router'

// Creamos una instancia
const api = axios.create({
  baseURL: 'http://localhost:9000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token JWT a cada request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    //console.log('Token que se va a enviar:', token);

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar errores globales
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('No autorizado, redirigir al login o limpiar sesión');
            // 1. Borrar token
            localStorage.removeItem('access_token')
            // 2. Opcional: mensaje
            alert('Tu sesión expiró. Por favor, volvé a iniciar sesión.')
            // 3. Redirigir al login
            router.push('/login')
      
            
            

    }
    return Promise.reject(error);
  }
);

export default api;