# API Specifications
현 단계에서는 전체 요청에 대해 일괄적으로 200 응답만을 내보내도록 설계하였다.

#### 1. `/language`
##### 1) `POST` 메소드. 언어 데이터를 추가할 때 호출하며 요청 바디는 다음과 같이 구성된다.
* code: 언어 코드를 말함. 영어의 경우 en, 한국어는 kr, 일본어는 jp, 중국어는 cn 등이다.
```json
{
  "code": "en"
}
```

커맨드라인으로는 다음과 같이 호출 가능하다.
```
$curl -X POST localhost:5000/language --header "Content-Type: application/json" --data '{"code": "en"}'
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "message": "OK"
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "message": "Failure 1062 (23000): Duplicate entry 'en' for key 'code_UNIQUE'"
}
```

##### 2) `DELETE` 메소드. 언어 데이터를 삭제하는 기능이며 요청 바디는 다음과 같다.
* code: 언어 코드를 말함. 영어의 경우 en, 한국어는 kr, 일본어는 jp, 중국어는 cn 등이다.

```json
{
  "code": "en"
}
```

커맨드라인으로는 다음과 같이 호출 가능하다.
```
$curl -X DELETE localhost:5000/language --header "Content-Type: application/json" --data '{"code": "en"}'
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "message": "OK"
}
```

#### 2. `/company-group`
##### 1) `POST` 메소드. 회사 그룹 데이터를 추가할 때 호출하며 요청 바디는 다음과 같이 구성된다.
* name: 회사 그룹명.

```json
{
  "name": "좋은 회사"
}
```

커맨드라인으로는 다음과 같이 호출 가능하다.
```
$curl -X POST localhost:5000/company-group --header "Content-Type: application/json" --data '{"name": "원티드랩"}'
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "message": "OK"
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "message": "Failure: 1062 (23000): Duplicate entry '' for key 'name_UNIQUE'"
}
```

##### 2) `DELETE` 메소드. 회사 그룹 데이터를 삭제하며 요청 바디는 다음과 같이 구성된다.
* name: 회사 그룹명.
```json
{
  "name": "좋은 회사"
}
```

커맨드라인으로는 다음과 같이 호출 가능하다.
```
$curl -X DELETE localhost:5000/company-group --header "Content-Type: application/json" --data '{"name": "원티드랩"}'
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "message": ""
}
```

#### 3. `/company-group/tag-group`
회사 그룹에 대한 태그 그룹을 관리하는 API. 

##### 1) `POST` 메소드. 회사 그룹에 태그 그룹을 추가한다. 요청 바디는 다음과 같이 구성된다.
* company_group_name: 회사 그룹명.
* tag_group_name: 태그 그룹명.
```json
{
  "company_group_name": "ABC 상사",
  "tag_group_name": "태그"
}
```

curl 요청 예제는 다음과 같다.
```
$curl -X POST localhost:5000/company-group/tag-group --header "Content-Type: application/json" --data '{"company_group_name": "원티드랩", "tag_group_name": "TAG 1"}'
```

이후에 값을 처리하는 로직에 대해서는 [다음 이미지](../../images/flowcharts/add_tag_group_to_company_group.png) 참고.

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "message": "OK"
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "message": "Failure: 1062 (23000): Duplicate entry '' for key 'name_UNIQUE'"
}
```

##### 2) `DELETE` 메소드. 회사 그룹에서 태그 그룹을 삭제해 준다. 요청 바디는 다음과 같이 구성된다.
* company_group_name: 회사 그룹명.
* tag_group_name: 태그 그룹명.

```json
{
  "company_group_name": "ABC 상사",
  "tag_group_name": "태그"
}
```

curl 요청 예제는 다음과 같다.
```
$curl -X DELETE localhost:5000/company-group/tag-group --header "Content-Type: application/json" --data '{"company_group_name": "원티드랩", "tag_group_name": "TAG 1"}'
```

#### 4. `/tag-group`
`POST` 메소드. 태그 그룹 데이터를 추가할 때 호출하며 요청 바디는 다음과 같이 구성된다.
* name: 태그 그룹명.
```json
{
  "name": "스타트"
}
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "message": "OK"
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "message": "Failure: 1062 (23000): Duplicate entry '' for key 'name_UNIQUE'"
}
```

#### 5. `/tag`
##### 1) `POST` 메소드. 태그 데이터를 추가할 때 호출하며 요청 바디는 다음과 같이 구성된다.
* tag_name: 태그 그룹명.
* language_code: 언어 코드
* tag_group_name: 태그 그룹명

```json
{
  "tag_name": "startup",
  "language_code": "en",
  "tag_group_name": "startup"
}
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "message": "OK"
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "message": "Failure message"
}
```

#### 6. `/company`
##### 1) `POST` 메소드. 회사 추가. 요청 바디는 다음과 같다.
* name: 회사명.
* company_group_id: 회사 그룹
* language_code: 언어 코드 (en, kr, jp, cn, fr 등등)

```json
{
  "name": "startup",
  "company_group_name": "",
  "language_code": "en"
}
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "message": "OK"
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "message": "Failure message"
}
```

#### 7. `/search`
`GET` 메소드. 뒤에 붙는 파라미터 목록은 다음과 같다.
* `query_type`: 검색 타입. 회사명 검색인지 혹은 태그 기반 검색인지 정하는 부분.
* `keyword`: 검색어

요청 예시는 다음과 같다.
```
1. 태그 검색
GET /search?query_type=tag&keyword=tag_1

2. 회사명 검색
GET /search?query_type=company&keyword=株式会社
```

정상적인 요청이 이루어지면 다음과 같이 리턴한다.
```json
{
  "companies_list": 
    [
        {
            "company_group_id": 1,
            "company_name": {
                "kr": "ABC 주식회사",
                "en": "ABC LLC"
            }
        },
        {
            "company_group_id": 2,
            "company_name": {
                "kr": "ABC 상사",
                "en": "ABC Trading Co., Ltd."
            }
        }
    ]
}
```
