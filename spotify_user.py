from fastapi import Request
from datetime import datetime
from fastapi.responses import RedirectResponse,JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from spotify_api import get_auth_url, get_token_info, refresh_token
import json
from DB.models import SPOTIFY

def login(request: Request) -> RedirectResponse:
    #session = request.session
    #if session.get('access_token'):
    #    return RedirectResponse('/me') 
    scope = 'user-read-currently-playing user-read-recently-played user-read-private user-read-email playlist-read-private playlist-read-collaborative user-read-recently-played'
    auth_url = get_auth_url(scope)
    #auth_url = json.load(auth_url)

    return JSONResponse(auth_url)

def handle_callback(request: Request) -> RedirectResponse:
    session = request.session
    if 'error' in request.query_params:
        return JSONResponse({"error": request.query_params['error']})
    if 'code' in request.query_params:
        token_info = get_token_info(request.query_params['code'])
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        session['emotion'] = ''
        return RedirectResponse('/me')

def refresh_access_token(request: Request) -> RedirectResponse:
    session = request.session
    if 'refresh_token' not in session:
        return RedirectResponse('/login')
    if datetime.now().timestamp() > session['expires_at']:
        new_token_info = refresh_token(session['refresh_token'])
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        return RedirectResponse('/me')
