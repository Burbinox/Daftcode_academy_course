from fastapi import FastAPI, Depends, HTTPException, Response, Cookie
import models
from database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from hashlib import sha256
from datetime import datetime

app = FastAPI()
app.access_tokens = []
app.secret_key = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ-trythis'


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class TextObj(BaseModel):
    id: int
    text: str


class ResponseObj(BaseModel):
    id: int
    visit_counter: int
    text: str


@app.delete('/delete_text/{id}')
def delete_text_with_given_id(id: int, db: Session = Depends(get_db), session_token: str = Cookie(None)):
    """
    endpoint which delete Text object with given id from database, allowed only for authorized users
    """
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=401, detail="Unauthorised")
    text_obj = db.query(models.Text).filter(models.Text.id == id).first()
    if text_obj is None:
        raise HTTPException(status_code=404, detail='text_not_found')
    db.delete(text_obj)
    db.commit()
    return f"text with id: {id} - deleted"


@app.post("/put_text")
def create_or_edit_text(text_obj_from_user: TextObj, db: Session = Depends(get_db), session_token: str = Cookie(None)):
    """
    endpoint which create or edit (depends if object with given id exist in database or not)
    text object in database, allowed only for authorized users

    example object:
    {
      "id": 10,
      "text": "some text you wanna stored in db"
    }
    """
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=401, detail="Unauthorised")
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
    """
    endpoint which get text with given id from the database to the user,
    works for every user (both authorized and unauthorized)

    return: dict with text or HTTPException with 401 code when text not exist
    """
    text_obj = db.query(models.Text).filter(models.Text.id == id).first()
    if text_obj is None:
        raise HTTPException(status_code=404, detail='text_not_found')
    text_obj.visit_counter = text_obj.visit_counter + 1
    db.commit()
    return ResponseObj(id=text_obj.id, visit_counter=text_obj.visit_counter,
                       text=text_obj.text)


@app.get('/login')
def create_session_via_cookie(response: Response):
    """
    endpoint witch let you be authorized, its sets cookie for your session
    """
    now = datetime.now()
    session_token = sha256(f'{app.secret_key}{now}'.encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    return "Logged correctly"
