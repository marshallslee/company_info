# **회사 정보 검색 프로그램**

데이터베이스에 저장되어 있는 회사 정보를 회사 혹은 태그를 통해 검색하는 프로그램.

## 1. How to Run

본 프로그램은 다음 환경을 기반으로 구성되었다.
* Python: `3.6.8`
* Flask: `1.1.2`
* MySQL: `5.7.29` 

커맨드라인으로 실행하는 것으로 가정, 다음과 같이 진행한다.
###### 1) 가상환경 설치
```
$python -m venv venv
```

###### 2) 가상환경 활성화
```
$source venv/bin/activate
```

###### 3) `requirements.txt` 파일에 명시된 패키지를 설치하기 위해 
```
$pip install -r requirements.txt
```

###### 4) 애플리케이션 실행
```
$python -m flask run
```

## 2. Basic Rules
##### 1) 회사명 검색
* 회사명의 일부만으로도 검색이 된다.

##### 2) 태그 검색
* 태그 검색을 통해 관련된 회사가 검색되어야 한다.
* 다국어로 검색이 가능하다.
    * 일본어 태그로 검색을 해도 한국 회사가 노출이 된다.

## [3. DB Modeling](docs/kr/db-modeling.md)

## [4. API Specifications](docs/kr/api-specifications.md)
