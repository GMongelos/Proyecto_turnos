import re

regexpr = {
    'dni': r'^(PAS |pas )?[0-9]+$',
    'texto': r'^[^0-9]{2,}$',
    'email': r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+',
    'fecha': r'^(20\d{2})/(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])$'
}


def texto(s: str):
    return re.match(regexpr.get('texto'), s.strip())


def dni(s: str):
    return re.match(regexpr.get('dni'), s.strip())


def fecha(s: str):
    return re.match(regexpr.get('fecha'), s.strip())
