from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.infrastructure.core.config import settings

# SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,  # additional connections beyond pool_size
    pool_timeout=30,  # seconds to wait before giving up on getting a connection from
    # the pool
    pool_recycle=1800,  # recycle connections after 30 minutes
)

# Session factory - pravljene konekcija po zahtjevu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base klasa za modele
Base = declarative_base()
