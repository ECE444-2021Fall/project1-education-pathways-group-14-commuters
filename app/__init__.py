import os
from flask import Flask



def register_views(app: Flask):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

def create_app(*config_cls, **db_cls) -> Flask:
    config_cls = [
        config() if isinstance(config, type) else config for config in config_cls
    ]

    db_cls = [
         config() if isinstance(config, type) else config for config in db_cls
    ]

    app = Flask(__name__, instance_relative_config=True)

    for config in config_cls:
        app.config.from_object(config)

    #set config for db

    register_views(app)



    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    return app


app = create_app()

if __name__=="__main__":
    app.run(host='0.0.0.0')
