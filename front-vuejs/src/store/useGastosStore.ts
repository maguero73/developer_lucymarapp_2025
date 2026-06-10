import { defineStore } from 'pinia';
import gastosApi from '@/controllers/gastos';

export const useGastosStore = defineStore('gastos', {
    state: () => ({
        titulares: [],
        tiposGasto: [],
        loading: false,
        error: null as string | null
    }),
    actions: {
        async fetchInitialData() {
            this.loading = true;
            this.error = null;
            try {
                const [resTitulares, resTipos] = await Promise.all([
                    gastosApi.getTitulares(),
                    gastosApi.getTiposGasto()
                ]);
                this.titulares = resTitulares.data || [];
                this.tiposGasto = resTipos.data || [];
            } catch (err: any) {
                this.error = 'Error al cargar datos iniciales';
                console.error(err);
            } finally {
                this.loading = false;
            }
        }
    }
});
