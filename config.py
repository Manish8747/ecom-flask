import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = 'sqlite:///ecom.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "superjwtsecretkey"
