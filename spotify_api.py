import urllib.parse
import pkce
import requests
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

REDIRECT_URI = 'http://localhost:8000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
CODE_VERIFIER = pkce.generate_code_verifier(length=128)
CODE_CHALLENGE = pkce.get_code_challenge(CODE_VERIFIER)

def get_auth_url(scope):
    params = {
        'client_id' : CLIENT_ID,
        'response_type' : 'code',
        'scope' : scope,
        'redirect_uri' : REDIRECT_URI,
        'code_challenge_method': 'S256',
        'code_challenge' : CODE_CHALLENGE
    } 

    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
def get_playlist(access_token):
    headers = {
            'Authorization': f"Bearer {access_token}"
    }
    response = requests.get(API_BASE_URL + "me/player/recently-played", headers=headers)
        
    playlist = response.json()
    audio_names = {}
    for i in range(5):
        artist = playlist['items'][i]['track']['album']['artists'][0]['name']
        title = playlist['items'][i]['track']['name']
        audio_names[i] = {'artist': artist,
                        'title': title}
    return audio_names
    
def get_token_info(code):
    req_body = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'code_verifier' : CODE_VERIFIER
    }
    response = requests.post(TOKEN_URL, data=req_body)
    return response.json()

def refresh_token(refresh_token):
    req_body = {
        'grant_type' : 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=req_body)
    return response.json()