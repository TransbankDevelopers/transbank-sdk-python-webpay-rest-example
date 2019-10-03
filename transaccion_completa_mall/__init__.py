from flask import Blueprint

# from transaccion_completa.transaccion_completa import TransaccionCompleta

bp = Blueprint('transaccion_completa_mall', __name__)

from transaccion_completa_mall import routes
