from fastapi import FastAPI, HTTPException, Response
from typing import Optional
from pydantic import BaseModel
import hashlib

app = FastAPI()
app.counter = 0


class HelloResp(BaseModel):
    msg: str


class Patient(BaseModel):
    name: str
    surname: str


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/hello/{name}", response_model=HelloResp)
def hello_name_view(name: str):
    return HelloResp(msg=f"Hello {name}")


@app.get('/counter')
def counter():
    app.counter += 1
    return app.counter


@app.get('/method')
def method_get():
    return {"method": "GET"}


@app.post('/method', status_code=201)
def method_post():
    return {"method": "POST"}


@app.delete('/method')
def method_delete():
    return {"method": "DELETE"}


@app.put('/method')
def method_put():
    return {"method": "PUT"}


@app.options('/method')
def method_options():
    return {"method": "OPTIONS"}


@app.get('/auth', status_code=204)
def auth(password: Optional[str] = None, password_hash: Optional[str] = None):
    if not password or not password_hash or hashlib.sha512(str.encode(password)).hexdigest() != str(password_hash):
        raise HTTPException(status_code=401)


# @app.post('/register')
# def register(patient: Patient):
#     print(dict(patient))
