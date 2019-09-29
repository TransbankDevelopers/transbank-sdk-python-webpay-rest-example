from flask import Flask, Blueprint, Config
import os

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from transaccion_completa import bp as transaccion_completa_bp
    app.register_blueprint(transaccion_completa_bp, url_prefix='/transaccion_completa')

    # from main.auth import bp as auth_bp
    # main.register_blueprint(auth_bp, url_prefix='/auth')

    # from main.main import bp as main_bp
    #  main.register_blueprint(main_bp)

    return app


create_app()
