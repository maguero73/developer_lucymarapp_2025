import { defineStore } from 'pinia'
import solicitudesApi from '../controllers/solicitudes'; //OJO EN CONTROLLER NO SE LLAMA ASI
import { guardarGasto } from '../controllers/solicitudes'; 
import api from '../helpers/api';
import type { Titular, TipoGasto, TipoIngreso } from '../models/solicitudes'

export const useSolicitudesStore = defineStore('solicitudes', {

    //datos reactivos
    state: () => ({
      titulares: [] as { label: string; value: number }[],
      tiposGasto: [] as { label: string; value: number }[],
      tiposIngreso: [] as { label: string; value: number }[],
      gastos: [] as any[],
      loading: false,
      error: ''
    }),


    actions: {
      //llamadas GET
      async fetchTitulares() {
        this.loading = true
        this.error = ''
        try {
          const response = await solicitudesApi.getTitulares()
          this.titulares = response.data.map((item: Titular) => ({
            label: item.nombre,
            value: item.codigo
          }))
        } catch (err) {
          this.error = 'Error cargando titulares'
          console.error(err)
        } finally {
          this.loading = false
        }
      },
  
      async fetchTiposGasto() {
        this.loading = true
        this.error = ''
        try {
          const response = await solicitudesApi.getTiposGasto()
          this.tiposGasto = response.data.map((item: TipoGasto) => ({
            label: item.descripcion,
            value: item.codigo
          }))
        } catch (err) {
          this.error = 'Error cargando tipos de gasto'
          console.error(err)
        } finally {
          this.loading = false
        }
      },

      
      async fetchTiposIngreso() {
        this.loading = true
        this.error = ''
        try {
          const response = await solicitudesApi.getTiposIngreso()
          this.tiposIngreso = response.data.map((item: TipoIngreso) => ({
            label: item.descripcion,
            value: item.codigo
          }))
        } catch (err) {
          this.error = 'Error cargando tipos de ingreso'
          console.error(err)
        } finally {
          this.loading = false
        }
      },

      //llamadas POST

      async agregarGasto(gasto: {
        cod_titular: string,
        monto: number,
        cod_moneda: string,
        cod_tipo_gasto: string,
        fecha: string
      }) {
        this.loading=true;
        this.error= '';
        try {
          const nuevoGasto = await guardarGasto(gasto);
          this.gastos.push(nuevoGasto); // actualizás el estado
        } catch (error: any) {
          this.error = 'Error al guardar gasto';
          throw error;
        } finally {
          this.loading = false;
        }
          

    },

      async guardarIngreso(payload: {
        cod_titular: string,
        monto: number,
        cod_moneda: string,
        cod_tipo_ingreso: string,
        fecha: string
      }) {
        try {
          const response = await api.post('/ingresos', payload);
          console.log('Gasto guardado:', response.data);
          return response.data;
        } catch (error) {
          console.error('Error al guardar el gasto:', error);
          throw error; // se propaga para manejarlo en el componente si querés
        }

         },
      } 
    })