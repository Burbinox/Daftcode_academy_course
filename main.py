from fastapi import FastAPI, Depends, HTTPException
import models
from database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class TextObj(BaseModel):
    id: int
    text: str


@app.delete('/delete_text/{id}')
def delete_text_with_given_id(id: int, db: Session = Depends(get_db)):
    text_obj = db.query(models.Text).filter(models.Text.id == id).first()
    if text_obj is None:
        raise HTTPException(status_code=404, detail='text_not_found')
    db.delete(text_obj)
    db.commit()
    return f"text with id: {id} - deleted"


@app.post("/put_text")
def create_or_edit_text(text_obj_from_user: TextObj, db: Session = Depends(get_db)):
    text_obj_from_user = dict(text_obj_from_user)
    if len(text_obj_from_user['text']) > 160 or len(text_obj_from_user['text']) == 0:
        raise HTTPException(status_code=400, detail="text too long (more than 160 characters)")
    text_obj = db.query(models.Text).filter(models.Text.id == text_obj_from_user["id"]).first()
    if text_obj is None:
        item = models.Text(id=text_obj_from_user['id'], visit_counter=0,
                           text=text_obj_from_user['text'])
        db.add(item)
        db.commit()
        return f"text with id: {text_obj_from_user['id']} - created"
    else:
        text_obj.text = text_obj_from_user['text']
        text_obj.visit_counter = 0
        db.commit()
        return f"text with id: {text_obj_from_user['id']} - edited"


@app.get("/get_text/{id}")
def get_text_form_database(id: int, db: Session = Depends(get_db)):
    text_obj = db.query(models.Text).filter(models.Text.id == id).first()
    if text_obj is None:
        raise HTTPException(status_code=404, detail='text_not_found')
    text_obj.visit_counter = text_obj.visit_counter + 1
    db.commit()
    return db.query(models.Text).filter(models.Text.id == id).first()
