from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.lm_ingresos import LMIngreso
from app.schemas.ingreso_Model import IngresoIn
from datetime import datetime
import pytz

argentina = pytz.timezone("America/Argentina/Buenos_Aires")
fecha_creacion = datetime.now(argentina)

print(f"Fecha creación generada: {fecha_creacion}")   # DEBUG

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def crear_ingreso(ingreso: IngresoIn, db: Session = Depends(get_db)):
    try:
        print("Ingreso recibido:", ingreso)
        nuevo_ingreso = LMIngreso(
            cod_ingreso=ingreso.cod_ingreso,
            cod_titular=ingreso.cod_titular,
            monto=ingreso.monto,
            fecha=ingreso.fecha,
            cod_moneda=ingreso.cod_moneda,
            tipo_cambio=ingreso.tipo_cambio,
            fecha_creacion=ingreso.fecha_creacion,
        )
        print("antes del add")
        db.add(nuevo_ingreso)
        print("despues del add")
        db.commit()
        print("commit existoso")
        return {"mensaje": "Ingreso guardado con éxito"}
    except Exception as e:
        db.rollback()
        print("Error en insert:", e)
        raise HTTPException(status_code=500, detail="Error en insert de prueba")

