from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from config import Config  # Should now work



db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    
    from app.routes.auth import auth_bp
    from app.routes.assistant import assistant_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(assistant_bp)
    
    with app.app_context():
        db.create_all()
    
    return app