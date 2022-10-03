from flask import Blueprint

bp = Blueprint('transaccion_completa_deferred', __name__)

from transaccion_completa_deferred import routes