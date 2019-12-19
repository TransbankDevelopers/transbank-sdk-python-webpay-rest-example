from flask import Flask, Config, app, render_template
import os

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from transaccion_completa import bp as transaccion_completa_bp

    from oneclick import bp as oneclick_bp

    app.register_blueprint(transaccion_completa_bp, url_prefix='/fulltransaction')
    app.register_blueprint(oneclick_bp, url_prefix='/oneclick-mall')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


create_app()
