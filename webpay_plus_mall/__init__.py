from flask import Blueprint

bp = Blueprint('webpay_plus_mall', __name__)

from webpay_plus_mall import routes
