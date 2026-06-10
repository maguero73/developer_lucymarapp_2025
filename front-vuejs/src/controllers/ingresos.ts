import api from '@/helpers/api';

const ingresosApi = {
    getTitulares() {
        return api.get('/titulares');
    },
    getTiposIngreso() {
        return api.get('/tipos-ingreso');
    },
    saveIngreso(ingreso: any) {
        return api.post('/ingresos', ingreso);
    }
};

export default ingresosApi;
