from fastapi import FastAPI, HTTPException, Response
import hashlib
import datetime
from fastapi.responses import HTMLResponse

app = FastAPI()
app.secret_key = "bardzotrudnehaslodozlamaniaktorezawieraduzoznakowcyfr13412341spacji    iznakowspecjalnych#%^&$&$*%"
app.access_tokens = []


@app.get("/hello", response_class=HTMLResponse)
def hello():
    today_date = datetime.date.today()
    return f"""<h1>Hello! Today date is {today_date}</h1>"""


@app.post("/login_session")
def login_session(login: str, password: str, response: Response):
    if login == "4dm1n" and password == "NotSoSecurePa$$":
        session_token = hashlib.sha256(f"{login}{password}{app.secret_key}".encode()).hexdigest()
        app.access_tokens.append(session_token)
        response.set_cookie(key="session_token", value="raz_dwa_trzyaaa")
    else:
        raise HTTPException(status_code=401)


@app.post("/login_token")
def login_token(login: str, password: str, response: Response):
    if login == "4dm1n" and password == "NotSoSecurePa$$":
        session_token = hashlib.sha256(f"{login}{password}{app.secret_key}".encode()).hexdigest()
        app.access_tokens.append(session_token)
        response.set_cookie(key="session_token", value="raz_dwa_trzyaaa")
        return {"token": session_token}
    else:
        raise HTTPException(status_code=401)
