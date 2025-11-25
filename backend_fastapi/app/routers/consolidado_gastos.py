# routers/consolidado_gastos.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from pydantic import BaseModel
from app.core.database import SessionLocal
from sqlalchemy import text
from typing import Any, List
from datetime import date
from typing import Optional


router = APIRouter(
    prefix="/api",
    tags=["consolidado_gastos"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- MODELO DE ENTRADA ---
class FiltroConsolidado(BaseModel):
    fecha_desde: date
    fecha_hasta: date
    cod_titular: list[int]
    cod_gasto: list[int]
    codigo_moneda: str


# ---MODELO DE SALIDA ---
class ResultadosSalida(BaseModel):
    cod_titular: int
    cod_gasto: int
    codigo_moneda: str
    monto: float
    fecha: date


# --- FUNCIÓN 1: carga matriz base desde BD ---
async def cargar_matriz_base(db) -> List[List[Any]]:
    """
    Trae todos los registros de gastos sin filtrar.
    """
    query = text("""
        SELECT cod_titular, cod_gasto, codigo_moneda, monto, fecha
        FROM lm_gastos
    """)

     # Ejecutar query → devuelve CursorResult
    result = db.execute(query)  # SIN await
    filas = result.fetchall()   # 🔹 fetchall() sobre CursorResult, NO sobre lista

    # Convertir a lista de listas
    matriz_base = [list(row) for row in filas]

    return matriz_base

# --- FUNCIÓN 2: aplica filtros y consolida ---
async def filtrar_matriz(matriz_base: list[list[Any]], filtros: FiltroConsolidado) -> list[list[Any]]:
    """
    Aplica filtros sobre la matriz base y devuelve una nueva matriz consolidada.
    """
    
    matriz_filtrada = []

    for fila in matriz_base:
        cod_titular, cod_gasto, codigo_moneda, monto, fecha=fila 

        # Filtros
        if filtros.cod_titular and filtros.cod_titular != cod_titular:
            continue
        if filtros.cod_gasto and filtros.cod_gasto != cod_gasto:
            continue
        if filtros.codigo_moneda and filtros.codigo_moneda != codigo_moneda:
            continue
        if not (filtros.fecha_desde <= fecha <= filtros.fecha_hasta):
            continue

        matriz_filtrada.append(fila)

    return matriz_filtrada


# --- ENDPOINT FINAL ---
@router.post("/consolidado_gastos", response_model=List[ResultadosSalida])
async def obtener_consolidado(filtros: FiltroConsolidado, db=Depends(get_db)):
    matriz_base = await cargar_matriz_base(db)
    matriz_filtrada = await filtrar_matriz(matriz_base, filtros)

    # Convertir cada fila (list) en un objeto ResultadosSalida
    resultados = [
        ResultadosSalida(
            cod_titular=fila[0],
            cod_gasto=fila[1],
            codigo_moneda=fila[2],
            monto=fila[3],
            fecha=fila[4]
        )
        for fila in matriz_filtrada
    ]

    return resultados