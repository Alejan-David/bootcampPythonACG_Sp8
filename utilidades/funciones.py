from modelos.dueno import Dueno
from modelos.mascota import Mascota
from modelos.consulta import Consulta
from utilidades.logger import logger
from datetime import datetime
from base_datos.funciones_bd import agregar_mascota
from base_datos.funciones_bd import agregar_dueno
from base_datos.funciones_bd import eliminar_dueno
from base_datos.funciones_bd import eliminar_dueno
from base_datos.funciones_bd import listar_mascota_dueno

import os
import csv
import json

# Diccionario para almacenar mascotas por nombre
mascotas_registradas = {}

#Obtener los datos de mascota
def obtener_datos_mascota():
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
    return nombre_mascota, especie, raza, edad

#Obtener los datos de dueño
def obtener_datos_dueno():

        print("\n--- Datos del dueño ---")
        nombre_dueno = input("Nombre del dueño: ").strip().title()
        telefono = input("Teléfono: ").strip()

        while not telefono.isdigit():
            telefono = input("Teléfono inválido. Intente nuevamente: ").strip()
        direccion = input("Dirección: ").strip()
        return nombre_dueno,telefono,direccion

def verificar_duplicado(nombre_mascota, nombre_dueno,ruta_archivo):
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
                    return True
    return False

def crear_carpeta(nombre_carpeta="alamacenamiento"):
    # Crear carpeta si no existe
    ruta_carpeta = os.path.join(os.getcwd(), "almacenamiento")
    os.makedirs(ruta_carpeta, exist_ok=True)
    return ruta_carpeta


def guardar_archivo_csv(datos,ruta_archivo):
    nombre_mascota, especie, raza, edad, nombre_dueno, telefono, direccion = datos
    # Guardar en CSV
    archivo_existe = os.path.isfile(ruta_archivo)
    with open(ruta_archivo, mode='a', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        if not archivo_existe:
            escritor.writerow(["Nombre Mascota", "Especie", "Raza", "Edad", "Nombre Dueño", "Teléfono", "Dirección"])
        escritor.writerow([nombre_mascota, especie, raza, edad, nombre_dueno, telefono, direccion])

# Función para registrar mascotas
def registrar_mascota():
    try:
        #llamar las funciones de obtener_datos_mascotas y obtener_datos_dueno
        nombre_mascota, especie, raza, edad = obtener_datos_mascota()
        nombre_dueno, telefono, direccion = obtener_datos_dueno()        
        
        dueno = Dueno(nombre_dueno, telefono, direccion)
        mascota = Mascota(nombre_mascota, especie, raza, edad, dueno)

        #llamar la función de crear carpeta y ruta del archivo CSV
        ruta_carpeta = crear_carpeta()
        ruta_archivo = os.path.join(ruta_carpeta, "mascotas_dueños.csv")

        #llamar la función para verificar_duplicado 
        if verificar_duplicado(nombre_mascota,nombre_dueno,ruta_archivo):
            return 

        guardar_archivo_csv(
            [nombre_mascota, especie, raza, edad, nombre_dueno, telefono, direccion],
            ruta_archivo
        )
        #Registrar dueño en base de datos
        respuesta_dueno = agregar_dueno(dueno.__dict__)
        if not respuesta_dueno["Respuesta"]:
            mensaje = f"No se pudo registrar el dueño: {respuesta_dueno['Mensaje']}"
            print(mensaje)
            logger.error(mensaje)
            return
        
        #asignar el ID al dueño
        dueno.id = respuesta_dueno["id"]
        mascota.dueno = dueno

        #Registrar en base de datos mascota
        respuesta_mascota = agregar_mascota(mascota)
        if not respuesta_mascota["Respuesta"]:
            print("No se pudo registrar la mascota:", respuesta_mascota["Mensaje"])
            print(mensaje)
            logger.error(mensaje)

            #Si falla mascota, eliminar dueño creado
            eliminar_dueno(dueno.id)
            print(f"El dueño '{nombre_dueno}' fue eliminado porque no se pudo registrar la mascota.")
            logger.info(f"Dueño con ID {dueno.id} eliminado por fallo en registro de mascota.")
            return
        
        logger.info(f"Mascota registrada: {nombre_mascota} - Dueño: {nombre_dueno}")
        print(f"\nMascota '{nombre_mascota}' registrada con éxito.\n")
        
    except Exception as e:
        logger.error(f"Error registrando mascota: {str(e)}")
        print("Ocurrió un error al registrar la mascota.")

# validar formato de fecha 
def obtener_fecha_valida():
        while True:
            fecha_str = input("Fecha (DD/MM/AAAA): ").strip()
            try:
                fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
                return fecha
            except ValueError:
                print("Formato de fecha inválido. Intente con DD/MM/AAAA.")

# obtener demas datos de la consulta                
def obtener_datos_consulta():
    motivo = input("Motivo de la consulta: ").strip().capitalize()
    diagnostico = input("Diagnóstico: ").strip().capitalize()
    return motivo, diagnostico


# Crear estructura del registro
def estructura_registro_consulta(fecha,motivo,diagnostico,mascota):
        return {
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

#Cargar datos existentes
def cargar_datos_consulta(consulta_dict,ruta_json):
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

# Función para registrar una consulta
def registrar_consulta():
    try:
        print("\n--- Registrar Consulta ---")
        nombre_mascota = input("Nombre de la mascota: ").strip().lower()
        nombre_dueno = input("Nombre del dueño: ").strip().lower()

        mascota=mascotas_registradas.get(nombre_mascota)
        if not mascota or mascota.dueno.nombre.strip().lower() != nombre_dueno:
            logger.error(f"Mascota y dueño no coinciden o no existen: {nombre_mascota}, {nombre_dueno}")
            print("Mascota y dueño no coinciden o no están registrados.\n")
            return

        mascota = mascotas_registradas[nombre_mascota]
        fecha = obtener_fecha_valida()
        motivo,diagnostico = obtener_datos_consulta()

        consulta = Consulta(fecha, motivo, diagnostico, mascota)
        mascota.agregar_consulta(consulta)
        print("Consulta registrada correctamente.\n")

        #llamar la función de crear carpeta
        ruta_carpeta = crear_carpeta()
        # Ruta del archivo JSON
        ruta_json = os.path.join(ruta_carpeta, "consultas.json")
        consulta_dict = estructura_registro_consulta(fecha, motivo, diagnostico, mascota)
        cargar_datos_consulta(consulta_dict,ruta_json)

        logger.info(f"Consulta registrada para {mascota.nombre} en {fecha.strftime('%d/%m/%Y')}")

    except Exception as e:
        logger.error(f"Error registrando consulta: {str(e)}")
        print("Ocurrió un error al registrar la consulta.")


# Función para listar mascotas
def listar_mascotas():
    print("\n--- Lista de Mascotas Registradas (Base de Datos) ---")
    respuesta = listar_mascota_dueno()

    if not respuesta["Respuesta"]:
        print(respuesta["Mensaje"])
        return

    for dato in respuesta["Datos"]:
        print(f"Mascota: {dato['Nombre Mascota']}, {dato['Especie']} - {dato['Raza']}, Edad: {dato['Edad']} años")
        print(f"Dueño: {dato['Nombre Dueño']}, Tel: {dato['Teléfono']}, Dirección: {dato['Dirección']}")
        print("-" * 40)

# Función para ver historial de una mascota
def ver_historial_consultas():
    print("\n--- Historial de Consultas ---")
    nombre_mascota = input("Nombre de la mascota: ").strip().lower()
    nombre_dueno = input("Nombre del dueño: ").strip().lower()
    
    mascota = mascotas_registradas.get(nombre_mascota)

    if not mascota or mascota.dueno.nombre.strip().lower() != nombre_dueno:
        print("Mascota y dueño no coinciden o no están registrados.\n")
        return
    
    mascota = mascotas_registradas[nombre_mascota]
    if not mascota.consultas:
        print(f"\nLa mascota '{mascota.nombre}' no tiene consultas registradas.\n")
    else:
        print(f"\nHistorial de consultas para {mascota.nombre}:")
        print(mascota.mostrar_historial())

# Ruta absoluta a la carpeta "almacenamiento", relativa a este archivo
def obtener_rutas_archivos():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_carpeta = os.path.abspath(os.path.join(script_dir, "..", "almacenamiento"))
    return {
        "csv": os.path.join(ruta_carpeta, "mascotas_dueños.csv"),
        "json": os.path.join(ruta_carpeta, "consultas.json")
    }

def cargar_mascotas_desde_csv(ruta_csv):
    if not os.path.isfile(ruta_csv):
        logger.warning(f"No se encontró el archivo CSV: {ruta_csv}")
        return
    with open(ruta_csv, mode='r', encoding='utf-8') as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            nombre_mascota = fila["Nombre Mascota"].strip().title()
            if nombre_mascota.lower() in mascotas_registradas:
                continue

            especie = fila["Especie"].strip().capitalize()
            raza = fila["Raza"].strip().title()
            edad = int(fila["Edad"])
            nombre_dueno = fila["Nombre Dueño"].strip().title()
            telefono = fila["Teléfono"].strip()
            direccion = fila["Dirección"].strip()

            dueno = Dueno(nombre_dueno, telefono, direccion)
            mascota = Mascota(nombre_mascota, especie, raza, edad, dueno)
            mascotas_registradas[nombre_mascota.lower()] = mascota

    logger.info("Datos de mascotas cargados correctamente desde CSV.")

def cargar_consultas_desde_json(ruta_json):
    if not os.path.isfile(ruta_json):
        logger.warning(f"No se encontró el archivo JSON: {ruta_json}")
        return

    try:
        with open(ruta_json, 'r', encoding='utf-8') as archivo_json:
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

# Función para cargar los datos de los archivos CSV y JSON
def cargar_datos_almacenados():
    try:
        rutas = obtener_rutas_archivos()
        cargar_mascotas_desde_csv(rutas["csv"])
        cargar_consultas_desde_json(rutas["json"])
    except Exception as e:
        logger.error(f"Error cargando datos almacenados: {str(e)}")
        print("Ocurrió un error al cargar los datos almacenados.")