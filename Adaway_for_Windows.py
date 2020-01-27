#-*- coding: utf-8 -*-

# Module import
import os
import time
from bs4 import BeautifulSoup
import requests
import urllib.request
import zipfile
import shutil
import socket
import webbrowser

if __name__ == "__main__":
    
    # 압축 상태 확인
    if not os.path.exists("system/Adaway_for_Windows"):
        print("Please unzip the file properly and execute it.\n\nPress the ENTER key to exit the program.")
        os.system("pause")
        exit()

    # 메인파일 버전
    mainafw = "1.0"

    if os.path.exists("system/ver"):
        file = open("system/ver", "r", encoding = 'UTF-8')
        version = file.read()
        file.close()
    else:
        version = "*.*"

    # 기본설정
    os.system("title Adaway_for_Windows V.%s" %version)
    os.system("mode.com con cols=120 lines=40")

    print("""

    Adaway for Windows

    Version : V.%s
    Loading. . .
    """ %version)

    language = "language"

    while True:
        # 설정파일이 존재하지 않을 경우 언어 선택
        if not os.path.exists("setting.xml"):
            print("""언어를 선택하세요
Please select a language
1. 한글 - Korean
2. English - 영어
""")

            language = input("<1/2> : ")

            if language == '1' or language == 'ko' or language == '한글' or language == 'korean':
                language = "ko"
                break
            elif language == '2' or language == 'en' or language == '영어' or language == "english":
                language = "en"
                break
            else:
                pass
        else:
            break
    # 설정파일 만들기
    if language == "ko" or language == "en":
        file = open("setting.xml", "w", encoding = 'UTF-8')
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write("<!-- Language (언어) -->\n")
        file.write("<language>%s</language>\n\n" %language)
        file.write("<!-- File name (미끼파일 이름) -->\n")
        file.write("<filename>EICAR.TXT</filename>\n\n")
        file.write("<!-- File internal code (미끼파일 내부 코드) -->\n")
        file.write("<!-- default value  (기본값) : X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H* -->\n")
        file.write("<fileinside>X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*</fileinside>\n")
        file.close()
    else:
        pass

    # 설정파일 읽어오기
    file = open("setting.xml", "r", encoding = 'UTF-8')
    html = file.read()
    file.close()
    soup = BeautifulSoup(html, 'html.parser')
    language = soup.find("language")
    language = language.get_text()
    filename = soup.find("filename")
    filename = filename.get_text()
    fileinside = soup.find("fileinside")
    fileinside = fileinside.get_text()

    # 프로그램이 사용 가능한 언어인지 확인
    if language == "ko" or language == "en":
        pass
    
    # 지원하지 않는 언어일 경우
    else:
        print("Language error\n언어오류\n\nModify the language settings of the setting.xml file(en/ko)\nsetting.xml 파일의 언어설정을 수정하세요(en/ko)")
        os.system("pause")
        exit()

    # 인터넷 연결 확인
    ipaddress = socket.gethostbyname(socket.gethostname())

    # 인터넷 연결이 안되어 있을때
    if ipaddress == "127.0.0.1":

        # 이전에 다운받은 버전 존재 확인
        if os.path.exists("system/rtitpath"):
            file = open("system/rtitpath", "r", encoding = 'UTF-8')
            rtitpath=file.read()
            file.close()
            # 이전에 설치해둔 버전 실행
            os.system("call %s" %rtitpath)

        # 이전에 받아둔 버전이 없을 경우
        else:
            if language == "ko":
                print("\n    컴퓨터가 인터넷에 연결되어 있지 않고 이전에 설치한 프로그램이 존재하지 않습니다.\n    ENTER 키를 누르시면 종료합니다.")
                os.system("pause>nul")
                exit()
            else:
                print("\n    Your computer is not connected to the Internet and there are no programs installed previously.\n    Press ENTER to exit.")
                os.system("pause>nul")
                exit()

    # 인터넷 연결되어 있을때
    else:
        pass

    # 버전 확인
    url = "https://newpremium.github.io/version/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    rtit = soup.find("rtit")
    rtit = rtit.get_text()
    rtitdownload = soup.find("rtitdownload")
    url = rtitdownload.get_text()
    rtitpath1 = soup.find("rtitpath1")
    rtitpath1 = rtitpath1.get_text()
    rtitpath2 = soup.find("rtitpath2")
    rtitpath2 = rtitpath2.get_text()
    rtitmainver = soup.find("rtitmainver")
    rtitmainver = rtitmainver.get_text()
    rtitmainlink = soup.find("rtitmainlink")
    rtitmainlink = rtitmainlink.get_text()

    # 메인파일 버전 확인
    if not rtitmainver == mainafw:
        if language == "ko":
            updatemsg = "메인 프로그램을 업데이트 해야 합니다. 3초후 다운로드 사이트로 이동합니다."
        else:
            updatemsg = "You need to update the main program. Go to the download site in 3 seconds."
        print(updatemsg)
        time.sleep(3)
        webbrowser.open_new(rtitmainlink)
        exit()

    # 설치된 버전과 최신버전이 다를때
    if not rtit == version:
        if language == "ko":
            updatemsg = "프로그램을 새 버전으로 업데이트 해야 합니다. 자동으로 업데이트가 진행됩니다."
        else:
            updatemsg = "You need to update the program to a new version. The update will proceed automatically."
        print(updatemsg)
        
        # 업데이트 폴더 초기화
        try:
            shutil.rmtree('update')
        except FileNotFoundError:
            pass
        os.mkdir("update")

        # 최신버전 다운로드
        urllib.request.urlretrieve(url, "update/update.zip")

        # 압축풀기
        zip_ref = zipfile.ZipFile("update/update.zip", 'r')
        zip_ref.extractall("update")
        zip_ref.close()

        # 다운로드한 압축파일 삭제
        if os.path.isfile("update/update.zip"):
            os.remove("update/update.zip")

        # 설정파일 설치
        file = open("%s/setting.xml" %rtitpath2, "w", encoding = 'UTF-8')
        file.write(html)
        file.close()

        # 이전버전 다운로드 기록 저장 / 현재 버전 확인용
        file = open("system/ver", "w", encoding = 'UTF-8')
        file.write(rtit)
        file.close()

        # 이전버전 경로저장 / 인터넷 연결 없을때 이용
        file = open("system/path", "w", encoding = 'UTF-8')
        file.write(rtitpath1)
        file.close()

        # 최신버전 실행
        os.system("call %s" %rtitpath1)
        exit()

    # 업데이트가 필요하지 않을 경우
    else:
        # 설정파일 설치
        file = open("%s/setting.xml" %rtitpath2, "w", encoding = 'UTF-8')
        file.write(html)
        file.close()

        # 실행
        os.system("call %s" %rtitpath1)

# 이 프로그램은 모듈이 아닙니다!
else:
    exit()