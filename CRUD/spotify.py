from DB.database import engineconn
from DB.models import SPOTIFY, USERS, VOD
from sqlalchemy import *
import json
engine = engineconn()
session_maker = engine.sessionmaker()

def check_Spotify_accesstoken(user_id: str) -> bool:
    result = session_maker.execute(
        select(USERS.SPOTIFY).where(USERS.USER_ID == user_id)
    ).fetchone()

    if result and result[0]:  # 액세스 토큰이 존재하는 경우
        return True
    else:
        return False


def insert_SpotifyInfo(user_id, access_token, refresh_token, expires_at):
    print(type(user_id), type(access_token), type(refresh_token), type(expires_at))
    session_maker.execute(
        insert(SPOTIFY),
        [
            {
                'USER_ID': int(user_id),
                'ACCESS_TOKEN': access_token,
                'REFRESH_TOKEN': refresh_token,
                'EXPIRE_DATE': expires_at
            }
        ]
    )
    session_maker.commit()
def select_SpotifyInfo(user_id):
    info = session_maker.query(SPOTIFY).filter(SPOTIFY.USER_ID == user_id)
    serialized_example = [item.to_dict() for item in info]
    return serialized_example



def select_Spotify_accesstoken(user_id):
    access_token = session_maker.execute(
        select(SPOTIFY.ACCESS_TOKEN).where(SPOTIFY.USER_ID == user_id)
    )
    return access_token

'''def vodlist_match_useremotion(user_id) -> dict:

    # 사용자의 감정에 맞는 VOD 목록 검색
    join_condition = VOD.EMOTION == SPOTIFY.EMOTION

    subquery = session_maker.query(SPOTIFY.EMOTION).filter(SPOTIFY.USER_ID == user_id).scalar()

    query = (
        select(VOD.TITLE, VOD.VOD_ID, VOD.POSTER_URL)
        .where(VOD.EMOTION == subquery)
        .select_from(join(VOD, SPOTIFY, join_condition))
    )
    vod_list = session_maker.execute(query).fetchall()
    print(vod_list)
    return vod_list'''
def vodlist_match_useremotion(user_id) -> str:
    # 사용자의 감정에 맞는 VOD 목록 검색
    join_condition = VOD.EMOTION == SPOTIFY.EMOTION

    subquery = session_maker.query(SPOTIFY.EMOTION).filter(SPOTIFY.USER_ID == user_id).scalar()

    query = (
        select(VOD.TITLE, VOD.VOD_ID, VOD.POSTER_URL)
        .where(VOD.EMOTION == subquery)
        .select_from(join(VOD, SPOTIFY, join_condition))
    )
    vod_list = session_maker.execute(query).fetchall()

    # 결과를 딕셔너리로 변환
    formatted_results = []
    for row in vod_list:
        formatted_results.append({
            'TITLE': row[0],
            'VOD_ID': row[1],
            'POSTER_URL': row[2]
        })

    # JSON 직렬화
    json_results = json.dumps(formatted_results)
    print(json_results)
    return json_results

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

def update_emotion(user_id, emotion):
    session_maker.execute(
        update(SPOTIFY)
        .where(SPOTIFY.USER_ID == user_id)
        .values(
            {
                SPOTIFY.EMOTION : emotion
            }
        )
    )
    session_maker.commit()

def update_spotify_status(user_id):
    session_maker.execute(
        update(SPOTIFY)
        .where(USERS.USER_ID == user_id)
        .values(
            {
                USERS.SPOTIFY: 1
            }
        )
    )
    session_maker.commit()