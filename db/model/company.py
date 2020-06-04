from sqlalchemy import Column, VARCHAR, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from db import session
from mysql import connector
from sqlalchemy.exc import SQLAlchemyError
from db.model.tag import TagModel
from db.model.companytag import CompanyTagModel
from db.model.companygroup import CompanyGroupModel
from db.model.language import LanguageModel
from util.formatter import format_company_search_result

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
            success = False
            error_msg = e.__cause__

        finally:
            session.close()

        return success, error_msg

    @staticmethod
    def select_companies_by_tag(tag):
        subquery = session.query(TagModel.tag_group_id).filter(TagModel.name == tag).subquery()
        query = session. \
            query(CompanyGroupModel.id, LanguageModel.code, CompanyModel.name). \
            join(CompanyGroupModel, CompanyModel.company_group_id == CompanyGroupModel.id). \
            join(LanguageModel, CompanyModel.language_id == LanguageModel.id). \
            join(CompanyTagModel, CompanyGroupModel.id == CompanyTagModel.company_group_id). \
            join(subquery, CompanyTagModel.tag_group_id == subquery.c.tag_group_id)

        company_query_result = query.order_by(
            CompanyModel.company_group_id.asc(), CompanyModel.name.asc()
        ).all()

        result = format_company_search_result(company_query_result)
        return result

    @staticmethod
    def select_companies_by_name(company_name):
        subquery = session.query(CompanyModel.company_group_id).filter(CompanyModel.name.match(company_name)).\
            distinct().subquery()

        query_result = session. \
            query(CompanyGroupModel.id, LanguageModel.code, CompanyModel.name). \
            join(CompanyGroupModel, CompanyModel.company_group_id == CompanyGroupModel.id). \
            join(LanguageModel, CompanyModel.language_id == LanguageModel.id). \
            join(subquery, CompanyGroupModel.id == subquery.c.company_group_id).\
            order_by(
                CompanyModel.company_group_id.asc(), CompanyModel.name.asc()
            ).all()

        result = format_company_search_result(query_result)
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
            company = session. \
                query(CompanyModel). \
                filter(CompanyModel.name == company_name,
                       CompanyModel.company_group_id == company_group_id,
                       CompanyModel.language_id == language_id). \
                one()
            session.delete(company)
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
