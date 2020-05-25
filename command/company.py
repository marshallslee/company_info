from http import HTTPStatus
from .command import Command
from db.model.language import LanguageModel
from db.model.company import CompanyModel
import logging


logger = logging.getLogger('app')


class GetCompaniesByCompanyGroupIDCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def execute(self, **kwargs):
        kwargs = Command.validate(**kwargs)
        data = kwargs.get('data')
        response = kwargs.get("response")
        payload = data.get('payload')

        company_group_ids = data['company_group_ids']
        # JSON array 결과값을 담기 위한 res_list 변수 선언
        companies_list = []
        for company_group_id in company_group_ids:
            companies = CompanyModel.select_company_by_company_group_id(company_group_id)

            # 언어별 회사명을 담을 딕셔너리 변수 선언.
            company_lang_name_mapper = {}

            for company in companies:
                language_code = LanguageModel.select_language_code_by_language_id(company.language_id)
                company_lang_name_mapper[language_code] = company.name

            company_info = {
                'company_group_id': company_group_id,
                'company_name': company_lang_name_mapper
            }
            companies_list.append(company_info)

        response['companies_list'] = companies_list
        return self.command.execute(**kwargs) if self.command else (HTTPStatus.OK, response)
