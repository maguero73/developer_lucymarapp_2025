from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from app.core.database import DBBase

#------------------------------------------------------------------------
class DBLMTitular(DBBase):
    __tablename__ = "lm_titular"

    codigo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20))

#------------------------------------------------------------------------
def get_titular(session: Session, id = int):
    return session.query(DBLMTitular).all()

#------------------------------------------------------------------------

def get_titulares(session:Session, offset:int = 0, limit: int = 1000):
    query = session.query(DBLMTitular).offset(offset).limit(limit).all()
    return query