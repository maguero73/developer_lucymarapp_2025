import { defineStore } from 'pinia'
import solicitudesApi from '../controllers/solicitudes';
import type { Titular, TipoGasto, TipoIngreso } from '../models/solicitudes'

export const useSolicitudesStore = defineStore('solicitudes', {


    state: () => ({
      titulares: [] as { label: string; value: number }[],
      tiposGasto: [] as { label: string; value: number }[],
      tiposIngreso: [] as { label: string; value: number }[],
      loading: false,
      error: ''
    }),


    actions: {
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
      }
    }
  })