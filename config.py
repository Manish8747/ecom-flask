import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
