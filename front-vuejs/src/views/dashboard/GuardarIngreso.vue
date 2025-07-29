<template>
  <form>
    <div class="cuadrante" id="ingresos">
      <h2>Carga de Ingresos</h2>


     <!-- Dropdown Titulares -->
     <div v-if="store.titulares.length">
      <label for="titular">Titular:</label>
      <select v-model="formIngreso.cod_titular">
        <option value="">Seleccione un titular</option>
        <option v-for="t in store.titulares" :key="t.value" :value="t.value">
          {{ t.label }}
        </option>
      </select>
    </div>
    <div v-else>Cargando titulares...</div>

    <!-- Dropdown para seleccionar tipo de ingreso -->

    <label for="tipo_ingreso">Tipo de Ingreso:</label>
    <select v-model="formIngreso.cod_ingreso">
      <option disabled value="">Seleccione un concepto</option>
      <option v-for="t in store.tiposIngreso" :key="t.value" :value="t.value">
        {{ t.label }}
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
import { reactive, ref, onMounted, watch } from 'vue'
import api from '@/helpers/api';
import { useSolicitudesStore } from '@/store/useSolicitudesStore'



const titulares = ref([])
const tiposIngreso = ref([])
const mensaje = ref('')
const error = ref('')
const success = ref('')
const store = useSolicitudesStore()
const loading = ref(true)



// Usamos reactive para manejar el formulario completo
const formIngreso = reactive({
  cod_titular: '',
  cod_ingreso: '',
  fecha: '',
  monto: '',
  cod_moneda: ''
})

onMounted(async () => {
  try{
      await Promise.all([
        store.fetchTitulares(),
        store.fetchTiposIngreso()
      ]);

  }catch (error) {
    console.error('error fetching data', error);
  }finally{
    loading.value= false;
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

console.log('form.cod_titular:', formIngreso.cod_titular, typeof formIngreso.cod_titular)
console.log('form.cod_ingreso:', formIngreso.cod_ingreso, typeof formIngreso.cod_ingreso)

if (!formIngreso.cod_titular || !formIngreso.cod_ingreso) {
  alert('Debe seleccionar un titular y un tipo de ingreso.')
  return
}

const ingreso = {
  cod_ingreso,
  cod_titular,
  monto,
  fecha: new Date(formIngreso.fecha).toISOString(),
  cod_moneda: formIngreso.cod_moneda,
  tipo_cambio,
  fecha_creacion: new Date().toISOString()
}


try {
    await store.guardarIngreso(ingreso)
    success.value = 'Ingreso guardado correctamente'
    alert(success.value)
    resetIngreso()
  } catch (err) {
    console.error('Error al guardar ingreso:', err)
    error.value = 'Error al guardar ingreso'
  }
}


/*
console.log('ingreso que se enviará:', ingreso)

// Enviar a la API
try {
  
  console.log('Entrando en guardaringreso')
  const response = await api.post('/ingresos', ingreso)
  success.value = response.data.mensaje || 'Ingreso guardado correctamente'
  alert('Ingreso guardado correctamente')
  

} catch (err) {
  const error = err.response?.data?.detail;

  if (typeof error === 'object' && error.error_id) {
    alert(`Error al guardar ingreso. Código de error: ${error.error_id}`);
  } else {
    alert("Error desconocido al guardar ingreso.");
  }

  console.error("Error completo:", err);
}

// Si es error HTTP con Axios
if (err.response) {
  console.log('Código de estado:', err.response.status)
  console.log('Respuesta del servidor:', err.response.data)
}

error.value = 'Error al guardar ingreso'
}

*/

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
  
