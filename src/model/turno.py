from src.model.exceptions import CamposVaciosError


class Turno:
    def __init__(self, nombre, apellido, dni, profesional, fecha, observaciones='', **kwargs):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.profesional = profesional
        self.fecha = fecha
        self.observaciones = observaciones
        self.validar()

    def validar(self):
        campos = self.__dict__
        del (campos['observaciones'])
        vacios = [k for k, v in campos.items() if not v.strip()]
        if vacios:
            raise CamposVaciosError(vacios)
