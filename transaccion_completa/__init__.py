from flask import Blueprint

bp = Blueprint('transaccion_completa', __name__)

from transaccion_completa import routes
