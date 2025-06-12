from modelos.dueno import Dueno
from modelos.mascota import Mascota
from modelos.consulta import Consulta
from utilidades.logger import logger
from datetime import datetime

from base_datos.funciones.dueno import (
    buscar_dueno_por_documento_bd
)

from base_datos.funciones.mascota import(
    listar_mascotas_por_dueno_bd
)

from base_datos.funciones.consulta import(
    registrar_consulta_bd,
    listar_consultas_por_id_mascota_bd,
    modificar_consulta_bd,
    eliminar_consulta_bd
)


def registrar_consulta():
    try:
        print("\n--- Registrar Consulta ---")

        documento = input("Documento del dueño: ").strip()
        if not documento:
            print("El documento no puede estar vacío.")
            return

        # Buscar dueño
        respuesta_dueno = buscar_dueno_por_documento_bd(documento)
        if not respuesta_dueno["Respuesta"]:
            print(respuesta_dueno["Mensaje"])
            return

        dueno = Dueno(**respuesta_dueno["Datos"])
        print("\nDueño encontrado:")
        print(dueno)

        # Listar mascotas activas
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

        nombre_mascota = input("Nombre de la mascota para registrar la consulta: ").strip()
        mascota_seleccionada = next((m for m in mascotas if m.nombre.lower() == nombre_mascota.lower()), None)
        if not mascota_seleccionada:
            print("No se encontró una mascota con ese nombre.")
            return

        # Obtener consultas existentes de la mascota
        respuesta_consultas = listar_consultas_por_id_mascota_bd({"id_mascota": mascota_seleccionada.id})
        consultas_existentes = respuesta_consultas["Datos"] if respuesta_consultas["Respuesta"] else []

        # Solicitar la fecha con reintento
        while True:
            fecha_str = input("Fecha de la consulta (dd/mm/aaaa): ").strip()
            try:
                fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
                fecha_formateada = fecha_obj.strftime("%Y-%m-%d")  # para BD

                if any(c["fecha"] == fecha_formateada for c in consultas_existentes):
                    print(f"Ya existe una consulta registrada en esa fecha ({fecha_str}) para esta mascota.")
                    continue

                break  # Fecha válida y no duplicada

            except ValueError:
                print("Formato de fecha inválido. Use dd/mm/aaaa.")

        motivo = input("Motivo de la consulta: ").strip()
        diagnostico = input("Diagnóstico: ").strip()

        # Crear objeto Consulta
        consulta = Consulta(
            id=None,
            fecha=fecha_formateada,
            motivo=motivo,
            diagnostico=diagnostico,
            id_mascota=mascota_seleccionada.id,
            activo=None
        )

        # Registrar en base de datos
        datos_consulta = {
            "fecha": consulta.fecha,
            "motivo": consulta.motivo,
            "diagnostico": consulta.diagnostico,
            "id_mascota": consulta.id_mascota
        }

        respuesta = registrar_consulta_bd(datos_consulta)
        print(respuesta["Mensaje"])

    except Exception as e:
        print(f"Error inesperado al registrar la consulta: {e}")


def listar_consultas_por_mascota():
    try:
        print("\n--- Historial de Consultas ---")

        documento = input("Documento del dueño: ").strip()
        if not documento:
            print("El documento no puede estar vacío.")
            return

        # Buscar dueño
        respuesta_dueno = buscar_dueno_por_documento_bd(documento)
        if not respuesta_dueno["Respuesta"]:
            print(respuesta_dueno["Mensaje"])
            return

        dueno = Dueno(**respuesta_dueno["Datos"])
        print("\nDueño encontrado:")
        print(dueno)

        # Listar mascotas activas del dueño
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

        nombre_mascota = input("Nombre de la mascota para ver el historial de consultas: ").strip()

        mascota_seleccionada = next((m for m in mascotas if m.nombre.lower() == nombre_mascota.lower()), None)
        if not mascota_seleccionada:
            print("No se encontró una mascota con ese nombre.")
            return

        # Consultas activas por ID de mascota
        respuesta_consultas = listar_consultas_por_id_mascota_bd({"id_mascota": mascota_seleccionada.id})

        if not respuesta_consultas["Respuesta"]:
            print(respuesta_consultas["Mensaje"])
            return

        consultas_data = respuesta_consultas["Datos"]
        if not consultas_data:
            print("No hay consultas activas registradas para esta mascota.")
            return

        print(f"\nHistorial de consultas para {mascota_seleccionada.nombre}:")
        for c in consultas_data:
            # Formatear fecha para presentación
            try:
                fecha_mostrar = datetime.strptime(c["fecha"], "%Y-%m-%d").strftime("%d/%m/%Y")
            except ValueError:
                fecha_mostrar = c["fecha"]  # Si no se puede convertir, mostrar como está

            print(f"  - Fecha: {fecha_mostrar}, Motivo: {c['motivo']}, Diagnóstico: {c['diagnostico']}")

    except Exception as e:
        print(f"Error inesperado al listar consultas: {e}")


def modificar_consulta():
    """
    Modifica los datos de una consulta registrada a una mascota de un dueño.
    Permite conservar los valores actuales si se dejan en blanco los nuevos campos.
    """
    try:
        print("\n--- Modificar Consulta ---")

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

        # Listar mascotas activas del dueño
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

        nombre_mascota = input("Nombre de la mascota: ").strip().title()
        mascota_encontrada = next((m for m in mascotas if m.nombre == nombre_mascota), None)
        if not mascota_encontrada:
            print(f"No se encontró una mascota activa llamada '{nombre_mascota}'.")
            return

        # Listar consultas activas de esa mascota
        respuesta_consultas = listar_consultas_por_id_mascota_bd({"id_mascota": mascota_encontrada.id})
        if not respuesta_consultas["Respuesta"]:
            print(respuesta_consultas["Mensaje"])
            return

        consultas = respuesta_consultas["Datos"]
        if not consultas:
            print("No hay consultas activas registradas para esta mascota.")
            return

        print(f"\nConsultas activas para {mascota_encontrada.nombre}:")
        for c in consultas:
            fecha_mostrar = datetime.strptime(c["fecha"], "%Y-%m-%d").strftime("%d/%m/%Y")
            print(f"  - Fecha: {fecha_mostrar}, Motivo: {c['motivo']}, Diagnóstico: {c['diagnostico']}")

        # Solicitar la fecha de la consulta a modificar (con reintento)
        consulta_actual = None
        while not consulta_actual:
            fecha_original_str = input("Fecha de la consulta a modificar (dd/mm/aaaa): ").strip()
            try:
                fecha_original = datetime.strptime(fecha_original_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                print("Formato de fecha inválido. Use dd/mm/aaaa.")
                continue

            consulta_actual = next((c for c in consultas if c["fecha"] == fecha_original), None)
            if not consulta_actual:
                print("No se encontró una consulta con esa fecha. Intente nuevamente.")
        
        print("\nIngrese los nuevos datos (deje en blanco para mantener el valor actual):")

        while True:
            nueva_fecha_str = input(f"Nueva fecha [{fecha_original_str}]: ").strip()
            if not nueva_fecha_str:
                nueva_fecha = consulta_actual["fecha"]
                break
            try:
                nueva_fecha_dt = datetime.strptime(nueva_fecha_str, "%d/%m/%Y")
                nueva_fecha = nueva_fecha_dt.strftime("%Y-%m-%d")
                if nueva_fecha != consulta_actual["fecha"]:
                    fechas_existentes = [c["fecha"] for c in consultas if c["id"] != consulta_actual["id"]]
                    if nueva_fecha in fechas_existentes:
                        print("Ya existe una consulta en esa fecha para esta mascota. Usa otra.")
                        continue
                break
            except ValueError:
                print("Formato de fecha inválido. Use dd/mm/aaaa.")

        nuevo_motivo = input(f"Motivo [{consulta_actual['motivo']}]: ").strip() or consulta_actual["motivo"]
        nuevo_diagnostico = input(f"Diagnóstico [{consulta_actual['diagnostico']}]: ").strip() or consulta_actual["diagnostico"]

        datos_modificados = {
            "id": consulta_actual["id"],
            "fecha": nueva_fecha,
            "motivo": nuevo_motivo,
            "diagnostico": nuevo_diagnostico
        }

        respuesta = modificar_consulta_bd(datos_modificados)

        if respuesta["Respuesta"]:
            print("Consulta modificada exitosamente.")
            logger.info(f"Consulta modificada para mascota '{mascota_encontrada.nombre}'")
        else:
            print(f"No se pudo modificar la consulta: {respuesta['Mensaje']}")
            logger.error(respuesta["Mensaje"])

    except Exception as e:
        logger.exception("Error modificando consulta")
        print("Ocurrió un error al modificar la consulta.")


def eliminar_consulta():
    """
    Elimina (inhabilita) una consulta activa de una mascota, permitiendo reintento en caso de error al ingresar la fecha.
    """
    try:
        print("\n--- Eliminar Consulta ---")

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

        # Listar mascotas activas
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

        print("\nMascotas activas:")
        for mascota in mascotas:
            print(f"  - {mascota.nombre}")

        nombre_mascota = input("Nombre de la mascota: ").strip().title()
        mascota_seleccionada = next((m for m in mascotas if m.nombre == nombre_mascota), None)
        if not mascota_seleccionada:
            print(f"No se encontró una mascota activa llamada '{nombre_mascota}'.")
            return

        # Listar consultas activas
        respuesta_consultas = listar_consultas_por_id_mascota_bd({"id_mascota": mascota_seleccionada.id})
        if not respuesta_consultas["Respuesta"]:
            print(respuesta_consultas["Mensaje"])
            return

        consultas = respuesta_consultas["Datos"]
        if not consultas:
            print("No hay consultas activas para esta mascota.")
            return

        print(f"\nConsultas activas para {mascota_seleccionada.nombre}:")
        for c in consultas:
            fecha_mostrar = datetime.strptime(c["fecha"], "%Y-%m-%d").strftime("%d/%m/%Y")
            print(f"  - Fecha: {fecha_mostrar}, Motivo: {c['motivo']}, Diagnóstico: {c['diagnostico']}")

        # Reintento al ingresar la fecha
        consulta_a_eliminar = None
        while True:
            fecha_str = input("Fecha de la consulta a eliminar (dd/mm/aaaa): ").strip()
            try:
                fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
                fecha_bd = fecha_obj.strftime("%Y-%m-%d")

                consulta_a_eliminar = next((c for c in consultas if c["fecha"] == fecha_bd), None)
                if not consulta_a_eliminar:
                    print("No se encontró una consulta activa en esa fecha. Intente nuevamente.")
                    continue
                break

            except ValueError:
                print("Formato de fecha inválido. Use dd/mm/aaaa.")

        # Confirmar eliminación
        confirmar = input(f"¿Desea eliminar la consulta del {fecha_str}? (s/n): ").strip().lower()
        if confirmar != 's':
            print("Operación cancelada.")
            return

        respuesta = eliminar_consulta_bd({"id": consulta_a_eliminar["id"]})
        if respuesta["Respuesta"]:
            print("Consulta eliminada exitosamente.")
            logger.info(f"Consulta eliminada para mascota '{mascota_seleccionada.nombre}' en fecha {fecha_str}")
        else:
            print(f"No se pudo eliminar la consulta: {respuesta['Mensaje']}")
            logger.error(respuesta["Mensaje"])

    except Exception as e:
        logger.exception("Error eliminando consulta")
        print("Ocurrió un error al eliminar la consulta.")


