
<script setup>

import '@/assets/gastos.css'
import { ref, reactive, onMounted, watch } from 'vue'
import api from '@/helpers/api';

const titulares = ref([])
const tipos_gasto = ref([]) 

const error = ref('')
const success = ref('')

const form = reactive({
  cod_titular: '',
  cod_gasto: '',
  monto: '',
  fecha: '',
  cod_moneda: ''
})

const loading = ref(true)

onMounted(async () => {
  console.log('Montado: fetch titulares y tipos de gasto')
  try {
    const [res1, res2] = await Promise.all([

    api.get('/titulares'),
    api.get('/tipos-gasto')
    ])

    const data1 = res1.data
    const data2 = res2.data

    console.log('Titulares recibidos:', data1)
    console.log('Tipos de gasto recibidos:', data2)

    titulares.value = data1
    tipos_gasto.value = data2

  } catch (err) {
    console.error('Error al cargar datos:', err)
    error.value = 'Error al cargar datos'
  } finally {
    loading.value = false
  }
})


//ACA INICIA LA FUNCION JAVASCRIPT GUARDAR GASTO


const guardarGasto = async () => {

  success.value = ''
  error.value = ''

  // Validaciones iniciales
  if (
    !form.cod_gasto ||
    !form.cod_titular ||
    form.monto === '' ||
    !form.fecha ||
    !form.cod_moneda
  ) {
    alert('Por favor, complete todos los campos.')
    return
  }

  // Conversión segura de los campos numéricos
  const cod_gasto = Number(form.cod_gasto)
  const cod_titular = Number(form.cod_titular)
  const monto = parseFloat(form.monto)
  const tipo_cambio = 1200

  console.log('form.cod_titular:', form.cod_titular, typeof form.cod_titular)
  console.log('form.cod_gasto:', form.cod_gasto, typeof form.cod_gasto)

  if (!form.cod_titular || !form.cod_gasto) {
    alert('Debe seleccionar un titular y un tipo de gasto.')
    return
  }

  const gasto = {
    cod_gasto,
    cod_titular,
    monto,
    fecha: new Date(form.fecha).toISOString(),
    cod_moneda: form.cod_moneda,
    tipo_cambio,
    fecha_creacion: new Date().toISOString()
  }

  console.log('Gasto que se enviará:', gasto)

  // Enviar a la API
  try {
    
    console.log('Entrando en guardarGasto')
    const response = await api.post('/gastos', gasto)
    success.value = response.data.mensaje || 'Gasto guardado correctamente'
    alert('Gasto guardado correctamente')
    

  } catch (err) {
    alert('Error al guardar gasto')
  console.error('Error completo:', err)

  // Si es error HTTP con Axios
  if (err.response) {
    console.log('Código de estado:', err.response.status)
    console.log('Respuesta del servidor:', err.response.data)
  }

  error.value = 'Error al guardar gasto'
}
}


function resetGasto() {
  form.cod_titular = null
  form.cod_gasto = null
  form.monto = 0
  form.fecha = ''
  form.cod_moneda = ''
  form.tipo_cambio = ''

  success.value = ''
  error.value = ''
}

</script>




<template>
  <form>
<div class="cuadrante" id="gastos">
  <h2>Carga de Gastos</h2>

  <!-- Dropdown para seleccionar Titulares -->

<div v-if="titulares.length">
  <label for="titular">Titular del Gasto:</label>
  <select id="titular" v-model="form.cod_titular">
    <option disabled value="">Seleccione un titular</option>
    <option v-for="titular in titulares" :key="titular.codigo" :value="titular.codigo">
      {{ titular.nombre }}
    </option>
  </select>
</div>
<div v-else>
  Cargando titulares...
</div>



  <!-- Dropdown para seleccionar tipo de gasto -->
 <!-- Tipos de gasto -->
<div v-if="tipos_gasto.length">
  <label for="tipo_gasto">Tipo de Gasto:</label>
  <select id="tipo_gasto" v-model="form.cod_gasto">
    <option disabled value="">Seleccione un concepto</option>
    <option v-for="tipo in tipos_gasto" :key="tipo.codigo" :value="tipo.codigo">
      {{ tipo.descripcion }}
    </option>
  </select>
</div>
<div v-else>
  Cargando tipos de gasto...
</div>


  <!-- Input para la fecha -->
  <label for="fecha">Fecha del Gasto:</label>
  <input type="date" v-model="form.fecha" />

  <!-- Input para el radio button tipo_moneda --> 

  <div class="radio-group">
  <input type="radio" id="ARS" name="moneda" value="ARS" v-model="form.cod_moneda" />
  <label for="ARS">Pesos</label>

  <input type="radio" id="USD" name="moneda" value="USD" v-model="form.cod_moneda" />
  <label for="USD">Dólares</label>
</div>


  <!-- Input para el monto -->
  <label for="monto">Monto Gasto:</label>
  <input type="number" v-model="form.monto" required min="0" step="0.01" />



  <!-- Input para tipo de cambio 
<label for="tipo_cambio">Tipo de Cambio:</label>
<input type="number" v-model="form.tipo_cambio" required min="0" step="0.01" />
-->

  <!-- Botón para guardar -->
  <button type="button" @click="guardarGasto" :disabled="loading">
  Guardar Gasto
</button>

 <!-- Botón para resetear -->
<button type="button" @click="resetGasto">Nuevo Gasto</button>


<p v-if="success" class="success">{{ success }}</p>
<p v-if="error" class="error">{{ error }}</p>


  
</div>
</form>



</template>