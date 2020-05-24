from flask import request, json, jsonify, Blueprint, make_response
from db.model.company import CompanyModel
from db.model.companygroup import CompanyGroupModel
from db.model.tag import TagModel
from db.model.taggroup import TagGroupModel
from db.model.companytag import CompanyTagModel
from db.model.language import LanguageModel
from http import HTTPStatus
import logging

app_route = Blueprint('v1', __name__, url_prefix='/v1')
logger = logging.getLogger('app')


@app_route.route('/language', methods=['POST', 'DELETE'])
def manage_languages():
    success, error_msg = None, None
    data = request.get_json()
    language_code = data['code']
    response = {}

    if request.method == 'POST':
        success, error_msg = LanguageModel.insert(language_code)

    elif request.method == 'DELETE':
        success, error_msg = LanguageModel.delete(language_code)

    if success:
        response['message'] = 'OK'
    else:
        response['message'] = 'Failure: {}'.format(error_msg)

    return make_response(jsonify(response), HTTPStatus.OK)


@app_route.route('/company-group', methods=['POST', 'DELETE'])
def manage_company_groups():
    response = {}
    success, error_msg = None, None
    data = request.get_json()
    group_name = data['name']

    if request.method == 'POST':
        success, error_msg = CompanyGroupModel.insert_new_company_group(group_name)

    elif request.method == 'DELETE':
        success, error_msg = CompanyGroupModel.delete_company_group(group_name)

    if success:
        response['message'] = 'OK'
    else:
        response['message'] = 'Failure: {}'.format(error_msg)

    return make_response(jsonify(response), HTTPStatus.OK)


# 회사 그룹에 대한 태그 그룹을 관리하는 API
@app_route.route('/company-group/tag-group', methods=['POST', 'DELETE'])
def manage_tag_groups_for_company_groups():
    data = request.get_json()
    company_group_name = data['company_group_name']
    tag_group_name = data['tag_group_name']
    response = dict()

    company_group_id = CompanyGroupModel.select_company_group_id_by_company_group_name(company_group_name)
    tag_group_id = TagGroupModel.select_tag_group_id_by_tag_group_name(tag_group_name)

    # 두 데이터가 모두 존재한다면 트랜잭션을 이어서 진행한다.
    if company_group_id and tag_group_id:

        # POST 메소드 호출시 태그 정보를 회사에 추가.
        if request.method == 'POST':
            success, err_msg = CompanyTagModel.insert_company_group_id_and_tag_group_id_to_company_tag(company_group_id, tag_group_id)
            if success:
                response['message'] = 'OK'
            else:
                response['message'] = 'Failure: {}'.format(err_msg)

        elif request.method == 'DELETE':
            success, err_msg = CompanyTagModel.delete_company_group_id_and_tag_group_id_from_company_tag(company_group_id, tag_group_id)
            if success:
                response['message'] = 'OK'
            else:
                response['message'] = 'Failure: {}'.format(err_msg)

    # 두 값 모두 데이터가 존재하지 않는 경우
    elif not company_group_id and not tag_group_id:
        response['message'] = "No record that matches {} and {}.".format(company_group_name, tag_group_name)

    # 회사 그룹 ID를 찾을 수 없는 경우
    elif not company_group_id:
        response['message'] = "No record that matches {}.".format(company_group_name)

    # 태그 그룹 ID를 찾을 수 없는 경우
    elif not tag_group_id:
        response['message'] = "No record that matches {}.".format(tag_group_name)

    return make_response(jsonify(response), HTTPStatus.OK)


# 태그 그룹을 관리하는 API
@app_route.route('/tag-group', methods=['POST', 'DELETE'])
def manage_tag_groups():
    response = {}
    success, error_msg = None, None
    data = request.get_json()
    tag_group_name = data['name']

    # POST 메소드 호출시 태그 그룹 추가.
    if request.method == 'POST':
        success, error_msg = TagGroupModel.insert(tag_group_name)

    # DELETE 메소드 호출시 태그 그룹 삭제.
    elif request.method == 'DELETE':
        success, error_msg = TagGroupModel.delete(tag_group_name)

    if success:
        response['message'] = 'OK'
    else:
        response['message'] = 'Failure: {}'.format(error_msg)

    return make_response(jsonify(response), HTTPStatus.OK)


# 각 언어별 태그를 관리하는 API
@app_route.route('/tag', methods=['POST', 'DELETE'])
def manage_tags():
    response = {}
    data = request.get_json()
    success, error_msg = None, None
    tag_group_name = data['tag_group_name']
    tag_name = data['tag_name']
    language_code = data['language_code']

    # POST 메소드 호출 시 태그 추가.
    if request.method == 'POST':
        success, error_msg = TagModel.insert(tag_name, tag_group_name, language_code)

    # DELETE 메소드 호출 시 태그 삭제.
    elif request.method == 'DELETE':
        success, error_msg = TagModel.delete(tag_name, tag_group_name, language_code)

    if success:
        response['message'] = 'OK'
    else:
        response['message'] = 'Failure: {}'.format(error_msg)

    return make_response(jsonify(response), HTTPStatus.OK)


@app_route.route('/company', methods=['POST', 'DELETE'])
def manage_companies():
    response = {}
    data = request.get_json()
    success, error_msg = None, None
    company_name = data['company_name']
    company_group_name = data['company_group_name']
    language_code = data['language_code']

    # POST 메소드 호출시 회사 레코드 추가
    if request.method == 'POST':
        success, error_msg = CompanyModel.insert(
            company_name=company_name,
            company_group_name=company_group_name,
            language_code=language_code
        )

    # DELETE 메소드 호출시 회사 레코드 삭제
    elif request.method == 'DELETE':
        success, error_msg = CompanyModel.delete(
            company_name=company_name,
            company_group_name=company_group_name,
            language_code=language_code
        )

    if success:
        response['message'] = 'OK'
    else:
        response['message'] = 'Failure: {}'.format(error_msg)

    return make_response(jsonify(response), HTTPStatus.OK)


# 회사 검색 결과를 리턴해주는 함수.
@app_route.route('/search', methods=['GET'])
def search():
    company_group_ids = []
    query_type = request.args.get('query_type')
    keyword = request.args.get('keyword')

    # 회사명으로 회사 검색시
    if query_type == 'company':
        company_group_ids = CompanyModel.select_company_group_ids_by_company_name(keyword)

    # 태그명으로 회사 검색시
    elif query_type == 'tag':
        company_group_ids = CompanyTagModel.select_company_group_ids_by_tag(keyword)

    company_group_ids = [r for r, in company_group_ids]

    # JSON array 결과값을 담기 위한 res_list 변수 선언
    res_list = []
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
        res_list.append(company_info)

    json_response = json.dumps(res_list)
    return json_response
