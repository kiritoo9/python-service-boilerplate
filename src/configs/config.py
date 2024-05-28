import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    APP_NAME:str = os.getenv("APP_NAME")
    APP_HOST:str = os.getenv("APP_HOST")
    APP_PORT:str = os.getenv("APP_PORT")
    APP_VERSION:str = os.getenv("APP_VERSION")

    DB_HOST:str = os.getenv("DB_HOST")
    DB_USER:str = os.getenv("DB_USER")
    DB_PASS:str = os.getenv("DB_PASS")
    DB_NAME:str = os.getenv("DB_NAME")
    DB_PORT:str = os.getenv("DB_PORT")
    DB_CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SECRET_KEY:str = os.getenv("SECRET_KEY")

settings = Settings()