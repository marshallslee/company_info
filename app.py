from flask import Flask, request, json, jsonify
from mysql import connector
from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from config.config import DB_URI
from db.model import Language, CompanyGroup, TagGroup, CompanyTag, Company, Tag


app = Flask(__name__)
engine = create_engine(DB_URI)
_session = sessionmaker(bind=engine)
session = _session()

# UTF-8 서포트
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def main_page():
    return 'COMPANY INFO'


@app.route('/language', methods=['POST'])
def add_new_language():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        language_code = data['code']
        language = Language(code=language_code)
        try:
            session.add(language)
            session.commit()
            response['result'] = 'OK'

        except (
            connector.Error,
            IntegrityError
        ) as e:
            session.rollback()
            response['result'] = 'Failure: {}'.format(e.__cause__)

        finally:
            session.close()

        json_response = json.dumps(response)
        return json_response


@app.route('/company-group', methods=['POST'])
def add_new_company_group():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        group_name = data['name']
        company_group = CompanyGroup(group_name)

        try:
            session.add(company_group)
            session.commit()
            response['message'] = 'OK'

        except (
            connector.Error,
            IntegrityError
        ) as e:
            session.rollback()
            response['message'] = 'Failure: {}'.format(e.__cause__)
            return jsonify(response), 400

        finally:
            session.close()

        json_response = json.dumps(response)
        return json_response


@app.route('/company-group/tag-group', methods=['POST'])
def add_tag_group_to_company_group():
    data = request.get_json()
    company_group_name = data['company_group_name']
    tag_group_name = data['tag_group_name']
    response = {}

    if request.method == 'POST':
        try:
            company_group_id = session.\
                query(CompanyGroup.id).\
                filter(CompanyGroup.name == company_group_name).\
                scalar()

            tag_group_id = session.\
                query(TagGroup.id).\
                filter(TagGroup.name == tag_group_name).\
                scalar()

            # 두 데이터가 모두 존재한다면 저장 작업을 이어서 진행한다.
            if company_group_id and tag_group_id:
                company_tag = CompanyTag(company_group_id=company_group_id, tag_group_id=tag_group_id)
                session.add(company_tag)
                session.commit()
                response['message'] = "Successfully processed the request."

            # 두 값 모두 데이터가 존재하지 않는 경우
            elif not company_group_id and not tag_group_id:
                response['message'] = "No record that matches {} and {}.".format(company_group_name, tag_group_name)
                return jsonify(response), 400

            # 회사 그룹 ID를 찾을 수 없는 경우
            elif not company_group_id:
                response['message'] = "No record that matches {}.".format(company_group_name)
                return jsonify(response), 400

            # 태그 그룹 ID를 찾을 수 없는 경우
            elif not tag_group_id:
                response['message'] = "No record that matches {}.".format(tag_group_name)
                return jsonify(response), 400

        except (
            connector.Error,
            IntegrityError
        ) as e:
            response['message'] = e.__cause__
            return jsonify(response), 400

        json_response = json.dumps(response)
        return json_response


@app.route('/tag-group', methods=['POST'])
def add_new_tag_group():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        tag_group_name = data['name']
        company_group_id = data['company_group_id']
        tag_group = TagGroup(tag_group_name, company_group_id)
        try:
            session.add(tag_group)
            session.commit()
            response['result'] = 'OK'
        except (
            connector.Error,
            IntegrityError
        ) as e:
            response['result'] = "Failed to process the request. {}".format(e.msg)
        json_response = json.dumps(response)
        return json_response


@app.route('/tag', methods=['POST'])
def add_new_tag():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        tag_group_name = data['name']
        company_group_id = data['company_group_id']
        tag_group = TagGroup(tag_group_name, company_group_id)

        try:
            session.add(tag_group)
            session.commit()
            response['result'] = 'OK'

        except (
            connector.Error,
            IntegrityError
         ) as e:
            response['result'] = "Failed to process the request. {}".format(e.msg)

        json_response = json.dumps(response)
        return json_response


@app.route('/company', methods=['POST'])
def add_new_company():
    response = {}
    if request.method == 'POST':
        data = request.get_json()
        tag_group_name = data['name']
        company_group_id = data['company_group_id']
        tag_group = TagGroup(tag_group_name, company_group_id)

        try:
            session.add(tag_group)
            session.commit()
            response['result'] = 'OK'

        except (
            connector.Error,
            IntegrityError
         ) as e:
            response['result'] = "Failed to process the request. {}".format(e.msg)

        json_response = json.dumps(response)
        return json_response


@app.route('/search', methods=['GET'])
def search():
    response = {}
    query_type = request.args.get('query_type')
    keyword = request.args.get('keyword')

    # 회사명으로 검색시
    if query_type == 'company':
        res = []

        company_group_ids = session.query(Company.company_group_id).filter(Company.name.match(keyword)).distinct().all()

        for company_group_id in company_group_ids:
            res.append(company_group_id)

        response['message'] = res

    elif query_type == 'tag':
        company_groups = session.\
            query(CompanyTag).\
            filter(CompanyTag.tag_group_id ==
                   session.
                   query(Tag.tag_group_id).
                   filter(Tag.name ==
                          keyword)).\
            all()

        res = []
        for company_group in company_groups:
            res.append(company_group.company_group_id)

        response['message'] = res

    json_response = json.dumps(response)
    return json_response


if __name__ == '__main__':
    app.run()
