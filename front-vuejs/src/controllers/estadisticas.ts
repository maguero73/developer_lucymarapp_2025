import api from '@/helpers/api';

const estadisticasApi = {
    getTitulares() {
        return api.get('/titulares');
    },
    getTiposGasto() {
        return api.get('/tipos-gasto');
    },
    getAnios() {
        return api.get('/reportes/anios');
    },
    getReporteGastosAnuales(params: { cod_titular: number; cod_gasto: number }) {
        return api.get('/reportes/gastos-anuales', { params });
    }
};

export default estadisticasApi;
