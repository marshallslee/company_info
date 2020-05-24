from sqlalchemy import Column, VARCHAR, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import session
from mysql import connector
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class TagGroupModel(Base):
    __tablename__ = 'tag_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def select_tag_group_id_by_tag_group_name(tag_group_name):
        return session. \
            query(TagGroupModel.id). \
            filter(TagGroupModel.name == tag_group_name). \
            scalar()

    @staticmethod
    def insert(tag_group_name):
        success = True
        error_msg = None
        tag_group = TagGroupModel(tag_group_name)

        try:
            session.add(tag_group)
            session.commit()

        except (
            connector.Error,
            SQLAlchemyError
        ) as e:
            session.rollback()
            session.flush()
            success = False
            error_msg = e.__cause__

        finally:
            session.close()

        return success, error_msg

    @staticmethod
    def delete(tag_group_name):
        success = True
        error_msg = None

        try:
            tag_group = session.query(TagGroupModel).filter(TagGroupModel.name == tag_group_name).one()
            session.delete(tag_group)
            session.commit()

        except (
                connector.Error,
                SQLAlchemyError
        ) as e:
            session.rollback()
            session.flush()
            success = False
            error_msg = e.__cause__

        finally:
            session.close()

        return success, error_msg
