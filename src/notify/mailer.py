from abc import abstractmethod

from src.model.turno import TurnoORM

import smtplib
import ssl

from email.mime.text import MIMEText

PUERTO = 465  # SSL
SMTP_SERVER = "smtp.gmail.com"
SENDER = "sistema.turnos.dev@gmail.com"
PASSWORD = 'estoesunacontrasenia1234'


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
        mensaje = self.armar_mail(turno.atrss(), self.cuerpo_nuevo_turno)
        self.enviar_mail(turno.mail, mensaje)

    def turno_modificado(self, turno: TurnoORM):
        mensaje = self.armar_mail(turno.atrss(), self.cuerpo_modificacion_turno)
        self.enviar_mail(turno.mail, mensaje)

    def turno_borrado(self, turno: TurnoORM):
        mensaje = self.armar_mail(turno.atrss(), self.cuerpo_eliminacion_turno)
        self.enviar_mail(turno.mail, mensaje)

    def enviar_mail(self, mail, mensaje):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, PUERTO, context=context) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, mail, mensaje)

    def armar_mail(self, datos: dict, tipo):
        texto = self.mail_header(datos)
        texto += tipo(datos)
        texto += self.mail_footer()

        message = MIMEText(texto)
        message["Subject"] = "Notificador Sistema de Turnos"
        return message.as_string()

    def mail_header(self, datos: dict):
        return f"Querido/a {datos.get('nombre')}, {datos.get('apellido')}:\n\n"

    def mail_footer(self):
        return "\n\nSaludos coordiales\nEquipo de pitón"

    def cuerpo_nuevo_turno(self, datos: dict):
        msg = f"Se ha reservado un turno para la fecha {datos.get('fecha')} con el profesional {datos.get('profesional')}"
        return msg

    def cuerpo_eliminacion_turno(datos: dict):
        msg = f"""Lamentamos comunicarle que, por motivos administrativos, su turno 
        con el profesional {datos.get('profesional')} para la fecha {datos.get('fecha')} ha sido cancelado. Favor de contactarse
        con el área administrativa para reservar otro.
        """
        return msg

    def cuerpo_modificacion_turno(datos: dict):
        msg = f"""Queremos comunicarle que, por motivos administrativos, su turno se ha modificado:
        -profesional: {datos.get('profesional')}
        -fecha {datos.get('fecha')}
        -nombre paciente: {datos.get('nombre')}
        -apellido paciente: {datos.get('apellido')}
        -dni paciente: {datos.get('dni')}
        \n\nFavor de contactarse con el área administrativa por cualquier inquietud al respecto.
        """
        return msg
