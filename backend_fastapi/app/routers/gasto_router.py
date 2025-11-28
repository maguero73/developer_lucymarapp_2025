from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import SessionLocal
from app.dbmodels.db_lm_gasto import DBLMGasto
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


# --- MODELO DE ENTRADA ---
class GastoIn(BaseModel):
    cod_gasto: int
    cod_titular: int
    monto: float
    fecha: datetime
    codigo_moneda: str
    tipo_cambio: float
    fecha_creacion: Optional[datetime] = None  # <- Ahora es opcional



@router.post("/")
async def crear_gasto(gasto: GastoIn, db: Session = Depends(get_db)):
    try:
        print("Gasto recibido:", gasto)
        nuevo_gasto = DBLMGasto(
            cod_gasto=gasto.cod_gasto,
            cod_titular=gasto.cod_titular,
            monto=gasto.monto,
            fecha=gasto.fecha,
            codigo_moneda=gasto.codigo_moneda,
            tipo_cambio=gasto.tipo_cambio,
            fecha_creacion=gasto.fecha_creacion,
        )
        db.add(nuevo_gasto)
        db.commit()
        print("commit existoso")
        return {"mensaje": "Gasto guardado con éxito"}
    except Exception as e:
        db.rollback()
        print("Error en test insert:", e)
        raise HTTPException(status_code=500, detail="Error en insert de prueba")

