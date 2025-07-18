from sqlalchemy import Column, Integer, String
from app.core.database import Base  # ajusta esto según tu estructura

class LMTipoGasto(Base):
    __tablename__ = "lm_tipo_gasto"

    codigo = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(50), nullable=False)
