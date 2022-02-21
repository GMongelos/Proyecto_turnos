
class Vista:
    def __init__(self):
        self.menu_vista = {
            '1': "Agregar turno",
            '2': "Ver todos los turnos",
            '3': "Consultar y modificar turnos en particular",
            '4': "Salir de la aplicacion"
        }

    @staticmethod
    def separador(text=''):
        if text:
            print(f"\n{text}")
        print('-' * 50)
        print()

    def renderizar_menu(self):
        """Renderiza el menu en pantalla y espera un input de usuario que define lo que va a hacer"""
        for key, value in self.menu_vista.items():
            print(f'{key}. {value}')

        opcion = input("Elija una opcion: ")
        if not opcion.isdigit() or int(opcion) not in range(1, len(self.menu_vista) + 1):
            print("Opcion incorrecta, intente de nuevo")
            self.renderizar_menu()
        else:
            print()
            return opcion

    def renderizar_agregar_turno(self, validador):
        self.separador()
        datos_turno = {
            'nombre': validador.validar('texto', "Nombre del paciente: "),
            'apellido': validador.validar('texto', "Apellido del paciente: "),
            'dni': validador.validar('dni', "DNI del paciente: "),
            'fecha': validador.validar('fecha', "Fecha del turno(AAAA/MM/DD): "),
            'profesional': validador.validar('texto', "Profesional que lo atiende: "),
            'observaciones': input("Observaciones(opcional): ")
        }
        return datos_turno

    def renderizar_ver_turnos(self):
        pass

    def renderizar_modificar_turnos(self):
        pass

    def renderizar_salir_aplicacion(self):
        pass

    print = print
    # def print(self, *args, **kwargs):
    #     print(*args, **kwargs)

    def input(self, propmt='', validador=None):
        val = input(propmt)
        if validador:
            while not validador(val):
                print("El dato ingresado no es valido, intente de nuevo")
                val = input(propmt)
        return val

    def renderizar_turno(self, datos_turno):
        for count, (key, value) in enumerate(datos_turno.items(), 1):
            print(f'{count} - {key.capitalize()}: {value}')
        print(f'{len(datos_turno) + 1} - Eliminar Turno')

consola = Vista()
