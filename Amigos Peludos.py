# Clase Dueño
class Dueno:
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return f"Dueño: {self.nombre}, Tel: {self.telefono}, Dirección: {self.direccion}"


# Clase Mascota
class Mascota:
    def __init__(self, nombre, especie, raza, edad, dueno):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.dueno = dueno
        self.consultas = []  # Lista para almacenar historial de consultas

    def agregar_consulta(self, consulta):
        self.consultas.append(consulta)

    def mostrar_historial(self):
        return "\n".join(str(consulta) for consulta in self.consultas)

    def __str__(self):
        unidad_edad = "año" if self.edad == 1 else "años"
        return f"Mascota: {self.nombre}, {self.especie} - {self.raza}, Edad: {self.edad} {unidad_edad}\n{self.dueno}"


# Clase Consulta
class Consulta:
    def __init__(self, fecha, motivo, diagnostico, mascota):
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.mascota = mascota

    def __str__(self):
        return f"Fecha: {self.fecha}, Motivo: {self.motivo}, Diagnóstico: {self.diagnostico}"


# Diccionario para almacenar mascotas por nombre
mascotas_registradas = {}


# Función para registrar una mascota
def registrar_mascota():
    print("\n--- Registrar Mascota ---")
    nombre_mascota = input("Nombre de la mascota: ").strip().title()
    especie = input("Especie (Ej: Perro, Gato): ").strip().capitalize()
    raza = input("Raza: ").strip().title()

    while True:
        try:
            edad = int(input("Edad: ").strip())
            if edad >= 0:
                break
            else:
                print("La edad debe ser igual o mayor a 0. Inténtalo nuevamente.")
        except ValueError:
            print("Por favor, ingresa un número válido para la edad.")

    print("\n--- Datos del dueño ---")
    nombre_dueno = input("Nombre del dueño: ").strip().title()

    while True:
        telefono = input("Teléfono: ").strip()
        if telefono.isdigit():
            break
        else:
            print("El teléfono solo debe contener números. Inténtalo nuevamente.")

    direccion = input("Dirección: ").strip().capitalize()

    # Se guarda la información en cada clase con argumentos posicionales 
    dueno = Dueno(nombre_dueno, telefono, direccion)
    mascota = Mascota(nombre_mascota, especie, raza, edad, dueno)

    # Se guarda el objeto mascota en el diccionario "mascotas_registradas" con el nombre de la mascota como clave
    # y la clase mascota como valor, la cual contiene la clase dueño y su método __str__
    mascotas_registradas[nombre_mascota.lower()] = mascota
    print(f"\nMascota '{nombre_mascota}' registrada con éxito.\n")



# Función para registrar una consulta
def registrar_consulta():
    print("\n--- Registrar Consulta ---")
    nombre_mascota = input("Nombre de la mascota: ").strip().lower()

    if nombre_mascota not in mascotas_registradas:
        print("Mascota no encontrada. Registre primero la mascota.\n")
        return

    mascota = mascotas_registradas[nombre_mascota]
    fecha = input("Fecha (DD/MM/AAAA): ").strip()
    motivo = input("Motivo de la consulta: ").strip().capitalize()
    diagnostico = input("Diagnóstico: ").strip().capitalize()

    consulta = Consulta(fecha, motivo, diagnostico, mascota)
    mascota.agregar_consulta(consulta)
    print("Consulta registrada correctamente.\n")




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
    else:
        mascota = mascotas_registradas[nombre_mascota]
        if not mascota.consultas:
            print(f"\nLa mascota '{mascota.nombre}' no tiene consultas registradas.\n")
        else:
            print(f"\nHistorial de consultas para {mascota.nombre}:")
            print(mascota.mostrar_historial())
            print("-" * 40)


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
    menu()