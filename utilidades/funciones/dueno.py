from modelos.dueno import Dueno
from modelos.mascota import Mascota
from utilidades.logger import logger
from base_datos.funciones.dueno import (
    registrar_dueno_bd,
    eliminar_dueno_bd,
    modificar_dueno_bd,
    buscar_dueno_por_documento_bd,
    listar_todos_los_duenos_y_mascotas_bd
)

from base_datos.funciones.mascota import (
    listar_mascotas_por_dueno_bd
)

def registrar_dueno():
    """
    Registra un dueño solicitando documento (con confirmación), nombre, teléfono y dirección.
    """
    try:
        print("\n--- Registrar Dueño ---")
        while True:
            documento = input("Documento: ").strip()
            confirmacion = input("Confirme el Documento: ").strip()
            if documento == confirmacion:
                break
            print("Los documentos no coinciden. Intente nuevamente.")

        nombre = input("Nombre: ").strip().title()
        telefono = input("Teléfono: ").strip()
        while not telefono.isdigit():
            telefono = input("Teléfono inválido. Intente nuevamente: ").strip()

        direccion = input("Dirección: ").strip()

        dueno = Dueno(id=None, documento=documento, nombre=nombre, telefono=telefono, direccion=direccion, activo=None)
        respuesta = registrar_dueno_bd(dueno.__dict__)

        if respuesta["Respuesta"]:
            print(f"Dueño '{nombre}' registrado con éxito.\n")
            logger.info(f"Dueño registrado: {nombre} - Documento: {documento}")
        else:
            print(f"No se pudo registrar el dueño: {respuesta['Mensaje']}")
            logger.error(respuesta["Mensaje"])

    except Exception as e:
        logger.exception("Error registrando dueño")
        print("Ocurrió un error al registrar el dueño.")


def buscar_dueno_por_documento():
    """
    Busca un dueño por documento e imprime sus datos junto con las mascotas registradas.
    """
    try:
        documento = input("\nIngrese el documento del dueño a buscar: ").strip()
        if not documento:
            print("Debe ingresar un documento.")
            return

        # Buscar dueño
        respuesta = buscar_dueno_por_documento_bd(documento)
        if not respuesta["Respuesta"]:
            print(respuesta["Mensaje"])
            return

        dueno = Dueno(**respuesta["Datos"])
        print(f"\nDueño encontrado:\n{dueno}")

        # Buscar mascotas del dueño
        respuesta_mascotas = listar_mascotas_por_dueno_bd({"documento": documento})
        if not respuesta_mascotas["Respuesta"]:
            print(respuesta_mascotas["Mensaje"])
            return

        mascotas_data = respuesta_mascotas["Datos"]
        mascotas = []

        for m in mascotas_data:
            if not m.get("nombre_mascota"):
                continue  # Evitar registros nulos por LEFT JOIN

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

        # Mostrar resultados
        if mascotas:
            print("\nMascotas registradas:")
            for mascota in mascotas:
                print(f"  - {mascota}")
        else:
            print("No tiene mascotas registradas.")

    except Exception as e:
        logger.exception("Error buscando dueño y mascotas")
        print("Ocurrió un error al buscar el dueño y sus mascotas.")


def listar_duenos():
    """
    Lista todos los dueños activos junto con los nombres de sus mascotas activas desde la base de datos.
    """
    try:
        print("\n--- Lista de Dueños con sus Mascotas ---")
        respuesta = listar_todos_los_duenos_y_mascotas_bd()

        if not respuesta["Respuesta"]:
            print(respuesta["Mensaje"])
            return

        duenos_agrupados = {}

        for r in respuesta["Datos"]:
            documento = r["documento"]
            if documento not in duenos_agrupados:
                # Construir el diccionario compatible con el constructor de Dueno
                datos_dueno = {
                    "id": r["id_dueno"],
                    "documento": r["documento"],
                    "nombre": r["nombre"],
                    "telefono": r["telefono"],
                    "direccion": r["direccion"],
                    "activo": r["activo"]
                }

                duenos_agrupados[documento] = {
                    "dueno": Dueno(**datos_dueno),
                    "mascotas": []
                }

            if r.get("nombre_mascota"):  # Validar que exista mascota
                duenos_agrupados[documento]["mascotas"].append(r["nombre_mascota"])

        # Imprimir resultados agrupados
        for doc, info in duenos_agrupados.items():
            dueno = info["dueno"]
            print(f"\n{dueno}")
            if info["mascotas"]:
                print("Mascotas:")
                for nombre in info["mascotas"]:
                    print(f"  - {nombre}")
            else:
                print("Mascotas: Ninguna registrada")

        print("-" * 40)

    except Exception as e:
        logger.exception("Error listando dueños y mascotas")
        print("Ocurrió un error al listar los dueños.")


def eliminar_dueno():
    """
    Elimina un dueño y sus mascotas asociadas, buscándolo por su documento.
    """
    try:
        print("\n--- Eliminar Dueño ---")
        documento = input("Ingrese el documento del dueño a eliminar: ").strip()

        respuesta = buscar_dueno_por_documento_bd(documento)
        if not respuesta["Respuesta"]:
            print(respuesta["Mensaje"])
            return

        nombre = respuesta["Datos"]["nombre"]
        confirmacion = input(f"¿Eliminar a '{nombre}' y sus mascotas? (s/n): ").strip().lower()
        if confirmacion != "s":
            print("Operación cancelada.")
            return

        respuesta_eliminar = eliminar_dueno_bd(documento)
        if respuesta_eliminar["Respuesta"]:
            print("Dueño y sus mascotas eliminados correctamente.")
            logger.info(f"Dueño eliminado: {documento}")
        else:
            print(f"No se pudo eliminar el dueño: {respuesta_eliminar['Mensaje']}")
            logger.error(respuesta_eliminar["Mensaje"])

    except Exception as e:
        logger.exception("Error eliminando dueño")
        print("Ocurrió un error al eliminar el dueño.")


def modificar_dueno():
    """
    Modifica los datos de un dueño existente, buscándolo por su documento.
    El campo 'documento' no puede ser modificado.
    """
    try:
        print("\n--- Modificar Dueño ---")
        documento = input("Ingrese el documento del dueño a modificar: ").strip()

        respuesta = buscar_dueno_por_documento_bd(documento)
        if not respuesta["Respuesta"]:
            print(respuesta["Mensaje"])
            return

        datos = respuesta["Datos"]
        dueno = Dueno(**datos)

        print(f"\nInformación actual del dueño:\n{dueno}")
        print("Ingrese los nuevos datos (deje en blanco para mantener el valor actual):")

        nombre = input(f"Nombre [{dueno.nombre}]: ").strip().title() or dueno.nombre
        telefono = input(f"Teléfono [{dueno.telefono}]: ").strip() or dueno.telefono
        direccion = input(f"Dirección [{dueno.direccion}]: ").strip() or dueno.direccion

        if telefono and not telefono.isdigit():
            print("El teléfono ingresado no es válido. La modificación fue cancelada.")
            return

        respuesta_modificar = modificar_dueno_bd({
            "documento": documento,
            "nombre": nombre,
            "telefono": telefono,
            "direccion": direccion
        })

        if respuesta_modificar["Respuesta"]:
            print("Dueño modificado exitosamente.")
            logger.info(f"Dueño modificado: {documento}")
        else:
            print(f"No se pudo modificar el dueño: {respuesta_modificar['Mensaje']}")
            logger.error(respuesta_modificar["Mensaje"])

    except Exception as e:
        logger.exception("Error modificando dueño")
        print("Ocurrió un error al modificar el dueño.")