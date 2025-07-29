from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.models.lm_errores import ErrorLog
from app.core.database import SessionLocal  # tu función para obtener una sesión

async def log_error_to_db(status_code: int, codigo_error: str, detail: str):
    try:
        db = SessionLocal()  # o tu forma de obtener la sesión
        error = ErrorLog(
            status_code=status_code,
            codigo_error=codigo_error,
            MENSAJE_ERROR=str(detail)[:255],
            DETALLE_ERROR=str(detail)
        )
        db.add(error)
        db.commit()
        db.refresh(error)
        print("Error guardado con id:", error.id)
    except Exception as e:
        print("No se pudo guardar el error en la base:", str(e))
    finally:
        db.close()

# Handler para errores de validación
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    await log_error_to_db(422, "RequestValidationError", str(exc))
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

# Handler para errores HTTP genéricos
async def http_exception_handler(request: Request, exc: HTTPException):
    if not getattr(exc, "already_logged", True):
        await log_error_to_db(exc.status_code, "HTTPException", exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Handler para errores no esperados
async def generic_exception_handler(request: Request, exc: Exception):
    await log_error_to_db(500, "UnhandledException", str(exc))
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error interno del servidor"},
    )
