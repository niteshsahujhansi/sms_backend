from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL

# engine = create_engine(DATABASE_URL)
engine = create_engine("postgresql://postgres:root@localhost/sms")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables manually since we are not using Alembic yet
# def init_db():
#     Base.metadata.create_all(bind=engine)

def init_db():
    with engine.begin() as conn:
        # Base.metadata.drop_all(conn)  # WARNING: This deletes all data!
        # Base.metadata.drop_all(engine, checkfirst=True)
        Base.metadata.create_all(conn)

# def init_db():
#     with engine.begin() as conn:
#         # Drop association table first
#         conn.execute(text("DROP TABLE IF EXISTS parent_addresses CASCADE"))
#         conn.execute(text("DROP TABLE IF EXISTS parents CASCADE"))
#         conn.execute(text("DROP TABLE IF EXISTS addresses CASCADE"))

#         # Now drop all remaining tables
#         Base.metadata.drop_all(conn)
#         Base.metadata.create_all(conn)
