from flask import Blueprint

bp = Blueprint('webpay_plus_mall_deferred', __name__)

from webpay_plus_mall_deferred import routes
