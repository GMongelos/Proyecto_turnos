"""
Controlador
"""
import sys
import time
from typing import List

import src.orm.orm as modelo
from src.model.turno import TurnoORM

from src.model.exceptions import CamposVaciosError
from src.notify.mailer import Notificador, Mailer
from src.vista import consola
from src.log.logger import Logger
from src.validador import texto, dni, fecha, mail, validadores


class Program:
    def __init__(self, session: modelo.DBManager):
        """Al inicio del programa, me conecto con la db y creo la tabla vacia si no existe"""
        self.session = session
        self.notificador: List[Notificador] = [Mailer()]

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
            'mail': consola.input("Mail del paciente(opcional): ", mail),
            'fecha': consola.input("Fecha del turno(AAAA/MM/DD): ", fecha),
            'profesional': consola.input("Profesional que lo atiende: ", texto),
            'observaciones': consola.input("Observaciones(opcional): ")
        }

        try:
            nuevo_turno = TurnoORM(**datos_turno)
            self.session.create(nuevo_turno)
            consola.separador("Turno agregado!")

        except CamposVaciosError as e:
            consola.print(e)
            self.agregar_turno()

        else:
            for mailer in self.notificador:
                mailer.turno_nuevo(nuevo_turno)

    def ver_turnos(self):
        """Se visualizan en pantalla todos los turnos"""
        turnos = self.session.get_todos_turnos()

        if not turnos:
            consola.separador("Aún no hay turnos cargados")
        else:
            columnas = 'NOMBRE', 'APELLIDO', 'DNI', 'FECHA', 'PROFESIONAL', 'OBSERVACIONES', 'MAIL'
            datos = {k: [] for k in columnas}
            for turno in turnos:
                atrss: dict = turno[0].atrss()

                for key, value in atrss.items():
                    if key.upper() not in columnas:
                        continue
                    datos[key.upper()].append(value)

            consola.renderizar_tabla(title="TURNOS", cols=columnas, rows=datos)

    def modificar_turno(self):
        """Busca el ultimo turno por dni y lo modifica/elimina, según la eleccion"""

        nro_dni = consola.input("Ingrese el dni para buscar su ultimo turno: ", dni)
        turno = self.session.get_turnos_dni(nro_dni)

        if not turno:
            consola.separador("No se encontro ningun turno asociado al dni.")
        else:
            menu = {n: (k, v) for n, (k, v) in enumerate(turno.atrss(False).items(), 1)}
            menu[len(menu) + 1] = ("Eliminar Turno", None)

            consola.renderizar_modificar_turno(menu)
            index = consola.input("\nQue desea modificar? ")

            if int(index) == len(menu):
                # Borramos el registro de la base
                consola.print("\nTurno eliminado!")
                consola.separador()
                self.session.delete(turno)
                for mailer in self.notificador:
                    mailer.turno_borrado(turno)
                return

            else:
                campo = menu[int(index)][0]

                validador = validadores[campo]
                valor = consola.input(f"Ingrese nuevo valor para {campo.lower()}: ", validador)
                turno.update(campo, valor)

            self.session.update(turno)
            for mailer in self.notificador:
                mailer.turno_nuevo(turno)

            consola.print("\nTurno actualizado!")
            consola.separador()

    def salir_aplicacion(self):
        """Termina la ejecucion de la aplicacion"""

        consola.print("\nUsted decidio salir de la aplicacion")
        logger = Logger(log_filename='main')
        logger.loguear_exit()
        time.sleep(3)
        sys.exit()
