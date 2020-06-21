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
import re

def downloadhost():
    # Reset hosts folder
    try:
        shutil.rmtree('hosts')
    except FileNotFoundError:
        pass
    os.mkdir("hosts")
    try:
        file = open("hosts/hosts", "w", encoding = 'UTF-8')
    except:
        exit()
    f = open(hostlist, 'r', encoding = 'UTF-8')
    while True:
        line = f.readline()
        if not line: break
        # Host file download
        print("%s : %s" %(hostdownload, line))

        host_name = re.sub('[\/:*?"<>|.]', '', line)
        urllib.request.urlretrieve(line, "hosts/%s" %host_name)

        host = open("hosts/%s" %host_name, "r", encoding = 'UTF-8')
        h = host.read()
        host.close()
        os.remove("hosts/%s" %host_name)
        file.write("\n# %s\n" %line)
        file.write("%s\n\n" %h)
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
    hostlist = "hosts_list.txt"
    hostsfilepath = "C:\Windows\System32\drivers\etc\hosts"

    # Default Settings
    os.system("title Adaway_for_Windows V.%s" %version)
    os.system("mode.com con cols=120 lines=40")

    print("""



               rQBBBBBBBBBBBBBi              
             .BBBBBQBQBBBQBQBBBR.            
            PBBBRQMRMQMRMRgRMQQBBh           
          JBBBBBBBBQBQQQQgMgQRBQBQB7         
        iBBBRB1:1MBBQBBBBBQBQBQBQQBBBi       
        BBQMRQg:.   ...igBBBQ..rBRQQBB       
        QBMMgMBBi:       iPL   :BQMQQB       
        BBQgMgQQRX.           iBBMMMBB       Adaway for Windows V.%s
        BBgMgMgQBB            PBQRgRQB       Developer : 천상의나무
        BBRgRgRgQQM    :.     MBRgMMBB       Loading. . .
        BBMRgRgRMQBBBBBB:    LBQgMgQBB       
        BBBRRgRgRMBBg7     rBBBMRgQQBB       
        :BQBRQgMgRBP      BBQQMMgQBBB:       
          vBBQQgRgQQB2P  hBQQMQRBBBr         
            XBBBMQMQQBBBQBQQgQQBB2           
              QBBBBBBBBQBBBQBBBD             
               iBBBBBBBBQBQBBB:              
    """ %version)

    # Chack admin permission
    if ctypes.windll.shell32.IsUserAnAdmin(): 
        pass
    else:
        print("This program requires administrator privileges.\nPress Enter to run the program again with administrator privileges.")
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
    soup = BeautifulSoup(setting, 'lxml')
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
        soup = BeautifulSoup(languagecode, 'lxml')
        afwver = soup.find("afwver")
        afwver = afwver.get_text()
        # Check compatibility of language packs and programs
        if not afwver == version:
            if afwver == "1.0":
                pass
            else:
                languageerror = soup.find("languageerror")
                languageerror = languageerror.get_text()
                print(languageerror)
                os.system("pause")
                exit()
        nointernet = soup.find("nointernet").get_text()
        verup = soup.find("verup").get_text()
        status = soup.find("status").get_text()
        adawayon = soup.find("adawayon").get_text()
        adawayoff = soup.find("adawayoff").get_text()
        adawayupdate = soup.find("adawayupdate").get_text()
        checkupdate = soup.find("checkupdate").get_text()
        adawaylatestinstall = soup.find("adawaylatestinstall").get_text()
        adawaydisable = soup.find("adawaydisable").get_text()
        hostssource = soup.find("hostssource").get_text()
        hostdownload = soup.find("hostdownload").get_text()
        hostsislatest = soup.find("hostsislatest").get_text()
        hostsisoriginal = soup.find("hostsisoriginal").get_text()
        installing = soup.find("installing").get_text()
        installfinish = soup.find("installfinish").get_text()
        mainchoose = soup.find("mainchoose").get_text()
        afwexit = soup.find("afwexit").get_text()


    # Check your internet connection
    ipaddress = socket.gethostbyname(socket.gethostname())

    # When you have an internet connection
    if not ipaddress == "127.0.0.1":
        # https://github.com/NewPremium/version/blob/master/index.xml
        url = "https://newpremium.github.io/version/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
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

    while True:
        # Start
        file = open(hostsfilepath, "r", encoding = 'UTF-8')
        hosts = file.read()
        file.close()
        if not os.path.exists("backup/hosts"):
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

        downloadhost()

        file = open("hosts/hosts", "r", encoding = 'UTF-8')
        latesthosts = file.read()
        file.close()

        # Set status
        if hosts == backup:
            adawaystatus = adawayoff

        elif hosts == latesthosts:
            adawaystatus = adawayon

        elif not hosts == latesthosts:
            adawaystatus = adawayupdate

        else:
            adawaystatus = "Status error"

        while True:

            os.system("cls")
            print("""------------------------------------------------------------------------------------------------------------------------
%s : %s
------------------------------------------------------------------------------------------------------------------------

               rQBBBBBBBBBBBBBi              
             .BBBBBQBQBBBQBQBBBR.            
            PBBBRQMRMQMRMRgRMQQBBh           
          JBBBBBBBBQBQQQQgMgQRBQBQB7         
        iBBBRB1:1MBBQBBBBBQBQBQBQQBBBi       
        BBQMRQg:.   ...igBBBQ..rBRQQBB       Adaway for Windows
        QBMMgMBBi:       iPL   :BQMQQB       
        BBQgMgQQRX.           iBBMMMBB       1. %s
        BBgMgMgQBB            PBQRgRQB       2. %s
        BBRgRgRgQQM    :.     MBRgMMBB       3. %s
        BBMRgRgRMQBBBBBB:    LBQgMgQBB       4. %s
        BBBRRgRgRMBBg7     rBBBMRgQQBB       5. %s
        :BQBRQgMgRBP      BBQQMMgQBBB:       
          vBBQQgRgQQB2P  hBQQMQRBBBr         
            XBBBMQMQQBBBQBQQgQQBB2           
              QBBBBBBBBQBBBQBBBD             
               iBBBBBBBBQBQBBB:              

------------------------------------------------------------------------------------------------------------------------
""" %(status, adawaystatus, checkupdate, adawaylatestinstall, adawaydisable, hostssource, afwexit))

            choose = input("\n%s : " %mainchoose)

            # Check for updates
            if choose == "1":
                break

            # Install hosts file
            elif choose == "2":
                print(installing)
                while True:
                    if adawaystatus == adawayon or adawaystatus == hostsislatest:
                        adawaystatus = hostsislatest
                        break
                    try:
                        file = open("hosts/hosts", "r", encoding = 'UTF-8')
                        latesthosts = file.read()
                        file.close()
                    except PermissionError:
                        adawaystatus = "Permission Error. Please restart program - latesthosts read error"
                        file.close()
                        break
                    except:
                        adawaystatus = "Unknown error"
                        file.close()
                        break
                    latesthosts = file.read()
                    file.close()
                    try:
                        file = open(hostsfilepath, "w", encoding = 'UTF-8')
                        file.write(latesthosts)
                        file.close()
                    except PermissionError:
                        adawaystatus = "Permission Error. Please restart program - hosts write error"
                        file.close()
                        break
                    except:
                        adawaystatus = "Unknown error"
                        file.close()
                        break
                    # Flush DNS
                    os.system("ipconfig /flushdns")
                    print(installfinish)
                    adawaystatus = adawayon
                    break

            # Restore hosts file
            elif choose == "3":
                while True:
                    if adawaystatus == adawayoff or adawaystatus == hostsisoriginal:
                        adawaystatus = hostsisoriginal
                        break
                    try:
                        file = open(hostsfilepath, "w", encoding = 'UTF-8')
                        file.write(backup)
                        file.close()
                    except PermissionError:
                        adawaystatus = "Permission Error. Please restart program - hosts write error"
                        file.close()
                        break
                    except:
                        adawaystatus = "Unknown error"
                        file.close()
                        break
                    # Flush DNS
                    os.system("ipconfig /flushdns")
                    adawaystatus = adawayoff
                    break

            # Open hosts list
            elif choose == "4":
                os.system("start %s" %hostlist)

            # Exit
            elif choose == "5":
                exit()

            else:
                pass

# This program is not a module!
else:
    exit()
