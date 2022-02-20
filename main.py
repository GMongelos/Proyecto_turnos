"""
Aplicacion principal
"""
import os
from src.Utils import Logger

from src.Program import Program

if __name__ == '__main__':
    try:
        p = Program()
        while True:
            p.run()
    except Exception as e:
        print('Ha ocurrido un error. Por favor revise el log para mas informacion.')
        obj_logger = Logger()
        obj_logger.loguear_error(e)
