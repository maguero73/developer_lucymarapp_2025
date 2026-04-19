from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.database import SessionLocal
from app.dbmodels import db_lm_gasto, db_lm_ingreso, db_lm_tipo_gasto

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTS DE GASTOS ---

#--------------------------------------------------------------------------------
@router.get("/api/reportes/gastos-altos")
def reporte_gastos_altos(monto_minimo: float, db:Session=Depends(get_db)):
    """
    Devuelve gastos que superan el monto especificado.
    """
    return db_lm_gasto.get_gastos_mayor_a(db, monto_minimo)


#-----------------------------------------------------------------------------------------

@router.get("/api/reportes/ultimo-gasto/{cod_titular}")
def reporte_ultimo_gasto(cod_titular: int, db:Session=Depends(get_db)):
    """
    Devuelve el último gasto de un titular, incluyendo la descripción del tipo de gasto.
    """
    gasto = db_lm_gasto.get_ultimo_gasto_titular(db, cod_titular)
    
    if not gasto:
        raise HTTPException(status_code=404, detail="No se encontraron gastos para este titular")
    
    # Enriquecemos la respuesta con la descripción del tipo
    descripcion_tipo = db_lm_tipo_gasto.get_descripcion_tipo(db, gasto.cod_gasto)
    
    # Retornamos un diccionario combinando los datos
    return {
        "id": gasto.id,
        "fecha": gasto.fecha,
        "monto": gasto.monto,
        "moneda": gasto.codigo_moneda,
        "tipo_gasto": descripcion_tipo,
        "cod_gasto": gasto.cod_gasto
    }

# --- ENDPOINTS DE INGRESOS ---

@router.get("/api/reportes/ingresos-mensuales")
def reporte_ingresos_mensuales(anio: int, mes: int, db: Session = Depends(get_db)):
    """
    Devuelve los ingresos de un mes específico.
    """
    return db_lm_ingreso.get_ingresos_del_mes(db, anio, mes)
