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
    if signup:
        session_maker.execute(
            insert(USERS),
            [
                {
                    "SETTOP_NUM" : signup.SETTOP_NUM,
                    "USER_NAME" : signup.USER_NAME,
                    "GENDER" : signup.GENDER,
                    "AGE" : signup.AGE,
                }
            ]
          )
        return JSONResponse(content='FINISH INSERT USERS', status_code= 200)
    else :
        return JSONResponse(content='EMPTY_SIGNUP_ELEMENTS', status_code = 400)
