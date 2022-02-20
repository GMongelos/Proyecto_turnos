"""
Conexion a la base de datos
"""
import sqlite3
from sqlite3 import Error

from src.Utils import Logger, update_string


class Database:

    def __init__(self, nombre):
        self.nombre_db = nombre + ".db"
        self.db_logger = Logger()

    def conectar(self):
        """Conecta con la base de datos"""
        try:
            con = sqlite3.connect(self.nombre_db)
            self.db_logger.loguear_notice(f"Conectado a la base de datos ({self.nombre_db})")
            return con
        except Error:
            print("Ocurrio un error al intentar conectar con la base de datos")
            self.db_logger.loguear_error(Error)

    @staticmethod
    def crear_tabla(conexion):
        """Crea la tabla de turnos"""

        try:
            cursor_obj = conexion.cursor()
            cursor_obj.execute("""CREATE TABLE IF NOT EXISTS turnos(
                                id integer PRIMARY KEY, 
                                nombre TEXT NOT NULL,
                                apellido TEXT NOT NULL,
                                dni TEXT NOT NULL,
                                fecha TEXT NOT NULL,
                                profesional TEXT NOT NULL,
                                observaciones TEXT)""")
            conexion.commit()
        except Error:
            print("Hubo un error al crear tabla")
            obj_logger = Logger()
            obj_logger.loguear_error(Error)

    # TODO: Parametrizar el nombre de la bd
    def insertar_registro(self, conexion, datos):
        cursor = conexion.cursor()
        cursor.execute("""INSERT INTO turnos (nombre, apellido, dni, fecha, profesional, observaciones)
                                    VALUES(:nombre, :apellido, :dni, :fecha, :profesional, :observaciones)""",
                       datos)
        conexion.commit()

    def obtener_registros(self, conexion):
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM turnos ORDER BY fecha DESC")
        return cursor.fetchall()

    def seleccionar_registro(self, conexion, dni):
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM turnos WHERE dni = :dni ORDER BY fecha", {'dni': dni})
        return cursor.fetchone()

    def borrar_registro(self, conexion, id_turno):
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM turnos WHERE id=:id", {'id': id_turno})
        conexion.commit()

    def actualizar_registro(self, conexion, datos):
        cursor = conexion.cursor()
        cursor.execute(f'UPDATE turnos {update_string()} WHERE id=:id', datos)
        conexion.commit()


if __name__ == '__main__':
    pass
