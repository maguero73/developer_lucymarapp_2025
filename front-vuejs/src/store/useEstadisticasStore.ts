import { defineStore } from 'pinia';
import estadisticasApi from '@/controllers/estadisticas';

export const useEstadisticasStore = defineStore('estadisticas', {
    state: () => ({
        titulares: [],
        tiposGasto: [],
        anios: [],
        reporteData: [],
        loading: false,
        error: null as string | null
    }),
    actions: {
        async fetchInitialData() {
            this.loading = true;
            this.error = null;
            try {
                const [resTitulares, resTipos, resAnios] = await Promise.all([
                    estadisticasApi.getTitulares(),
                    estadisticasApi.getTiposGasto(),
                    estadisticasApi.getAnios()
                ]);
                this.titulares = resTitulares.data || [];
                this.tiposGasto = resTipos.data || [];
                this.anios = resAnios.data || [];
            } catch (err: any) {
                this.error = 'Error al cargar filtros de estadísticas';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
        async fetchReportData(params: { cod_titular: number; cod_gasto: number }) {
            this.loading = true;
            this.error = null;
            try {
                const response = await estadisticasApi.getReporteGastosAnuales(params);
                this.reporteData = response.data || [];
            } catch (err: any) {
                this.error = 'Error al obtener datos del reporte';
                console.error(err);
                throw err;
            } finally {
                this.loading = false;
            }
        }
    }
});
