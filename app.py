import os
from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
from BackEnd.API import api_bp
from BackEnd.routes import routes_blueprint
from flask_migrate import Migrate
from BackEnd.Database.ProjectDatabase import db

load_dotenv()

app = Flask(__name__,
            static_folder='FrontEnd',  # Serve static files (CSS, JS, images) from FrontEnd
            template_folder='FrontEnd/HTML' # Look for templates (HTML) in FrontEnd/HTML
            )

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_secret_key_123') # Use environment variable or fallback
app.config['SESSION_TYPE'] = 'filesystem' # Store session data in the filesystem
app.config['SESSION_PERMANENT'] = False # Session expires when browser closes
app.config['SESSION_USE_SIGNER'] = True # Encrypt session cookie
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Session
Session(app)

# Initialize database
db.init_app(app=app)

# Register Blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(routes_blueprint)

# Initialize Flask-Migrate
migrate = Migrate(app=app, db=db)

if __name__ == '__main__':
    # Ensure instance folder exists for database and sessions if needed elsewhere
    try:
        os.makedirs(app.instance_path)
        os.makedirs(os.path.join(app.instance_path, 'flask_session')) # Create default session dir if filesystem is used
    except OSError:
        pass
    with app.app_context():
        db.create_all()
    app.run(debug=True) # Enable debug mode for development