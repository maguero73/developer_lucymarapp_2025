<template>
  <section class="estadisticas-panel">
    <header class="panel-header">
      <h2>Estadísticas y Reportes</h2>
      <p>Consultá reportes de negocio con una interfaz optimizada para desktop, tablet y pantallas táctiles.</p>
    </header>

    <div class="report-tabs" role="tablist" aria-label="Tipos de reportes">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        type="button"
        class="tab-button"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </div>

    <article v-if="activeTab === 'gastosAltos'" class="report-card">
      <h3>Gastos altos</h3>
      <p>Endpoint: <code>GET /api/reportes/gastos-altos?monto_minimo=...</code></p>
      <div class="report-form">
        <label for="monto_minimo">Monto mínimo</label>
        <input id="monto_minimo" v-model.number="gastosAltosForm.monto_minimo" type="number" min="0" step="0.01" />
        <button type="button" @click="consultarGastosAltos" :disabled="loading">
          {{ loading ? 'Consultando...' : 'Consultar gastos altos' }}
        </button>
      </div>
    </article>

    <article v-if="activeTab === 'ultimoGasto'" class="report-card">
      <h3>Último gasto por titular</h3>
      <p>Endpoint: <code>GET /api/reportes/ultimo-gasto/{cod_titular}</code></p>
      <div class="report-form">
        <label for="cod_titular">Código de titular</label>
        <input id="cod_titular" v-model.number="ultimoGastoForm.cod_titular" type="number" min="1" step="1" />
        <button type="button" @click="consultarUltimoGasto" :disabled="loading">
          {{ loading ? 'Consultando...' : 'Consultar último gasto' }}
        </button>
      </div>
    </article>

    <article v-if="activeTab === 'ingresosMensuales'" class="report-card">
      <h3>Ingresos mensuales</h3>
      <p>Endpoint: <code>GET /api/reportes/ingresos-mensuales?anio=...&mes=...</code></p>
      <div class="report-form report-form-inline">
        <div>
          <label for="anio">Año</label>
          <input id="anio" v-model.number="ingresosMensualesForm.anio" type="number" min="2000" step="1" />
        </div>
        <div>
          <label for="mes">Mes</label>
          <input id="mes" v-model.number="ingresosMensualesForm.mes" type="number" min="1" max="12" step="1" />
        </div>
        <button type="button" @click="consultarIngresosMensuales" :disabled="loading">
          {{ loading ? 'Consultando...' : 'Consultar ingresos' }}
        </button>
      </div>
    </article>

    <p v-if="error" class="message error">{{ error }}</p>
    <p v-if="success" class="message success">{{ success }}</p>

    <section v-if="resultado" class="result-card">
      <h3>Resultado</h3>
      <pre>{{ JSON.stringify(resultado, null, 2) }}</pre>
    </section>
  </section>
</template>

<script setup>
import '@/assets/estadisticas.css'
import { ref, reactive } from 'vue'
import api from '@/helpers/api'

const today = new Date()
const tabs = [
  { id: 'gastosAltos', label: 'Gastos altos' },
  { id: 'ultimoGasto', label: 'Último gasto' },
  { id: 'ingresosMensuales', label: 'Ingresos mensuales' }
]

const activeTab = ref('gastosAltos')
const loading = ref(false)
const error = ref('')
const success = ref('')
const resultado = ref(null)

const gastosAltosForm = reactive({
  monto_minimo: 10000
})

const ultimoGastoForm = reactive({
  cod_titular: 1
})

const ingresosMensualesForm = reactive({
  anio: today.getFullYear(),
  mes: today.getMonth() + 1
})

const limpiarMensajes = () => {
  error.value = ''
  success.value = ''
  resultado.value = null
}

const consultarGastosAltos = async () => {
  limpiarMensajes()
  if (gastosAltosForm.monto_minimo < 0) {
    error.value = 'El monto mínimo debe ser mayor o igual a 0.'
    return
  }

  loading.value = true
  try {
    const response = await api.get('/reportes/gastos-altos', {
      params: { monto_minimo: gastosAltosForm.monto_minimo }
    })
    resultado.value = response.data
    success.value = 'Reporte de gastos altos obtenido correctamente.'
  } catch (err) {
    error.value = err.response?.data?.detail || 'No se pudo consultar el reporte de gastos altos.'
  } finally {
    loading.value = false
  }
}

const consultarUltimoGasto = async () => {
  limpiarMensajes()
  if (!ultimoGastoForm.cod_titular || ultimoGastoForm.cod_titular < 1) {
    error.value = 'El código de titular debe ser un número mayor a 0.'
    return
  }

  loading.value = true
  try {
    const response = await api.get(`/reportes/ultimo-gasto/${ultimoGastoForm.cod_titular}`)
    resultado.value = response.data
    success.value = 'Reporte de último gasto obtenido correctamente.'
  } catch (err) {
    error.value = err.response?.data?.detail || 'No se pudo consultar el último gasto del titular.'
  } finally {
    loading.value = false
  }
}

const consultarIngresosMensuales = async () => {
  limpiarMensajes()
  if (ingresosMensualesForm.mes < 1 || ingresosMensualesForm.mes > 12) {
    error.value = 'El mes debe estar entre 1 y 12.'
    return
  }

  loading.value = true
  try {
    const response = await api.get('/reportes/ingresos-mensuales', {
      params: {
        anio: ingresosMensualesForm.anio,
        mes: ingresosMensualesForm.mes
      }
    })
    resultado.value = response.data
    success.value = 'Reporte de ingresos mensuales obtenido correctamente.'
  } catch (err) {
    error.value = err.response?.data?.detail || 'No se pudo consultar el reporte de ingresos mensuales.'
  } finally {
    loading.value = false
  }
}
</script>
