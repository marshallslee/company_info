from sqlalchemy import Column, VARCHAR, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import session
from mysql import connector
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class LanguageModel(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(VARCHAR(5), nullable=False, unique=True)

    def __init__(self, code):
        self.code = code

    @staticmethod
    def insert(language_code):
        success = True
        error_msg = None
        language = LanguageModel(code=language_code)
        try:
            session.add(language)
            session.commit()

        except (
                connector.Error,
                SQLAlchemyError
        ) as e:
            session.rollback()
            success = False
            error_msg = e.__cause__

        finally:
            session.close()

        return success, error_msg

    @staticmethod
    def select_language_code_by_language_id(language_id):
        return session. \
            query(LanguageModel.code). \
            filter(LanguageModel.id == language_id). \
            scalar()

    @staticmethod
    def select_language_id_by_code(language_code):
        return session. \
            query(LanguageModel.id). \
            filter(LanguageModel.code == language_code). \
            scalar()

    @staticmethod
    def delete(language_code):
        success = True
        error_msg = None

        try:
            language = session.query(LanguageModel).filter(LanguageModel.code == language_code).one()
            session.delete(language)
            session.commit()

        except (
                connector.Error,
                SQLAlchemyError
        ) as e:
            session.rollback()
            success = False
            error_msg = e.__cause__

        finally:
            session.close()

        return success, error_msg
