from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from db import session
from mysql import connector
from sqlalchemy.exc import SQLAlchemyError
from db.model.companygroup import CompanyGroupModel
from db.model.taggroup import TagGroupModel

Base = declarative_base()


class CompanyTagModel(Base):
    __tablename__ = 'company_tag'
    __table_args__ = (
        PrimaryKeyConstraint('company_group_id', 'tag_group_id'),
    )
    company_group_id = Column(ForeignKey(CompanyGroupModel.id), nullable=False)
    tag_group_id = Column(ForeignKey(TagGroupModel.id), nullable=False)

    def __init__(self, company_group_id, tag_group_id):
        self.company_group_id = company_group_id
        self.tag_group_id = tag_group_id

    @staticmethod
    def insert(company_group_id, tag_group_id):
        success = True
        error_msg = None

        try:
            company_tag = CompanyTagModel(company_group_id=company_group_id, tag_group_id=tag_group_id)
            session.add(company_tag)
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
    def delete(company_group_id, tag_group_id):
        success = True
        error_msg = None

        try:
            company_tag = session. \
                query(CompanyTagModel). \
                filter(CompanyTagModel.company_group_id == company_group_id, CompanyTagModel.tag_group_id == tag_group_id). \
                one()
            session.delete(company_tag)
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
