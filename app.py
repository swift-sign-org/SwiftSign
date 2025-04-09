from flask import Flask
from flask_cors import CORS
from BackEnd.API import api_bp
from BackEnd.routes import routes_bp

app = Flask(__name__)


app.register_blueprint(api_bp, url_prefix='/')
app.register_blueprint(routes_bp, url_prefix='/')
CORS(app)

