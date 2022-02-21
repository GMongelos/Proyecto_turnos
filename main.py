"""
Aplicacion principal
"""
import os

from src.logger import Logger
from src.program import Program

if __name__ == '__main__':
    try:
        p = Program()
        while True:
            p.run()
    except Exception as e:
        print('Ha ocurrido un error. Por favor revise el log para mas informacion.')
        logger = Logger()
        logger.loguear_error(e)
        logger.loguear_exit()
