from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

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
        'fecha': fecha,
        'observaciones': texto
    }

    def __init__(self, nombre, apellido, nro_dni, _fecha, profesional, observaciones='', **kwargs):
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


Base = declarative_base()


class TurnoORM(Base):
    __tablename__ = "turnos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    dni = Column(String(30), nullable=False)
    mail = Column(String(30))
    fecha = Column(String(30), nullable=False)
    profesional = Column(String(30), nullable=False)
    observaciones = Column(String(30))

    def __repr__(self):
        return f"Turno(id={self.id!r}, " \
               f"nombre={self.nombre!r}, " \
               f"apellido={self.apellido!r}, " \
               f"dni={self.dni!r}, " \
               f"mail={self.mail!r}, " \
               f"fecha={self.fecha!r}, " \
               f"profesional={self.profesional!r}, " \
               f"observaciones={self.observaciones!r})"

    def atrss(self, con_id=True):
        d = self.__dict__.copy()

        del (d['_sa_instance_state'])
        if not con_id:
            del (d['id'])
        return d

    def update(self, campo, valor):
        """
        Actualiza el valor de un campo
        """
        self.__setattr__(campo, valor)