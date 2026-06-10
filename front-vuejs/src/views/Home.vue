<template>
  <div class="home-hub">
    <div class="welcome-section">
      <h1>Bienvenido a Lucymar App</h1>
      <p>Selecciona el módulo con el que deseas trabajar hoy.</p>
    </div>

    <div class="modules-grid">
      <!-- Módulo Control de Gastos -->
      <router-link to="/gastos" class="module-card gastos">
        <div class="card-content">
          <div class="icon-wrapper">💰</div>
          <h3>Gastos</h3>
          <p>Gestiona tus ingresos, gastos y visualiza estadísticas detalladas.</p>
          <span class="btn-enter">Entrar →</span>
        </div>
      </router-link>

      <!-- Módulo Control de Estudio -->
      <router-link to="/estudio" class="module-card estudio">
        <div class="card-content">
          <div class="icon-wrapper">📚</div>
          <h3>Control de Estudio</h3>
          <p>Organiza tus materias, horarios y seguimiento de progreso académico.</p>
          <span class="btn-enter">Próximamente</span>
        </div>
      </router-link>

      <!-- Módulo Futuro (Ejemplo) -->
      <div class="module-card disabled">
        <div class="card-content">
          <div class="icon-wrapper">⚙️</div>
          <h3>Más Módulos</h3>
          <p>Estamos trabajando en nuevas herramientas para ti.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No logic needed for now
</script>

<style scoped>
.home-hub {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-section {
  text-align: center;
  margin-bottom: 50px;
  animation: fadeInDown 0.8s ease-out;
}

.welcome-section h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 10px;
  background: linear-gradient(135deg, var(--accent-color) 0%, #a855f7 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.welcome-section p {
  font-size: 1.1rem;
  opacity: 0.7;
}

.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  animation: fadeInUp 0.8s ease-out;
}

.module-card {
  background: var(--card-bg);
  border: 1px solid var(--borde-color);
  border-radius: 24px;
  padding: 40px;
  text-decoration: none;
  color: var(--texto-principal);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.module-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--accent-color) 0%, transparent 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
  z-index: 0;
}

.module-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  border-color: var(--accent-color);
}

.module-card:hover::before {
  opacity: 0.05;
}

.card-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.icon-wrapper {
  font-size: 4rem;
  margin-bottom: 20px;
  display: inline-block;
  transition: transform 0.3s ease;
}

.module-card:hover .icon-wrapper {
  transform: scale(1.2) rotate(5deg);
}

.module-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 15px;
}

.module-card p {
  font-size: 1rem;
  opacity: 0.7;
  margin-bottom: 25px;
  line-height: 1.6;
}

.btn-enter {
  display: inline-block;
  padding: 10px 25px;
  background: var(--accent-color);
  color: white;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.module-card:hover .btn-enter {
  padding: 10px 35px;
  box-shadow: 0 5px 15px rgba(var(--accent-color-rgb, 0, 123, 255), 0.4);
}

.module-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.module-card.disabled:hover {
  transform: none;
  box-shadow: none;
  border-color: var(--borde-color);
}

.module-card.disabled .btn-enter {
  background: #ccc;
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
