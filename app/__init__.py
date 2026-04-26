from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(
        __name__,
        template_folder='../frontend/templates',
        static_folder='../frontend/static'
    )

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-123')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///sma.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['APIFY_API_TOKEN'] = os.getenv('APIFY_API_TOKEN', '')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.auth.routes import auth
    from app.routes.dashboard import dashboard
    from app.routes.api import api
    from app.routes.cases import cases

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(cases, url_prefix='/cases')

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
