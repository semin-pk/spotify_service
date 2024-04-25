from sqlalchemy import Column, TEXT, INT, BIGINT, DATE, VARCHAR, CHAR, SMALLINT, FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class USERS(Base):
    __tablename__ = "USERS"
    USER_ID = Column(INT, nullable=False, autoincrement = True, primary_key=True)
    SETTOP_NUM = Column(INT, nullable = False)
    USER_NAME = Column(VARCHAR(10), nullable = False)
    GENDER = Column(CHAR, nullable = True)
    AGE = Column(INT, nullable = True)
    SPOTIFY = Column(SMALLINT, nullable = True)

class ACTOR(Base):
    __tablename__ = "ACTOR"
    ACTOR_ID = Column(INT, nullable = False, autoincrement = True, primary_key = True)
    ACTOR_NAME = Column(VARCHAR, nullable = True)

class LIKES(Base):
    __tablename__ = "LIKES"
    LIKE_ID = Column(INT, nullable = False, autoincrement = True, primary_key = True)
    USER_ID = Column(INT, nullable = True)
    VOD_ID = Column(INT, nullable = True)

class REVIEW(Base):
    __tablename__ = "REVIEW"
    REVIEW_ID = Column(INT, nullable = False, autoincrement = True, primary_key = True)
    USER_ID = Column(INT, nullable = False)
    VOD_ID = Column(INT, nullable = True)
    RATING = Column(INT, nullable = False)
    COMMENT = Column(VARCHAR(150), nullable = True)
    REVIEW_WDATE = Column(DATE, nullable = True)
    REVIEW_MDATE = Column(DATE, nullable = True)
    POS_NEG = Column(SMALLINT, nullable = True)

class SPOTIFY(Base):
    __tablename__ = "SPOTIFY"
    SPOTIFY_ID = Column(INT, nullable = False, autoincrement = True, primary_key = True)
    USER_ID = Column(INT, nullable = False)
    ACCESS_TOKEN = Column(VARCHAR(255), nullable = False)
    REFRESH_TOKEN = Column(VARCHAR(255), nullable = False)
    EXPIRE_DATE = Column(FLOAT, nullable = True)

class VOD(Base):
    __tablename__ = "VOD"
    VOD_ID = Column(INT, nullable = False, autoincrement = True, primary_key = True)
    SUB_CATEGORY = Column(VARCHAR(5), nullable = True)
    TITLE = Column(VARCHAR(100), nullable = True)
    GENRE = Column(VARCHAR(10), nullable = True)
    SERIES_NUM = Column(INT, nullable = True)
    CONTENT_SUM = Column(VARCHAR(200), nullable = True)
    EMOTION = Column(VARCHAR(10), nullable = True)
    CAST = Column(VARCHAR(20), nullable = True)
    CREW = Column(VARCHAR(20), nullable = True)
    POSTER_URL = Column(VARCHAR(255), nullable = True)
    TRAILER_URL = Column(VARCHAR(255), nullable = True)
    RTM = Column(INT, nullable = True)