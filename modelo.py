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

        del(d['_sa_instance_state'])
        if not con_id:
            del(d['id'])
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
    # session = Session(engine)
    consulta = select(TurnoORM).order_by(TurnoORM.fecha.desc())

    return session.execute(consulta).all()


def seleccionar_registro(dni):
    # session = Session(engine)
    consulta = select(TurnoORM).where(TurnoORM.dni == dni).order_by(TurnoORM.fecha.desc())

    dato = session.execute(consulta).first()[0]
    return dato


def borrar_registro():
    pass


def actualizar_registro():
    pass

# class Database:
#     """
#     Clase que encapsula todos los métodos relacionados con un abmc. Todos los
#     errores quedan registrados en /log
#     """
#
#     def __init__(self, nombre):
#         """
#         Define el nombre de el archivo de la base de datos
#         :param nombre: Nombre para la base de datos. Ej base -> base.db
#         """
#         self.nombre_db = nombre + ".db"
#         self.db_logger = Logger(log_filename='database')
#
#     def conectar(self):
#         """
#         Conecta con la base de datos
#         :raises Error:
#         """
#         try:
#             con = sqlite3.connect(self.nombre_db)
#             self.db_logger.loguear_info(f"Conectado a la base de datos ({self.nombre_db})")
#         except Error:
#             print("Ocurrio un error al intentar conectar con la base de datos")
#             self.db_logger.loguear_exepcion(Error)
#         else:
#             return con
#
#     def crear_tabla(self, conexion):
#         """
#         Crea la tabla de turnos
#         :raises Error:
#         """
#         try:
#             cursor_obj = conexion.cursor()
#             cursor_obj.execute("""CREATE TABLE IF NOT EXISTS turnos(
#                                 id integer PRIMARY KEY,
#                                 nombre TEXT NOT NULL,
#                                 apellido TEXT NOT NULL,
#                                 dni TEXT NOT NULL,
#                                 fecha TEXT NOT NULL,
#                                 profesional TEXT NOT NULL,
#                                 email TEXT,
#                                 observaciones TEXT)""")
#             conexion.commit()
#         except Error:
#             print("Hubo un error al crear tabla")
#             self.db_logger.loguear_exepcion(Error)
#
#     def insertar_registro(self, conexion, turno: Turno):
#         """Inserta un registro nuevo en la tabla turnos"""
#
#         datos = turno.db_values()
#
#         cursor = conexion.cursor()
#         cursor.execute(f"""INSERT INTO turnos ({', '.join(datos.keys())})
#                            VALUES({', '.join([f':{c}' for c in datos.keys()])})""",
#                        datos)
#         self.db_logger.loguear_info(f'Se insertó un registro en la bd.')
#         conexion.commit()
#
#     @staticmethod
#     def obtener_registros(conexion):
#         """Obtiene todos los registros de la tabla turnos"""
#
#         cursor = conexion.cursor()
#         cursor.execute("SELECT * FROM turnos ORDER BY fecha DESC")
#         return cursor.fetchall()
#
#     @staticmethod
#     def seleccionar_registro(conexion, dni):
#         """Selecciona el registro más reciente según el dni"""
#
#         cursor = conexion.cursor()
#         cursor.execute("SELECT * FROM turnos WHERE dni = :dni ORDER BY fecha", {'dni': dni})
#         return cursor.fetchone()
#
#     def borrar_registro(self, conexion, id_turno):
#         """Borra un registro según el id provisto. Por seguridad loguea la accion"""
#
#         cursor = conexion.cursor()
#         cursor.execute("DELETE FROM turnos WHERE id=:id", {'id': id_turno})
#         conexion.commit()
#         self.db_logger.loguear_info(f'Registro con id [{id_turno}] eliminado.')
#
#     def actualizar_registro(self, conexion, _id, turno):
#         """Actualiza un registro en la tabla segun su id"""
#         datos = turno.db_values()
#         datos['id'] = _id
#         cursor = conexion.cursor()
#         cursor.execute(f'UPDATE turnos {update_string()} WHERE id=:id', datos)
#         self.db_logger.loguear_info(f'Registro con id [{_id}] actualizado.')
#         conexion.commit()
