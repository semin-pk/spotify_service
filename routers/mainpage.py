from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from DB.models import USERS
from DB.database import engineconn
from sqlalchemy import *
from fastapi.responses import JSONResponse
from CRUD.spotify import *
from lyrics_crawler import crawling_lyrics
from datetime import datetime
from spotify_api import get_playlist
from predict_emotion import predict_emotion
from collections import deque
from pprint import pprint
d = deque()
router = APIRouter(prefix='/mainpage')
dic = {}

def get_deque():
    return d

@router.get('/')
async def example():
    return {'message':'hello'}

@router.post('/spotify/{user_id}') #spotify 플레이리스트에 맞는  vod리스트
async def spotify_list(user_id):
    vod_list = vodlist_match_useremotion(user_id)
    pprint(vod_list)
    return JSONResponse(vod_list)

@router.post('/spotify/{user_id}/status') #spotify 연동상태 확인
async def spotify_status(user_id):
    status = check_Spotify_accesstoken(user_id)
    data = {
        'response' : status
    }
    return JSONResponse(data)


@router.post('/spotify/{user_id}/connect_url') #spotify 로그인  url
async def login_route(request: Request, user_id):
    d.append(int(user_id))
    print(d)
    from spotify_user import login
    return login(request)

@router.post('/spotify/{user_id}/userinfo') #spotify access_token을 이용하여 플레이리스트 가사 크롤링 후 감정 파악 감정 DB에 저장
async def get_emotion(request: Request, user_id):

    #try:
    user_info = select_SpotifyInfo(user_id)
    print(user_info)
    user_info = user_info[0]
    print(len(user_info))
    if len(user_info) == 0:
        from spotify_user import refresh_access_token
        return refresh_access_token(user_info)
    if datetime.now().timestamp() > user_info['EXPIRE_DATE']:
        from spotify_user import refresh_access_token
        return refresh_access_token(user_info)
    audio_names = get_playlist(user_info['ACCESS_TOKEN'])
    lyrics_list = crawling_lyrics(audio_names)
    emotion=predict_emotion(lyrics_list)
    print(type(emotion))
    update_emotion(user_id,emotion)
    return JSONResponse(emotion)
    #except Exception:
    #    error = '연동실패!'
    #    return JSONResponse(error)
