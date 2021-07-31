# Adaway_for_Windows

[![CodeFactor](https://www.codefactor.io/repository/github/newpremium/adaway_for_windows/badge/master)](https://www.codefactor.io/repository/github/newpremium/adaway_for_windows/overview/master)
![GitHub all releases](https://img.shields.io/github/downloads/ajb3296/Adaway_for_Windows/total?style=flat-square)

## 다운로드

[여기](https://github.com/ajb3296/Adaway_for_Windows/releases) 에서 프로그램 다운로드가 가능합니다.

## 주의사항

  * 이 프로그램은 **GNU GPL 라이센스**가 적용됩니다.
  * Kaspersky 사용자분들은 먼저 카스퍼스키 예외처리에서 C:\Windows\System32\drivers\etc\hosts 경로와 프로그램이 들어있는 폴더를 예외항목에 추가해 주세요.
  * 백신이 설치되어 있다면 프로그램이 들어있는 폴더를 통째로 검사 예외처리 해주세요.
  * 이 프로그램은 관리자 권한이 필요합니다.
  * V3 사용자분들은 hosts 파일 설치 후 hosts 파일 초기화 권장 메시지가 나올 수 있는데 이때 '아니오'를 눌러주세요. '예'를 누르실 경우 hosts 파일을 재설치해야 합니다.
  * hosts 파일 설치 후 재부팅을 **권장**합니다.
  * f-string 사용으로 python3.6 이상 버전에서 실행 가능합니다.
  
  
### Known Issues

  * ~~광고차단을 활성화 할 경우 hosts 파일 설치 후, 그리고 매번 부팅시마다 약 3~5분간 인터넷 접속이 되지 않습니다.~~ --> V.1.1 버전에서 수정된...줄 알았음. 수정중...
  * ~~hosts 파일 다운로드가 더럽게 느립니다.~~ --> V.1.2 버전에서 수정됨(비동기 적용).

## 설명

* 이 프로그램은 [AdAway](https://adaway.org/)의 hosts 파일만 이용했으며 [AdAway](https://adaway.org/) 앱과는 무관한 프로그램입니다.
* 프로그램 사용 중 에러는 증상을 스크린샷과 함께 [여기](https://telegram.me/ajb3296) (먼저 텔레그램을 설치하셔야 합니다) 로 보내주세요.
* 이 프로그램은 GPL 라이선스가 적용되어 있습니다. 사용 중 발생하는 모든 문제의 책임은 사용자에게 있습니다.
* ~~쓰고 싶으면 쓰는 호스트파일입니다 : https://newpremium.github.io/adaway_host/hosts.txt~~ --> V.1.1 부터 기본 
* 호스트 추가는 hosts_list.txt 에 하시면 됩니다.
