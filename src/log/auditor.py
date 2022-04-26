from src.log.logger import Logger

auditlogger = Logger(log_filename='audit')


def audit(tipo):
    """Decorator que audita los inserts y deletes de la DB"""

    def decorator(f, *args, **kwargs):
        def wrap(*args, **kwargs):
            auditlogger.log_compuesto_iniciar(header=tipo)
            for arg in args[1::]:
                auditlogger.log_compuesto_add(repr(arg))
            auditlogger.log_compuesto_commit('-' * 50)
            return f(*args, **kwargs)

        return wrap

    return decorator
