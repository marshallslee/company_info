from sqlalchemy import Column, VARCHAR, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import session
from mysql import connector
from sqlalchemy.exc import SQLAlchemyError
from db.model.language import LanguageModel
from db.model.taggroup import TagGroupModel

Base = declarative_base()


class TagModel(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False)
    language_id = Column(ForeignKey(LanguageModel.id), nullable=False)
    tag_group_id = Column(ForeignKey(TagGroupModel.id), nullable=False)

    def __init__(self, name, language_id, tag_group_id):
        self.name = name
        self.language_id = language_id
        self.tag_group_id = tag_group_id

    @staticmethod
    def insert(tag_name, tag_group_name, language_code):
        success = True
        error_msg = None
        tag_group_id = TagGroupModel.select_tag_group_id_by_tag_group_name(tag_group_name)
        language_id = LanguageModel.select_language_id_by_code(language_code)
        tag = TagModel(name=tag_name, tag_group_id=tag_group_id, language_id=language_id)

        try:
            session.add(tag)
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
    def delete(tag_name, tag_group_name, language_code):
        success = True
        error_msg = None
        tag_group_id = TagGroupModel.select_tag_group_id_by_tag_group_name(tag_group_name)
        language_id = LanguageModel.select_language_id_by_code(language_code)

        try:
            tag = session.\
                query(TagModel).\
                filter(TagModel.name == tag_name,
                       TagModel.tag_group_id == tag_group_id,
                       TagModel.language_id == language_id).\
                one()
            session.delete(tag)
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
