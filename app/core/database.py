from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
# engine = create_engine("postgresql://postgres:root@localhost/sms")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    with engine.begin() as conn:
        # Base.metadata.drop_all(conn)  # WARNING: This deletes all data!
        Base.metadata.create_all(conn)

