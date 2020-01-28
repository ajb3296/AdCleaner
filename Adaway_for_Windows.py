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
import ctypes

if __name__ == "__main__":
    
    # Check the status of the zip file
    if not os.path.exists("system/Adaway_for_Windows"):
        print("Please unzip the file properly and execute it.\n\nPress the ENTER key to exit the program.")
        os.system("pause")
        exit()

    # Main program version
    version = "1.0"

    # Default Settings
    os.system("title Adaway_for_Windows V.%s" %version)
    os.system("mode.com con cols=120 lines=40")

    print("""

    Adaway for Windows

    Version : V.%s
    Loading. . .
    """ %version)

    language = "language"

    if ctypes.windll.shell32.IsUserAnAdmin(): 
        pass
    else:
        print("This program requires administrator privileges.\nPlease run the program again with administrative authority.")
        os.system("pause")
        exit()

    while True:
        # Select language if setting file does not exist
        if not os.path.exists("setting.xml"):
            print("\nPlease select a language.\n")
            for file in os.listdir("language"):
                if file.endswith(".xml"):
                    print(file)

            language = input("\nEnter file name excluding filename extension : ")

            if os.path.exists("language/%s.xml" %language):

                # Create setting file
                file = open("setting.xml", "w", encoding = 'UTF-8')
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write("<!-- Language (언어) -->\n")
                file.write("<language>%s</language>\n" %language)
                file.close()

                break
            else:
                os.system("cls")
                print("The language pack for the language you entered does not exist.\nAdd the desired language pack to the language folder or select another language.")
        else:
            break

    # Reading setting file
    file = open("setting.xml", "r", encoding = 'UTF-8')
    setting = file.read()
    file.close()
    soup = BeautifulSoup(setting, 'html.parser')
    language = soup.find("language")
    language = language.get_text()

    # Check for the existence of language packs for the language you want to use
    if not os.path.exists("language/%s.xml" %language):
        print("The language pack for the language you entered does not exist.\nAdd the desired language pack to the language folder or select another language.")
        os.system("pause")
        exit()

    else:
        # Reading language pack
        file = open("language/%s.xml" %language, "r", encoding = 'UTF-8')
        languagecode = file.read()
        file.close()
        soup = BeautifulSoup(languagecode, 'html.parser')
        verup = soup.find("verup")
        verup = verup.get_text()

    # Check your internet connection
    ipaddress = socket.gethostbyname(socket.gethostname())

    # When you have an internet connection
    if not ipaddress == "127.0.0.1":
        # https://github.com/NewPremium/version/blob/master/index.xml
        url = "https://newpremium.github.io/version/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        afw = soup.find("afw")
        afw = afw.get_text()
        afwdownload = soup.find("afwdownload")
        afwdownload = afwdownload.get_text()

        # Version chack
        if not afw == version:
            print(verup)
            time.sleep(3)
            webbrowser.open_new(afwdownload)
            exit()

    # Pass the version check when there is no internet connection.
    else:
        pass

    # Start
    print("기초 설정및 체크 완료")

# This program is not a module!
else:
    exit()
