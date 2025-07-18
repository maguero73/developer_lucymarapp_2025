from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.lm_tipo_ingreso import LMTipoIngreso

router = APIRouter()

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_tipos_ingreso(db: Session =Depends(get_db)):
    return db.query(LMTipoIngreso).all()