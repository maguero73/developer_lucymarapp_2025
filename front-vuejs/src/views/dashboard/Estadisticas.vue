<template>
    <div class="cuadrante" id="estadisticas">
      <h2>Estadísticas</h2>
      <h2 class="text-center mb-4 text-primary">📊 Estadísticas de Gastos</h2>
  
      <div class="text-center mb-3">
        <select v-model="anioSeleccionado" class="form-select w-auto d-inline-block me-2">
          <option disabled value="">Seleccione un año</option>
          <option v-for="anio in anios" :key="anio" :value="anio">{{ anio }}</option>
        </select>
  
        <button
          class="btn btn-success"
          @click="fetchData"
        >
          Consultar
        </button>
      </div>
  
      <!-- Mostrar tabla solo si hay datos -->
      <transition name="fade">
        <div v-if="resultado !== null" class="card shadow p-4 mt-4">
          <h4 class="text-center mb-3 text-secondary">
            Total acumulado hasta Diciembre inclusive de {{ anioSeleccionado }} 💰
          </h4>
  
          <div class="table-responsive">
            <table class="table table-striped table-bordered align-middle text-center">
              <thead class="table-dark">
                <tr>
                  <th>Año</th>
                  <th>Total Gastos Acumulados</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{{ anioSeleccionado }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script>
  export default {
    name: "Estadistica",
    data() {
      return {
        resultado: null,
        anioSeleccionado: "",
        anios: [2022, 2023, 2024, 2025],
      };
    },
    methods: {
      async fetchData() {
        if (!this.anioSeleccionado) {
          alert("Por favor seleccioná un año");
          return;
        }
  
        //Llamada a GET
        try {
          const response = await fetch(`http://localhost:9000/api/consolidado_gastos${this.anioSeleccionado}`);
          if (!response.ok) throw new Error("Error en la respuesta del servidor");
          this.resultado = await response.json();
        } catch (error) {
          console.error("Error al obtener datos:", error);
          alert("No se pudieron obtener los datos");
        }
      },
      volver() {
      this.$router.push("/inicio"); // Regresa a la página principal
    }
    },
  };
  </script>
  
<style scoped>
  .estadisticas {
    padding: 10px;
  }
</style>
  