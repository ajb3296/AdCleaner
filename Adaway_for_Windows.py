import os
import re
import sys
import eel
import ctypes
import shutil
import socket
import asyncio
import platform
import subprocess
import urllib.request
from urllib import parse

#from config import main_path, port, title, black_list, log


eel.init("web")

async def download(url, loop):
    # Make file name
    host_name = "%s.txt" %re.sub('[\/:*?" <> |.]', '', url).replace('\n', '')
    print(f" : {url}")
    try:
        await loop.run_in_executor(None, urllib.request.urlretrieve, url, "hosts/%s" %host_name)
    except Exception as a:
        print(f"다운로드 실패 : {url}, {a}")
        return "fail"
    else:
        print(f"다운로드 성공 : {url}")
        return host_name

async def downloadhost(urls, loop):

    fts = [asyncio.ensure_future(download(u, loop)) for u in urls]
    r = await asyncio.gather(*fts)

    try:
        file = open(TempHosts, "a", encoding = 'UTF-8')
    except Exception:
        pass

    for i in r:
        if not i == "fail":
            host = open("hosts/%s" %i, "r", encoding = 'UTF-8')
            data = host.read()
            host.close()

            # Remove unnecessary file
            os.remove(f"hosts/{i}")

            file.write(f"{data}\n\n")
    file.close()

@eel.expose
def chackupdate():

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
    file.write("# Adaway for Windows\n")
    file.close()

    # Hosts Download
    loop = asyncio.get_event_loop()
    loop.run_until_complete(downloadhost(urls, loop))
    loop.close

    file = open(TempHosts, "r", encoding = 'UTF-8')
    latesthosts = file.read()
    file.close()

    # Set status
    if hosts == backup:
        adawaystatus = "Off"

    elif hosts == latesthosts:
        adawaystatus = "On"

    elif not hosts == latesthosts:
        adawaystatus = "Need update"

    else:
        adawaystatus = "Status error"

    return adawaystatus

@eel.expose
def adawayon():
    # Read latest hosts
    try:
        file = open(TempHosts, "r", encoding = 'UTF-8')
        latesthosts = file.read()
        file.close()
    except Exception:
        status = "fail"
        file.close()
        return status
    # Write latest hosts in system hosts
    try:
        file = open(hostsfilepath, "w", encoding = 'UTF-8')
        file.write(latesthosts)
        file.close()
    except Exception:
        status = "fail"
        file.close()
        return status
    # Flush DNS
    subprocess.call("ipconfig /flushdns", shell=False)
    return "finish"

@eel.expose
def adawayoff():
    # Read backup hosts
    try:
        file = open(BackupHosts, "r", encoding = 'UTF-8')
        backup = file.read()
        file.close()
    except Exception:
        status = "fail"
        file.close()
        return status
    # Write hosts
    try:
        file = open(hostsfilepath, "w", encoding = 'UTF-8')
        file.write(backup)
        file.close()
    except Exception:
        status = "fail"
        file.close()
        return status
    # Flush DNS
    subprocess.call("ipconfig /flushdns", shell=False)
    return "finish"

# =-=-=-=-=-=-=-=-=-=-=-=-=

@eel.expose
def chackadmin():
    # Chack admin permission
    try:
        admin_permission = ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        admin_permission = False
    if not admin_permission:
        admin_chack = "no"
    else:
        admin_chack = "yes"
    return admin_chack

@eel.expose
def chackinternet():
    try:
        ipaddress = socket.gethostbyname(socket.gethostname())
    except Exception:
        ipaddress = "127.0.0.1"
    if ipaddress == "127.0.0.1":
        internet_chack = "no"
    else:
        internet_chack = "yes"
    return internet_chack

@eel.expose
def shutdown():
    sys.exit()

if __name__ == '__main__':
    # Main program version
    version = "2.0"

    # Path setting
    TempHosts = "hosts/hosts"
    BackupHosts = "backup/hosts"
    hostlist = "hosts_list.txt"

    platform_sys = platform.system()
    if platform_sys == "Linux":
        hostsfilepath = "/etc/hosts"

    elif platform_sys == "Darwin":
        if os.path.exists("/etc/hosts"):
            hostsfilepath = "/etc/hosts"
        else:
            hostsfilepath = "/private/etc/hosts"

    elif platform_sys == "Windows":
        hostsfilepath = "C:\Windows\System32\drivers\etc\hosts"

    program_name = "Adaway for Windows"

    eel.start("index.html")