from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__, static_folder='static')

database_url = os.environ.get('DATABASE_URL') or os.getenv('DATABASE_URI')

# Força o SQLAlchemy a usar o driver psycopg2 explicitamente para PostgreSQL
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql+psycopg2://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.views import home_login
from app.models import UserLogin, UserDados, UserBJJ