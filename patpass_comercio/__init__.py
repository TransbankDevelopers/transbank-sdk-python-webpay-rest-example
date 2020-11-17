from flask import Blueprint

bp = Blueprint('patpass_comercio', __name__)

from patpass_comercio import routes
