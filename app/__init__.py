from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config

bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
