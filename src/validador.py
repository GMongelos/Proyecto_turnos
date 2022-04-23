import re

regexpr = {
    'dni': r'^(PAS |pas )?[0-9]+$',
    'texto': r'^[^0-9]{2,}$',
    'mail': r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+',
    'fecha': r'^(20\d{2})/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])$'
}


def texto(s: str):
    """
    Validacion de tipo texto, espera por lo menos 2 caracteres
    """

    return re.match(regexpr.get('texto'), s.strip())


def dni(s: str):
    """
    Validacion de tipo dni, acepta solo numeros o un pasaporte
    """

    return re.match(regexpr.get('dni'), s.strip())


def fecha(s: str):
    """
    Validacion de tipo fecha, espera una fecha con el separador '/'
    """
    return re.match(regexpr.get('fecha'), s.strip())


def mail(s: str):
    """
    Validacion de tipo mail, espera un mail
    """
    return re.match(regexpr.get('mail'), s.strip())
