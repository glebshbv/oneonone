import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import create_database, drop_database, database_exists
from db.database import Base, get_db
from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv

load_dotenv()

# Read the database URL from the environment variable
DATABASE_URL = "postgresql+psycopg2://postgres@localhost/oneonone_test"

@pytest.fixture(scope="module")
def db_engine():
    # Create a test database if it doesn't exist
    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    drop_database(DATABASE_URL)

@pytest.fixture(scope="module")
def db_session(db_engine) -> Session:
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="module")
def client(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
