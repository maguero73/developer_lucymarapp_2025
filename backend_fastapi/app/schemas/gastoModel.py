from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class GastoIn(BaseModel):
    cod_gasto: int
    cod_titular: int
    monto: float
    fecha: datetime
    cod_moneda: str
    tipo_cambio: float
    fecha_creacion: Optional[datetime] = None  # <- Ahora es opcional