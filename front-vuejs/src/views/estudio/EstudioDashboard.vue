<template>
  <div class="estudio-dashboard">
    <div class="placeholder-content">
      <div class="icon">📚</div>
      <h1>Control de Estudio</h1>
      <p>Este módulo está en desarrollo.</p>
      <div class="features-preview">
        <div class="feature">
          <span>📅</span>
          <p>Calendario de Exámenes</p>
        </div>
        <div class="feature">
          <span>📝</span>
          <p>Seguimiento de Materias</p>
        </div>
        <div class="feature">
          <span>📊</span>
          <p>Gráficos de Progreso</p>
        </div>
      </div>
      <router-link to="/home" class="btn-back">Volver al Inicio</router-link>
    </div>
  </div>
</template>

<style scoped>
.estudio-dashboard {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.placeholder-content {
  text-align: center;
  background: var(--card-bg);
  padding: 50px;
  border-radius: 30px;
  border: 1px solid var(--borde-color);
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
  max-width: 600px;
}

.icon {
  font-size: 5rem;
  margin-bottom: 20px;
}

h1 {
  font-size: 2rem;
  margin-bottom: 10px;
}

p {
  opacity: 0.7;
  margin-bottom: 30px;
}

.features-preview {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 40px;
}

.feature {
  background: rgba(var(--accent-color-rgb, 0, 123, 255), 0.05);
  padding: 15px;
  border-radius: 15px;
  width: 120px;
}

.feature span {
  font-size: 1.5rem;
  display: block;
  margin-bottom: 5px;
}

.feature p {
  font-size: 0.8rem;
  margin: 0;
  opacity: 0.9;
}

.btn-back {
  display: inline-block;
  padding: 12px 30px;
  background: var(--accent-color);
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-back:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(var(--accent-color-rgb, 0, 123, 255), 0.3);
}
</style>
