from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import requests
import os
import random
from typing import Optional
app = FastAPI()
templates = Jinja2Templates(directory="my_app/templates")
load_dotenv("./.env", verbose=True)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

@app.get(path="/", response_class=HTMLResponse)
def read_root(request: Request):

    return templates.TemplateResponse("index.html", {"request": request, "name": "FastAPI"})


@app.get(path="/oauth/naver", response_class=HTMLResponse)
def oauth_naver(request: Request):
    state = str(random.getrandbits(130))
    url = f'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri=http://localhost:8000/main&state={state}'
    return RedirectResponse(url=url)

@app.get(path="/main", response_class=HTMLResponse)
def main(request: Request, code: Optional[str]):
    url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}"
    response = requests.get(url)
    token = response.json()
    token["request"] = request
    return templates.TemplateResponse("main.html", context=token)
