"""
Script para vaciar los logs. La carpeta por defecto se llama logs, si posee otro nombre
cambiar el string en DIR_LOGS
"""
import os

DIR_LOGS = os.path.join(os.getcwd(), 'logs')

with os.scandir(DIR_LOGS) as dirs:
    for file in dirs:
        open(os.path.join(DIR_LOGS, file.name), 'w').close()
        print(f'Archivo {file.name} vaciado!')
