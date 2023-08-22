import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


DB_CONFIG = {
    "username": os.getenv("DB_USER_NAME"),
    "password": os.getenv("DB_PASS_WORD"),
    "url": os.getenv("DB_URL"),
    "name": os.getenv("DB_NAME"),
}


def start_engine():
    engine = create_engine(
        url=f"mysql+mysqlconnector://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['url']}/{DB_CONFIG['name']}"
    )
    return engine


def create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

if __name__ == "__main__":
    eng = start_engine()
    sess = create_session(eng)
    print(sess)