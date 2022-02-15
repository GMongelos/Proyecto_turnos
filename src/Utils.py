import re


def validar_input_dni():
    """Valida el input de un dni con regex"""
    valido = False
    while not valido:
        dni = input("DNI del paciente: ")
        # Utilizo regex para verificar si ingreso un dni valido
        if not re.match("^[0-9]+$", dni):
            print("El dni ingresado no es valido, intente de nuevo")
        else:
            return dni


def separador(text=''):
    if text:
        print(f"\n{text}")
    print('-' * 50)
    print()


def update_string():
    return "SET " + ', '.join(["nombre =:nombre", "apellido =:apellido", "dni =:dni",
                               "fecha =:fecha", "profesional =:profesional", "observaciones =:observaciones"])


