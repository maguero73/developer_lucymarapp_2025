<template>
  <div class="cuadrante" id="estadisticas">
    <div class="header-section">
      <h2>Estadísticas</h2>
      <p class="subtitle">Visualiza el resumen de gastos anuales con filtros personalizados</p>
    </div>

    <div class="filtros-container">
      <div class="filtros-grid">
        <div class="form-group">
          <label for="anio">Año</label>
          <select id="anio" v-model="anioSeleccionado" class="form-select">
            <option disabled value="">Seleccione un año</option>
            <option v-for="anio in anios" :key="anio" :value="anio">{{ anio }}</option>
          </select>
        </div>

        <div class="form-group">
          <label for="titular">Titular</label>
          <select id="titular" v-model="codTitular" class="form-select">
            <option :value="0">Todos los titulares</option>
            <option v-for="titular in titulares" :key="titular.codigo" :value="titular.codigo">
              {{ titular.nombre }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="tipo_gasto">Tipo de Gasto</label>
          <select id="tipo_gasto" v-model="codGasto" class="form-select">
            <option :value="0">Todos los conceptos</option>
            <option v-for="tipo in tiposGasto" :key="tipo.codigo" :value="tipo.codigo">
              {{ tipo.descripcion }}
            </option>
          </select>
        </div>

        <div class="actions">
          <button
            class="btn-consultar"
            @click="fetchData"
            :disabled="loading"
          >
            <span v-if="loading" class="loader"></span>
            <span v-else>Consultar Reporte</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Mostrar tabla solo si hay datos -->
    <transition name="fade">
      <div v-if="resultado !== null" class="resultados-card">
        <div class="card-header">
          <h4>Resumen Anual: {{ anioSeleccionado }}</h4>
          <p>Total acumulado hasta Diciembre inclusive</p>
        </div>

        <div class="table-responsive">
          <table class="stats-table">
            <thead>
              <tr>
                <th>Periodo</th>
                <th>Concepto</th>
                <th>Monto Total</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Año {{ anioSeleccionado }}</td>
                <td>{{ getConceptoLabel() }}</td>
                <td class="monto-total">{{ formatCurrency(resultado.total || 0) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else-if="!loading && hasQueried" class="no-results-msg">
        <i class="info-icon">!</i>
        <p>No se encontraron datos para los filtros seleccionados en el año {{ anioSeleccionado }}.</p>
      </div>
    </transition>
  </div>
</template>

<script setup>
import '@/assets/estadisticas.css'
import { ref, onMounted, computed } from 'vue'
import { useEstadisticasStore } from '@/store/useEstadisticasStore'

const estadisticasStore = useEstadisticasStore()

const resultado = ref(null)
const anioSeleccionado = ref("")
const hasQueried = ref(false)

const titulares = computed(() => estadisticasStore.titulares)
const tiposGasto = computed(() => estadisticasStore.tiposGasto)
const anios = computed(() => estadisticasStore.anios)
const loading = computed(() => estadisticasStore.loading)

const codTitular = ref(0)
const codGasto = ref(0)

onMounted(async () => {
  console.log('Montado: fetch filtros de estadísticas via Modular Pinia')
  await estadisticasStore.fetchInitialData()
})

const fetchData = async () => {
  if (!anioSeleccionado.value) {
    alert("Por favor seleccioná un año")
    return
  }

  resultado.value = null
  hasQueried.value = false

  try {
    await estadisticasStore.fetchReportData({
      cod_titular: codTitular.value,
      cod_gasto: codGasto.value
    })
    
    const dataForYear = estadisticasStore.reporteData.find(item => item.anio === parseInt(anioSeleccionado.value))
    
    if (dataForYear) {
      resultado.value = dataForYear
    } else {
      resultado.value = null
    }
    hasQueried.value = true
  } catch (error) {
    console.error("Error al obtener datos:", error)
    alert("No se pudieron obtener los datos del reporte anual")
  }
}

const getConceptoLabel = () => {
  if (codGasto.value === 0) return 'Todos los conceptos'
  const tipo = tiposGasto.value.find(t => t.codigo === codGasto.value)
  return tipo ? tipo.descripcion : 'Concepto seleccionado'
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS'
  }).format(value)
}
</script>

