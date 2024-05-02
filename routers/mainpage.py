from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from DB.models import USERS
from DB.database import engineconn
from sqlalchemy import *
from fastapi.responses import JSONResponse
from CRUD.spotify import *
from spotify_user import login, handle_callback, refresh_access_token
from lyrics_crawler import crawling_lyrics
from datetime import datetime
from spotify_api import get_playlist
from predict_emotion import predict_emotion
engine = engineconn()
session_maker = engine.sessionmaker()
router = APIRouter(prefix='/mainpage')
dic = {}
@router.post('/spotify/{user_id}')
async def spotify_list(user_id):
    vod_list = vodlist_match_useremotion(user_id)
    return JSONResponse(vod_list)

@router.post('/spotify/{user_id}/status')
async def spotify_status(user_id):
    status = check_Spotify_accesstoken(user_id)
    return JSONResponse(status)


@router.post('/spotify/{user_id}/connect_url')
async def login_route(request: Request, user_id):
    session = request.session
    session['user_id'] = user_id
    return login(request)

@router.get('/callback')
async def callback(request: Request):
    return handle_callback(request)

@router.post('/spotify/{user_id}')
async def get_emotion(request: Request, user_id):
    try:
        user_info = select_SpotifyInfo(user_id)
        print(user_info)
        if 'access_token' not in user_info:
            return refresh_access_token(user_info)
        if datetime.now().timestamp() > session['expires_at']:
            return refresh_access_token(request)
        audio_names = get_playlist(session['access_token'])
        lyrics_list = crawling_lyrics(audio_names)
        emotion=predict_emotion(lyrics_list)
        dic[user_id] = emotion
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




    


