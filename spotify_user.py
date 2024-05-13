from fastapi import Request
from datetime import datetime
from fastapi.responses import RedirectResponse,JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from spotify_api import use_refresh_token, get_auth_url, get_token_info
import json
from DB.models import SPOTIFY
from CRUD.spotify import *
from routers.mainpage import get_deque

d = get_deque()

def login(request: Request) -> RedirectResponse:
    #session = request.session
    #if session.get('access_token'):
    #    return RedirectResponse('/me') 
    scope = 'user-read-currently-playing user-read-recently-played user-read-private user-read-email playlist-read-private playlist-read-collaborative user-read-recently-played'
    auth_url = get_auth_url(scope)
    #auth_url = json.load(auth_url)

    return JSONResponse(auth_url)

def handle_callback(request: Request) -> RedirectResponse:
    if 'error' in request.query_params:
        return JSONResponse({"error": request.query_params['error']})
    if 'code' in request.query_params:
        token_info = get_token_info(request.query_params['code'])
        expires_at = datetime.now().timestamp() + token_info['expires_in']
        print(token_info)
        user_id = d.popleft()
        insert_SpotifyInfo(user_id, token_info['access_token'], token_info['refresh_token'], expires_at)
        update_spotify_status(user_id)
        return JSONResponse(content='ok', status_code=200)

def refresh_access_token(user_info:dict) -> RedirectResponse:
    
    if 'REFRESH_TOKEN' not in user_info:
        return RedirectResponse('/login')
    if datetime.now().timestamp() > user_info['EXPIRE_DATE']:
        print(user_info['REFRESH_TOKEN'])
        new_token_info = use_refresh_token(user_info['REFRESH_TOKEN'])
        print(new_token_info)
        access_token= new_token_info['access_token']
        refresh_token = new_token_info['refresh_token']
        expire_date= datetime.now().timestamp() + new_token_info['expires_in']
        user_id = user_info['USER_ID']
        update_refreshtoken(user_id, access_token, refresh_token, expire_date)
        return RedirectResponse(f'/mainpage/spotify/{user_id}/userinfo')
