# API Specifications

#### 1. `/language`
`POST` 메소드. 언어 데이터를 추가할 때 호출하며 요청 바디는 다음과 같이 구성된다.
```
code: 언어 코드를 말함. 영어의 경우 en, 한국어는 kr, 일본어는 jp, 중국어는 cn 등이다.

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
  "response_code": 200,
  "message": ""
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "response_code": 500,
  "message": "Duplicate entry"
}
```

#### 2. `/company-group`
`POST` 메소드. 회사 그룹 데이터를 추가할 때 호출하며 요청 바디는 다음과 같이 구성된다.
```
name: 회사 그룹명.

{
  "name": "좋은 회사"
}
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "response_code": 200,
  "message": ""
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "response_code": 500,
  "message": "Duplicate entry"
}
```

#### 3. `/company-group/tag-group`
##### 1) `POST` 메소드. 회사 그룹에 태그 그룹을 추가한다. 요청 바디는 다음과 같이 구성된다.
```
company_group_name: 회사 그룹명.
tag_group_name: 태그 그룹명.

{
  "company_group_name": "ABC 상사",
  "tag_group_name": "태그"
}
```

이후에 값을 처리하는 로직에 대해서는 [다음 이미지](../../images/flowcharts/add_tag_group_to_company_group.png) 참고.

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "response_code": 200,
  "message": ""
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "response_code": 500,
  "message": "Duplicate entry"
}
```

##### 2) `DELETE` 메소드. 회사 그룹에서 태그 그룹을 삭제해 준다.

#### 4. `/tag-group`
`POST` 메소드. 태그 그룹 데이터를 추가할 때 호출하며 요청 바디는 다음과 같이 구성된다.
```
name: 태그 그룹명.

{
  "name": "스타트"
}
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "response_code": 200,
  "message": ""
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "response_code": 500,
  "message": "Duplicate entry"
}
```

#### 5. `/tag`
##### 1) `POST` 메소드. 태그 데이터를 추가할 때 호출하며 요청 바디는 다음과 같이 구성된다.
```
name: 태그 그룹명.
language_code: 언어 코드
tag_group_id: 태그 그룹명

{
  "name": "startup",
  "language_code": "en",
  "tag_group_name": "startup"
}
```

성공적으로 추가 작업이 이루어지는 경우 다음과 같이 응답을 돌려받는다.
```json
{
  "response_code": 200,
  "message": ""
}
```

중복된 데이터를 추가하려다 실패하는 경우의 응답은 다음과 같다.
```json
{
  "response_code": 500,
  "message": "Duplicate entry"
}
```

#### 6. `/company`

#### 7. `/search`
`GET` 메소드. 뒤에 붙는 파라미터 목록은 다음과 같다.
* `type`: 검색 타입. 회사명 검색인지 혹은 태그 기반 검색인지 정하는 부분.
* `query`: 검색어

예제 요청은 다음과 같다.
```
GET /search?type=tag&query=스타트업
```

정상적인 요청이 이루어지면 다음과 같이 리턴한다.
```
HTTP/1.1 200 OK
{
    "result": [
        {
            "company_name": "ABC 주식회사",
            "tags": [
                "스타트업",
                "100명 이상 직원",
                "강남"
            ]
        },
        ...
    ]
}
```

검색 및 결과 리턴 순서도는 각각 다음 참조.
* [회사명 검색](../../images/flowcharts/search_by_company.png)
* [태그 검색](../../images/flowcharts/search_by_tag.png)
