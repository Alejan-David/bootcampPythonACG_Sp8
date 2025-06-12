# Clase Consulta
class Consulta:
    def __init__(self, id, fecha, motivo, diagnostico, id_mascota, activo):
        self.id = id
        self.fecha = fecha
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.id_mascota = id_mascota
        self.activo = activo

    def __str__(self):
        return f"Fecha: {self.fecha}, Motivo: {self.motivo}, Diagnóstico: {self.diagnostico}"