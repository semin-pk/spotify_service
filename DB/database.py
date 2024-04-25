from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

USERNAME = 'root'
PASSWORD = '12340131'
HOST = 'hellovision.c3gk86ic62pt.ap-northeast-2.rds.amazonaws.com'
PORT = 3306
DB = 'hellovision'
DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'

class engineconn:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session
    
    def connection(self):
        conn = self.engine.connect()
        return conn