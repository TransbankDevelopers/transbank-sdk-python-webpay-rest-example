from flask import Blueprint

bp = Blueprint('oneclick_deferred', __name__)

from oneclick_deferred import routes
