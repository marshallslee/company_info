from sqlalchemy import Column, VARCHAR, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import session
from mysql import connector
from sqlalchemy.exc import SQLAlchemyError
from db.model.companygroup import CompanyGroupModel
from db.model.language import LanguageModel

Base = declarative_base()


class CompanyModel(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False)
    company_group_id = Column(ForeignKey(CompanyGroupModel.id), nullable=False)
    language_id = Column(ForeignKey(LanguageModel.id), nullable=False)

    def __init__(self, name, company_group_id, language_id):
        self.name = name
        self.company_group_id = company_group_id
        self.language_id = language_id

    @staticmethod
    def insert(company_name, company_group_name, language_code):
        success = True
        error_msg = None

        company_group_id = CompanyGroupModel.select_company_group_id_by_company_group_name(company_group_name)
        if not company_group_id:
            success = False
            error_msg = "No record found for the company group name: {}".format(company_group_name)
            return success, error_msg

        language_id = LanguageModel.select_language_id_by_code(language_code)
        if not language_id:
            success = False
            error_msg = "No record found for the language code: {}".format(language_code)
            return success, error_msg

        company = CompanyModel(name=company_name, company_group_id=company_group_id, language_id=language_id)
        try:
            session.add(company)
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
    def select_company_group_ids_by_company_name(company_name, limit, page):
        # limit: 페이지당 노출되는 개시물의 갯수
        # offset: 몇 번 인덱스 레코드부터 보여질 것인지 결정하는 파라미터.
        offset = limit * (page - 1)
        result = []
        query = session.\
            query(CompanyModel.company_group_id).\
            filter(CompanyModel.name.match(company_name)).\
            distinct()

        count = query.count()

        if count == 0:
            return 'no result'

        elif offset + 1 > count:
            return None

        else:
            query_by_page = query.offset(offset).limit(limit).all()
            for company_group_id in query_by_page:
                result.append(company_group_id)
            result = [item for item, in result]

        return result

    @staticmethod
    def select_company_by_company_group_id(company_group_id):
        return session. \
            query(CompanyModel). \
            filter(CompanyModel.company_group_id == company_group_id). \
            all()

    @staticmethod
    def delete(company_name, company_group_name, language_code):
        success = True
        error_msg = None

        company_group_id = CompanyGroupModel.select_company_group_id_by_company_group_name(company_group_name)
        if not company_group_id:
            success = False
            error_msg = "No record found for the company group name: {}".format(company_group_name)
            return success, error_msg

        language_id = LanguageModel.select_language_id_by_code(language_code)
        if not language_id:
            success = False
            error_msg = "No record found for the language code: {}".format(language_code)
            return success, error_msg

        try:
            tag = session.\
                query(CompanyModel).\
                filter(CompanyModel.name == company_name,
                       CompanyModel.company_group_id == company_group_id,
                       CompanyModel.language_id == language_id).\
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
