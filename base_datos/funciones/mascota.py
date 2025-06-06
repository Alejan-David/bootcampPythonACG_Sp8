import sqlite3
from base_datos.conexion import conectar
from utilidades.logger import logger

def registrar_mascota_bd(datos_mascota):
    """
    Registra una nueva mascota en la base de datos.

    :param datos_mascota: Diccionario con las claves:
        'nombre', 'especie', 'raza', 'edad', 'id_dueno'
    :return: Diccionario con 'Respuesta' (bool) y 'Mensaje' (str)
    """
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute('''
            INSERT INTO tabla_mascotas (nombre, especie, raza, edad, id_dueno)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datos_mascota['nombre'],
            datos_mascota['especie'],
            datos_mascota['raza'],
            datos_mascota['edad'],
            datos_mascota['id_dueno']
        ))

        conexion.commit()

        return {"Respuesta": True, "Mensaje": "Mascota registrada exitosamente."}

    except sqlite3.Error as e:
        logger.error(f"Error registrando mascota en BD: {e}")
        return {"Respuesta": False, "Mensaje": f"Error en la base de datos: {str(e)}"}

    except Exception as e:
        logger.error(f"Error inesperado registrando mascota: {e}")
        return {"Respuesta": False, "Mensaje": f"Error inesperado: {str(e)}"}

    finally:
        if 'conexion' in locals():
            conexion.close()
