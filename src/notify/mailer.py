"""
Observador que notifica al usuario sobre los eventos asociados con el turno.

Se intentó mandar un mail personalizado con los datos del turno, pero al concatenar el mensaje no estaban enviando los
datos, ej: llegaba al mail como: "querido/a None, None. Se reservó un turno para None el Dia None...etc"
Por lo tanto dejamos mensajes fijos sin formato para los datos hasta que podamos averiguar por qué no funciona
Ademas dejamos comentadas las lineas que formateaban el mensaje con los datos del turno.
"""

from abc import abstractmethod

from src.model.turno import TurnoORM

import smtplib
import ssl

from email.mime.text import MIMEText


class Notificador:
    """
    Clase base para notificadores usados para notificar los eventos sobre un turno (Alta, Baja y Modificación)
    """

    @abstractmethod
    def turno_nuevo(self, turno: TurnoORM):
        """
        Evento triggerado cuando un turno se crea
        @param turno: Turno creado
        """
        pass

    @abstractmethod
    def turno_modificado(self, turno: TurnoORM):
        """
        Evento triggerado cuando un turno se modifica
        @param turno: Turno modificado
        """
        pass

    @abstractmethod
    def turno_borrado(self, turno: TurnoORM):
        """
        Evento triggerado cuando un turno se borra
        @param turno: Turno borrado
        """
        pass


class Mailer(Notificador):
    """Observador que notifica al usuario mediante el anvio de mails."""

    PUERTO = 465  # SSL
    SMTP_SERVER = "smtp.gmail.com"
    SENDER = "sistema.turnos.dev@gmail.com"
    PASSWORD = 'estoesunacontrasenia1234'  # Se sabe que esto esta mal, pero lo dejamos para probar(Mail descartable)

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
        """Envia un mail al paciente con las credenciales provistas como atrivutos de clase"""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.SMTP_SERVER, self.PUERTO, context=context) as server:
            server.login(self.SENDER, self.PASSWORD)
            server.sendmail(self.SENDER, mail, mensaje)

    def armar_mail(self, datos: dict, tipo):
        """Arma un mail con su header, cuarpo y footer segun el tipo"""
        texto = self.mail_header(datos)
        texto += tipo(datos)
        texto += self.mail_footer()

        message = MIMEText(texto)
        message["Subject"] = "Notificador Sistema de Turnos"
        return message.as_string()

    def mail_header(self, datos: dict):
        # return f"Querido/a {datos.get('nombre')}, {datos.get('apellido')}:\n\n"
        return "Querido/a:\n"

    def mail_footer(self):
        return "\n\nSaludos coordiales\nEquipo de Turnos"

    def cuerpo_nuevo_turno(self, datos: dict):
        # msg = "Se ha reservado un turno para la fecha {} con el profesional {}".format(datos.get('fecha'), datos.get('profesional'))
        msg = "Se ha reservado un nuevo turno"
        return msg

    def cuerpo_eliminacion_turno(self, datos: dict):
        # msg = f"""Lamentamos comunicarle que, por motivos administrativos, su turno
        # con el profesional {datos.get('profesional')} para la fecha {datos.get('fecha')} ha sido cancelado. Favor de contactarse
        # con el área administrativa para reservar otro.
        # """
        msg = "Por motivos administrativos, se ha eliminado su turno"
        return msg

    def cuerpo_modificacion_turno(self, datos: dict):
        # msg = f"""Queremos comunicarle que, por motivos administrativos, su turno se ha modificado:
        # -profesional: {datos.get('profesional')}
        # -fecha {datos.get('fecha')}
        # -nombre paciente: {datos.get('nombre')}
        # -apellido paciente: {datos.get('apellido')}
        # -dni paciente: {datos.get('dni')}
        # \n\nFavor de contactarse con el área administrativa por cualquier inquietud al respecto.
        # """
        msg = "Se ha modificado un turno que había reservado"
        return msg
