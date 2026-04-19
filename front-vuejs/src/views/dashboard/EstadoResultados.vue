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
  
  <style scoped>
  .estado-resultados {
    padding: 10px;
  }
  
  .description {
    color: #666;
    margin-bottom: 20px;
  }
  
  /* Estilos del formulario */
  .filtros-container {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 25px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }
  
  .filtros-container h3 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 1.1rem;
    color: #444;
    border-bottom: 2px solid #ff9800;
    display: inline-block;
    padding-bottom: 5px;
  }
  
  .filtros-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  .form-group label {
    font-size: 0.9rem;
    margin-bottom: 5px;
    color: #555;
    font-weight: 500;
  }
  
  .form-group input,
  .form-group select {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.3s;
  }
  
  .form-group input:focus,
  .form-group select:focus {
    border-color: #ff9800;
    outline: none;
    box-shadow: 0 0 0 2px rgba(255, 152, 0, 0.2);
  }
  
  .actions {
    margin-bottom: 20px;
    text-align: center;
  }
  
  .btn-consolidar {
    background-color: #ff9800;
    color: white;
    border: none;
    padding: 12px 30px;
    font-size: 16px;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-weight: 600;
  }
  
  .btn-consolidar:hover:not(:disabled) {
    background-color: #f57c00;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
  }
  
  .btn-consolidar:disabled {
    background-color: #ffcc80;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  
  .error-msg {
    color: #d32f2f;
    background-color: #ffcdd2;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    text-align: center;
    border: 1px solid #e57373;
  }
  
  .resultados-container {
    animation: fadeIn 0.5s ease-in-out;
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  }

  .table-responsive {
    overflow-x: auto;
  }

  .resultados-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }

  .resultados-table th,
  .resultados-table td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #eee;
  }

  .resultados-table th {
    background-color: #f9f9f9;
    font-weight: 600;
    color: #555;
    text-transform: uppercase;
    font-size: 0.85rem;
  }

  .resultados-table tr:hover {
    background-color: #fff8e1; /* Hover suave naranja */
  }

  .resultados-table td.monto {
    font-weight: bold;
    color: #333;
    text-align: right;
  }
  
  .resultados-table th:last-child {
    text-align: right;
  }

  .no-results {
    text-align: center;
    color: #777;
    padding: 20px;
    background: white;
    border-radius: 8px;
  }
  
  .loader {
    border: 3px solid rgba(255,255,255,0.3);
    border-top: 3px solid #fff;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  </style>
  