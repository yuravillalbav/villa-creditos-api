"""
Configuración básica de la base de datos para Villa Créditos API.
"""
from dotenv import load_dotenv
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

load_dotenv()

# URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/loan_requests.db")

# Crear engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith(
        "sqlite") else {}
)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Función para obtener una sesión de base de datos.
    Se usa como dependency en FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Error en base de datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()
