from flask import Flask

# other blueprints
from .playground import playground_bp

# register blueprints
def register_blueprints(app: Flask):
    # Registering all other blueprints
    app.register_blueprint(playground_bp)