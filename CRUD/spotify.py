from DB.database import engineconn
from DB.models import SPOTIFY

engine = engineconn()
session_maker = engine.sessionmaker()

def insert_SpotifyInfo(user_id, access_token, refresh_token, expires_at):
    
    