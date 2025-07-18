'''
   Modulo para el manejo de conexiones a las BD

   Contiene un diccionario de BD.
   Otorga sesiones para realizar querys sobre la BD (get_session)
   Verifica conexión (is_connected)
'''
import contextlib
import oracledb
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import text
import pyapiafip as paa

from typing import Dict, Tuple,Iterator, List, Optional, Generator, Any, AsyncGenerator
from pydantic import BaseModel
from pyapiafip.services.base_service import BaseService, ServiceState
import pyapiafip.models.health_models as hm
from pyapiafip.utils.log_api import logger_api
from pyapiafip.utils import config #sync_to_async
from pyapiafip.models.environment import Environment

from pyapiafip.utils.log_api import logger_api

###############################################################################
ENV = config.app_conf['environment'].upper() if config.app_conf['environment'] else Environment.PROD.value
POOL_MIN_DEFAULT = 5
POOL_MAX_DEFAULT = 15
#------------------------------------------------------------------------------
class ExecProcedureException(Exception):
    pass

#------------------------------------------------------------------------------
class PoolStats(BaseModel):
    min:int
    max:int
    open:int
    in_use:int

#------------------------------------------------------------------------------
class Database(BaseService):
    # Se agrega __init__ para inicializar engine y sessionLocal
    def __init__(
            self,
            name:str,
            user:str,
            password:str,
            host:str,
            port:int,
            sid:str,
            version:int,  # Mayor version, ex: 11 or 18
            pool_min:int=5,
            pool_max:int=15
    ):
        super().__init__(name=name if name else f"{user}@{sid}", type="DATABASE", connection=f"{user}@{sid}/{host}:{port}")
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.sid = sid
        self.version = version  # Mayor version, ex: 11 or 18
        self.pool_min = pool_min
        self.pool_max = pool_max
        ora_version = self.version if self.version else 11 
        if ora_version<12:
            # Thick mode. Solo para conectar a oracle 11, desde version 12 no es necesario.
            # Para versiones de 12 en adelante, no deben tener seteado sec_case_sensitive_logon=false
            # que se usa para compatibilidad para librerías viejas y entre oracle 11 y nuevas.
            # Ver https://stackoverflow.com/questions/73853023/dpy-3015-password-verifier-type-0x939-is-not-supported-by-python-oracledb-in-th
            oracledb.init_oracle_client(lib_dir="/opt/oracle/instantclient")
        connection_string = (
            f"oracle+oracledb://{self.user}:{self.password}@" +
            oracledb.makedsn(host=self.host, port=self.port, service_name=self.sid)
        )   
        # Oculto parámetros si se ejecuta en prod (para que no se impriman en el log si hay error)
        hide_params:bool = False if ENV==Environment.DEV.value or ENV==Environment.TEST.value else True
        # Muestro sql en desa o test
        show_eco:bool = not hide_params
        self.engine:Engine = create_engine(
            url=connection_string, 
            echo=show_eco, 
            hide_parameters=hide_params,
            pool_size=pool_min,
            max_overflow=pool_max-pool_min
        ) #, echo_pool="debug")
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    #----------------------------------------------------------------------------------
    @classmethod
    def map_config_data(cls, config_data: Dict):
        """permite incorporar servicios de BD basados en archivos de configuración 
        utilizados en versiones previas de pyapiafip, donde cada propiedad comenzaba 
        con "db_".

        Args:
            config_data (Dict): diccionario con el mapeo de la propiedad origen a la
            de esta clase.

        Returns:
            dict: diccionario con las propiedades de esta clase y sus valores
        """
        # Mapear nombres de propiedades si es necesario
        mapped_data = {
            "name": config_data.get("db_name", config_data.get("name")),
            "user": config_data.get("db_user", config_data.get("user")),
            "password": config_data.get("db_password", config_data.get("password")),
            "host": config_data.get("db_host", config_data.get("host")),
            "port": config_data.get("db_port", config_data.get("port")),
            "sid": config_data.get("db_sid", config_data.get("sid")),
            "version": config_data.get("db_version", config_data.get("version")),
            "pool_min": config_data.get("db_pool_min", config_data.get("pool_min", POOL_MIN_DEFAULT)),
            "pool_max": config_data.get("db_pool_max", config_data.get("pool_max", POOL_MAX_DEFAULT))
        }
        return mapped_data
    
    #----------------------------------------------------------------------------------
    def state_sync(self)->Tuple[ServiceState,str]:
        try:
            if self.is_connected():
                return ServiceState.UP, f"Servicio accesible - Pool: {self.pool_stats()}"
            return ServiceState.DOWN, "Servicio inaccesible"
        except Exception as err:
            return ServiceState.DOWN, f"{err}"
        
    #----------------------------------------------------------------------------------
    async def state(self)->Tuple[ServiceState,str]:
        return await sync_to_async.run_async(func=self.state_sync)
                
    #----------------------------------------------------------------------------------
    @contextlib.contextmanager
    def get_session(self)->Generator[Session,Any,None]:
        """Devuelve la sesión de la conexión de la BD.
            Una vez utilizada, el control vuelve a esta función y se cierra la sesión.
        """
        sess = self.sessionLocal()
        try:
            logger_api.debug(f"DB[{self.name}] open - Pool.stats: {self.pool_stats()}")
            yield sess
        finally:
            sess.close()
            logger_api.debug(f"DB[{self.name}] close - Pool.stats: {self.pool_stats()}")

    #----------------------------------------------------------------------------------
    def is_connected(self) -> bool:
        """Valida la conexión a la BD.
            
            Returns: Si la conexión es válida, devuelve True y el mensaje 'Conexión activa', 
            de lo contrario False y el error devuelto por la BD.
        """
        try:
            sess = self.sessionLocal()
            logger_api.debug(f"DB[{self.name}] open - Pool.stats: {self.pool_stats()}")
            if sess.connection():
                return True
            else:
                return False            
        finally:
            sess.close()
            logger_api.debug(f"DB[{self.name}] close - Pool.stats: {self.pool_stats()}")

    #----------------------------------------------------------------------------------
    def execute_procedure(self, session:Session, proc, params):
        try:
            connection = session.connection().engine.raw_connection()
            cursor = connection.cursor()
            result=cursor.callproc(proc, params)
            cursor.close()
            connection.commit()
            return result
        except Exception as err:
            raise ExecProcedureException(f"Error to execute procedure: {err}")
        finally:
            connection.close()

    #----------------------------------------------------------------------------------
    def execute_sql(self, session:Session, sql:str):
        result = session.execute(text(sql))
        return result
    
    #----------------------------------------------------------------------------------
    def pool_stats(self)->PoolStats:
        '''
            min: min conexiones (max que permanecen abiertas)
            max: max conexiones que pueden usarse (min+overflow)
            open: conexiones abiertas (en uso + sin uso)
            in_use: conexiones en uso
        '''
        pool:QueuePool = self.engine.pool
        pool_stats:PoolStats= PoolStats(
            min= pool.size(),
            max= pool._max_overflow+pool.size(),
            in_use= pool.checkedout(),
            open= pool.checkedin()+pool.checkedout()
        )
        return pool_stats

    #----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------
    async def execute_procedure_async(self, session:Session, proc, params):
        return await sync_to_async.run_async(self.execute_procedure, session, proc, params)

    #----------------------------------------------------------------------------------
    async def execute_sql_async(self, session:Session, sql:str):
        return await sync_to_async.run_async(self.execute_sql, session, sql)

