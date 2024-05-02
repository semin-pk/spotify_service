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
emotion_test = ''
@app.get('/')
async def index():
    return {"message": "Hello World"}

@app.get('/{user_id}/login')
async def login_route(request: Request, user_id: str):
    return login(request)

@app.get('/callback')
async def callback(request: Request):
    return handle_callback(request)

@app.get('/{user_id}/me')
async def get_emotion(request: Request):
    try:
        session = request.session
        print(session)
        if 'access_token' not in session:
            return refresh_access_token(request)
        if datetime.now().timestamp() > session['expires_at']:
            return refresh_access_token(request)
        
        audio_names = get_playlist(session['access_token'])
        lyrics_list = crawling_lyrics(audio_names)
        emotion=predict_emotion(lyrics_list)
        dic['1'] = emotion
        print(dic['1'])
        session['emotion'] = emotion
        print(session)
        return JSONResponse(session['emotion'])
    except Exception:
        error = '연동실패!'
        return JSONResponse(error)
@app.get('/emotion')
async def send_emotion():
    print(dic['1'])
    
    return JSONResponse(dic['1'])

@app.get('/refresh-token')
def refresh_token(request: Request):
    return refresh_access_token(request)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)