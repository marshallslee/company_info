from flask import Blueprint, make_response, jsonify
from http import HTTPStatus
from route.v1 import app_route as app_route_v1

home_route = Blueprint('home', __name__, url_prefix='/')


@home_route.route('', methods=['GET'])
def home():
    res_data = {'message': 'Company Info Web API'}
    return make_response(jsonify(res_data), HTTPStatus.OK)


def register_route(server):
    server.register_blueprint(home_route)
    server.register_blueprint(app_route_v1)
