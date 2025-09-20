"""SQLite database."""

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
