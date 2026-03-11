from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings import settings

engine = create_engine(settings.sql_alchemy_connection_url)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
