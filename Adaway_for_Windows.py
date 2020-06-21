#-*- coding: utf-8 -*-

# Modules import
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
import multiprocessing

def download(url, host_name, host_download_fail, host_download_success):
    try:
        urllib.request.urlretrieve(url, "hosts/%s" %host_name)

    except Exception as e:
        print("%s : %s" %(host_download_fail, url))

    else:
        print("%s : %s" %(host_download_success, url))
        host = open("hosts/%s" %host_name, "r", encoding = 'UTF-8')
        data = host.read()
        host.close()
        # Remove unnecessary files
        os.remove("hosts/%s" %host_name)

        while True:
            try:
                file = open("hosts/hosts", "a", encoding = 'UTF-8')
            except:
                pass
            else:
                break
        file.write("\n# %s\n\n" %url)
        file.write("%s\n\n" %data)
        file.close()
    return

def downloadhost(host_download, host_download_fail, host_download_success):
    q = multiprocessing.Queue()
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
    file.write("# Adaway for Windows\n")
    file.close()

    # Read host list
    f = open(hostlist, 'r', encoding = 'UTF-8')
    while True:
        l = f.readline()
        if not l:
            break

        print("%s : %s" %(host_download, l))

        # Make file name
        host_name = re.sub('[\/:*?"<>|.]', '', l)

        multiprocessing.Process(target=download, args=(l, host_name, host_download_fail, host_download_success)).start()
    
    q.join()
    f.close()
    return

def main():

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
            languageerror = soup.find("languageerror")
            languageerror = languageerror.get_text()
            print(languageerror)
            os.system("pause")
            exit()
        nointernet = soup.find("nointernet").get_text()
        verup = soup.find("verup").get_text()
        status = soup.find("status").get_text()
        adaway_on = soup.find("adaway_on").get_text()
        adaway_off = soup.find("adaway_off").get_text()
        adaway_update = soup.find("adaway_update").get_text()
        check_update = soup.find("check_update").get_text()
        adaway_latest_install = soup.find("adaway_latest_install").get_text()
        adaway_disable = soup.find("adaway_disable").get_text()
        hosts_source = soup.find("hosts_source").get_text()
        host_download = soup.find("host_download").get_text()
        hosts_is_latest = soup.find("hosts_is_latest").get_text()
        hosts_is_original = soup.find("hosts_is_original").get_text()
        installing = soup.find("installing").get_text()
        install_finish = soup.find("install_finish").get_text()
        main_choose = soup.find("main_choose").get_text()
        afw_exit = soup.find("afw_exit").get_text()
        host_download_fail = soup.find("host_download_fail").get_text()
        host_download_success = soup.find("host_download_success").get_text()

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

        downloadhost(host_download, host_download_fail, host_download_success)

        file = open("hosts/hosts", "r", encoding = 'UTF-8')
        latesthosts = file.read()
        file.close()

        # Set status
        if hosts == backup:
            adawaystatus = adaway_off

        elif hosts == latesthosts:
            adawaystatus = adaway_on

        elif not hosts == latesthosts:
            adawaystatus = adaway_update

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
""" %(status, adawaystatus, check_update, adaway_latest_install, adaway_disable, hosts_source, afw_exit))

            choose = input("\n%s : " %main_choose)

            # Check for updates
            if choose == "1":
                break

            # Install hosts file
            elif choose == "2":
                print(installing)
                while True:
                    if adawaystatus == adaway_on or adawaystatus == hosts_is_latest:
                        adawaystatus = hosts_is_latest
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
                    print(install_finish)
                    adawaystatus = adaway_on
                    break

            # Restore hosts file
            elif choose == "3":
                while True:
                    if adawaystatus == adaway_off or adawaystatus == hosts_is_original:
                        adawaystatus = hosts_is_original
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
                    adawaystatus = adaway_off
                    break

            # Open hosts list
            elif choose == "4":
                os.system("start %s" %hostlist)

            # Exit
            elif choose == "5":
                exit()

            else:
                pass

if __name__ == "__main__":

    if not os.path.exists("system/Adaway_for_Windows"):
        print("Please unzip the file properly and execute it.\n\nPress the ENTER key to exit the program.")
        os.system("pause")
        exit()
    # Main program version
    version = "1.2"

    # Host file list path setting
    hostlist = "hosts_list.txt"
    hostsfilepath = "C:\Windows\System32\drivers\etc\hosts"
    main()
