# Actividad 2: Conexión a una base de datos PostgreSQL

**Equipo:** Equipo ZAGH  
**Integrantes:**
- Zurisadai Cruz Valdez
- Angel Aldahir Mejia Cabrera
- Guadalupe Vargas Trejo
- Hugo Rafael Castro Hernandez

## Descripción
Aplicación web desarrollada en Python y Streamlit conectada a una base de datos PostgreSQL para el escenario de Tienda de abarrotes. Implementa validación de datos mediante restricciones SQL, consultas parametrizadas y manejo seguro de credenciales mediante variables de entorno.

## Requisitos
- Python 3.10 o superior
- PostgreSQL 14 o superior (con pgAdmin)

## Creación de la base de datos
1. Abrir pgAdmin y conectarse a la base `postgres`.
2. Ejecutar el **Paso 1** del archivo `crear_bd.sql` para crear la base `tienda`.
3. Conectarse a la nueva base `tienda` y ejecutar el **Paso 2** de `crear_bd.sql` para crear la tabla, los 5 registros de ejemplo y el usuario `app_tienda1`.

## Instalación
```bash
pip install -r requirements.txt