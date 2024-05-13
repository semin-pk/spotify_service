from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from DB.models import USERS
from DB.database import engineconn
from sqlalchemy import *
from fastapi.responses import JSONResponse
engine = engineconn()
session_maker = engine.sessionmaker()
router = APIRouter(prefix='/signup')
class Signup(BaseModel):
     SETTOP_NUM : str
     USER_NAME : str
     GENDER : str
     AGE : int
@router.post('/')
def signup(signup: Signup):
    print(signup)
    SETTOP_NUM = signup.SETTOP_NUM.replace('"', '')
    if signup:
        session_maker.execute(
            insert(USERS),
            [
                {
                    "SETTOP_NUM" : SETTOP_NUM,
                    "USER_NAME" : signup.USER_NAME,
                    "GENDER" : signup.GENDER,
                    "AGE" : int(signup.AGE),
                }
            ]
          )
        session_maker.commit()
        return JSONResponse(content={'response': 'FINISH INSERT USERS'}, status_code= 200)
    else :
        return JSONResponse(content={'error' : 'EMPTY_SIGNUP_ELEMENTS'}, status_code = 400)
