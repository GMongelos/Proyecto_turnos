"""
Conexion a la base de datos
"""

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.model.turno import Base, TurnoORM

DB_NAME = 'baseturnos'

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
