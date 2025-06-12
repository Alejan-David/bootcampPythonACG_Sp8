class Dueno:
    def __init__(self, id, documento, nombre, telefono, direccion, activo):
        self.id = id
        self.documento = documento
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.activo = activo

    def __str__(self):
        estado = "Activo" if self.activo == 's' else "Inactivo"
        return (
            f"Documento: {self.documento}, Nombre: {self.nombre}, "
            f"Tel: {self.telefono}, Dirección: {self.direccion}, Estado: {estado}"
        )
