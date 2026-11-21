import os
import psycopg2
from dotenv import load_dotenv

# Carga las variables de entorno definidas en el archivo .env
load_dotenv()


def obtener_conexion():
    # Lista con los nombres de las variables que no pueden estar vacías
    variables_obligatorias = ['DB_NAME', 'DB_USER', 'DB_PASSWORD']
    variables_faltantes = []

    # Recorre la lista para detectar si falta alguna configuración en el entorno
    for nombre_variable in variables_obligatorias:
        if not os.getenv(nombre_variable):
            variables_faltantes.append(nombre_variable)

    # Lanza un error descriptivo si se detectaron variables vacías o inexistentes
    if variables_faltantes:
        raise ValueError(f"Faltan variables en el archivo .env: {', '.join(variables_faltantes)}")

    # Obtiene los parámetros de conexión asignando valores por defecto a host y puerto
    servidor = os.getenv('DB_HOST', 'localhost')
    puerto = int(os.getenv('DB_PORT', '5432'))
    base_datos = os.getenv('DB_NAME')
    usuario = os.getenv('DB_USER')
    contrasena = os.getenv('DB_PASSWORD')

    # Establece y devuelve la conexión con un límite de espera de 5 segundos
    return psycopg2.connect(
        host=servidor,
        port=puerto,
        dbname=base_datos,
        user=usuario,
        password=contrasena,
        connect_timeout=5
    )


def consultar(sql, parametros=()):
    conexion = None
    cursor = None
    try:
        # Abre la conexión y crea un cursor para ejecutar instrucciones SQL
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Ejecuta la consulta parametrizada para prevenir inyecciones SQL
        cursor.execute(sql, parametros)

        # Extrae los nombres de las columnas y recupera todos los registros
        columnas = [descripcion[0] for descripcion in cursor.description]
        filas = cursor.fetchall()
        return columnas, filas
    finally:
        # Garantiza el cierre del cursor y de la conexión incluso si ocurre un error
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()