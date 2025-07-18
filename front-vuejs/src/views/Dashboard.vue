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
  import GuardarGasto from './dashboard/GuardarGasto.vue'
  import EstadoResultados from './dashboard/EstadoResultados.vue'
  import GuardarIngreso from './dashboard/GuardarIngreso.vue'
  import Estadisticas from './dashboard/Estadisticas.vue'
  </script>
  