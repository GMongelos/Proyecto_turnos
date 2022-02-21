class TurnoError(Exception):
    """Clase base para excepciones de turnos"""


class CamposVaciosError(TurnoError):
    """Error cuando se intenta instanciar un turno con campos invalidos"""

    def __init__(self, campos_vacios):
        self.campos_vacios = campos_vacios
        super().__init__(f'Error, el/los campo/s {", ".join(self.campos_vacios)} no puede/n ser vacíos')
