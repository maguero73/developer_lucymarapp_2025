<template>
  <form>
    <div class="cuadrante" id="ingresos">
      <h2>Carga de Ingresos</h2>


       <!-- Dropdown para seleccionar titular -->

    <label for="titular">Titular del Ingreso:</label>
    <select v-model="formIngreso.cod_titular">
      <option disabled value="">Seleccione un titular</option>
      <option v-for="titular in titulares" :key="titular.codigo" :value="titular.codigo">
        {{ titular.nombre }}
      </option>
    </select>

    <!-- Dropdown para seleccionar tipo de ingreso -->

    <label for="tipo_ingreso">Tipo de Ingreso:</label>
    <select v-model="formIngreso.cod_ingreso">
      <option disabled value="">Seleccione un concepto</option>
      <option v-for="tipo in tiposIngreso" :key="tipo.codigo" :value="tipo.codigo">
        {{ tipo.descripcion }}
      </option>
    </select>

    
    
    <!-- Input para la fecha -->
    <label for="fecha">Fecha del Ingreso:</label>
    <input type="date" v-model="formIngreso.fecha" />

      <!-- Input para el radio button tipo_moneda --> 

  <div class="radio-group-2">
  <input type="radio" id="ARS_2" name="moneda_ingreso" value="ARS" v-model="formIngreso.cod_moneda" />
  <label for="ARS_2">Pesos</label>

  <input type="radio" id="USD_2" name="moneda_ingreso" value="USD" v-model="formIngreso.cod_moneda" />
  <label for="USD_2">Dólares</label>
</div>

    <!-- Input para el monto -->
    <label for="monto">Monto Ingreso:</label>
    <input type="number" v-model="formIngreso.monto" required min="0" step="0.01" />

    <!-- Botón para guardar -->
    <button type="button" @click="guardarIngreso">Guardar Ingreso</button>
    <!-- Botón para resetear -->
    <button type="button" @click="resetIngreso">Nuevo Ingreso</button>


    <p v-if="success" class="success">{{ success }}</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</form>
</template>



<script setup>
import '@/assets/ingresos.css'
import { reactive, ref, onMounted, computed } from 'vue'
import ingresosApi from '@/controllers/ingresos'
import { useIngresosStore } from '@/store/useIngresosStore'

const ingresosStore = useIngresosStore()
const titulares = computed(() => ingresosStore.titulares)
const tiposIngreso = computed(() => ingresosStore.tiposIngreso)

const error = ref('')
const success = ref('')

// Usamos reactive para manejar el formulario completo
const formIngreso = reactive({
  cod_titular: '',
  cod_ingreso: '',
  fecha: '',
  monto: '',
  cod_moneda: ''
})

const loading = computed(() => ingresosStore.loading)

onMounted(async () => {
  console.log('Montado: fetch titulares y tipos de ingreso via Modular Pinia')
  await ingresosStore.fetchInitialData()
  if (ingresosStore.error) {
    error.value = ingresosStore.error
  }
})

//ACA INICIA LA FUNCION JAVASCRIPT GUARDAR INGRESO

const guardarIngreso = async () => {
  success.value = ''
  error.value = ''

  // Validaciones iniciales
  if (
    !formIngreso.cod_ingreso ||
    !formIngreso.cod_titular ||
    formIngreso.monto === '' ||
    !formIngreso.fecha ||
    !formIngreso.cod_moneda
  ) {
    alert('Por favor, complete todos los campos.')
    return
  }

  // Conversión segura de los campos numéricos
  const cod_ingreso = Number(formIngreso.cod_ingreso)
  const cod_titular = Number(formIngreso.cod_titular)
  const monto = parseFloat(formIngreso.monto)
  const tipo_cambio = 1200

  const ingreso = {
    cod_ingreso,
    cod_titular,
    monto,
    fecha: new Date(formIngreso.fecha).toISOString(),
    cod_moneda: formIngreso.cod_moneda,
    tipo_cambio,
    fecha_creacion: new Date().toISOString()
  }

  console.log('ingreso que se enviará:', ingreso)

  // Enviar a la API via Controller
  try {
    console.log('Entrando en guardaringreso')
    const response = await ingresosApi.saveIngreso(ingreso)
    success.value = response.data.mensaje || 'Ingreso guardado correctamente'
    alert('Ingreso guardado correctamente')
  } catch (err) {
    alert('Error al guardar ingreso')
    console.error('Error completo:', err)
    error.value = 'Error al guardar ingreso'
  }
}

function resetIngreso() {
  formIngreso.cod_titular = null
  formIngreso.cod_ingreso = null
  formIngreso.monto = 0
  formIngreso.fecha = ''
  formIngreso.cod_moneda = ''
  formIngreso.tipo_cambio = ''

  success.value = ''
  error.value = ''
}
</script>


  
  
