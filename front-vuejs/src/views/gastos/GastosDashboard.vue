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
</template>

<script setup>
import GuardarGasto from '../dashboard/GuardarGasto.vue'
import EstadoResultados from '../dashboard/EstadoResultados.vue'
import GuardarIngreso from '../dashboard/GuardarIngreso.vue'
import Estadisticas from '../dashboard/Estadisticas.vue'
</script>

<style scoped>
/* Estilos específicos del grid de gastos */
.grid-container {
  display: grid;
  grid-template-areas:
    "gastos resultados"
    "ingresos estadisticas";
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 20px;
  padding: 10px;
}

@media (max-width: 1024px) {
  .grid-container {
    grid-template-areas:
      "gastos"
      "resultados"
      "ingresos"
      "estadisticas";
    grid-template-columns: 1fr;
  }
}
</style>
