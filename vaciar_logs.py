"""
Script para vaciar los logs
"""
import os

dir_log = os.path.join(os.getcwd(), 'log')

with os.scandir(dir_log) as dirs:
    for file in dirs:
        open(os.path.join(dir_log, file.name), 'w').close()
        print(f'Archivo {file.name} vaciado!')
