# 프로젝트 소개

네이버 부동산에서 제공해주는 데이터를 크롤링하는 프로그램

## 목적

매매물건을 크롤링후 거래방식, 가격, 면적, 층수, 평단가(최대값,최소값, 중앙값, 평균값, 최빈값), 대략적인 위치 표시

## 순차도

작업전 선택사항

1. 지역 : url로 받음(zoom 19고정)  
   ex) https://new.land.naver.com/offices?ms=37.5470331,126.923912,19&a=SG:SMS:GJCG:APTHGJ:GM:TJ&e=RETAIL

2. 매매종류 : 종류중 하나만 되도록  
   ex) 상가, 사무실, 공장/창고, 지식산업센터, 건물, 토지 존재  
   상가도 일반상가,복합상가등 종류가 다양함으로 추후 개선예정

작업중

1. 브라우저 열기
2. 입력받은 url로 이동
3. 지도에 표시된 동그라미 선택
4. 좌측의 스크롤 최대로 밑으로 내리기 후 캡쳐
5. 좌측에 표시된 매매정보 크롤링
6. 캡쳐한 이미지와 수집한 데이터 저장
7. 3-7반복

## 업그레이드 부분

1. 매매종류를 여러게 지정
2. 텔레그램 및 sns를 이용해서 현재위치보내면 현재위치를 기준으로 매매정보 및 데이터 받기
3. 중도 정지기능
4. 응용프로그램처럼 항상 실행상태를 유지했으면 함
5. 예외처리에 대해 준비가 더 필요해보임

## 파일설명

1. requirements.txt : 설치한 패키지 목록
2. LICENSE.chromedriver : 크롬 드라이버 라이선스
3. chromedriver.exe : 크롬 드라이버
4. excle.py : 엑셀 코드
5. crawling.py : 크롤링 코드
6. run.py : 실행코드
7. result 폴더 : 실행결과 파일이 저장됨

## 실행환경

Windows  
python 3.9.7  
selenium 4.8.0
chrome driver 109.0.5414.120  
https://chromedriver.chromium.org/downloads 에서 자신의 버전과 맞는걸 설치  
beautifulsoup4 4.11.1
openpyxl 3.1.0  
Pillow-9.4.0

## 동작화면

![run](https://user-images.githubusercontent.com/86402585/216768037-075a2fc9-7a0a-4435-886e-9c19a297567d.gif)
