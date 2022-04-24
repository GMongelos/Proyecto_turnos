"""
Aplicacion principal
"""

from src.log.logger import Logger
from src.controller import Program
from src.orm.orm import Session, engine, DBManager

if __name__ == '__main__':
    try:
        with Session(engine) as session:
            manager = DBManager(session)
            p = Program(manager)
            while True:
                p.run()
    except Exception as e:
        print('Ha ocurrido un error. Por favor revise el log para mas informacion.')
        logger = Logger(log_filename='main')
        logger.loguear_exepcion(e)
        logger.loguear_exit()
