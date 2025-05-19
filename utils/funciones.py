from modelos.dueno import Dueno
from modelos.mascota import Mascota
from modelos.consulta import Consulta
from utils.logger import logger
from datetime import datetime


# Diccionario para almacenar mascotas por nombre
mascotas_registradas = {}

# Función para registrar una mascota
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
        
        # Se guarda la información en cada clase con argumentos posicionales 
        dueno = Dueno(nombre_dueno, telefono, direccion)
        mascota = Mascota(nombre_mascota, especie, raza, edad, dueno)
        # Se guarda el objeto mascota en el diccionario "mascotas_registradas" con el nombre de la mascota como clave
        # y la clase mascota como valor, la cual contiene la clase dueño y su método __str__
        mascotas_registradas[nombre_mascota.lower()] = mascota
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