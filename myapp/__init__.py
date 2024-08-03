from flask import Flask
from flask_cors import CORS
from .config import Config
from .models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    db.init_app(app)
    CORS(app)

    from .routes import route, init_keep_alive
    app.register_blueprint(route, url_prefix='/route')
    init_keep_alive()

    return app
