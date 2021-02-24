#-*- coding: utf-8 -*-

# Modules import
import os
import time
from bs4 import BeautifulSoup
import requests
import urllib.request
import shutil
import socket
import webbrowser
import ctypes
import re
import asyncio
import subprocess

async def download(url):
    # Make file name
    host_name = "%s.txt" %re.sub('[\/:*?" <> |.]', '', url).replace('\n', '')
    print(f"{host_download} : {url}")
    try:
        await loop.run_in_executor(None, urllib.request.urlretrieve, url, "hosts/%s" %host_name)
    except Exception:
        print(f"{host_download_fail} : {url}")
        return "fail"
    else:
        print(f"{host_download_success} : {url}")
        return host_name

async def downloadhost():

    fts = [asyncio.ensure_future(download(u)) for u in urls]
    r = await asyncio.gather(*fts)

    try:
        file = open(TempHosts, "a", encoding = 'UTF-8')
    except Exception:
        print(temp_host_error)

    for i in r:
        if not i == "fail":
            host = open("hosts/%s" %i, "r", encoding = 'UTF-8')
            data = host.read()
            host.close()

            # Remove unnecessary file
            os.remove(f"hosts/{i}")

            file.write(f"{data}\n\n")
    file.close()

if __name__ == "__main__":

    if not os.path.exists("system/Adaway_for_Windows"):
        print("Please unzip the file properly and execute it.\n\nPress the ENTER key to exit the program.")
        subprocess.call("pause", shell=False)
        exit()

    # Main program version
    version = "1.2"

    # Path setting
    TempHosts = "hosts/hosts"
    BackupHosts = "backup/hosts"
    hostlist = "hosts_list.txt"
    hostsfilepath = "C:\Windows\System32\drivers\etc\hosts"

    program_name = "Adaway for Windows"

    # Default Settings
    subprocess.call(f"title {program_name.replace(' ', '_')} V.{version}", shell=False)
    subprocess.call("mode.com con cols=120 lines=40", shell=False)

    SettingPath = "setting.xml"

    print(f"""
               rQBBBBBBBBBBBBBi              
             .BBBBBQBQBBBQBQBBBR.            
            PBBBRQMRMQMRMRgRMQQBBh           
          JBBBBBBBBQBQQQQgMgQRBQBQB7         
        iBBBRB1:1MBBQBBBBBQBQBQBQQBBBi       
        BBQMRQg:.   ...igBBBQ..rBRQQBB       
        QBMMgMBBi:       iPL   :BQMQQB       
        BBQgMgQQRX.           iBBMMMBB       {program_name} V.{version}
        BBgMgMgQBB            PBQRgRQB       Developer : 천상의나무
        BBRgRgRgQQM    :.     MBRgMMBB       Loading. . .
        BBMRgRgRMQBBBBBB:    LBQgMgQBB       
        BBBRRgRgRMBBg7     rBBBMRgQQBB       
        :BQBRQgMgRBP      BBQQMMgQBBB:       
          vBBQQgRgQQB2P  hBQQMQRBBBr         
            XBBBMQMQQBBBQBQQgQQBB2           
              QBBBBBBBBQBBBQBBBD             
               iBBBBBBBBQBQBBB:              
    """)
    
    # Chack admin permission
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("This program requires administrator privileges.\nPress Enter to run the program again with administrator privileges.")
        subprocess.call("pause", shell=False)
        exit()
    
    while True:
        # Select language if setting file does not exist
        if not os.path.exists(SettingPath):
            print("\nPlease select a language.\n")
            for file in os.listdir("language"):
                if file.endswith(".xml"):
                    print(file)

            language = input("\nEnter file name excluding filename extension : ")

            if os.path.exists(f"language/{language}.xml"):

                # Create setting file
                file = open(SettingPath, "w", encoding = 'UTF-8')
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write("<!-- Language (언어) -->\n")
                file.write(f"<language>{language}</language>\n")
                file.close()

                break
            else:
                subprocess.call("cls", shell=False)
                print("The language pack for the language you entered does not exist.\nAdd the desired language pack to the language folder or select another language.")
        else:
            break

    # Reading setting file
    file = open(SettingPath, "r", encoding = 'UTF-8')
    setting = file.read()
    file.close()
    soup = BeautifulSoup(setting, 'lxml')
    language = soup.find("language")
    language = language.get_text()
    language_path = (f"language/{language}.xml")

    # Check for the existence of language packs for the language you want to use
    if not os.path.exists(language_path):
        print("The language pack for the language you entered does not exist.\nAdd the desired language pack to the language folder or select another language.")
        subprocess.call("pause", shell=False)
        exit()

    else:

        # Reading language pack
        file = open(language_path, "r", encoding = 'UTF-8')
        languagecode = file.read()
        file.close()
        soup = BeautifulSoup(languagecode, 'lxml')
        afwver = soup.find("afwver")
        afwver = afwver.get_text()
        # Check compatibility of language packs and programs
        if not afwver == version:
            languageerror = soup.find("languageerror").get_text()
            print(languageerror)
            subprocess.call("pause", shell=False)
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
        temp_host_error = soup.find("temp_host_error").get_text()

        Unknown_error = "Unknown error"
    
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
        subprocess.call("pause", shell=False)
        exit()

    while True:
        # Start
        file = open(hostsfilepath, "r", encoding = 'UTF-8')
        hosts = file.read()
        file.close()
        if not os.path.exists(BackupHosts):
            # Backup of existing 'C:\Windows\System32\drivers\etc\hosts' file on first run of the program
            try:
                shutil.rmtree('backup')
            except FileNotFoundError:
                pass
            os.mkdir("backup")
            file = open(BackupHosts, "w", encoding = 'UTF-8')
            file.write(hosts)
            file.close()

        file = open(BackupHosts, "r", encoding = 'UTF-8')
        backup = file.read()
        file.close()

        urls = []
        f = open(hostlist, 'r', encoding = 'UTF-8')
        while True:
            l = f.readline()
            if not l:
                break
            urls.append(l)
        f.close()

        # Make hosts folder	
        try:	
            shutil.rmtree('hosts')	
        except FileNotFoundError:	
            pass	
        os.mkdir("hosts")

        # Make temp hosts file
        try:
            file = open(TempHosts, "w", encoding = 'UTF-8')
        except:
            raise PermissionError(f'Failed to create temporary {TempHosts}')
        file.write("# Adaway for Windows")
        file.close()

        # Hosts Download                    
        asyncio.run(downloadhost())

        file = open(TempHosts, "r", encoding = 'UTF-8')
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
            subprocess.call("cls", shell=False)
            print(f"""------------------------------------------------------------------------------------------------------------------------
{status} : {adawaystatus}
------------------------------------------------------------------------------------------------------------------------
               rQBBBBBBBBBBBBBi              
             .BBBBBQBQBBBQBQBBBR.            
            PBBBRQMRMQMRMRgRMQQBBh           
          JBBBBBBBBQBQQQQgMgQRBQBQB7         
        iBBBRB1:1MBBQBBBBBQBQBQBQQBBBi       
        BBQMRQg:.   ...igBBBQ..rBRQQBB       {program_name}
        QBMMgMBBi:       iPL   :BQMQQB       
        BBQgMgQQRX.           iBBMMMBB       1. {check_update}
        BBgMgMgQBB            PBQRgRQB       2. {adaway_latest_install}
        BBRgRgRgQQM    :.     MBRgMMBB       3. {adaway_disable}
        BBMRgRgRMQBBBBBB:    LBQgMgQBB       4. {hosts_source}
        BBBRRgRgRMBBg7     rBBBMRgQQBB       5. {afw_exit}
        :BQBRQgMgRBP      BBQQMMgQBBB:       
          vBBQQgRgQQB2P  hBQQMQRBBBr         
            XBBBMQMQQBBBQBQQgQQBB2           
              QBBBBBBBBQBBBQBBBD             
               iBBBBBBBBQBQBBB:              
------------------------------------------------------------------------------------------------------------------------
""")

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
                        file = open(TempHosts, "r", encoding = 'UTF-8')
                        latesthosts = file.read()
                        file.close()
                    except PermissionError:
                        adawaystatus = "Permission Error. Please restart program - latesthosts read error"
                        file.close()
                        break
                    except Exception:
                        adawaystatus = Unknown_error
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
                    except Exception:
                        adawaystatus = Unknown_error
                        file.close()
                        break
                    # Flush DNS
                    subprocess.call("ipconfig /flushdns", shell=False)
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
                    except Exception:
                        adawaystatus = "Unknown error"
                        file.close()
                        break
                    # Flush DNS
                    subprocess.call("ipconfig /flushdns", shell=False)
                    adawaystatus = adaway_off
                    break

            # Open hosts list
            elif choose == "4":
                subprocess.call(f"start {hostlist}", shell=False)

            # Exit
            elif choose == "5":
                exit()

            else:
                pass
