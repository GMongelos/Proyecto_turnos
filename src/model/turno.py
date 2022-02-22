from src.model.exceptions import CamposVaciosError
from src.validador import texto, dni, fecha


class Turno:
    """
    Modelo de turnos
    """
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
        """
        Validaciones al crear el turno
        """
        campos = self.__dict__.copy()
        del (campos['observaciones'])
        vacios = [k for k, v in campos.items() if not v.strip()]
        if vacios:
            raise CamposVaciosError(vacios)

    def db_values(self):
        """
        Retorna el diccionario de valores que se almacenan en la db
        """
        return self.__dict__.copy()

    def update(self, campo, valor):
        """
        Actualiza el valor de un campo
        """
        self.__setattr__(campo, valor)
