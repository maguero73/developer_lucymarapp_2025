################################################    -----pruebas_mariano   ---############################################################
import traceback
from contextlib import asynccontextmanager



from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import titulares
from app.endpoints import tipo_gasto
from app.routers import gasto_router, ingreso_router, auth_router
from app.endpoints import tipo_ingreso
from app.middlewares.audit_middleware_auth import JWTMiddleware


from fastapi.security import HTTPBearer
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

import pyapiafip as paa
from app.services import database_service
#from app.helpers import token_preprocess
from app.routers import auth_router #prueba_mariano


app= FastAPI(title="Backend-FastAPI")
#app = paa.PyApiAFIP




bearer_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

#----------------------------Middleware---------------------------------------------#

#app.add_middleware(JWTMiddleware, database_service='desa@fiscodb')

#---------------------------Services--------------------------------------------
# Conexiones a BD
#app.add_services_from_path(database_service.Database,'conf/ds/')



#----------------------------Routers----------------------------------------

app.include_router(titulares.router, prefix="/api/titulares", tags=["Titulares"]) #dependencies=[Depends(oauth2_scheme)])
app.include_router(tipo_gasto.router, prefix="/api/tipos-gasto", tags=["Tipo Gasto"]) #dependencies=[Depends(bearer_scheme)])
app.include_router(tipo_ingreso.router, prefix="/api/tipos-ingreso", tags=["tipos_ingreso"])#dependencies=[Depends(bearer_scheme)])
app.include_router(gasto_router.router, prefix="/api/gastos") #dependencies=[Depends(bearer_scheme)])
app.include_router(ingreso_router.router, prefix="/api/ingresos")#dependencies=[Depends(bearer_scheme)])
#------------------------Auths Login-------------------------------------------
app.include_router(auth_router.router, prefix="/api")



# ------------------------- Middlewares --------------------------------------------------------

# -------- CORS (cross origin resource sharing) -----------------------------------
origins = [
        "http://localhost:5173"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # O "*" si estas probando
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)