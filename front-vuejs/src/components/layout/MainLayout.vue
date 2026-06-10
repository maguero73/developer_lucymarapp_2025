<template>
  <div class="layout-container">
    <!-- Sidebar Moderna -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <span v-if="!isCollapsed" class="logo-text">Lucymar App</span>
        </div>
        <button @click="isCollapsed = !isCollapsed" class="btn-toggle">
          {{ isCollapsed ? '→' : '←' }}
        </button>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/home" class="nav-item" title="Inicio">
          <span class="nav-icon">🏠</span>
          <span v-if="!isCollapsed" class="nav-text">Inicio</span>
        </router-link>
        <router-link to="/gastos" class="nav-item" title="Control de Gastos">
          <span class="nav-icon">💰</span>
          <span v-if="!isCollapsed" class="nav-text">Gastos</span>
        </router-link>
        <router-link to="/estudio" class="nav-item" title="Control de Estudio">
          <span class="nav-icon">📚</span>
          <span v-if="!isCollapsed" class="nav-text">Estudio</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="nav-item logout" title="Cerrar Sesión">
          <span class="nav-icon">🚪</span>
          <span v-if="!isCollapsed" class="nav-text">Salir</span>
        </button>
      </div>
    </aside>

    <!-- Contenido Principal -->
    <main class="main-content">
      <header class="top-bar">
        <h2 class="page-title">{{ currentPageTitle }}</h2>
        
        <div class="top-bar-actions">
          <!-- Configuración Gear (Movido aquí) -->
          <div class="contenedor-configuracion">
            <button @click="menuAbierto = !menuAbierto" class="btn-configuracion" aria-label="Configuración">
              <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="icon-gear">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
            </button>

            <transition name="slide-fade">
              <div v-if="menuAbierto" class="menu-desplegable">
                <h3>Configuración</h3>
                <hr />
                <div class="seccion-menu">
                  <h4>Apariencia</h4>
                  <div class="opciones-tema">
                    <button @click="setTheme('light')" :class="{ activo: currentTheme === 'light' }" class="btn-tema light" title="Claro"></button>
                    <button @click="setTheme('dark')" :class="{ activo: currentTheme === 'dark' }" class="btn-tema dark" title="Oscuro"></button>
                    <button @click="setTheme('ocean')" :class="{ activo: currentTheme === 'ocean' }" class="btn-tema ocean" title="Océano"></button>
                    <button @click="setTheme('forest')" :class="{ activo: currentTheme === 'forest' }" class="btn-tema forest" title="Bosque"></button>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </header>

      <div class="content-wrapper">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isCollapsed = ref(false)
const menuAbierto = ref(false)
const currentTheme = ref('light')

const currentPageTitle = computed(() => {
  switch (route.path) {
    case '/home': return 'Panel de Control'
    case '/gastos': return 'Control de Gastos'
    case '/estudio': return 'Control de Estudio'
    default: return 'Lucymar App'
  }
})

const setTheme = (theme) => {
  currentTheme.value = theme
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) setTheme(savedTheme)
})
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: var(--bg-principal);
  color: var(--texto-principal);
  transition: all 0.4s ease;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: var(--card-bg);
  border-right: 1px solid var(--borde-color);
  display: flex;
  flex-direction: column;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 100;
}

.sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--borde-color);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  font-size: 1.2rem;
  white-space: nowrap;
}

.logo-icon {
  font-size: 1.5rem;
}

.btn-toggle {
  background: none;
  border: none;
  color: var(--texto-principal);
  cursor: pointer;
  font-size: 1.2rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.btn-toggle:hover {
  opacity: 1;
}

.sidebar-nav {
  flex: 1;
  padding: 20px 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 15px;
  border-radius: 10px;
  text-decoration: none;
  color: var(--texto-principal);
  opacity: 0.7;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.nav-item:hover, .nav-item.router-link-active {
  opacity: 1;
  background: rgba(var(--accent-color-rgb, 0, 123, 255), 0.1);
  color: var(--accent-color);
}

.nav-icon {
  font-size: 1.2rem;
  min-width: 24px;
  text-align: center;
}

.sidebar-footer {
  padding: 20px 10px;
  border-top: 1px solid var(--borde-color);
}

.logout:hover {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-bar {
  height: 70px;
  padding: 0 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(var(--bg-principal-rgb, 255, 255, 255), 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--borde-color);
  z-index: 90;
}

.page-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0;
}

.content-wrapper {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  background: var(--bg-principal);
}

/* Configuración Gear Styles (Adaptados) */
.contenedor-configuracion {
  position: relative;
}

.btn-configuracion {
  background: var(--card-bg);
  border: 1px solid var(--borde-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: var(--texto-principal);
}

.btn-configuracion:hover {
  transform: rotate(45deg);
  border-color: var(--accent-color);
}

.menu-desplegable {
  position: absolute;
  top: 50px;
  right: 0;
  background: var(--card-bg);
  border: 1px solid var(--borde-color);
  border-radius: 12px;
  padding: 15px;
  width: 200px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.opciones-tema {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.btn-tema {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
}

.btn-tema.activo {
  border-color: var(--accent-color);
}

.btn-tema.light { background: #fff; border: 1px solid #ddd; }
.btn-tema.dark { background: #333; }
.btn-tema.ocean { background: #001f3f; }
.btn-tema.forest { background: #1b3022; }

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from, .slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>
