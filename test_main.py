from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest
from backend.main import app , Base, SessionLocal, engine as _engine
from backend.main import get_db
from backend.models import Base, FormData,Form

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)  # Clear the test database
    Base.metadata.create_all(bind=engine)  # Recreate the tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



def test_create_item(db_session):
    response = client.post("/submit_form/", json={"name": "Rakesh", "email":"rakeshchittala@gmail.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Rakesh"
    assert data["email"] == "rakeshchittala@gmail.com"
    


def test_get_all_items(db_session):
    item1 = Form(name="Item 1", email="Description of Item 1")
    item2 = Form(name="Item 2", email="Description of Item 2")
    db_session.add(item1)
    db_session.add(item2)
    db_session.commit()



    # Now, call the GET endpoint to fetch all items
    response = client.get("/get_details")
    assert response.status_code == 200
    data = response.json()

    # Ensure the data returned is correct
    assert len(data) == 2
    titles = {item['name'] for item in data}



def test_update_item(db_session):
    # Create an form instance to update
    item = Form(name="Item 1", email="Description of Item 1")
    db_session.add(item)
    db_session.commit()

    # Call the PUT endpoint to update the item
    response = client.put(f"/update_form/{item.id}", json={"name": "Updated Item", "email": "Updated Description"})
    assert response.status_code == 200
    data = response.json()

    # Ensure the item has been updated successfully
    assert data["name"] == "Updated Item"
    assert data["email"] == "Updated Description"
    assert data["id"] == item.id