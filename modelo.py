"""
Conexion a la base de datos
"""
import sqlite3
from sqlite3 import Error

from src.logger import Logger


def update_string():
    """
    Funcion que ayuda a generar el string necesario para actualizar registross la BD

    :returns: Un string para la cláusula SET
    """

    return "SET " + ', '.join(["nombre =:nombre", "apellido =:apellido", "dni =:dni",
                               "fecha =:fecha", "profesional =:profesional", "observaciones =:observaciones"])


class Database:
    """
    Clase que encapsula todos los métodos relacionados con un abmc. Todos los
    errores quedan registrados en /log
    """

    def __init__(self, nombre):
        """
        Define el nombre de el archivo de la base de datos
        :param nombre: Nombre para la base de datos. Ej base -> base.db
        """
        self.nombre_db = nombre + ".db"
        self.db_logger = Logger()

    def conectar(self):
        """
        Conecta con la base de datos
        :raises Error:
        """
        try:
            con = sqlite3.connect(self.nombre_db)
            self.db_logger.loguear_notice(f"Conectado a la base de datos ({self.nombre_db})")
            return con
        except Error:
            print("Ocurrio un error al intentar conectar con la base de datos")
            self.db_logger.loguear_error(Error)

    def crear_tabla(self, conexion):
        """
        Crea la tabla de turnos
        :raises Error:
        """
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
            self.db_logger.loguear_error(Error)

    @staticmethod
    def insertar_registro(conexion, datos):
        """Inserta un registro nuevo en la tabla turnos"""

        cursor = conexion.cursor()
        cursor.execute("""INSERT INTO turnos (nombre, apellido, dni, fecha, profesional, observaciones)
                                    VALUES(:nombre, :apellido, :dni, :fecha, :profesional, :observaciones)""",
                       datos)
        conexion.commit()

    @staticmethod
    def obtener_registros(conexion):
        """Obtiene todos los registros de la tabla turnos"""

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM turnos ORDER BY fecha DESC")
        return cursor.fetchall()

    @staticmethod
    def seleccionar_registro(conexion, dni):
        """Selecciona el registro más reciente según el dni"""

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM turnos WHERE dni = :dni ORDER BY fecha", {'dni': dni})
        return cursor.fetchone()

    def borrar_registro(self, conexion, id_turno):
        """Borra un registro según el id provisto. Por seguridad loguea la accion"""

        cursor = conexion.cursor()
        cursor.execute("DELETE FROM turnos WHERE id=:id", {'id': id_turno})
        conexion.commit()
        self.db_logger.loguear_notice(f'Registro con id [{id_turno}] eliminado.')

    @staticmethod
    def actualizar_registro(conexion, datos):
        """Actualiza un registro en la tabla segun su id"""

        cursor = conexion.cursor()
        cursor.execute(f'UPDATE turnos {update_string()} WHERE id=:id', datos)
        conexion.commit()


if __name__ == '__main__':
    pass
