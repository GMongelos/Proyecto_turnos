"""
Aplicacion principal
"""
import os

from src.Program import Program

if __name__ == '__main__':
    try:
        p = Program()
        while True:
            p.run()
    except Exception as e:
        print('Ha ocurrido un error')
        dir_log = os.path.join(os.getcwd(), 'log')
        path_log = os.path.join(dir_log, 'errores.log')
        os.makedirs(dir_log, exist_ok=True)
        with open(path_log, 'a') as f:
            f.write(f"[ERROR]: {e}\n")
