import { defineStore } from 'pinia';
import ingresosApi from '@/controllers/ingresos';

export const useIngresosStore = defineStore('ingresos', {
    state: () => ({
        titulares: [],
        tiposIngreso: [],
        loading: false,
        error: null as string | null
    }),
    actions: {
        async fetchInitialData() {
            this.loading = true;
            this.error = null;
            try {
                const [resTitulares, resTipos] = await Promise.all([
                    ingresosApi.getTitulares(),
                    ingresosApi.getTiposIngreso()
                ]);
                this.titulares = resTitulares.data || [];
                this.tiposIngreso = resTipos.data || [];
            } catch (err: any) {
                this.error = 'Error al cargar datos iniciales de ingresos';
                console.error(err);
            } finally {
                this.loading = false;
            }
        }
    }
});
