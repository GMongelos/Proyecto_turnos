import datetime
import os
import sys


class Logger:
    """Clase para loguear datos a distintos niveles"""
    exit_string = ("-" * 10) + " APLICACION TERMINADA " + ("-" * 10)
    # line_exep = sys.exc_info()[-1].tb_lineno()

    def __init__(self):
        self.dir_log = os.path.join(os.getcwd(), 'log')
        self.path_log_error = os.path.join(self.dir_log, 'errores.log')
        self.path_log_info = os.path.join(self.dir_log, 'info.log')
        os.makedirs(self.dir_log, exist_ok=True)

    def loguear_error(self, error):
        with open(self.path_log_error, 'a') as f:
            f.write(f"[ERROR][{self.obtener_timestamp()}][LINEA ]: {error}\n")

    def loguear_warning(self, mensaje):
        with open(self.path_log_info, 'a') as f:
            f.write(f"[WARNING][{self.obtener_timestamp()}]: {mensaje}\n")

    def loguear_notice(self, mensaje):
        with open(self.path_log_info, 'a') as f:
            f.write(f"[NOTICE][{self.obtener_timestamp()}]: {mensaje}\n")

    def loguear_exit(self):
        self.loguear_notice(self.exit_string)

    @staticmethod
    def obtener_timestamp():
        return datetime.datetime.now()
