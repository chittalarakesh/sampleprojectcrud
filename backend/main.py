 

# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, FormData
from .controller import Service
from fastapi.exceptions import HTTPException

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submit_form/")
def submit_form_endpoint(form_data: FormData, db: Session = Depends(get_db)):
    return Service.create_form(db, form_data)

@app.put("/update_form/{form_id}")
def update_form_endpoint(form_id: int, form_data: FormData, db: Session = Depends(get_db)):
    return Service.update_form(db, form_id, form_data)

@app.get("/get_details")
def get_details_endpoint(db: Session = Depends(get_db)):
    return Service.get_forms(db)

@app.delete("/delete_record/{record_id}")
def delete_record_endpoint(record_id: int, db: Session = Depends(get_db)):
    return Service.delete_form(db, record_id)