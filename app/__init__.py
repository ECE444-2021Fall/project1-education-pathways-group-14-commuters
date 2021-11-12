import os
from flask import Flask


def register_views(app: Flask):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

def create_app(*config_cls, **db_cls) -> Flask:
    global app

    config_cls = [
        config() if isinstance(config, type) else config for config in config_cls
    ]

    db_cls = [
         config() if isinstance(config, type) else config for config in db_cls
    ]

    app = Flask(__name__)

    for config in config_cls:
        app.config.from_object(config)

    for db_config in db_cls:
        app.config.from_object(db_config)

    register_views(app)

    return app