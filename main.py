from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from spotify_user import login, handle_callback, refresh_access_token
from lyrics_crawler import crawling_lyrics
from datetime import datetime
from spotify_api import get_playlist
from predict_emotion import predict_emotion
from fastapi.middleware.cors import CORSMiddleware
import requests
from DB.database import engineconn
from CRUD.spotify import *
from routers.login import router as login_router
from routers.signup import router as signup_router
from routers.mainpage import router as mainpage_router
import uvicorn
engine = engineconn()
session_maker = engine.sessionmaker()


dic = {'1':''}
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # 허용할 origin을 설정하세요
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(signup_router)
app.include_router(mainpage_router)
emotion_test = ''
@app.get('/')
async def index():
    return {"message": "Hello World"}

@app.get('/callback')
async def callback(request: Request):
    return handle_callback(request)



@app.get('/refresh-token')
def refresh_token(request: Request):
    return refresh_access_token(request)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)