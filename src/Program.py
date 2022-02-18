import sys
import time

import conexion
import src.Utils as Utils


class Program:
    def __init__(self):
        self.con = conexion.conectar()
        conexion.crear_tabla(self.con)

        self.menu = {
            '1': ("Agregar turno", self.agregar_turno),
            '2': ("Ver todos los turnos", self.ver_turnos),
            '3': ("Consultar y modificar turnos en particular", self.modificar_turno),
            '4': ("Salir de la aplicacion", self.salir_aplicacion)
        }

    def run(self):
        """Menu principal de la aplicacion"""

        for key, value in self.menu.items():
            print(f'{key}. {value[0]}')

        opcion = input("Elija una opcion: ")
        if not opcion.isdigit() or int(opcion) not in range(1, len(self.menu) + 1):
            print("Opcion incorrecta, intente de nuevo")
        else:
            print()
            self.menu.get(opcion)[1]()
        # menu_principal()

    def agregar_turno(self):
        """Agrega un turno a la bd"""

        Utils.separador()
        datos_turno = {
            'nombre': Utils.validar_input('texto', "Nombre del paciente: "),
            'apellido': Utils.validar_input('texto', "Apellido del paciente: "),
            'dni': Utils.validar_input('dni', "DNI del paciente: "),
            'fecha': Utils.validar_input('fecha', "Fecha del turno(AAAA/MM/DD): "),
            'profesional': Utils.validar_input('texto', "Profesional que lo atiende: "),
            'observaciones': input("Observaciones(opcional): ")
        }

        # Controla que los campos esenciales no esten vacios
        campos_escenciales = [k for k in datos_turno.keys() if k != 'observaciones']
        campos_vacios = [k for k in campos_escenciales if not datos_turno[k].strip()]

        if campos_vacios:
            print(f'Error, el/los campo/s {", ".join(campos_vacios)} no puede/n ser vacíos')
            self.agregar_turno()

        # Insertamos el turno en la base
        cursor = self.con.cursor()
        cursor.execute("""INSERT INTO turnos (nombre, apellido, dni, fecha, profesional, observaciones)
                            VALUES(:nombre, :apellido, :dni, :fecha, :profesional, :observaciones)""", datos_turno)
        self.con.commit()
        Utils.separador("Turno agregado!")

    def ver_turnos(self):
        """Se visualizan en pantalla todos los turnos"""

        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM turnos ORDER BY fecha DESC")

        turnos = cursor.fetchall()

        if not turnos:
            Utils.separador("Aun no hay turnos cargados")
        else:
            print("TURNOS:")
            columnas = 'NOMBRE', 'APELLIDO', 'DNI', 'FECHA', 'PROFESIONAL', 'OBSERVACIONES'
            datos = {k: [] for k in columnas}
            for turno in turnos:
                for i, dato in enumerate(turno[1::]):
                    datos[columnas[i]].append(dato)

            # versión one line
            # anchos = {col: max(max(len(value) for value in values), len(col)) for col, values in datos.items()}
            anchos = {k: [] for k in columnas}
            for columna, valores in datos.items():
                largos = [len(v) for v in valores]
                mas_largo = max(largos)
                largo_encabezado = len(columna)
                ancho = max(mas_largo, largo_encabezado) + 5
                anchos[columna] = ancho

            print(''.join([k.ljust(v) for k, v in anchos.items()]))
            for i in range(len(datos['NOMBRE'])):
                fila = []
                for columna in columnas:
                    fila.append(datos[columna][i].ljust(anchos[columna]))
                print(''.join(fila))
            Utils.separador()

    def modificar_turno(self):
        """Busca el ultimo turno por dni y lo modifica/elimina, según la eleccion"""

        dni = input("Ingrese el dni para buscar su ultimo turno: ")

        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM turnos WHERE dni = :dni ORDER BY fecha", {'dni': dni})

        turno_dni = cursor.fetchone()

        if not turno_dni:
            Utils.separador("No se encontro ningun turno asociado al dni.")
        else:
            datos_turno = dict(
                zip(('nombre', 'apellido', 'dni', 'fecha', 'profesional', 'observaciones'), turno_dni[1::]))
            print("\nTurno encontrado:")
            # count = 1
            for count, (key, value) in enumerate(datos_turno.items(), 1):
                print(f'{count} - {key.capitalize()}: {value}')
            print(f'{len(datos_turno) + 1} - Eliminar Turno')

            index = input("\nQue desea modificar? ")

            if int(index) == len(datos_turno) + 1:
                cursor.execute("DELETE FROM turnos WHERE id=:id", {'id': turno_dni[0]})
                self.con.commit()
                print("\nTurno eliminado!")
                return

            if index == '3':
                valor = Utils.validar_input_dni()
            else:
                valor = input("Ingrese el nuevo valor: ")

            lista_aux = list(datos_turno.values())
            lista_aux[int(index) - 1] = valor

            datos_turno.update(zip(datos_turno, lista_aux))
            datos_turno['id'] = turno_dni[0]

            cursor.execute(f'UPDATE turnos {Utils.update_string()} WHERE id=:id', datos_turno)
            self.con.commit()
            print("\nTurno actualizado!")
            Utils.separador()

    def salir_aplicacion(self):
        """Termina la ejecucion de la aplicacion"""

        print("\nUsted decidio salir de la aplicacion")
        time.sleep(3)
        self.con.close()
        sys.exit()
