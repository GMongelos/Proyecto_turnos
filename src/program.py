import sys
import time

from modelo import Database
from src.model.exceptions import CamposVaciosError
from src.model.turno import Turno
from src.vista import consola
from src.logger import Logger
from src.validador import texto, dni, fecha


class Program:
    def __init__(self):
        """Al inicio del programa, me conecto con la db y creo la tabla vacia si no existe"""

        self.db = Database("turnos")

        # Me conecto a la base de datos y creo la tabla
        self.con = self.db.conectar()
        self.db.crear_tabla(self.con)

        self.menu = {
            '1': ("Agregar turno", self.agregar_turno),
            '2': ("Ver todos los turnos", self.ver_turnos),
            '3': ("Consultar y modificar turnos en particular", self.modificar_turno),
            '4': ("Salir de la aplicacion", self.salir_aplicacion)
        }

    def run(self):
        """Menu principal de la aplicacion"""

        opcion = consola.renderizar_menu()
        self.menu.get(opcion)[1]()

    def agregar_turno(self):
        """Agrega un turno a la bd"""

        datos_turno = {
            'nombre': consola.input("Nombre del paciente: ", texto),
            'apellido': consola.input("Apellido del paciente: ", texto),
            'nro_dni': consola.input("DNI del paciente: ", dni),
            '_fecha': consola.input("Fecha del turno(AAAA/MM/DD): ", fecha),
            'profesional': consola.input("Profesional que lo atiende: ", texto),
            'observaciones': consola.input("Observaciones(opcional): ")
        }

        try:
            turno = Turno(**datos_turno)
        except CamposVaciosError as e:
            consola.print(e)
            self.agregar_turno()
        else:
            self.db.insertar_registro(self.con, turno)
            consola.separador("Turno agregado!")

    def ver_turnos(self):
        """Se visualizan en pantalla todos los turnos"""
        turnos = self.db.obtener_registros(self.con)

        if not turnos:
            consola.separador("Aún no hay turnos cargados")
        else:
            columnas = 'NOMBRE', 'APELLIDO', 'DNI', 'FECHA', 'PROFESIONAL', 'OBSERVACIONES'
            datos = {k: [] for k in columnas}
            for turno in turnos:
                for i, dato in enumerate(turno[1::]):
                    datos[columnas[i]].append(dato)

            consola.renderizar_tabla(title="TURNOS", cols=columnas, rows=datos)

    def modificar_turno(self):
        """Busca el ultimo turno por dni y lo modifica/elimina, según la eleccion"""

        nro_dni = consola.input("Ingrese el dni para buscar su ultimo turno: ", dni)
        datos_db = self.db.seleccionar_registro(self.con, nro_dni)

        if not datos_db:
            consola.separador("No se encontro ningun turno asociado al dni.")
        else:
            turno = Turno(*datos_db[1::])
            id_db = datos_db[0]

            menu = {n: (k, v) for n, (k, v) in enumerate(turno.__dict__.items(), 1)}
            menu[len(menu) + 1] = ("Eliminar Turno", None)

            consola.renderizar_modificar_turno(menu)
            index = consola.input("\nQue desea modificar? ")

            if int(index) == len(menu) + 1:
                # Borramos el registro de la base
                self.db.borrar_registro(self.con, turno.dni)
                consola.print("\nTurno eliminado!")
                consola.separador()
                return

            else:
                campo = menu[int(index)][0]
                validador = turno.validadores[campo]
                valor = consola.input(f"Ingrese nuevo valor para {campo.lower()}: ", validador)
                turno.update(campo, valor)

            # Actualizamos el registro
            self.db.actualizar_registro(self.con, id_db, turno)
            consola.print("\nTurno actualizado!")
            consola.separador()

    def salir_aplicacion(self):
        """Termina la ejecucion de la aplicacion"""

        consola.print("\nUsted decidio salir de la aplicacion")
        logger = Logger()
        logger.loguear_exit()
        time.sleep(3)
        self.con.close()
        sys.exit()
