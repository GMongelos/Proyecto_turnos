import datetime
import os
import sys


class Logger:
    """Clase para loguear datos a distintos niveles"""

    exit_string = ("-" * 10) + " APLICACION TERMINADA " + ("-" * 10)

    def __init__(self):
        """
        Crea el objeto Logger junto con su directorio de archivos
        """
        self.dir_log = os.path.join(os.getcwd(), 'log')
        self.path_log_error = os.path.join(self.dir_log, 'errores.log')
        self.path_log_info = os.path.join(self.dir_log, 'info.log')
        os.makedirs(self.dir_log, exist_ok=True)

    def loguear_error(self, error):
        """
        Loguea un error en errores.log
        """

        exc_tb = sys.exc_info()[2]
        archivo = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        with open(self.path_log_error, 'a') as f:
            f.write(f"[ERROR][{self.obtener_timestamp()}][Archivo: {archivo}][Linea {exc_tb.tb_lineno}]: {error}\n")

    def loguear_warning(self, mensaje):
        """
        Loguea un warning en info.log
        """

        with open(self.path_log_info, 'a') as f:
            f.write(f"[WARNING][{self.obtener_timestamp()}]: {mensaje}\n")

    def loguear_notice(self, mensaje):
        """
        Loguea un notice en info.log
        """

        with open(self.path_log_info, 'a') as f:
            f.write(f"[NOTICE][{self.obtener_timestamp()}]: {mensaje}\n")

    def loguear_exit(self):
        """
        Loguea elmomento en el cual se cierra la aplicacion, ya sea por error o por eleccion del usuario
        """

        self.loguear_notice(self.exit_string)

    @staticmethod
    def obtener_timestamp():
        return datetime.datetime.now()
