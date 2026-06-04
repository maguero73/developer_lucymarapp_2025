<template>
    <main class="grid-container">
      <div class="cuadrante" id="gastos">
        <GuardarGasto />
      </div>
      <div class="cuadrante" id="resultados">
        <EstadoResultados />
      </div>
      <div class="cuadrante" id="ingresos">
        <GuardarIngreso />
      </div>
      <div class="cuadrante" id="estadisticas">
        <Estadisticas />
      </div>
    </main>


  <div class="contenedor-configuracion">
    <!-- Botón de la Tuerca -->
    <button @click="alternarMenu" class="btn-configuracion" aria-label="Configuración">
      ⚙️
    </button>

    <!-- Menú Desplegable -->
    <div v-if="menuAbierto" class="menu-desplegable">
      <h3>Configuración</h3>
      <hr />
      
      <!-- BLOQUE 1: APARIENCIA  -->
      <div class="seccion-menu">
        <h4>Apariencia</h4>
        <p>Tema:</p>
        
        <!-- Tu botón original ahora dentro del menú -->
        <button @click="cambiarApariencia" class="btn-accion">
          Dark
        </button>
      </div>
    </div>


  </div>
  </template>
  
  <script setup>

import GuardarGasto from './dashboard/GuardarGasto.vue'
import EstadoResultados from './dashboard/EstadoResultados.vue'
import GuardarIngreso from './dashboard/GuardarIngreso.vue'
import Estadisticas from './dashboard/Estadisticas.vue'

 
import { ref, onMounted } from 'vue'




// Estado para abrir/cerrar el menú
const menuAbierto = ref(false)

const alternarMenu = () => {
  menuAbierto.value = !menuAbierto.value
}

const isDark = ref(false)

const cambiarApariencia = () => {
  isDark.value = !isDark.value
  const theme = isDark.value ? 'dark' : 'light'
  
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}



onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    isDark.value = true
    document.documentElement.setAttribute('data-theme', 'dark')
  } else {
    document.documentElement.setAttribute('data-theme', 'light')
  }
})
  </script>
  

  <style scoped>
/* Contenedor fijo en la esquina superior derecha */
.contenedor-configuracion {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  font-family: sans-serif;
}

/* Estilo del botón de tuerca */
.btn-configuracion {
  font-size: 24px;
  background: #ffffff;
  border: 1px solid #ccc;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

/* Animación de rotación al pasar el mouse */
.btn-configuracion:hover {
  transform: rotate(45deg);
}

/* Ventana del menú desplegable */
.menu-desplegable {
  position: absolute;
  top: 55px;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  width: 220px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.15);
}

.menu-desplegable h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
}

.seccion-menu h4 {
  margin: 10px 0 5px 0;
  font-size: 14px;
  color: #555;
}

.seccion-menu p {
  font-size: 12px;
  color: #777;
  margin: 0 0 10px 0;
}

/* Estilo del botón interno (Apariencia) */
.btn-accion {
  width: 100%;
  padding: 8px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-accion:hover {
  background-color: #0056b3;
}
</style>