from flask import Blueprint

# from transaccion_completa.transaccion_completa import TransaccionCompleta

bp = Blueprint('patpass_by_webpay', __name__)

from patpass_by_webpay import routes
