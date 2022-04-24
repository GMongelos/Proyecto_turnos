from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TurnoORM(Base):
    __tablename__ = "turnos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    dni = Column(String(30), nullable=False)
    mail = Column(String(30))
    fecha = Column(String(30), nullable=False)
    profesional = Column(String(30), nullable=False)
    observaciones = Column(String(30))

    modificado = False

    def __repr__(self):
        return f"Turno(id={self.id!r}, " \
               f"nombre={self.nombre!r}, " \
               f"apellido={self.apellido!r}, " \
               f"dni={self.dni!r}, " \
               f"mail={self.mail!r}, " \
               f"fecha={self.fecha!r}, " \
               f"profesional={self.profesional!r}, " \
               f"observaciones={self.observaciones!r})"

    def atrss(self, con_id=True):
        d = self.__dict__.copy()

        del (d['_sa_instance_state'])
        if not con_id:
            del (d['id'])
        return d

    def update(self, campo, valor):
        """
        Actualiza el valor de un campo
        """
        if self.__getattribute__(campo) != valor:
            self.modificado = True
        self.__setattr__(campo, valor)
