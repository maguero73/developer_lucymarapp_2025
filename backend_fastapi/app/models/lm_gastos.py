from sqlalchemy import Column, Integer, Numeric, DateTime, String, Float
from app.core.database import Base
from datetime import datetime, timedelta, timezone

ARG_TZ = timezone(timedelta(hours=-3))  # UTC-3 Argentina



class LMGasto(Base):
    __tablename__ = "lm_gastos"

    id = Column(Integer, primary_key=True, index=True)
    cod_gasto = Column(Integer)
    cod_titular = Column(Integer)   
    monto = Column(Float)
    fecha = Column(DateTime)
    cod_moneda =Column(String(3))
    tipo_cambio =Column(Float)
    fecha_creacion = Column(
    DateTime,
    nullable=False,
    default=lambda: datetime.now(ARG_TZ)
    )