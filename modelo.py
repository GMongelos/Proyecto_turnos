"""
Conexion a la base de datos
"""

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base, Session

import os
# import sqlite3
# from sqlite3 import Error

from src.logger import Logger
from src.model.turno import Turno

DB_NAME = 'baseturnos'


def update_string():
    """
    Funcion que ayuda a generar el string necesario para actualizar registross la BD

    :returns: Un string para la cláusula SET
    """

    return "SET " + ', '.join(["nombre =:nombre", "apellido =:apellido", "dni =:dni",
                               "fecha =:fecha", "profesional =:profesional", "observaciones =:observaciones"])


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


engine = create_engine(f"sqlite:///{DB_NAME}.db", echo=True, future=True)
session = Session(engine)
Base.metadata.create_all(engine)


def obtener_registros():
    consulta = select(TurnoORM).order_by(TurnoORM.fecha.desc())

    return session.execute(consulta).all()


def seleccionar_registro(dni):
    consulta = select(TurnoORM).where(TurnoORM.dni == dni).order_by(TurnoORM.fecha.desc())

    dato = session.execute(consulta).first()[0]
    return dato
