from abc import abstractmethod

from src.model.turno import TurnoORM


class Notificador:

    @abstractmethod
    def turno_nuevo(self, turno: TurnoORM):
        pass

    @abstractmethod
    def turno_modificado(self, turno: TurnoORM):
        pass

    @abstractmethod
    def turno_borrado(self, turno: TurnoORM):
        pass


class Mailer(Notificador):
    def turno_nuevo(self, turno: TurnoORM):
        pass

    def turno_modificado(self, turno: TurnoORM):
        pass

    def turno_borrado(self, turno: TurnoORM):
        pass