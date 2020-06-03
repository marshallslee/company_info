from sqlalchemy import Column, VARCHAR, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import session
from mysql import connector
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class CompanyGroupModel(Base):
    __tablename__ = 'company_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def insert_new_company_group(group_name):
        success = True
        error_msg = None
        company_group = CompanyGroupModel(group_name)

        try:
            session.add(company_group)
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
    def delete_company_group(company_group_name):
        success = True
        error_msg = None

        try:
            company_group = session.query(CompanyGroupModel).filter(CompanyGroupModel.name == company_group_name).one()
            session.delete(company_group)
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
    def select_company_group_id_by_company_group_name(company_group_name):
        return session. \
            query(CompanyGroupModel.id). \
            filter(CompanyGroupModel.name == company_group_name). \
            scalar()
