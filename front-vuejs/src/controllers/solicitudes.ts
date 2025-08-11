import api from '../helpers/api' 
import type { AxiosResponse } from 'axios';
import type { Titular, TipoGasto, TipoIngreso } from '../models/solicitudes'

/** LLAMADAS GET
 * Obtiene la lista de titulares
 */

export default {
  async getTitulares(): Promise<AxiosResponse<Titular[]>> {
    return await api.get('/titulares')
  },

    /**
   * Obtiene la lista de tipos de gasto
   */

   async getTiposGasto(): Promise<AxiosResponse<TipoGasto[]>> {
    return await api.get('/tipos-gasto')
  },

  /**
   * Obtiene la lista de tipos de ingreso
   */
  async getTiposIngreso(): Promise<AxiosResponse<TipoIngreso[]>> {
    return await api.get('/tipos-ingreso')
  }
}  


  /**
   * LLAMADAS POST
   */
  export async function guardarGasto(payload: {
      cod_titular: string;
      monto: number;
      cod_moneda: string;
      cod_tipo_gasto: string;
      fecha: string;
    }) {
      try {
        const response = await api.post('/gastos', payload);
        return response.data;
      } catch (error) {
        console.error('Error al guardar el gasto:', error);
        throw error;
      }
    }