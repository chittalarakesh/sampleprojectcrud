# controllers.py
from sqlalchemy.orm import Session
from .models import Form, FormData
from fastapi import HTTPException

class Service():

    def create_form(db: Session, form_data: FormData):
        db_form = Form(name=form_data.name, email=form_data.email)
        db.add(db_form)
        db.commit()
        db.refresh(db_form)
        print(db)
        return db_form

    def update_form(db: Session, form_id: int, form_data: FormData):
        db_form = db.query(Form).filter(Form.id == form_id).first()
        if not db_form:
            raise HTTPException(status_code=404, detail="Form not found")
        db_form.name = form_data.name
        db_form.email = form_data.email
        db.commit()
        db.refresh(db_form)
        return db_form

    def get_forms(db: Session):
        return db.query(Form).all()

    def delete_form(db: Session, form_id: int):
        db_form = db.query(Form).filter(Form.id == form_id).first()
        if not db_form:
            raise HTTPException(status_code=404, detail=f"Record with ID {form_id} not found")
        db.delete(db_form)
        db.commit()