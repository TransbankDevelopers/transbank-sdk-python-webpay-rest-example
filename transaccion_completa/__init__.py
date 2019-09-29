from flask import Blueprint

# from transaccion_completa.transaccion_completa import TransaccionCompleta

bp = Blueprint('transaccion_completa', __name__)

from transaccion_completa import routes
