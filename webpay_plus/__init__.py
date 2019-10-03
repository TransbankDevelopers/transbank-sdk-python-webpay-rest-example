from flask import Blueprint

bp = Blueprint('webpay_plus', __name__)

from webpay_plus import routes
