import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()

def init_db():
    with engine.begin() as conn:
        # Base.metadata.drop_all(conn)  # WARNING: This deletes all data!
        Base.metadata.create_all(conn)

def custom_create_engine(user, password, host, port, db_name):
    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    # return create_engine(DATABASE_URL, connect_args={"check_same_thread": False, "connect_timeout": 10})
    return create_engine(DATABASE_URL, connect_args={"connect_timeout": 10})

def get_central_db():
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "root")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "sms_central")
    return custom_create_engine(
        user=user,
        password=password,
        host=host,
        port=port,
        db_name=db_name
    )       
