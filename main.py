from fastapi import FastAPI, Depends, status, HTTPException
import datetime
from fastapi.responses import HTMLResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import base64

app = FastAPI()
security = HTTPBasic()

app.secret_key = 'verysecrethardtobreakkeywhichhavenumbers62315231andspecialcharacters$^&$^^$*$'
app.access_session = []
app.access_token = []


@app.get("/hello", response_class=HTMLResponse)
def hello():
    today_date = datetime.date.today()
    return f"""<h1>Hello! Today date is {today_date}</h1>"""


def get_session_token(response: Response,
                      credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password,
                                              "NotSoSecurePa$$")

    if not (correct_username or correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        session_token_decode = f'{credentials.username}' \
                               f'{credentials.password}{app.secret_key}'
        session_token_bytes = session_token_decode.encode('ascii')
        base64_bytes = base64.b64encode(session_token_bytes)
        session_token = base64_bytes.decode('ascii')

        return session_token


@app.post("/login_session", status_code=201)
def login_session(response: Response,
                  session_token: str = Depends(get_session_token)):
    response.set_cookie(key="session_token",
                        value=session_token)
    app.access_session.append(session_token)

    return {"token": session_token}


@app.post("/login_token", status_code=201)
def login_token(token: str = Depends(get_session_token)):
    app.access_token.append(token)
    return {'token': token}