from utils.funciones import registrar_mascota, registrar_consulta, listar_mascotas, ver_historial_consultas
from utils.logger import logger

# Menú principal
def menu():
    while True:
        print("\n🐾 Clínica Veterinaria 'Amigos Peludos' 🐾\n")
        print("1. Registrar mascota")
        print("2. Registrar consulta")
        print("3. Listar mascotas")
        print("4. Ver historial de consultas")
        print("5. Salir")

        opcion = input("\nSeleccione una opción (1-5): ")

        if opcion == '1':
            registrar_mascota()
        elif opcion == '2':
            registrar_consulta()
        elif opcion == '3':
            listar_mascotas()
        elif opcion == '4':
            ver_historial_consultas()
        elif opcion == '5':
            print("\nGracias por usar la aplicación. ¡Hasta pronto!")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.\n")


# Ejecutar el menú
if __name__ == "__main__":
    logger.info("Aplicación iniciada")
    menu()  # llama a la función del menú
    logger.info("Aplicación finalizada")    