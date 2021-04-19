from fastapi import FastAPI, HTTPException, Response
from typing import Optional
from pydantic import BaseModel
import hashlib
import datetime

app = FastAPI()
app.counter = 0
app.patient_id = 0
app.patients = []


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


@app.post('/register', status_code=201)
def register(patient: Patient):
    app.patient_id += 1
    register_date = datetime.date.today()
    name_and_surname_sum = len(get_only_letters(patient.name)) + len(get_only_letters(patient.surname))
    vaccination_date = register_date + datetime.timedelta(days=name_and_surname_sum)
    registered_patient_data = {
        "id": app.patient_id,
        "name": patient.name,
        "surname": patient.surname,
        "register_date": str(register_date),
        "vaccination_date": str(vaccination_date)
    }
    app.patients.append(registered_patient_data)
    return registered_patient_data


@app.get("/patient/{id}")
def get_patient_by_id(id: int):
    if id < 1:
        raise HTTPException(status_code=400)
    for patient in app.patients:
        if patient['id'] == id:
            return patient
    raise HTTPException(status_code=404)


def get_only_letters(name):
    final_name = ''.join([elem for elem in name if elem.isalpha()])
    return final_name
