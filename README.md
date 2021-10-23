# 파이썬 HTTP 처리의 기본: WSGI 부터 ASGI까지

+ 이 Repository는 파이썬을 통한 HTTP 처리를 설명한다.

+ 이 Repository를 통해 학습하려는 사용자는 아래의 선수 지식이 필요하다
  + 웹
  + HTTP 프로토콜

## 웹(The Web)이란?

+ 팀 버너스 리 경이 만든 월드 와이드 웹의 줄임말이다.
+ 정보 검색 시스템이다.
+ HTTP 프로토콜을 기반으로 HTML로 작성된 하이퍼텍스트를 웹 브라우저로 읽을 수 있도록 구성되어있다.

### References:
+ https://developer.mozilla.org/en-US/docs/Glossary/World_Wide_Web
+ https://en.wikipedia.org/wiki/World_Wide_Web

## HTTP 프로토콜?

+ 클라이언트와 서버 간 이루어지는 요청-응답 프로토콜이다
+ 월드 와이드 웹으로 엮인 하이퍼텍스트를 조회하는 용도로 시작되었다
+ 요청 메시지와 응답 메시지를 기본적으로 알 필요가 있다
  + 요청 메시지 문법
    + 요청라인
      + 요청 메소드 (e.g. `GET`, `POST`, ...)
    + Header
    + 공란
    + Body
  + 응답 메시지 문법
    + 상태 라인
      + 상태 코드 (e.g. `200`, `404`, ...)
    + Header
    + 공란
    + Body

### References:
+ https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol
+ https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
