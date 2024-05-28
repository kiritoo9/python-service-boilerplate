from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.configs.config import settings
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = settings.DB_CONNECTION_STRING
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

DB_SESSION = sessionmaker(autocommit=False, autoflush=False, bind=engine)