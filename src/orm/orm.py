"""
Conexion a la base de datos
"""

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.model.turno import Base, TurnoORM
from src.log.auditor import audit

DB_NAME = 'baseturnos'

engine = create_engine(f"sqlite:///{DB_NAME}.db", echo=False, future=True)
Base.metadata.create_all(engine)

class DBManager:
    def __init__(self, session: Session):
        self.session = session

    @audit('DELETES')
    def delete(self, *objs):
        for obj in objs:
            self.session.delete(obj)
        self.session.commit()

    @audit('UPDATE')
    def update(self, *objs):
        self.session.add_all(objs)
        self.session.commit()

    @audit('CREATE')
    def create(self, *objs):
        self.session.add_all(objs)
        self.session.commit()

    def get_todos_turnos(self):
        consulta = select(TurnoORM).order_by(TurnoORM.fecha.desc())
        return self.session.execute(consulta).all()

    def get_turnos_dni(self, dni):
        consulta = select(TurnoORM).where(TurnoORM.dni == dni).order_by(TurnoORM.fecha.desc())

        dato = self.session.execute(consulta).first()[0]
        return dato
