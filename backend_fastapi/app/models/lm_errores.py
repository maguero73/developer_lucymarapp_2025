from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base
from sqlalchemy import Column, BigInteger, Integer, String, Text, TIMESTAMP, func

class ErrorLog(Base):
    __tablename__ = "lm_errores"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    codigo_error = Column(String(255), nullable=True)
    MENSAJE_ERROR = Column(String(255), nullable=True)
    DETALLE_ERROR = Column(Text, nullable=True)
    FECHA_ERROR = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    status_code = Column(Integer, nullable=True)
