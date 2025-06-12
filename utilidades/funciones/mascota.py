from modelos.dueno import Dueno
from modelos.mascota import Mascota
from utilidades.logger import logger

from base_datos.funciones.dueno import (
    buscar_dueno_por_documento_bd
)

from base_datos.funciones.mascota import(
    registrar_mascota_bd,
    listar_mascotas_por_dueno_bd,
    modificar_mascota_bd,
    eliminar_mascota_bd
)

def registrar_mascota():
    """
    Registra una mascota solicitando primero el documento del dueño y validando su existencia.
    Luego solicita los datos de la mascota y registra asociándola al dueño confirmado.
    No se permite registrar mascotas con el mismo nombre para el mismo dueño.
    """
    try:
        print("\n--- Registrar Mascota ---")

        # Confirmar existencia del dueño
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
            dueno = Dueno(**datos_dueno)

            print("\n--- Datos del Dueño Encontrado ---")
            print(dueno)

            confirmar = input("¿Deseas registrar la mascota a este dueño? (s/n): ").strip().lower()
            if confirmar == 's':
                break
            print("Vamos a solicitar nuevamente el documento...\n")

        # Consultar mascotas activas del dueño
        respuesta_mascotas = listar_mascotas_por_dueno_bd({"documento": documento_dueno})
        mascotas_existentes = []

        if respuesta_mascotas["Respuesta"]:
            mascotas_data = respuesta_mascotas["Datos"]
            for m in mascotas_data:
                if m.get("nombre_mascota"):
                    mascotas_existentes.append(m["nombre_mascota"].strip().lower())

            if mascotas_existentes:
                print("\nMascotas ya registradas para este dueño:")
                for nombre_m in mascotas_existentes:
                    print(f"  - {nombre_m.capitalize()}")

        # Solicitar datos de la nueva mascota
        while True:
            nombre = input("Nombre de la nueva mascota: ").strip().title()
            if not nombre:
                print("El nombre no puede estar vacío.")
                continue
            if nombre.lower() in mascotas_existentes:
                print(f"Ya existe una mascota llamada '{nombre}' registrada para este dueño. Usa otro nombre.")
                continue
            break

        especie = input("Especie (Ej: Perro, Gato): ").strip().capitalize()
        raza = input("Raza: ").strip().title()

        while True:
            edad_input = input("Edad: ").strip()
            try:
                edad = int(edad_input)
                if edad >= 0:
                    break
                print("La edad debe ser igual o mayor a 0.")
            except ValueError:
                print("Por favor, ingresa un número válido para la edad.")

        # Crear objeto Mascota sin campo activo
        mascota = Mascota(id=None, nombre=nombre, especie=especie, raza=raza,
                          edad=edad, id_dueno=dueno.id, activo=None)
        datos_mascota = mascota.__dict__

        # Registrar en la base de datos
        respuesta = registrar_mascota_bd(datos_mascota)

        if respuesta["Respuesta"]:
            print(f"Mascota '{nombre}' registrada con éxito.\n")
            logger.info(f"Mascota registrada: {nombre} - Documento dueño: {documento_dueno}")
        else:
            print(f"No se pudo registrar la mascota: {respuesta['Mensaje']}")
            logger.error(respuesta["Mensaje"])

    except Exception as e:
        logger.error(f"Error registrando mascota: {str(e)}")
        print("Ocurrió un error al registrar la mascota.")


def modificar_mascota():
    """
    Modifica los datos de una mascota registrada a un dueño existente.
    Busca por documento del dueño y nombre de la mascota.
    Verifica que el nuevo nombre no esté en uso por otra mascota del mismo dueño.
    """
    try:
        print("\n--- Modificar Mascota ---")

        documento = input("Documento del dueño: ").strip()
        if not documento:
            print("El documento no puede estar vacío.")
            return

        respuesta_dueno = buscar_dueno_por_documento_bd(documento)
        if not respuesta_dueno["Respuesta"]:
            print(respuesta_dueno["Mensaje"])
            return

        dueno = Dueno(**respuesta_dueno["Datos"])
        print("\nDueño encontrado:")
        print(dueno)

        # Listar mascotas del dueño
        respuesta_mascotas = listar_mascotas_por_dueno_bd({"documento": documento})
        if not respuesta_mascotas["Respuesta"]:
            print(respuesta_mascotas["Mensaje"])
            return

        mascotas_data = respuesta_mascotas["Datos"]
        mascotas = []

        for m in mascotas_data:
            if not m.get("nombre_mascota"):
                continue
            datos_mascota = {
                "id": m["id_mascota"],
                "nombre": m["nombre_mascota"],
                "especie": m["especie"],
                "raza": m["raza"],
                "edad": m["edad"],
                "id_dueno": m["id_dueno"],
                "activo": m["activo"]
            }
            mascotas.append(Mascota(**datos_mascota))

        if not mascotas:
            print("Este dueño no tiene mascotas activas registradas.")
            return

        print("\nMascotas activas registradas:")
        for mascota in mascotas:
            print(f"  - {mascota.nombre}")

        nombre_original = input("Nombre de la mascota que desea modificar: ").strip().title()
        mascota_encontrada = next((m for m in mascotas if m.nombre == nombre_original), None)

        if not mascota_encontrada:
            print(f"No se encontró una mascota activa llamada '{nombre_original}'.")
            return

        print(f"\nDatos actuales de '{nombre_original}':\n{mascota_encontrada}")
        print("Ingrese los nuevos datos (deje en blanco para mantener el valor actual):")

        while True:
            nuevo_nombre = input(f"Nuevo nombre [{mascota_encontrada.nombre}]: ").strip().title()
            if not nuevo_nombre:
                nuevo_nombre = mascota_encontrada.nombre
                break
            # Verificar duplicado (ignorando el nombre actual)
            nombres_existentes = [
                m.nombre.lower()
                for m in mascotas
                if m.nombre.lower() != mascota_encontrada.nombre.lower()
            ]
            if nuevo_nombre.lower() in nombres_existentes:
                print(f"Ya existe otra mascota llamada '{nuevo_nombre}' registrada para este dueño. Usa otro nombre.")
                continue
            break

        nueva_especie = input(f"Especie [{mascota_encontrada.especie}]: ").strip().capitalize() or mascota_encontrada.especie
        nueva_raza = input(f"Raza [{mascota_encontrada.raza}]: ").strip().title() or mascota_encontrada.raza

        while True:
            nueva_edad_input = input(f"Edad [{mascota_encontrada.edad}]: ").strip()
            if not nueva_edad_input:
                nueva_edad = mascota_encontrada.edad
                break
            try:
                nueva_edad = int(nueva_edad_input)
                if nueva_edad >= 0:
                    break
                print("La edad debe ser igual o mayor a 0.")
            except ValueError:
                print("Por favor, ingresa un número válido para la edad.")

        # Construir diccionario para la función de base de datos
        datos_modificados = {
            "documento": documento,
            "nombre_original": nombre_original,
            "nombre": nuevo_nombre,
            "especie": nueva_especie,
            "raza": nueva_raza,
            "edad": nueva_edad
        }

        respuesta = modificar_mascota_bd(datos_modificados)

        if respuesta["Respuesta"]:
            print("Mascota modificada exitosamente.")
            logger.info(f"Mascota modificada: {nombre_original} -> {nuevo_nombre}")
        else:
            print(f"No se pudo modificar la mascota: {respuesta['Mensaje']}")
            logger.error(respuesta["Mensaje"])

    except Exception as e:
        logger.exception("Error modificando mascota")
        print("Ocurrió un error al modificar la mascota.")


def eliminar_mascota():
    """
    Elimina una mascota asociada a un dueño. Solicita primero el documento del dueño,
    muestra sus mascotas registradas y luego permite seleccionar una por nombre para eliminarla.
    """
    try:
        print("\n--- Eliminar Mascota ---")

        # Confirmar existencia del dueño
        while True:
            documento_dueno = input("Documento del dueño: ").strip()
            if not documento_dueno:
                print("El documento no puede estar vacío. Intenta nuevamente.")
                continue

            respuesta_dueno = buscar_dueno_por_documento_bd(documento_dueno)
            if not respuesta_dueno["Respuesta"]:
                print(respuesta_dueno["Mensaje"])
                continue

            datos_dueno = respuesta_dueno["Datos"]
            dueno = Dueno(**datos_dueno)

            print("\n--- Datos del Dueño ---")
            print(dueno)

            # Obtener mascotas asociadas
            respuesta_mascotas = listar_mascotas_por_dueno_bd({"documento": documento_dueno})
            if not respuesta_mascotas["Respuesta"]:
                print(respuesta_mascotas["Mensaje"])
                return

            mascotas_data = respuesta_mascotas["Datos"]
            mascotas = [
                Mascota(
                    id=m["id_mascota"],
                    nombre=m["nombre_mascota"],
                    especie=m["especie"],
                    raza=m["raza"],
                    edad=m["edad"],
                    id_dueno=m["id_dueno"],
                    activo=m["activo"]
                )
                for m in mascotas_data if m.get("nombre_mascota")
            ]

            if not mascotas:
                print("El dueño no tiene mascotas registradas.")
                return

            print("\n--- Mascotas Registradas ---")
            for mascota in mascotas:
                print(f"  - {mascota.nombre}")

            break

        # Solicitar nombre de la mascota a eliminar
        nombre_mascota = input("Nombre de la mascota a eliminar: ").strip().title()

        mascota_a_eliminar = next((m for m in mascotas if m.nombre == nombre_mascota), None)
        if not mascota_a_eliminar:
            print(f"No se encontró una mascota con el nombre '{nombre_mascota}' para este dueño.")
            return

        confirmacion = input(f"¿Deseas eliminar a '{nombre_mascota}'? (s/n): ").strip().lower()
        if confirmacion != 's':
            print("Operación cancelada.")
            return

        respuesta_eliminacion = eliminar_mascota_bd(documento_dueno, nombre_mascota)
        if respuesta_eliminacion["Respuesta"]:
            print(f"Mascota '{nombre_mascota}' eliminada exitosamente.")
            logger.info(f"Mascota eliminada: {nombre_mascota} - Dueño: {documento_dueno}")
        else:
            print(respuesta_eliminacion["Mensaje"])
            logger.error(respuesta_eliminacion["Mensaje"])

    except Exception as e:
        logger.exception("Error eliminando mascota")
        print("Ocurrió un error al eliminar la mascota.")
