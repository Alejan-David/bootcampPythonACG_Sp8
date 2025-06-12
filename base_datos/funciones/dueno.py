import sqlite3
from base_datos.conexion import conectar

def registrar_dueno_bd(datos):
    """
    Inserta un nuevo dueño en la base de datos.
    
    :param datos: Diccionario con las claves 'documento', 'nombre', 'telefono' y 'direccion'.
    :return: Diccionario con 'Respuesta' (bool) y 'Mensaje' (str).
    """
    try:
        miConexion = conectar()
        miCursor = miConexion.cursor()

        miCursor.execute('''
            INSERT INTO tabla_duenos (documento, nombre, telefono, direccion)
            VALUES (?, ?, ?, ?)
        ''', (
            datos["documento"],
            datos["nombre"],
            datos["telefono"],
            datos["direccion"]
        ))

        miConexion.commit()
        return {"Respuesta": True, "Mensaje": "Dueño registrado exitosamente."}

    except sqlite3.IntegrityError as e:
        return {"Respuesta": False, "Mensaje": f"Error de integridad: {str(e)}"}

    except Exception as e:
        return {"Respuesta": False, "Mensaje": f"Error inesperado: {str(e)}"}

    finally:
        miConexion.close()


def eliminar_dueno_bd(documento):
    """
    Realiza una eliminación lógica del dueño y sus mascotas asociadas.
    Cambia el campo 'activo' a 'n' en ambas tablas (dueños y mascotas).
    
    :param documento: Documento del dueño a eliminar.
    :return: Diccionario con 'Respuesta' (bool) y 'Mensaje' (str).
    """
    try:
        miConexion = conectar()
        miCursor = miConexion.cursor()

        # Verificar si el dueño activo existe
        miCursor.execute("SELECT id FROM tabla_duenos WHERE documento = ? AND activo = 's'", (documento,))
        resultado = miCursor.fetchone()

        if not resultado:
            return {"Respuesta": False, "Mensaje": "El dueño no existe o ya está eliminado."}

        id_dueno = resultado[0]

        # Marcar como inactivo al dueño y sus mascotas
        miCursor.execute("UPDATE tabla_duenos SET activo = 'n' WHERE id = ?", (id_dueno,))
        miCursor.execute("UPDATE tabla_mascotas SET activo = 'n' WHERE id_dueno = ?", (id_dueno,))

        miConexion.commit()
        return {"Respuesta": True, "Mensaje": "Dueño y sus mascotas eliminados lógicamente."}

    except Exception as e:
        return {"Respuesta": False, "Mensaje": f"Error eliminando dueño: {str(e)}"}

    finally:
        miConexion.close()


def modificar_dueno_bd(datos):
    """
    Modifica los datos de un dueño identificado por su documento.

    :param datos: Diccionario con las claves 'documento', 'nombre', 'telefono' y 'direccion'.
    :return: Diccionario con 'Respuesta' (bool) y 'Mensaje' (str).
    """
    try:
        miConexion = conectar()
        miCursor = miConexion.cursor()

        documento = datos["documento"]

        # Verificar existencia del dueño activo
        miCursor.execute("SELECT * FROM tabla_duenos WHERE documento = ? AND activo = 's'", (documento,))
        resultado = miCursor.fetchone()

        if not resultado:
            return {"Respuesta": False, "Mensaje": "El dueño no existe o ya está eliminado."}

        # Actualizar los datos
        miCursor.execute('''
            UPDATE tabla_duenos
            SET nombre = ?, telefono = ?, direccion = ?
            WHERE documento = ? AND activo = 's'
        ''', (
            datos["nombre"],
            datos["telefono"],
            datos["direccion"],
            documento
        ))

        miConexion.commit()
        return {"Respuesta": True, "Mensaje": "Dueño modificado con éxito."}

    except Exception as e:
        return {"Respuesta": False, "Mensaje": f"Error modificando dueño: {str(e)}"}

    finally:
        miConexion.close()


def buscar_dueno_por_documento_bd(documento):
    """
    Busca un dueño activo por su documento.
    
    :param documento: Documento del dueño a buscar.
    :return: Diccionario con 'Respuesta' (bool), 'Mensaje' (str) y 'Datos' (dict).
    """
    try:
        miConexion = conectar()
        miCursor = miConexion.cursor()

        miCursor.execute('''
            SELECT id, documento, nombre, telefono, direccion, activo
            FROM tabla_duenos
            WHERE documento = ? AND activo = 's'
        ''', (documento,))
        
        resultado = miCursor.fetchone()
        if not resultado:
            return {"Respuesta": False, "Mensaje": f"No se encontró un dueño activo con documento '{documento}'."}
        
        columnas = [col[0] for col in miCursor.description]
        datos = dict(zip(columnas, resultado))

        return {"Respuesta": True, "Datos": datos}

    except Exception as e:
        return {"Respuesta": False, "Mensaje": f"Error buscando dueño: {str(e)}"}

    finally:
        miConexion.close()


def listar_todos_los_duenos_y_mascotas_bd():
    """
    Lista todos los dueños activos y sus mascotas activas.

    :return: Diccionario con 'Respuesta' (bool), 'Mensaje' (str) y 'Datos' (list).
    """
    try:
        miConexion = conectar()
        miCursor = miConexion.cursor()

        miCursor.execute('''
            SELECT d.id AS id_dueno, d.documento, d.nombre AS nombre, d.telefono, d.direccion, d.activo,
                   m.nombre AS nombre_mascota, m.especie, m.raza, m.edad
            FROM tabla_duenos d
            LEFT JOIN tabla_mascotas m ON d.id = m.id_dueno AND m.activo = 's'
            WHERE d.activo = 's'
            ORDER BY d.nombre
        ''')

        columnas = [col[0] for col in miCursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in miCursor.fetchall()]

        return {"Respuesta": True, "Datos": resultados}

    except Exception as e:
        return {"Respuesta": False, "Mensaje": f"Error listando dueños y mascotas: {str(e)}"}

    finally:
        miConexion.close()
