from base_datos.inicializar import inicializar_bd
from utilidades.logger import logger

from utilidades.funciones.dueno import(
    registrar_dueno,
    buscar_dueno_por_documento,
    listar_duenos,
    eliminar_dueno,
    modificar_dueno
) 

from utilidades.funciones.mascota import(
    registrar_mascota,
    modificar_mascota,
    eliminar_mascota
)

from utilidades.funciones.consulta import(
    registrar_consulta,
    listar_consultas_por_mascota,
    modificar_consulta,
    eliminar_consulta
)

def menu_principal():
    while True:
        print(
            """
🐾 Clínica Veterinaria 'Amigos Peludos' 🐾

Seleccione el menú al cuál desea acceder 

1. Dueños
2. Mascotas
3. Consultas
4. Salir de la aplicación
"""
        )

        try:
            opcion = int(input("Seleccione una opción (1-5): "))
        except ValueError:
            print("\nEntrada inválida. Por favor, ingrese un número del 1 al 5.\n")
            continue

        if opcion == 1:
            menu_duenos()
        elif opcion == 2:
            menu_mascotas()
        elif opcion == 3:
            menu_consultas()                 
        elif opcion == 4:
            print("\nGracias por usar la aplicación. ¡Hasta pronto!")
            break
        else:
            print("\nOpción fuera de rango. Intente nuevamente.\n")

def menu_duenos():
    while True:
        print(
            """
🐾 Menú Dueños 🐾

1. Registrar dueño
2. Buscar dueño
3. Modificar dueño
4. Eliminar dueño
5. Ver lista de dueños
6. Menú principal
"""
        )

        try:
            opcion = int(input("Seleccione una opción (1-5): "))
        except ValueError:
            print("\nEntrada inválida. Por favor, ingrese un número del 1 al 5.\n")
            continue

        if opcion == 1:
            registrar_dueno()
        elif opcion == 2:
            buscar_dueno_por_documento()
        elif opcion == 3:
            modificar_dueno()
        elif opcion == 4:
            eliminar_dueno()
        elif opcion == 5:
            listar_duenos()            
        elif opcion == 6:
            menu_principal()
        else:
            print("\nOpción fuera de rango. Intente nuevamente.\n")

def menu_mascotas():
    while True:
        print(
            """
🐾 Menú Mascotas 🐾

1. Registrar mascota
2. Buscar mascotas por dueño
3. Modificar mascota
4. Eliminar mascota
5. Menú principal
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
            buscar_dueno_por_documento()
        elif opcion == 3:
            modificar_mascota()
        elif opcion == 4:
            eliminar_mascota()      
        elif opcion == 5:
            menu_principal()
        else:
            print("\nOpción fuera de rango. Intente nuevamente.\n")

def menu_consultas():
    while True:
        print(
            """
🐾 Menú Consultas 🐾

1. Registrar consulta
2. Buscar consultas por mascota
3. Modificar consulta
4. Eliminar consulta
5. Menú principal
"""
        )

        try:
            opcion = int(input("Seleccione una opción (1-5): "))
        except ValueError:
            print("\nEntrada inválida. Por favor, ingrese un número del 1 al 5.\n")
            continue

        if opcion == 1:
            registrar_consulta()
        elif opcion == 2:
            listar_consultas_por_mascota()
        elif opcion == 3:
            modificar_consulta()
        elif opcion == 4:
            eliminar_consulta()      
        elif opcion == 5:
            menu_principal()
        else:
            print("\nOpción fuera de rango. Intente nuevamente.\n")
# Ejecutar el menú
if __name__ == "__main__":
    logger.info("Aplicación iniciada")
    inicializar_bd()
    menu_principal()
    logger.info("Aplicación finalizada")
