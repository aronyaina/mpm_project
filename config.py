from dotenv import load_dotenv
import os

load_dotenv()
SECRETE_KEY = os.getenv('SECRET_KEY')
BASE_DIR = os.getenv('BASE_DIR')
DEBUG = os.getenv('DEBUG')
SQL_URL = os.getenv('SQLALCHEMY_DATABASE_URI')
SQL_TRACK_MODIF = os.getenv('SQLALCHEMY_TRACK_MODIFICATION')
