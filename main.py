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
emotion_test = ''
@app.get('/')
async def index():
    return {"message": "Hello World"}

@app.get('/login')
async def login_route(request: Request):
    return login(request)

@app.get('/callback')
async def callback(request: Request):
    return handle_callback(request)

@app.get('/me')
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
        #emotion = '기쁨, 설렘'
        #return RedirectResponse(url = 'http://localhost:3000')
        #return JSONResponse(session['emotion'])
        
        #return RedirectResponse('/emotion')
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
