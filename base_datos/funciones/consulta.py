import sqlite3
from base_datos.conexion import conectar
from utilidades.logger import logger

def registrar_consulta_bd(datos_consulta):
    """
    Registra una nueva consulta en la base de datos.

    :param datos_consulta: Diccionario con claves: fecha (en formato "YYYY-MM-DD"), motivo, diagnostico, id_mascota
    :return: Diccionario con 'Respuesta' (bool) y 'Mensaje' (str)
    """
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute('''
            INSERT INTO tabla_consultas (fecha, motivo, diagnostico, id_mascota)
            VALUES (?, ?, ?, ?)
        ''', (
            datos_consulta['fecha'],
            datos_consulta['motivo'],
            datos_consulta['diagnostico'],
            datos_consulta['id_mascota']
        ))

        conexion.commit()

        return {"Respuesta": True, "Mensaje": "Consulta registrada exitosamente."}

    except sqlite3.Error as e:
        logger.error(f"Error registrando consulta en BD: {e}")
        return {"Respuesta": False, "Mensaje": f"Error en la base de datos: {str(e)}"}

    except Exception as e:
        logger.error(f"Error inesperado registrando consulta: {e}")
        return {"Respuesta": False, "Mensaje": f"Error inesperado: {str(e)}"}

    finally:
        if 'conexion' in locals():
            conexion.close()


def listar_consultas_por_id_mascota_bd(datos):
    """
    Lista las consultas activas asociadas a una mascota específica.

    :param datos: Diccionario con la clave 'id_mascota'.
    :return: Diccionario con 'Respuesta' (bool), 'Mensaje' (str) y 'Datos' (list).
    """
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute('''
            SELECT id, fecha, motivo, diagnostico, id_mascota, activo
            FROM tabla_consultas
            WHERE activo = 's' AND id_mascota = ?
            ORDER BY fecha DESC
        ''', (datos["id_mascota"],))

        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

        return {"Respuesta": True, "Datos": resultados}

    except sqlite3.Error as e:
        logger.error(f"Error listando consultas por ID de mascota: {e}")
        return {"Respuesta": False, "Mensaje": f"Error en la base de datos: {str(e)}"}

    except Exception as e:
        logger.error(f"Error inesperado listando consultas: {e}")
        return {"Respuesta": False, "Mensaje": f"Error inesperado: {str(e)}"}

    finally:
        if 'conexion' in locals():
            conexion.close()


def modificar_consulta_bd(datos):
    """
    Modifica una consulta activa en la base de datos.

    :param datos: Diccionario con claves: id, fecha (formato 'YYYY-MM-DD'), motivo, diagnostico
    :return: Diccionario con 'Respuesta' (bool) y 'Mensaje' (str)
    """
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute('''
            UPDATE tabla_consultas
            SET fecha = ?, motivo = ?, diagnostico = ?
            WHERE id = ? AND activo = 's'
        ''', (
            datos["fecha"],
            datos["motivo"],
            datos["diagnostico"],
            datos["id"]
        ))

        if cursor.rowcount == 0:
            return {"Respuesta": False, "Mensaje": "No se encontró una consulta activa con ese ID."}

        conexion.commit()

        return {"Respuesta": True, "Mensaje": "Consulta modificada exitosamente."}

    except sqlite3.Error as e:
        logger.error(f"Error modificando consulta en BD: {e}")
        return {"Respuesta": False, "Mensaje": f"Error en la base de datos: {str(e)}"}

    except Exception as e:
        logger.error(f"Error inesperado modificando consulta: {e}")
        return {"Respuesta": False, "Mensaje": f"Error inesperado: {str(e)}"}

    finally:
        if 'conexion' in locals():
            conexion.close()



def eliminar_consulta_bd(datos):
    """
    Marca una consulta como inactiva ('activo' = 'n') en la base de datos.

    Parámetros:
        datos (dict): Debe contener la clave 'id' con el ID de la consulta a eliminar.

    Retorna:
        dict: {'Respuesta': bool, 'Mensaje': str}
    """
    try:
        consulta_id = datos.get("id")
        if not consulta_id:
            return {"Respuesta": False, "Mensaje": "ID de consulta no proporcionado."}

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE tabla_consultas
            SET activo = 'n'
            WHERE id = ? AND activo = 's'
        """, (consulta_id,))

        if cursor.rowcount == 0:
            return {"Respuesta": False, "Mensaje": "No se encontró una consulta activa con ese ID."}

        conexion.commit()
        return {"Respuesta": True, "Mensaje": "Consulta eliminada correctamente."}

    except sqlite3.Error as e:
        return {"Respuesta": False, "Mensaje": f"Error en la base de datos: {e}"}

    finally:
        if conexion:
            conexion.close()
