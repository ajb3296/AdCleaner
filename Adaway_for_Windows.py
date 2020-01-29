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

def hostdownload():
    file = open("hosts/hosts", "w", encoding = 'UTF-8')
    f = open(hostlist, 'r', encoding = 'UTF-8')
    while True:
        line = f.readline()
        if not line: break
        r = requests.get(line)
        file.write("%s\n\n"r)
    f.close()
    file.close()

if __name__ == "__main__":
    
    # Check the status of the zip file
    if not os.path.exists("system/Adaway_for_Windows"):
        print("Please unzip the file properly and execute it.\n\nPress the ENTER key to exit the program.")
        os.system("pause")
        exit()

    # Main program version
    version = "1.0"

    # Host file list path setting
    hostlist = "host_list.txt"

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
        afwver = soup.find("afwver")
        afwver = afwver.get_text()
        if not afwver == version:
            languageerror = soup.find("languageerror")
            languageerror = languageerror.get_text()
            print(languageerror)
            os.system("pause")
            exit()
        nointernet = soup.find("nointernet")
        nointernet = nointernet.get_text()
        verup = soup.find("verup")
        verup = verup.get_text()
        status = soup.find("status")
        status = status.get_text()
        adawaylatest = soup.find("adawaylatest")
        adawaylatest = adawaylatest.get_text()
        adawayoff = soup.find("adawayoff")
        adawayoff = adawayoff.get_text()


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

    # When you are not connected to the Internet
    else:
        print(nointernet)
        os.system("pause")
        exit()

    # Start
    file = open("C:\Windows\System32\drivers\etc\hosts", "r", encoding = 'UTF-8')
    hosts = file.read()
    file.close()
    if not os.path.exist("backup/hosts"):
        # Backup of existing 'C:\Windows\System32\drivers\etc\hosts' file on first run of the program
        try:
            shutil.rmtree('backup')
        except FileNotFoundError:
            pass
        os.mkdir("backup")
        file = open("backup/hosts", "w", encoding = 'UTF-8')
        file.write(hosts)
        file.close()

    file = open("backup/hosts", "r", encoding = 'UTF-8')
    backup = file.read()
    file.close()
    hostdownload()
    if hosts == backup:
        adawaystatus = adawayoff

    file = open("hosts/hosts", "r", encoding = 'UTF-8')
    latesthosts = file.read()
    file.close()
    elif latesthosts == backup:
        adawaystatus = adawaylatest

    else:
        adawaystatus = adawaylatest



    os.system("cls")
    print("""------------------------------------------------------------------------------------------------------------------------
%s : %s
""" %(status, adawaystatus))

# This program is not a module!
else:
    exit()
