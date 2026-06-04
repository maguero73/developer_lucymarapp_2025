<template>
    <div class="cuadrante" id="resultados">
      <h2>Estado de Resultados</h2>
      <p class="description">Consulta el consolidado de tus gastos actualizados.</p>
      
      <div class="filtros-container">
        <h3>Filtros de Consolidación</h3>
        <div class="filtros-grid">
          <div class="form-group">
            <label for="fecha_desde">Fecha Desde</label>
            <input type="date" id="fecha_desde" v-model="filtros.fecha_desde">
          </div>
          <div class="form-group">
            <label for="fecha_hasta">Fecha Hasta</label>
            <input type="date" id="fecha_hasta" v-model="filtros.fecha_hasta">
          </div>
          <div class="form-group">
            <label for="cod_titular">Cód. Titular (0 = todos)</label>
            <input type="text" id="cod_titular" v-model="filtros.cod_titular" placeholder="Ej: 1, 2">
          </div>
          <div class="form-group">
            <label for="cod_gasto">Cód. Gasto (0 = todos)</label>
            <input type="text" id="cod_gasto" v-model="filtros.cod_gasto" placeholder="Ej: 10, 20">
          </div>
          <div class="form-group">
            <label for="codigo_moneda">Moneda</label>
            <select id="codigo_moneda" v-model="filtros.codigo_moneda">
              <option value="ARS">ARS</option>
              <option value="USD">USD</option>
            </select>
          </div>
        </div>
      </div>
  
      <div class="actions">
        <button @click="consolidarGastos" :disabled="loading" class="btn-consolidar">
          <span v-if="loading" class="loader"></span>
          <span v-else>Consolidar Gastos</span>
        </button>
      </div>
  
      <div v-if="error" class="error-msg">
        {{ error }}
      </div>
  
      <div v-if="resultados && resultados.length > 0" class="resultados-container">
        <h3>Resumen de Gastos</h3>
        
        <!-- DEBUG: Eliminar luego -->
        <details style="margin-bottom: 1rem; background: #eee; padding: 0.5rem;">
          <summary>Ver datos crudos (Debug)</summary>
          <pre>{{ resultados }}</pre>
        </details>

        <div class="table-responsive">
          <table class="resultados-table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Titular</th>
                <th>Gasto</th>
                <th>Moneda</th>
                <th>Monto</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in resultados" :key="index">
                <td>{{ formatDate(item.fecha) }}</td>
                <td>{{ item.titular || item.cod_titular || 'Sin datos' }}</td>
                <td>{{ item.nombre_gasto || item.cod_gasto || 'Sin datos' }}</td>
                <td>{{ item.codigo_moneda }}</td>
                <td class="monto">{{ formatCurrency(item.monto, item.codigo_moneda) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else-if="resultados && resultados.length === 0" class="no-results">
        <p>No se encontraron resultados para los filtros seleccionados.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import '@/assets/resultados.css'
  import { ref, reactive } from 'vue'
  import api from '@/helpers/api'
  
  const resultados = ref(null)
  const loading = ref(false)
  const error = ref('')
  
  // Inicializamos fechas con el día de hoy
  const today = new Date().toISOString().split('T')[0]
  
  const filtros = reactive({
    fecha_desde: today,
    fecha_hasta: today,
    cod_titular: '0',
    cod_gasto: '0',
    codigo_moneda: 'ARS'
  })
  
  const consolidarGastos = async () => {
    loading.value = true
    error.value = ''
    resultados.value = null
  
    try {
      // Preparamos el payload convirtiendo strings a arrays de números
      const payload = {
        fecha_desde: filtros.fecha_desde,
        fecha_hasta: filtros.fecha_hasta,
        cod_titular: filtros.cod_titular.split(',').map(n => parseInt(n.trim()) || 0),
        cod_gasto: filtros.cod_gasto.split(',').map(n => parseInt(n.trim()) || 0),
        codigo_moneda: filtros.codigo_moneda
      }
  
      const response = await api.post('/consolidado_gastos', payload)
      console.log('Respuesta consolidado:', response.data)
      // Aseguramos que sea un array
      resultados.value = Array.isArray(response.data) ? response.data : [response.data]
    } catch (err) {
      console.error('Error al consolidar gastos:', err)
      if (err.response) {
        const detail = err.response.data?.detail || err.response.statusText || 'Error desconocido';
        error.value = `Error del servidor (${err.response.status}): ${typeof detail === 'object' ? JSON.stringify(detail) : detail}`
      } else if (err.request) {
        error.value = 'No se pudo conectar con el servidor. Verifica que el backend esté corriendo.'
      } else {
        error.value = `Error de configuración: ${err.message}`
      }
    } finally {
      loading.value = false
    }
  }
  
  const formatCurrency = (value, currency) => {
    if (typeof value === 'number') {
      return new Intl.NumberFormat('es-AR', { style: 'currency', currency: currency || filtros.codigo_moneda }).format(value)
    }
    return value
  }

  const formatDate = (dateString) => {
    if (!dateString) return '-'
    // Asumiendo formato YYYY-MM-DD
    const [year, month, day] = dateString.split('-')
    return `${day}/${month}/${year}`
  }
  </script>