"""
Aplicacion principal
"""

from src.logger import Logger
from src.program import Program
from src.orm.orm import session

if __name__ == '__main__':
    try:
        with session:
            p = Program(session)
            while True:
                p.run()
    except Exception as e:
        print('Ha ocurrido un error. Por favor revise el log para mas informacion.')
        logger = Logger(log_filename='main')
        logger.loguear_exepcion(e)
        logger.loguear_exit()
