from fastapi import FastAPI, HTTPException, Response, Depends, status, Cookie
from hashlib import sha512
import datetime
from fastapi.responses import HTMLResponse
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
app.access_tokens = []
security = HTTPBasic()


@app.get("/hello", response_class=HTMLResponse)
def hello():
    today_date = datetime.date.today()
    return f"""<h1>Hello! Today date is {today_date}</h1>"""


def get_current_username(response: Response,
                         credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")

    if not (correct_username or correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        session_token = sha512(f'{credentials.username}{credentials.password}12312'.encode()).hexdigest()
        app.access_tokens = session_token
        response.set_cookie(key="session_token", value=session_token)
    return credentials.username


@app.post("/login_session", status_code=201)
def login_session(username: str = Depends(get_current_username)):
    return {'ok'}


@app.post("/login_token")
def create_cookie(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=401)
    else:
        return {'token': session_token}