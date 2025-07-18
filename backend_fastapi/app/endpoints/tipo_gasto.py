from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.lm_tipo_gasto import LMTipoGasto

router = APIRouter()

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_tipos_gasto(db: Session =Depends(get_db)):
    return db.query(LMTipoGasto).all()