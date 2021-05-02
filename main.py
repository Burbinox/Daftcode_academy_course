from fastapi import FastAPI, HTTPException, Response, Cookie
import hashlib
import datetime
from fastapi.responses import HTMLResponse
from typing import Optional

app = FastAPI()
app.access_tokens = []


@app.get("/hello", response_class=HTMLResponse)
def hello():
    today_date = datetime.date.today()
    return f"""<h1>Hello! Today date is {today_date}</h1>"""


@app.post("/login_session")
def login_session(login: str, password: str, response: Response):
    if login == "4dm1n" and password == "NotSoSecurePa$$":
        session_token = hashlib.sha256(f"{login}{password}".encode()).hexdigest()
        response.set_cookie(key="session_token", value=session_token)
    else:
        raise HTTPException(status_code=401)


@app.post("/login_token")
def login_token(login: Optional[str], password: Optional[str], response: Response):
    if login == "4dm1n" and password == "NotSoSecurePa$$":
        session_token = hashlib.sha256(f"{login}{password}".encode()).hexdigest()
        app.access_tokens.append(session_token)
        response.set_cookie(key="session_token", value=session_token)
        return session_token
    else:
        raise HTTPException(status_code=401)


@app.post("/login_token")
def create_cookie(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=401)
    else:
        return {'token': session_token}
