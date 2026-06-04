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
    <!-- Botón de la Tuerca Mejorado -->
    <button @click="alternarMenu" class="btn-configuracion" aria-label="Configuración">
      <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="icon-gear">
        <circle cx="12" cy="12" r="3"></circle>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
      </svg>
    </button>

    <!-- Menú Desplegable -->
    <transition name="slide-fade">
      <div v-if="menuAbierto" class="menu-desplegable">
        <h3>Configuración</h3>
        <hr />
        
        <!-- BLOQUE 1: APARIENCIA  -->
        <div class="seccion-menu">
          <h4>Apariencia</h4>
          <p>Selecciona un tema:</p>
          
          <div class="opciones-tema">
            <button @click="setTheme('light')" :class="{ activo: currentTheme === 'light' }" class="btn-tema light" title="Claro"></button>
            <button @click="setTheme('dark')" :class="{ activo: currentTheme === 'dark' }" class="btn-tema dark" title="Oscuro"></button>
            <button @click="setTheme('ocean')" :class="{ activo: currentTheme === 'ocean' }" class="btn-tema ocean" title="Océano"></button>
            <button @click="setTheme('forest')" :class="{ activo: currentTheme === 'forest' }" class="btn-tema forest" title="Bosque"></button>
          </div>
          <p class="tema-actual">Actual: <span>{{ currentTheme }}</span></p>
        </div>
      </div>
    </transition>
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
const currentTheme = ref('light')

const alternarMenu = () => {
  menuAbierto.value = !menuAbierto.value
}

const setTheme = (theme) => {
  currentTheme.value = theme
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (savedTheme) {
    setTheme(savedTheme)
  } else if (prefersDark) {
    setTheme('dark')
  } else {
    setTheme('light')
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
  font-family: 'Poppins', sans-serif;
}

/* Estilo del botón de tuerca mejorado */
.btn-configuracion {
  background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
  border: 1px solid rgba(0,0,0,0.1);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #333;
}

.btn-configuracion:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
  background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
}

.btn-configuracion:hover .icon-gear {
  transform: rotate(90deg);
}

.icon-gear {
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Ventana del menú desplegable */
.menu-desplegable {
  position: absolute;
  top: 60px;
  right: 0;
  background: var(--bg-principal);
  color: var(--texto-principal);
  border: 1px solid var(--borde-color);
  border-radius: 12px;
  padding: 20px;
  width: 240px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  backdrop-filter: blur(5px);
}

.menu-desplegable h3 {
  margin: 0 0 15px 0;
  font-size: 18px;
  font-weight: 600;
}

.seccion-menu h4 {
  margin: 15px 0 10px 0;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.8;
}

.seccion-menu p {
  font-size: 13px;
  margin-bottom: 15px;
}

/* Opciones de tema */
.opciones-tema {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 15px;
}

.btn-tema {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
}

.btn-tema:hover {
  transform: scale(1.2);
}

.btn-tema.activo {
  border-color: var(--accent-color);
  box-shadow: 0 0 8px var(--accent-color);
}

.btn-tema.light { background-color: #ffffff; border: 1px solid #ddd; }
.btn-tema.dark { background-color: #121212; }
.btn-tema.ocean { background-color: #001f3f; }
.btn-tema.forest { background-color: #1b3022; }

.tema-actual {
  font-size: 12px;
  text-align: center;
  margin-top: 10px;
}

.tema-actual span {
  font-weight: bold;
  text-transform: capitalize;
  color: var(--accent-color);
}

/* Animaciones */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

hr {
  border: 0;
  border-top: 1px solid var(--borde-color);
  margin: 10px 0;
  opacity: 0.3;
}
</style>