from DB.database import engineconn
from DB.models import SPOTIFY, USERS, VOD
from sqlalchemy import *
engine = engineconn()
session_maker = engine.sessionmaker()
def check_Spotify_accesstoken(user_id : str) -> bool:
    status = session_maker.execute(
        select(USERS.SPOTIFY).where(USERS.USER_ID == user_id)
    )
    return status

def insert_SpotifyInfo(user_id, access_token, refresh_token, expires_at):
    session_maker.execute(
        insert(SPOTIFY),
        [
            {
                'user_id': user_id,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expire_date': expires_at
            }
        ]
    )
def select_SpotifyInfo(user_id):
    info = session_maker.execute(
        select(SPOTIFY).where(SPOTIFY.USER_ID == user_id)
    )
    return(info)
def select_Spotify_accesstoken(user_id):
    access_token = session_maker.execute(
        select(SPOTIFY.ACCESS_TOKEN).where(SPOTIFY.USER_ID == user_id)
    )
    return access_token

def vodlist_match_useremotion(user_id) -> dict:
    subquery = select(SPOTIFY.EMOTION).where(SPOTIFY.USER_ID == user_id).as_scalar()
    vod_list = session_maker.execute(
        select(VOD.TITLE)
        .where(VOD.EMOTION == subquery)
        .select_from(VOD)
        .join(SPOTIFY, VOD.EMOTION == SPOTIFY.EMOTION)
    )
    return vod_list

def update_refreshtoken(user_id, access_token, expires_at):
    session_maker.execute(
        update(SPOTIFY)
        .where(SPOTIFY.USER_ID == user_id)
        .values(
            {
                SPOTIFY.ACCESS_TOKEN : access_token,
                SPOTIFY.EXPIRE_DATE : expires_at
            }
        )
    )