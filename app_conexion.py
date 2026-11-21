import os
import streamlit as st
import psycopg2
from dotenv import load_dotenv
from conexion import consultar

load_dotenv()

st.title("Tienda de abarrotes")
st.caption("Equipo ZAGH | Integrantes: Zurisadai Cruz Valdez, Angel Aldahir Mejia Cabrera, Guadalupe Vargas Trejo,"
           " Hugo Rafael Castro Hernandez")

st.header("Datos de conexión")
st.text(f"Servidor: {os.getenv('DB_HOST', 'localhost')}")
st.text(f"Puerto: {os.getenv('DB_PORT', '5432')}")
st.text(f"Base de datos: {os.getenv('DB_NAME', 'No definida')}")
st.text(f"Usuario: {os.getenv('DB_USER', 'No definido')}")
st.text("Contraseña: ********")

if st.button("Probar conexión"):
    try:
        _, filas = consultar("SELECT current_database(), current_user, version();")
        if filas:
            base, usuario, version = filas[0]
            st.success(f"Conexión exitosa | Base: {base} | Usuario: {usuario} | Versión: {version}")
    except ValueError as error_val:
        st.error(str(error_val))
    except psycopg2.OperationalError:
        st.error("Error de conexión: No se pudo contactar con PostgreSQL. Revisa el puerto, servidor o contraseña.")
    except psycopg2.Error as error_bd:
        st.error(f"Error en la base de datos: {error_bd}")

try:
    consulta_metricas = "SELECT count(*), count(*) FILTER (WHERE activo) FROM productos;"
    _, filas_metricas = consultar(consulta_metricas)
    total_registros, registros_activos = filas_metricas[0]

    col1, col2 = st.columns(2)
    col1.metric("Registros en la tabla", total_registros)
    col2.metric("Registros con estado activo", registros_activos)

    st.header("Registros")
    categorias = ["Todas", "Lácteos", "Bebidas", "Abarrotes", "Limpieza", "Botanas"]
    categoria_elegida = st.selectbox("Filtrar por categoría:", categorias)

    if categoria_elegida == "Todas":
        consulta_tabla = """
            SELECT id_producto, codigo_producto, nombre_producto, categoria, precio, existencia, activo 
            FROM productos 
            ORDER BY id_producto;
        """
        parametros = ()
    else:
        consulta_tabla = """
            SELECT id_producto, codigo_producto, nombre_producto, categoria, precio, existencia, activo 
            FROM productos 
            WHERE categoria = %s 
            ORDER BY id_producto;
        """
        parametros = (categoria_elegida,)

    _, filas_tabla = consultar(consulta_tabla, parametros)

    # Convierte el tipo Decimal de precio a float y etiqueta las columnas para la tabla
    datos_formateados = []
    for fila in filas_tabla:
        datos_formateados.append({
            "ID": fila[0],
            "Código": fila[1],
            "Nombre": fila[2],
            "Categoría": fila[3],
            "Precio": float(fila[4]),
            "Existencia": fila[5],
            "Estado": fila[6]
        })

    st.dataframe(datos_formateados, hide_index=True)

except ValueError as error_val:
    st.error(str(error_val))
except psycopg2.OperationalError:
    st.error("No hay conexión con la base de datos. Verifica tus credenciales o que el servicio esté activo.")
except psycopg2.Error as error_bd:
    st.error(f"Error al consultar los registros: {error_bd}")