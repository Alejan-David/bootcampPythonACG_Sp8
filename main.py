from utilidades.funciones import registrar_mascota, registrar_consulta, listar_mascotas, ver_historial_consultas, cargar_datos_almacenados
from utilidades.logger import logger
# Menú principal
#cambio 2
def menu():
    while True:
        print(
            """
🐾 Clínica Veterinaria 'Amigos Peludos' 🐾

1. Registrar mascota
2. Registrar consulta
3. Listar mascotas
4. Ver historial de consultas
5. Salir
"""
        )

        try:
            opcion = int(input("Seleccione una opción (1-5): "))
        except ValueError:
            print("\nEntrada inválida. Por favor, ingrese un número del 1 al 5.\n")
            continue

        if opcion == 1:
            registrar_mascota()
        elif opcion == 2:
            registrar_consulta()
        elif opcion == 3:
            listar_mascotas()
        elif opcion == 4:
            ver_historial_consultas()
        elif opcion == 5:
            print("\nGracias por usar la aplicación. ¡Hasta pronto!")
            break
        else:
            print("\nOpción fuera de rango. Intente nuevamente.\n")

# Ejecutar el menú
if __name__ == "__main__":
    logger.info("Aplicación iniciada")
    cargar_datos_almacenados()
    menu()
    logger.info("Aplicación finalizada")
