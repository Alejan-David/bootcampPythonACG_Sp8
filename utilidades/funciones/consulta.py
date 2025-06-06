from modelos.dueno import Dueno
from modelos.mascota import Mascota
from modelos.consulta import Consulta
from utilidades.logger import logger
from datetime import datetime

from base_datos.funciones_bd import (
    agregar_consulta_bd,
    buscar_dueno_por_documento_bd,
    buscar_mascota_por_nombre_y_dueno_bd,
    obtener_consultas_por_mascota_bd
)

def obtener_fecha_valida():
    """
    Solicita al usuario ingresar una fecha válida en formato dd/mm/yyyy.
    Continúa pidiendo hasta que se ingrese correctamente.
    """
    while True:
        fecha_str = input("Fecha (dd/mm/yyyy): ").strip()
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
            return fecha
        except ValueError:
            print("Formato de fecha inválido. Intenta de nuevo.")

def registrar_consulta():
    """
    Registra una nueva consulta médica para una mascota,
    utilizando el documento del dueño y el nombre de la mascota como criterios.
    """
    try:
        print("\n--- Registrar Consulta ---")
        documento_dueno = input("Documento del dueño: ").strip()
        nombre_mascota = input("Nombre de la mascota: ").strip().title()

        # Buscar dueño por documento
        respuesta_dueno = buscar_dueno_por_documento_bd(documento_dueno)
        if not respuesta_dueno["Respuesta"]:
            print(f"No se encontró un dueño con documento '{documento_dueno}'.")
            return
        datos_dueno = respuesta_dueno["Datos"]
        dueno = Dueno(**datos_dueno)

        # Buscar mascota asociada al dueño
        respuesta_mascota = buscar_mascota_por_nombre_y_dueno_bd(nombre_mascota, datos_dueno["id"])
        if not respuesta_mascota["Respuesta"]:
            print(f"No se encontró la mascota '{nombre_mascota}' para el dueño con documento '{documento_dueno}'.")
            return
        datos_mascota = respuesta_mascota["Datos"]
        mascota = Mascota(
            nombre=datos_mascota["nombre"],
            especie=datos_mascota["especie"],
            raza=datos_mascota["raza"],
            edad=datos_mascota["edad"],
            dueno=dueno
        )
        id_mascota = datos_mascota["id"]

        # Capturar fecha, motivo y diagnóstico
        fecha = obtener_fecha_valida()
        motivo = input("Motivo de la consulta: ").strip().capitalize()
        diagnostico = input("Diagnóstico: ").strip().capitalize()

        # Crear objeto Consulta
        consulta = Consulta(fecha, motivo, diagnostico, mascota)

        # Guardar en base de datos
        respuesta_guardado = agregar_consulta_bd({
            "fecha": fecha.strftime("%Y-%m-%d"),
            "motivo": motivo,
            "diagnostico": diagnostico,
            "id_mascota": id_mascota
        })

        if respuesta_guardado["Respuesta"]:
            print("Consulta registrada correctamente.\n")
            logger.info(f"Consulta registrada para {mascota.nombre} en {fecha.strftime('%d/%m/%Y')}")
        else:
            print(f"No se pudo registrar la consulta: {respuesta_guardado['Mensaje']}")
            logger.error(respuesta_guardado["Mensaje"])

    except Exception as e:
        logger.error(f"Error registrando consulta: {str(e)}")
        print("Ocurrió un error al registrar la consulta.")

def ver_historial_consultas():
    """
    Muestra el historial de consultas de una mascota asociada a un dueño,
    usando como criterios el documento del dueño y el nombre de la mascota.
    """
    try:
        print("\n--- Historial de Consultas ---")
        documento_dueno = input("Documento del dueño: ").strip()
        nombre_mascota = input("Nombre de la mascota: ").strip().title()

        # Paso 1: Buscar dueño por documento
        respuesta_dueno = buscar_dueno_por_documento_bd(documento_dueno)
        if not respuesta_dueno["Respuesta"]:
            print(f"No se encontró un dueño con documento '{documento_dueno}'.")
            return
        dueno = respuesta_dueno["Datos"]
        id_dueno = dueno["id"]

        # Paso 2: Buscar mascota asociada a ese dueño
        respuesta_mascota = buscar_mascota_por_nombre_y_dueno_bd(nombre_mascota, id_dueno)
        if not respuesta_mascota["Respuesta"]:
            print(f"No se encontró la mascota '{nombre_mascota}' para el dueño con documento '{documento_dueno}'.")
            return
        mascota = respuesta_mascota["Datos"]
        id_mascota = mascota["id"]

        # Paso 3: Obtener historial de consultas de la mascota
        respuesta_consultas = obtener_consultas_por_mascota_bd(id_mascota)
        if not respuesta_consultas["Respuesta"]:
            print(f"No se encontraron consultas para la mascota '{nombre_mascota}'.")
            return

        consultas = respuesta_consultas["Datos"]
        print(f"\nHistorial de consultas para '{nombre_mascota}':")
        for consulta in consultas:
            fecha = consulta["fecha"]
            motivo = consulta["motivo"]
            diagnostico = consulta["diagnostico"]
            tratamiento = consulta.get("tratamiento", "No especificado")
            print(f"- Fecha: {fecha}, Motivo: {motivo}")
            print(f"  Diagnóstico: {diagnostico}")
            print(f"  Tratamiento: {tratamiento}")
            print("-" * 40)
    except Exception as e:
        logger.error(f"Error al ver historial de consultas: {str(e)}")
        print("Ocurrió un error al consultar el historial.")
