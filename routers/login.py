from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from DB.models import USERS
from DB.database import engineconn
from sqlalchemy import *
from fastapi.responses import JSONResponse
engine = engineconn()
session_maker = engine.sessionmaker()
router = APIRouter(prefix='/login')
class Settop_id(BaseModel):
    id : str
@router.post('/')
async def login(settop_id : Settop_id):
    if settop_id:
        settop_user_list = session_maker.execute(
            select(USERS.USER_NAME).
            where(USERS.SETTOP_NUM == settop_id.id))
        user_list = []
        for user in list(settop_user_list):
                print(user[0])
                user_list.append(user[0])
        if user_list:
            #print(len(sq_user_list))
            print(user_list)
            user = {
                'id' : user_list
            }
            return JSONResponse(user)
        else:
            print("error")
            return JSONResponse(content='error', status_code=402)
    else:
        result = {
            'check_response': 'error'
        }
        return JSONResponse(result)