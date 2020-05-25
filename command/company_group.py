from http import HTTPStatus
from .command import Command
from db.model.companytag import CompanyTagModel
from db.model.company import CompanyModel
import logging


logger = logging.getLogger('app')


class FindCompanyGroupIDsCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def execute(self, **kwargs):
        kwargs = Command.validate(**kwargs)
        data = kwargs.get('data')
        response = kwargs.get("response")
        payload = data.get('payload')

        query_type = payload['query_type']
        keyword = payload['keyword']
        limit = payload['limit']
        page = payload['page']

        query_result = None
        limit = int(limit)
        page = int(page)

        # 회사명으로 회사 검색시
        if query_type == 'company':
            query_result = CompanyModel.select_company_group_ids_by_company_name(keyword, limit, page)

        # 태그명으로 회사 검색시
        elif query_type == 'tag':
            query_result = CompanyTagModel.select_company_group_ids_by_tag(keyword, limit, page)

        if query_result == 'no result':
            response['message'] = 'no result'
            return HTTPStatus.OK, response

        elif query_result is None:
            response['message'] = 'out of page'
            return HTTPStatus.OK, response

        data['company_group_ids'] = query_result
        return self.command.execute(**kwargs) if self.command else (HTTPStatus.OK, response)
