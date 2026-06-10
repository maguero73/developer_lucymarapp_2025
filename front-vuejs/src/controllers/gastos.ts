import api from '@/helpers/api';

const gastosApi = {
    getTitulares() {
        return api.get('/titulares');
    },
    getTiposGasto() {
        return api.get('/tipos-gasto');
    },
    saveGasto(gasto: any) {
        return api.post('/gastos', gasto);
    }
};

export default gastosApi;
