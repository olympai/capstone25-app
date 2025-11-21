from flask import Flask
import os

# App Creator
def create_app():
    # Flask Initialisierung
    app = Flask(__name__)  
    app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")

    return app

app = create_app()