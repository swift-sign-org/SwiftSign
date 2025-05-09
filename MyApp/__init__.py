import os
from flask_migrate import Migrate
from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
from MyApp.BackEnd.Database.ProjectDatabase import db
from MyApp.BackEnd.API_auth import api_bp
from MyApp.BackEnd.API_verify import verify_bp
from MyApp.BackEnd.routes import routes_blueprint

# Load environment variables first
load_dotenv()

# Initialize extensions outside app factory (to avoid circular imports)
migrate = Migrate()
sess = Session()

def create_app(config_class=None):
    """Application factory with optional config class"""
    app = Flask(__name__,
                static_folder='FrontEnd',
                template_folder='FrontEnd/HTML'
    )

    # Configure application
    configure_app(app, config_class)
    
    # Initialize extensions with app
    initialize_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    return app

def configure_app(app, config_class):
    """Handle application configuration"""
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'fallback_secret_key_123'),
        SESSION_TYPE='filesystem',
        SESSION_PERMANENT=False,
        SESSION_USE_SIGNER=True,
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL') if os.getenv('DATABASE_URL') else 'postgresql://postgres:password@localhost:5432/FaceRecognitionDB',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    # Optional class-based configuration
    if config_class:
        app.config.from_object(config_class)

def initialize_extensions(app):
    """Initialize Flask extensions"""
    db.init_app(app)
    sess.init_app(app)
    migrate.init_app(app, db)
    
    # Create tables if in development
    if app.config.get('DEBUG'):
        with app.app_context():
            db.create_all()

def register_blueprints(app):
    """Register Flask blueprints"""
    
    app.register_blueprint(api_bp)
    app.register_blueprint(verify_bp)
    app.register_blueprint(routes_blueprint)