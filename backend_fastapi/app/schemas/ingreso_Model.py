from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class IngresoIn(BaseModel):
    cod_ingreso: int
    cod_titular: int
    monto: float
    fecha: datetime
    cod_moneda: str
    tipo_cambio: float
    fecha_creacion: Optional[datetime] = None  # <- Ahora es opcional