from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USER = "myusername"
PASSWORD = "mypassword"
HOST = "mydbinstance.abcdefg123456.us-west-2.rds.amazonaws.com"
PORT = "5432"
DATABASE = "mydatabase"

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

async def get_db():
    """
    Dependencies to provide a SQLAlchemy AsyncSession instance for database operations.

    Yields:
        AsyncSession: An instance of AsyncSession for database interaction.
    """
    async with SessionLocal() as session:
        yield session
