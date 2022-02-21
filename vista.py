

class Vista:

    def __init__(self):
        self.menu_vista = {
            '1': "Agregar turno",
            '2': "Ver todos los turnos",
            '3': "Consultar y modificar turnos en particular",
            '4': "Salir de la aplicacion"
        }

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

    def renderizar_agregar_turno(self):
        pass

    def renderizar_ver_turnos(self):
        pass

    def renderizar_modificar_turnos(self):
        pass

    def renderizar_salir_aplicacion(self):
        pass
