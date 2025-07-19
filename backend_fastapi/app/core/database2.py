#INTENTAR UNA CONSULTA BASICA A LA BASE
"""

try:
    with engine.connect() as connection:
        result=connection.execute(text("SELECT 1"))
        print("conexion exitosa:", result.scalar())
except Exception as e:
    print("Error al conectar:", e)        

"""
