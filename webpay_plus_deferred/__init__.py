from flask import Blueprint

bp = Blueprint('webpay_plus_deferred', __name__)

from webpay_plus_deferred import routes
