from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import DB_URI
from mysql import connector
from sqlalchemy.exc import SQLAlchemyError
import logging


engine = create_engine(DB_URI)
_session = sessionmaker(bind=engine)
session = _session()
logger = logging.getLogger('app')


def db_transaction(transaction):
    def wrapper(*args, **kwargs):
        try:
            result = transaction(*args, **kwargs)
        except (
            connector.Error,
            SQLAlchemyError
        ) as e:
            session.rollback()
            logger.error("An error occurred during the transaction: {}".format(e.__cause__))
            raise
        finally:
            session.close()
        return result
    return wrapper
