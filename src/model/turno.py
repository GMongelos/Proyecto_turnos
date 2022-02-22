from src.model.exceptions import CamposVaciosError
from src.validador import texto, dni, fecha


class Turno:
    validadores = {
        'nombre': texto,
        'apellido': texto,
        'dni': dni,
        'profesional': texto,
        'fecha': fecha
    }

    def __init__(self, nombre, apellido, nro_dni, profesional, _fecha, observaciones='', **kwargs):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = nro_dni
        self.profesional = profesional
        self.fecha = _fecha
        self.observaciones = observaciones if observaciones else ''
        self.validar()

    def validar(self):
        campos = self.__dict__.copy()
        del (campos['observaciones'])
        vacios = [k for k, v in campos.items() if not v.strip()]
        if vacios:
            raise CamposVaciosError(vacios)

    def db_values(self):
        return self.__dict__.copy()

    def update(self, campo, valor):
        self.__setattr__(campo, valor)
