# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "temporary-secret")

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app