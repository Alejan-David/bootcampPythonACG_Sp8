import sqlite3
from base_datos.conexion import conectar
from utilidades.logger import logger

def registrar_mascota_bd(datos_mascota):
    """
    Registra una nueva mascota en la base de datos.

    :param datos_mascota: Diccionario con claves: nombre, especie, raza, edad, id_dueno
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


def listar_mascotas_por_dueno_bd(datos):
    """
    Lista las mascotas activas de un dueño específico.

    :param datos: Diccionario con al menos la clave 'documento'.
    :return: Diccionario con 'Respuesta' (bool), 'Mensaje' (str) y 'Datos' (list).
    """
    try:
        miConexion = conectar()
        miCursor = miConexion.cursor()

        miCursor.execute('''
            SELECT d.id AS id_dueno, d.documento, d.nombre, d.telefono, d.direccion, d.activo,
                   m.id AS id_mascota, m.nombre AS nombre_mascota,
                   m.especie,
                   m.raza,
                   m.edad,
                   m.activo
            FROM tabla_duenos d
            LEFT JOIN tabla_mascotas m ON d.id = m.id_dueno AND m.activo = 's'
            WHERE d.activo = 's' AND d.documento = ?
        ''', (datos["documento"],))

        columnas = [col[0] for col in miCursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in miCursor.fetchall()]

        return {"Respuesta": True, "Datos": resultados}

    except Exception as e:
        return {"Respuesta": False, "Mensaje": f"Error listando mascotas del dueño: {str(e)}"}

    finally:
        miConexion.close()


def modificar_mascota_bd(datos):
    """
    Modifica los datos de una mascota activa en la base de datos.

    :param datos: Diccionario con las claves:
        - documento (str)
        - nombre_original (str)
        - nombre (str)
        - especie (str)
        - raza (str)
        - edad (int)
    :return: Diccionario con 'Respuesta' (bool) y 'Mensaje' (str)
    """
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Obtener ID del dueño
        cursor.execute('''
            SELECT id FROM tabla_duenos
            WHERE documento = ? AND activo = 's'
        ''', (datos['documento'],))
        resultado_dueno = cursor.fetchone()

        if not resultado_dueno:
            return {"Respuesta": False, "Mensaje": "No se encontró un dueño activo con ese documento."}

        id_dueno = resultado_dueno[0]

        # Obtener ID de la mascota activa con ese nombre
        cursor.execute('''
            SELECT id FROM tabla_mascotas
            WHERE id_dueno = ? AND nombre = ? AND activo = 's'
        ''', (id_dueno, datos['nombre_original']))
        resultado_mascota = cursor.fetchone()

        if not resultado_mascota:
            return {"Respuesta": False, "Mensaje": "No se encontró una mascota activa con ese nombre para el dueño especificado."}

        id_mascota = resultado_mascota[0]

        # Actualizar los datos de la mascota
        cursor.execute('''
            UPDATE tabla_mascotas
            SET nombre = ?, especie = ?, raza = ?, edad = ?
            WHERE id = ?
        ''', (
            datos['nombre'],
            datos['especie'],
            datos['raza'],
            datos['edad'],
            id_mascota
        ))

        conexion.commit()

        return {"Respuesta": True, "Mensaje": "Mascota modificada exitosamente."}

    except sqlite3.Error as e:
        logger.error(f"Error modificando mascota en BD: {e}")
        return {"Respuesta": False, "Mensaje": f"Error en la base de datos: {str(e)}"}

    except Exception as e:
        logger.error(f"Error inesperado modificando mascota: {e}")
        return {"Respuesta": False, "Mensaje": f"Error inesperado: {str(e)}"}

    finally:
        if 'conexion' in locals():
            conexion.close()


def eliminar_mascota_bd(documento_dueno, nombre_mascota):
    """
    Realiza la eliminación lógica de una mascota (cambia 'activo' a 'n').

    :param documento_dueno: Documento del dueño de la mascota
    :param nombre_mascota: Nombre de la mascota a eliminar
    :return: Diccionario con 'Respuesta' (bool) y 'Mensaje' (str)
    """
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Obtener el ID del dueño
        cursor.execute('''
            SELECT id FROM tabla_duenos
            WHERE documento = ? AND activo = 's'
        ''', (documento_dueno,))
        resultado = cursor.fetchone()

        if not resultado:
            return {"Respuesta": False, "Mensaje": "Dueño no encontrado o inactivo."}

        id_dueno = resultado[0]

        # Verificar existencia de la mascota
        cursor.execute('''
            SELECT id FROM tabla_mascotas
            WHERE nombre = ? AND id_dueno = ? AND activo = 's'
        ''', (nombre_mascota, id_dueno))
        mascota = cursor.fetchone()

        if not mascota:
            return {"Respuesta": False, "Mensaje": "Mascota no encontrada o ya está inactiva."}

        # Eliminar (lógicamente) la mascota
        cursor.execute('''
            UPDATE tabla_mascotas
            SET activo = 'n'
            WHERE id = ?
        ''', (mascota[0],))

        conexion.commit()
        return {"Respuesta": True, "Mensaje": "Mascota eliminada correctamente."}

    except sqlite3.Error as e:
        logger.error(f"Error eliminando mascota en BD: {e}")
        return {"Respuesta": False, "Mensaje": f"Error en la base de datos: {str(e)}"}

    except Exception as e:
        logger.error(f"Error inesperado eliminando mascota: {e}")
        return {"Respuesta": False, "Mensaje": f"Error inesperado: {str(e)}"}

    finally:
        if 'conexion' in locals():
            conexion.close()
