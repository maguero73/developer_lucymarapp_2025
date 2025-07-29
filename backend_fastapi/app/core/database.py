from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

#URL DE CONEXION
#DATABASE_URL = "mariadb+mariadbconnector://root:Admin@localhost:3306/lucymar_db"
#DATABASE_URL= "mysql://root:Dimaria123@localhost:3306/lucymar_db?allowPublicKeyRetrieval=true&useSSL=false"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://lucymar_user:Admin@192.168.0.9:3306/lucymar_db"


#CREAR EL MOTOR (engine)
engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True #podes porner False si no queres ver las consultas en consola
)

#CREAR UNA SESION LOCAL PARA USAR EN CADA REQUEST

SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=engine)

#BASE PARA DEFINIR TUS MODELOS ORM

Base = declarative_base()



# Intentar una consulta básica
'''
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexión exitosa:", result.scalar())
except Exception as e:
    print("Error al conectar:", e)
'''