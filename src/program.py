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
            'dni': consola.input("DNI del paciente: ", dni),
            'fecha': consola.input("Fecha del turno(AAAA/MM/DD): ", fecha),
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
        turno_dni = self.db.seleccionar_registro(self.con, nro_dni)

        if not turno_dni:
            consola.separador("No se encontro ningun turno asociado al dni.")
        else:
            datos_turno = dict(
                zip(('nombre', 'apellido', 'dni', 'fecha', 'profesional', 'observaciones'), turno_dni[1::]))
            print("\nTurno encontrado:")
            # count = 1

            consola.renderizar_turno(datos_turno)
            index = consola.input("\nQue desea modificar? ")

            if int(index) == len(datos_turno) + 1:
                # Borramos el registro de la base
                self.db.borrar_registro(self.con, turno_dni[0])
                consola.print("\nTurno eliminado!")
                consola.separador()
                return

            # Si quiere modificar el dni validamos su input. TODO: validar inputs para el resto de los campos
            if index == '3':
                # validador = Utils.ValidadorInput()
                valor = consola.input("Ingrese el nuevo dni:", dni)  #validador.validar('dni', "Ingrese el nuevo dni:")
            else:
                valor = consola.input("Ingrese el nuevo valor: ")

            # Armamos el registro para actualizarlo en la db
            lista_aux = list(datos_turno.values())
            lista_aux[int(index) - 1] = valor

            datos_turno.update(zip(datos_turno, lista_aux))
            datos_turno['id'] = turno_dni[0]

            # Actualizamos el registro
            self.db.actualizar_registro(self.con, datos_turno)
            print("\nTurno actualizado!")
            consola.separador()

    def salir_aplicacion(self):
        """Termina la ejecucion de la aplicacion"""

        consola.print("\nUsted decidio salir de la aplicacion")
        logger = Logger()
        logger.loguear_exit()
        time.sleep(3)
        self.con.close()
        sys.exit()
