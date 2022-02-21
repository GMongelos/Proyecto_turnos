import datetime
import os


class Logger:
    def __init__(self):
        self.dir_log = os.path.join(os.getcwd(), 'log')
        self.path_log = os.path.join(self.dir_log, 'errores.log')
        os.makedirs(self.dir_log, exist_ok=True)

    def loguear_error(self, error):
        with open(self.path_log, 'a') as f:
            f.write(f"[ERROR][{self.obtener_timestamp()}]: {error}\n")

    def loguear_warning(self, mensaje):
        with open(self.path_log, 'a') as f:
            f.write(f"[WARNING][{self.obtener_timestamp()}]: {mensaje}\n")

    def loguear_notice(self, mensaje):
        with open(self.path_log, 'a') as f:
            f.write(f"[NOTICE][{self.obtener_timestamp()}]: {mensaje}\n")

    @staticmethod
    def obtener_timestamp():
        return datetime.datetime.now()
