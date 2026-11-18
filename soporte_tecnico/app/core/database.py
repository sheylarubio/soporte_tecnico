from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# echo=True solo en desarrollo para ver las consultas SQL
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,      # evita conexiones "muertas"
    pool_recycle=3600,       # recicla conexiones cada hora
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()