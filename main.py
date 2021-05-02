from fastapi import FastAPI, HTTPException, Response, Cookie
import base64
from typing import Optional
import datetime
from fastapi.responses import HTMLResponse

app = FastAPI()
app.access_tokens = []


@app.get("/hello", response_class=HTMLResponse)
def hello():
    today_date = datetime.date.today()
    return f"""<h1>Hello! Today date is {today_date}</h1>"""


@app.post("/login_session")
def login(response: Response, user: Optional[str] = None,
          password: Optional[str] = None):
    if user == '4dm1n' and password == 'NotSoSecurePa$$':

        session_token_uncode = f'{user}{password}dfsds'
        session_token_bytes = session_token_uncode.encode('ascii')
        base64_bytes = base64.b64encode(session_token_bytes)
        session_token = base64_bytes.decode('ascii')
        app.access_tokens.append(session_token)
        response.set_cookie(key="session_token",
                            value=session_token)
        return {'token': session_token}
    else:
        raise HTTPException(status_code=401)


@app.post("/login_token")
def create_cookie(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=401)
    else:
        return {'token': session_token}