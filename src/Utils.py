import re
import os
import datetime


class ValidadorInput:
    # Definiciones de los distintos patrones de regex
    def __init__(self):
        self.regexpr = {
            'dni': r'^(PAS |pas )?[0-9]+$',
            'texto': r'^[^0-9]{2,}$',
            'email': r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+',
            'fecha': r'^(20\d{2})/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])$'
        }

    def validar(self, tipo, mensaje):
        """Valida input con regex"""
        valido = False
        while not valido:
            input_validar = input(mensaje)

            # Obtengo el patron
            patron = self.regexpr.get(tipo)

            if not re.match(patron, input_validar):
                print("El dato ingresado no es valido, intente de nuevo")
            else:
                return input_validar


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

    @staticmethod
    def obtener_timestamp():
        return datetime.datetime.now()



def separador(text=''):
    if text:
        print(f"\n{text}")
    print('-' * 50)
    print()


def update_string():
    return "SET " + ', '.join(["nombre =:nombre", "apellido =:apellido", "dni =:dni",
                               "fecha =:fecha", "profesional =:profesional", "observaciones =:observaciones"])
