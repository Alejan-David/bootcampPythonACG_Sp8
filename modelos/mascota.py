class Mascota:
    def __init__(self, id, nombre, especie, raza, edad, id_dueno, activo):

        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.id_dueno = id_dueno
        self.activo = activo

    def __str__(self):
        estado = "Activo" if self.activo == 's' else "Inactivo"
        unidad_edad = "año" if self.edad == 1 else "años"
        return (
            f"Nombre: {self.nombre}, Especie: {self.especie}, Raza: {self.raza}, "
            f"Edad: {self.edad} {unidad_edad}, Estado: {estado}"
        ) 