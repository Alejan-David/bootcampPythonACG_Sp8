class Mascota:
    def __init__(self, nombre, especie, raza, edad, dueno):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.dueno = dueno
        self.consultas = []  # Lista para almacenar historial de consultas

    def __str__(self):
        unidad_edad = "año" if self.edad == 1 else "años"
        return f"Mascota: {self.nombre}, {self.especie} - {self.raza}, Edad: {self.edad} {unidad_edad}" #Se eliminó la información del dueño temporalmente.