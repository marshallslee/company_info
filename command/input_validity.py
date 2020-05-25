from http import HTTPStatus
from .command import Command
import logging


logger = logging.getLogger('app')


class InputValidityCheckCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def execute(self, **kwargs):
        kwargs = Command.validate(**kwargs)
        data = kwargs.get('data')
        response = kwargs.get("response")
        payload = data.get('payload')

        limit = payload['limit']
        page = payload['page']

        try:
            limit = int(limit)
            page = int(page)
        except ValueError:
            response['message'] = 'Wrong page input: limit: {}, page: {}'.format(limit, page)
            return HTTPStatus.BAD_REQUEST, response

        return self.command.execute(**kwargs) if self.command else (HTTPStatus.OK, response)
