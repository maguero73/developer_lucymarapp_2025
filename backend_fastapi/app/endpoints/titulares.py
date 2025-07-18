from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.lm_titular import LMTitular

router = APIRouter()

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_titulares(db: Session =Depends(get_db)):
    return db.query(LMTitular).all()