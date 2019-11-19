from flask import Blueprint

bp = Blueprint('oneclick', __name__)

from oneclick import routes
