import re
import datetime

# Definicioes de los distintos patrones de regex
regexpr = {
    'dni': r'^(PAS |pas )?[0-9]+$',
    'texto': r'^[^0-9]{2,}$',
    'email': r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+',
    'fecha': r'^(20\d{2})/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])$'
}


def validar_input(tipo, mensaje):
    """Valida input con regex"""
    valido = False
    while not valido:
        input_validar = input(mensaje)

        # Obtengo el patron y verifico si es valido
        patron = regexpr.get(tipo)
        if not re.match(patron, input_validar):
            print("El dato ingresado no es valido, intente de nuevo")
        else:
            return input_validar


def separador(text=''):
    if text:
        print(f"\n{text}")
    print('-' * 50)
    print()


def update_string():
    return "SET " + ', '.join(["nombre =:nombre", "apellido =:apellido", "dni =:dni",
                               "fecha =:fecha", "profesional =:profesional", "observaciones =:observaciones"])
