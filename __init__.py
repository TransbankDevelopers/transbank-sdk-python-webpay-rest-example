from flask import Flask, Config, app, render_template
import os

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from transaccion_completa import bp as transaccion_completa_bp
    from patpass_by_webpay import bp as patpass_by_webpay_bp
    from webpay_plus import bp as webpay_plus_bp
    from webpay_plus_mall import bp as webpay_plus_mall_bp
    from transaccion_completa_mall import bp as transaccion_completa_mall_bp
    from patpass_comercio import bp as patpass_comercio_bp

    app.register_blueprint(transaccion_completa_bp, url_prefix='/fulltransaction')
    app.register_blueprint(patpass_by_webpay_bp, url_prefix='/patpass-webpay')
    app.register_blueprint(webpay_plus_bp, url_prefix="/webpay-plus")
    app.register_blueprint(webpay_plus_mall_bp, url_prefix="/webpay-plus-mall")
    app.register_blueprint(transaccion_completa_mall_bp, url_prefix='/mallfulltransaction/')
    app.register_blueprint(patpass_comercio_bp, url_prefix='/patpass-comercio')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


create_app()
