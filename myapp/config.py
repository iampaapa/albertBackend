from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = False

    @staticmethod
    def init_app(app):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10) # 10.24 MB
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.DEBUG)

        # Remove default Flask console handler
        app.logger.handlers = [file_handler]

        # Ensure all logs go to file
        for logger in [app.logger, logging.getLogger('werkzeug'), logging.getLogger('sqlalchemy')]:
            logger.addHandler(file_handler)
            logger.setLevel(logging.DEBUG)

        app.logger.info('Application startup')
