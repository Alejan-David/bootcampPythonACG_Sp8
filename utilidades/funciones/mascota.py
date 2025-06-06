from modelos.dueno import Dueno
from modelos.mascota import Mascota
from utilidades.logger import logger

from base_datos.funciones.dueno import (
    buscar_dueno_por_documento_bd
)

from base_datos.funciones.mascota import(
    registrar_mascota_bd
)

# Diccionario temporal para uso en memoria (opcional, si aún usas)
mascotas_registradas = {}

def registrar_mascota():
    """
    Registra una mascota solicitando primero el documento del dueño y validando su existencia.
    Luego solicita los datos de la mascota y registra asociándola al dueño confirmado.
    Valida que ningún campo esté vacío.
    """
    try:
        print("\n--- Registrar Mascota ---")

        # Solicitar documento del dueño y confirmar existencia
        while True:
            documento_dueno = input("Documento del dueño (debe estar registrado): ").strip()
            if not documento_dueno:
                print("El documento no puede estar vacío. Intenta nuevamente.")
                continue

            respuesta_dueno = buscar_dueno_por_documento_bd(documento_dueno)

            if not respuesta_dueno["Respuesta"]:
                print(f"No existe un dueño con documento '{documento_dueno}'. Intenta nuevamente.")
                continue

            datos_dueno = respuesta_dueno["Datos"]
            dueno = Dueno(
                id=datos_dueno.get("id"),
                documento=datos_dueno.get("documento"),
                nombre=datos_dueno.get("nombre"),
                telefono=datos_dueno.get("telefono"),
                direccion=datos_dueno.get("direccion"),
                activo='s'
            )

            print("\n--- Datos del Dueño Encontrado ---")
            print(dueno)

            confirmar = input("¿Deseas registrar la mascota a este dueño? (s/n): ").strip().lower()
            if confirmar == 's':
                break
            else:
                print("Vamos a solicitar nuevamente el documento...\n")

        # Solicitar y validar datos de la mascota
        while True:
            nombre = input("Nombre de la mascota: ").strip().title()
            if nombre:
                break
            print("El nombre no puede estar vacío.")

        while True:
            especie = input("Especie (Ej: Perro, Gato): ").strip().capitalize()
            if especie:
                break
            print("La especie no puede estar vacía.")

        while True:
            raza = input("Raza: ").strip().title()
            if raza:
                break
            print("La raza no puede estar vacía.")

        while True:
            edad_input = input("Edad: ").strip()
            if not edad_input:
                print("La edad no puede estar vacía.")
                continue
            try:
                edad = int(edad_input)
                if edad >= 0:
                    break
                print("La edad debe ser igual o mayor a 0.")
            except ValueError:
                print("Por favor, ingresa un número válido para la edad.")

        # Crear la mascota
        mascota = Mascota(nombre, especie, raza, edad, dueno)
        datos_mascota = mascota.__dict__
        datos_mascota["id_dueno"] = dueno.id  # <- se añade el id_dueno aquí

        # Registrar en la base de datos
        respuesta = registrar_mascota_bd(datos_mascota)

        if respuesta["Respuesta"]:
            print(f"Mascota '{nombre}' registrada con éxito.\n")
            logger.info(f"Mascota registrada: {nombre} - Documento dueño: {documento_dueno}")
            mascotas_registradas[nombre.lower()] = mascota
        else:
            print(f"No se pudo registrar la mascota: {respuesta['Mensaje']}")
            logger.error(respuesta["Mensaje"])

    except Exception as e:
        logger.error(f"Error registrando mascota: {str(e)}")
        print("Ocurrió un error al registrar la mascota.")
