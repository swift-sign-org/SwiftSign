from flask import Flask
from flask_cors import CORS
from BackEnd.API import api_bp
from BackEnd.routes import routes_bp
from BackEnd.Database.ProjectDatabase import db
import os
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app=app)

app.register_blueprint(api_bp, url_prefix='/')
app.register_blueprint(routes_bp, url_prefix='/')
CORS(app)

migrate = Migrate(app=app, db=db)  

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)