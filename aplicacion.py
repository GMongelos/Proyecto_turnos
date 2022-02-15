"""
Aplicacion principal
"""
import sys
import re
import time
import conexion


def menu_principal():
    """Menu principal de la aplicacion"""

    for key, value in menu.items():
        print(f'{key}. {value[0]}')

    opcion = input("Elija una opcion: ")
    if not opcion.isdigit() or int(opcion) not in range(1, len(menu)+1):
        print("opcion incorrecta, intente de nuevo")
    else:
        print()
        menu.get(opcion)[1]()


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
    print('-'*50)
    print()


def agregar_turno():
    """Agrega un turno a la bd"""

    separador()
    datos_turno = {}
    datos_turno['nombre'] = input("Nombre del paciente: ")
    datos_turno['apellido'] = input("Apellido del paciente: ")
    datos_turno['dni'] = validar_input_dni()
    datos_turno['fecha'] = input("Fecha del turno(AAAA/MM/DD): ")
    datos_turno['profesional'] = input("Profesional que lo atiende: ")
    datos_turno['observaciones'] = input("Observaciones(opcional): ")

    # Controla que los campos esenciales no esten vacios
    campos_escenciales = [k for k in datos_turno.keys() if k != 'observaciones']
    campos_vacios = [k for k in campos_escenciales if not datos_turno[k].strip()]

    if campos_vacios:
        print(f'Error, el/los campo/s {", ".join(campos_vacios)} no puede/n ser vacíos')
        agregar_turno()

    # Insertamos el turno en la base
    cursor = con.cursor()
    cursor.execute("""INSERT INTO turnos (nombre, apellido, dni, fecha, profesional, observaciones)
                        VALUES(:nombre, :apellido, :dni, :fecha, :profesional, :observaciones)""", datos_turno)
    con.commit()
    separador("Turno agregado!")


def ver_turnos():
    """Se visualizan en pantalla todos los turnos"""

    cursor = con.cursor()
    cursor.execute("SELECT * FROM turnos ORDER BY fecha DESC")

    turnos = cursor.fetchall()

    if not turnos:
        separador("Aun no hay turnos cargados")
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
        separador()


def update_string():
    return "SET " + ', '.join(["nombre =:nombre", "apellido =:apellido", "dni =:dni",
    "fecha =:fecha", "profesional =:profesional", "observaciones =:observaciones"])


def modificar_turno():
    """Busca el ultimo turno por dni y lo modifica/elimina, según la eleccion"""

    dni = input("Ingrese el dni para buscar su ultimo turno: ")

    cursor = con.cursor()
    cursor.execute("SELECT * FROM turnos WHERE dni = :dni ORDER BY fecha", {'dni': dni})

    turno_dni = cursor.fetchone()

    if not turno_dni:
        separador("No se encontro ningun turno asociado al dni.")
    else:
        datos_turno = dict(zip(('nombre', 'apellido', 'dni', 'fecha', 'profesional', 'observaciones'), turno_dni[1::]))
        print("\nTurno encontrado:")
        # count = 1
        for count, (key, value) in enumerate(datos_turno.items(), 1):
            print(f'{count} - {key.capitalize()}: {value}')
        print(f'{len(datos_turno) + 1} - Eliminar Turno')

        index = input("\nQue desea modificar? ")

        if index == len(datos_turno) + 1:
            cursor.execute("DELETE FROM turnos WHERE id=:id", {'id': turno_dni[0]})
            con.commit()
            print("\nTurno eliminado!")
            return

        if index == '3':
            valor = validar_input_dni()
        else:
            valor = input("Ingrese el nuevo valor: ")

        lista_aux = list(datos_turno.values())
        lista_aux[int(index) - 1] = valor

        datos_turno.update(zip(datos_turno, lista_aux))
        datos_turno['id'] = turno_dni[0]

        cursor.execute(f'UPDATE turnos {update_string()} WHERE id=:id', datos_turno)
        con.commit()
        print("\nTurno actualizado!")
        separador()

def salir_aplicacion():
    """Termina la ejecucion de la aplicacion"""

    print("\nUsted decidio salir de la aplicacion")
    time.sleep(3)
    con.close()
    sys.exit()

# Declaracion del menu principal
menu = {
    '1': ("Agregar turno", agregar_turno),
    '2': ("Ver todos los turnos", ver_turnos),
    '3': ("Consultar y modificar turnos en particular", modificar_turno),
    '4': ("Salir de la aplicacion", salir_aplicacion)
}

while True:
    con = conexion.conectar()
    conexion.crear_tabla(con)
    menu_principal()
