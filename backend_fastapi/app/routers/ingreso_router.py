from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.lm_ingresos import LMIngreso
from app.schemas.ingreso_Model import IngresoIn
from datetime import datetime
import pytz
from sqlalchemy.exc import SQLAlchemyError
from app.models.lm_errores import ErrorLog

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
        print("LLEGA AL ENDPOINT")
        nuevo_ingreso = LMIngreso(
            cod_ingreso=ingreso.cod_ingreso,
            cod_titular=ingreso.cod_titular,
            monto=ingreso.monto,
            fecha=ingreso.fecha,
            cod_moneda=ingreso.cod_moneda,
            tipo_cambio=ingreso.tipo_cambio,
            fecha_creacion=ingreso.fecha_creacion,
        )
        try:
            db.add(nuevo_ingreso)
            print("despues del add")
            db.commit()
            return {"mensaje": "Ingreso guardado con éxito"}
        except SQLAlchemyError as e:
            db.rollback()
            error_msg = str(e.__cause__) if e.__cause__ else str(e)

            # Registrar en la base de errores
            error_entry = ErrorLog(
            codigo_error="SQLAlchemyError",
            MENSAJE_ERROR="Error al guardar ingreso",
            DETALLE_ERROR=error_msg,
            FECHA_ERROR=datetime.now(argentina),
            status_code=422
        )
            db.add(error_entry)
            db.commit()
            db.refresh(error_entry)

            raise HTTPException(
                status_code=422,
                detail={
                    "mensaje": f"No se pudo guardar el ingreso",
                    "error_id": error_entry.id,
                    "descripcion": error_msg
                }
            )
            setattr(exc, "already_logged", True)
            raise exc
        
