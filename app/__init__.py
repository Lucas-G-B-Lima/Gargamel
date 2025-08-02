# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv('.env')
print(f"Valor de DATABASE_URL lido do .env: {os.getenv('DATABASE_URL')}")

app = Flask(__name__, static_folder='static') # Adicione instance_relative_config=True


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.views import home_login
from app.models import UserLogin, UserDados, UserBJJ