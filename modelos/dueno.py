# Clase Dueño
class Dueno:
    def __init__(self, nombre, telefono, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return f"Dueño: {self.nombre}, Tel: {self.telefono}, Dirección: {self.direccion}"