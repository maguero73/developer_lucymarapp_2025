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
import { ref, onMounted } from 'vue'
import api from '@/helpers/api'

const resultado = ref(null)
const anioSeleccionado = ref("")
const loading = ref(false)
const hasQueried = ref(false)
const anios = ref([])

const titulares = ref([])
const tiposGasto = ref([])
const codTitular = ref(0)
const codGasto = ref(0)

onMounted(async () => {
  try {
    const [resTitulares, resTipos, resAnios] = await Promise.all([
      api.get('/titulares'),
      api.get('/tipos-gasto'),
      api.get('/reportes/anios')
    ])
    titulares.value = resTitulares.data || []
    tiposGasto.value = resTipos.data || []
    anios.value = resAnios.data || []
  } catch (error) {
    console.error("Error al cargar filtros:", error)
  }
})

const fetchData = async () => {
  if (!anioSeleccionado.value) {
    alert("Por favor seleccioná un año")
    return
  }

  loading.value = true
  resultado.value = null
  hasQueried.value = false

  try {
    const response = await api.get('/reportes/gastos-anuales', {
      params: {
        cod_titular: codTitular.value,
        cod_gasto: codGasto.value
      }
    })
    
    const dataForYear = response.data.find(item => item.anio === parseInt(anioSeleccionado.value))
    
    if (dataForYear) {
      resultado.value = dataForYear
    } else {
      resultado.value = null
    }
    hasQueried.value = true
  } catch (error) {
    console.error("Error al obtener datos:", error)
    alert("No se pudieron obtener los datos del reporte anual")
  } finally {
    loading.value = false
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

<style scoped>
.header-section {
  text-align: center;
  margin-bottom: 2rem;
}

.subtitle {
  color: var(--texto-principal);
  opacity: 0.7;
  font-size: 0.95rem;
}

.filtros-container {
  background: var(--card-bg);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--borde-color);
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.filtros-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  align-items: end;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--accent-color, #3b82f6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-select {
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid var(--input-border);
  background-color: var(--input-bg);
  color: var(--input-text);
  width: 100%;
}

.btn-consultar {
  width: 100%;
  padding: 0.7rem;
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, #198754 0%, #157347 100%);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-consultar:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(25, 135, 84, 0.3);
}

.btn-consultar:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.resultados-card {
  background: var(--card-bg);
  border-radius: 12px;
  border: 1px solid var(--borde-color);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  animation: slideUp 0.4s ease-out;
}

.card-header {
  background: rgba(var(--bg-principal-rgb), 0.3);
  padding: 1.5rem;
  text-align: center;
  border-bottom: 1px solid var(--borde-color);
}

.card-header h4 {
  margin: 0;
  color: var(--texto-principal);
}

.card-header p {
  margin: 0.5rem 0 0;
  font-size: 0.85rem;
  color: var(--texto-principal);
  opacity: 0.6;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
}

.stats-table th {
  background: var(--texto-principal);
  color: var(--bg-principal);
  padding: 1rem;
  font-size: 0.9rem;
  text-align: center;
}

.stats-table td {
  padding: 1.2rem;
  text-align: center;
  border-bottom: 1px solid var(--borde-color);
  color: var(--texto-principal);
}

.monto-total {
  font-weight: 700;
  font-size: 1.2rem;
  color: #198754;
}

.no-results-msg {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 243, 205, 0.1);
  border: 1px solid #ffeeba;
  border-radius: 12px;
  color: var(--texto-principal);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.info-icon {
  width: 30px;
  height: 30px;
  background: #856404;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-style: normal;
}

.loader {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .filtros-grid {
    grid-template-columns: 1fr;
  }
}
</style>
