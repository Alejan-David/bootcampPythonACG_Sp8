from modelos.dueno import Dueno
from modelos.mascota import Mascota
from modelos.consulta import Consulta
from utils.logger import logger
from datetime import datetime
import os
import csv
import json

# Diccionario para almacenar mascotas por nombre
mascotas_registradas = {}

# Función para registrar mascotas
def registrar_mascota():
    try:
        print("\n--- Registrar Mascota ---")
        nombre_mascota = input("Nombre de la mascota: ").strip().title()
        especie = input("Especie (Ej: Perro, Gato): ").strip().capitalize()
        raza = input("Raza: ").strip().title()

        while True:
            try:
                edad = int(input("Edad: ").strip())
                if edad >= 0:
                    break
                print("La edad debe ser igual o mayor a 0. Inténtalo nuevamente.")
            except ValueError:
                print("Por favor, ingresa un número válido para la edad.")

        print("\n--- Datos del dueño ---")
        nombre_dueno = input("Nombre del dueño: ").strip().title()
        telefono = input("Teléfono: ").strip()

        while not telefono.isdigit():
            telefono = input("Teléfono inválido. Intente nuevamente: ").strip()
        direccion = input("Dirección: ").strip()
        
        dueno = Dueno(nombre_dueno, telefono, direccion)
        mascota = Mascota(nombre_mascota, especie, raza, edad, dueno)
        mascotas_registradas[nombre_mascota.lower()] = mascota

        # Crear carpeta si no existe
        ruta_carpeta = os.path.join(os.getcwd(), "almacenamiento")
        os.makedirs(ruta_carpeta, exist_ok=True)

        # Ruta del archivo CSV
        ruta_archivo = os.path.join(ruta_carpeta, "mascotas_dueños.csv")

        # Verificar duplicado por nombre de mascota y nombre de dueño
        if os.path.isfile(ruta_archivo):
            with open(ruta_archivo, mode='r', encoding='utf-8') as archivo_csv:
                lector = csv.DictReader(archivo_csv)
                for fila in lector:
                    if (
                        fila["Nombre Mascota"].strip().lower() == nombre_mascota.lower() and
                        fila["Nombre Dueño"].strip().lower() == nombre_dueno.lower()
                    ):
                        mensaje = f"Error: La mascota '{nombre_mascota}' ya está registrada con el dueño '{nombre_dueno}'."
                        logger.error(mensaje)
                        print(mensaje)
                        return  # No continuar con el registro

        # Guardar en CSV
        archivo_existe = os.path.isfile(ruta_archivo)
        with open(ruta_archivo, mode='a', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            if not archivo_existe:
                escritor.writerow(["Nombre Mascota", "Especie", "Raza", "Edad", "Nombre Dueño", "Teléfono", "Dirección"])
            escritor.writerow([nombre_mascota, especie, raza, edad, nombre_dueno, telefono, direccion])

        logger.info(f"Mascota registrada: {nombre_mascota} - Dueño: {nombre_dueno}")
        print(f"\nMascota '{nombre_mascota}' registrada con éxito.\n")

    except Exception as e:
        logger.error(f"Error registrando mascota: {str(e)}")
        print("Ocurrió un error al registrar la mascota.")


# Función para registrar una consulta
def registrar_consulta():
    try:
        print("\n--- Registrar Consulta ---")
        nombre_mascota = input("Nombre de la mascota: ").strip().lower()

        if nombre_mascota not in mascotas_registradas:
            logger.error(f"Mascota no encontrada. Registre primero la mascota.\n: {nombre_mascota}")
            print("Mascota no encontrada. Registre primero la mascota.\n")
            return

        mascota = mascotas_registradas[nombre_mascota]
        
        # Validar formato de fecha
        while True:
            fecha_str = input("Fecha (DD/MM/AAAA): ").strip()
            try:
                fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
                break
            except ValueError:
                print("Formato de fecha inválido. Intente con DD/MM/AAAA.")
                
        motivo = input("Motivo de la consulta: ").strip().capitalize()
        diagnostico = input("Diagnóstico: ").strip().capitalize()

        consulta = Consulta(fecha, motivo, diagnostico, mascota)
        mascota.agregar_consulta(consulta)
        print("Consulta registrada correctamente.\n")

        # Crear carpeta si no existe
        ruta_carpeta = os.path.join(os.getcwd(), "almacenamiento")
        os.makedirs(ruta_carpeta, exist_ok=True)

        # Ruta del archivo JSON
        ruta_json = os.path.join(ruta_carpeta, "consultas.json")

        # Crear estructura del registro
        consulta_dict = {
            "fecha": fecha.strftime("%d/%m/%Y"),
            "motivo": motivo,
            "diagnostico": diagnostico,
            "nombre_mascota": mascota.nombre,
            "especie": mascota.especie,
            "raza": mascota.raza,
            "edad": mascota.edad,
            "dueno": {
                "nombre": mascota.dueno.nombre,
                "telefono": mascota.dueno.telefono,
                "direccion": mascota.dueno.direccion
            }
        }

        # Cargar datos existentes (si hay)
        datos = []
        if os.path.exists(ruta_json):
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                try:
                    datos = json.load(archivo)
                except json.JSONDecodeError:
                    logger.warning("El archivo JSON de consultas estaba vacío o dañado. Se creará uno nuevo.")

        # Agregar nueva consulta
        datos.append(consulta_dict)

        # Guardar nuevamente
        with open(ruta_json, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

        logger.info(f"Consulta registrada para {mascota.nombre} en {fecha.strftime('%d/%m/%Y')}")

    except Exception as e:
        logger.error(f"Error registrando consulta: {str(e)}")
        print("Ocurrió un error al registrar la consulta.")


# Función para listar mascotas
def listar_mascotas():
    print("\n--- Lista de Mascotas Registradas ---")
    if not mascotas_registradas:
        print("No hay mascotas registradas.\n")
    else:
        for mascota in mascotas_registradas.values():
            print(mascota)
            print("-" * 40)


# Función para ver historial de una mascota
def ver_historial_consultas():
    print("\n--- Historial de Consultas ---")
    nombre_mascota = input("Nombre de la mascota: ").strip().lower()

    if nombre_mascota not in mascotas_registradas:
        print("Mascota no encontrada.\n")
        return
    
    mascota = mascotas_registradas[nombre_mascota]
    if not mascota.consultas:
        print(f"\nLa mascota '{mascota.nombre}' no tiene consultas registradas.\n")
    else:
        print(f"\nHistorial de consultas para {mascota.nombre}:")
        print(mascota.mostrar_historial())

# Función para cargar los datos de los archivos CSV y JSON
def cargar_datos_almacenados():
    try:
        # Ruta absoluta a la carpeta "almacenamiento", relativa a este archivo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_carpeta = os.path.abspath(os.path.join(script_dir, "..", "almacenamiento"))

        # Cargar mascotas desde CSV
        ruta_csv = os.path.join(ruta_carpeta, "mascotas_dueños.csv")
        if os.path.isfile(ruta_csv):
            with open(ruta_csv, mode='r', encoding='utf-8') as archivo_csv:
                lector = csv.DictReader(archivo_csv)
                for fila in lector:
                    nombre_mascota = fila["Nombre Mascota"].strip().title()
                    especie = fila["Especie"].strip().capitalize()
                    raza = fila["Raza"].strip().title()
                    edad = int(fila["Edad"])
                    nombre_dueno = fila["Nombre Dueño"].strip().title()
                    telefono = fila["Teléfono"].strip()
                    direccion = fila["Dirección"].strip()

                    if nombre_mascota.lower() not in mascotas_registradas:
                        dueno = Dueno(nombre_dueno, telefono, direccion)
                        mascota = Mascota(nombre_mascota, especie, raza, edad, dueno)
                        mascotas_registradas[nombre_mascota.lower()] = mascota

            logger.info("Datos de mascotas cargados correctamente desde CSV.")
        else:
            logger.warning(f"No se encontró el archivo CSV: {ruta_csv}")

        # Cargar consultas desde JSON
        ruta_json = os.path.join(ruta_carpeta, "consultas.json")
        if os.path.isfile(ruta_json):
            with open(ruta_json, 'r', encoding='utf-8') as archivo_json:
                try:
                    consultas_data = json.load(archivo_json)
                    for item in consultas_data:
                        nombre_mascota = item["nombre_mascota"].strip().lower()
                        if nombre_mascota in mascotas_registradas:
                            fecha = datetime.strptime(item["fecha"], "%d/%m/%Y").date()
                            motivo = item["motivo"]
                            diagnostico = item["diagnostico"]
                            consulta = Consulta(fecha, motivo, diagnostico, mascotas_registradas[nombre_mascota])
                            mascotas_registradas[nombre_mascota].agregar_consulta(consulta)
                    logger.info("Consultas cargadas correctamente desde JSON.")
                except json.JSONDecodeError:
                    logger.warning(f"El archivo JSON está vacío o mal formado: {ruta_json}")
        else:
            logger.warning(f"No se encontró el archivo JSON: {ruta_json}")

    except Exception as e:
        logger.error(f"Error cargando datos almacenados: {str(e)}")
        print("Ocurrió un error al cargar los datos almacenados.")