from fastapi import FastAPI, Depends, status, HTTPException, Cookie
import datetime
from fastapi.responses import HTMLResponse, Response, PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from hashlib import sha256
from time import time
from starlette.responses import RedirectResponse

app = FastAPI()
security = HTTPBasic()

app.secret_key = 'verysecrethardtobreakkeywhichhavenumbers62315231andspecialcharacters$^&$^^$*$'
app.access_session = []
app.access_token = []


@app.get("/hello", response_class=HTMLResponse)
def hello():
    today_date = datetime.date.today()
    return f"""<h1>Hello! Today date is {today_date}</h1>"""


def get_session_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username or correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    else:
        time_now = time()
        session_token = sha256(f"{credentials.username}{credentials.password}"
                               f"{app.secret_key}{time_now}".encode()).hexdigest()
        return session_token


@app.post("/login_session", status_code=201)
def login_session(response: Response, session_token: str = Depends(get_session_token)):
    response.set_cookie(key="session_token", value=session_token)
    app.access_session.append(session_token)
    return {"token": session_token}


@app.post("/login_token", status_code=201)
def login_token(token: str = Depends(get_session_token)):
    app.access_token.append(token)
    return {'token': token}


@app.get("/welcome_session")
def welcome_session(format: str = "", session_token: str = Cookie(None)):
    if session_token not in app.access_session or session_token == '':
        raise HTTPException(status_code=401, detail="Unauthorised")
    else:
        if format == 'json':
            return {"message": 'Welcome!'}
        elif format == 'html':
            return HTMLResponse(content="<h1>Welcome!</h1>", status_code=200)
        else:
            return PlainTextResponse(content="Welcome!", status_code=200)


@app.get("/welcome_token")
def welcome_token(token: str = "", format: str = ""):
    if token not in app.access_token or token == '':
        raise HTTPException(status_code=401, detail="Unauthorised")
    else:
        if format == 'json':
            return {"message": 'Welcome!'}
        elif format == 'html':
            return HTMLResponse(content="<h1>Welcome!</h1>", status_code=200)
        else:
            return PlainTextResponse(content="Welcome!", status_code=200)


@app.delete("/logout_session")
def logout_session(format: str = "", session_token: str = Cookie(None)):
    if session_token not in app.access_session or session_token == '':
        raise HTTPException(status_code=401, detail="Unauthorised")
    app.access_session.remove(session_token)
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=status.HTTP_302_FOUND)


@app.delete("/logout_token")
def logout_token(token: str = "", format: str = ""):
    if token not in app.access_token or token == '':
        raise HTTPException(status_code=401, detail="Unauthorised")
    app.access_token.remove(token)
    return RedirectResponse(url=f"/logged_out?format={format}", status_code=status.HTTP_302_FOUND)


@app.get("/logged_out")
def logged_out(format: str = ""):
    if format == 'json':
        return {"message": "Logged out!"}
    elif format == 'html':
        return HTMLResponse(content="<h1>Logged out!</h1>", status_code=200)
    else:
        return PlainTextResponse(content="Logged out!", status_code=200)
