from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import DB_URI


engine = create_engine(DB_URI)
_session = sessionmaker(bind=engine)
session = _session()
