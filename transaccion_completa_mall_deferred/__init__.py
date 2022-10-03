from flask import Blueprint


bp = Blueprint('transaccion_completa_mall_deferred', __name__)

from transaccion_completa_mall_deferred import routes
