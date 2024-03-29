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


eel.init("web")

async def download(url, loop):
    # Make file name
    host_name = "%s.txt" %re.sub('[\/:*?" <> |.]', '', url)
    print(f"Downloading : {url}")
    try:
        await loop.run_in_executor(None, urllib.request.urlretrieve, url, "hosts/%s" %host_name)
    except Exception as a:
        print(f"Download fail : {url}, {a}")
        return "fail"
    else:
        print(f"Download success : {url}")
        return host_name

async def downloadhost(urls, loop):

    fts = [asyncio.ensure_future(download(u, loop)) for u in urls]
    host_name = await asyncio.gather(*fts)
    
    host_name = sorted(host_name)

    try:
        file = open(TempHosts, "a", encoding = 'UTF-8')
    except Exception:
        pass

    for i in host_name:
        if not i == "fail":
            host = open("hosts/%s" %i, "r", encoding = 'UTF-8')
            data = host.read()
            host.close()

            # Remove unnecessary file
            os.remove(f"hosts/{i}")

            file.write(f"{data}\n\n")
    file.close()

@eel.expose
def checkupdate():

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
        urls.append(l.replace("\n", ""))
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
        adawaystatus_code = "off"
        adawaystatus = "Off"

    elif hosts == latesthosts:
        adawaystatus_code = "on"
        adawaystatus = "On"

    elif not hosts == latesthosts:
        adawaystatus_code = "need_update"
        adawaystatus = "Need Update"

    else:
        adawaystatus_code = "error"
        adawaystatus = "Error"

    return [adawaystatus_code, adawaystatus]

@eel.expose
def adawayon():
    # Read latest hosts
    try:
        file = open(TempHosts, "r", encoding = 'UTF-8')
        latesthosts = file.read()
        file.close()
    except Exception:
        status = "Can't read the latest host file"
        file.close()
        return status
    # Write latest hosts in system hosts
    try:
        file = open(hostsfilepath, "w", encoding = 'UTF-8')
        file.write(latesthosts)
        file.close()
    except Exception:
        status = "Can't update the system host file"
        file.close()
        return status
    # Flush DNS
    #subprocess.call("ipconfig /flushdns", shell=False)
    return "finish"

@eel.expose
def adawayoff():
    # Read backup hosts
    try:
        file = open(BackupHosts, "r", encoding = 'UTF-8')
        backup = file.read()
        file.close()
    except Exception:
        status = "Can't open the backup hosts file"
        file.close()
        return status
    # Write hosts
    try:
        file = open(hostsfilepath, "w", encoding = 'UTF-8')
        file.write(backup)
        file.close()
    except Exception:
        status = "Can't roll back the system host"
        file.close()
        return status
    # Flush DNS
    #subprocess.call("ipconfig /flushdns", shell=False)
    return "finish"

# =-=-=-=-=-=-=-=-=-=-=-=-=

@eel.expose
def checkadmin():
    # Windows
    if platform_sys == "Windows":
        # Check admin permission
        try:
            admin_permission = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            admin_permission = False
        if not admin_permission:
            admin_check = "no"
        else:
            admin_check = "yes"
    
    # OSX, Linux
    elif platform_sys == "Darwin" or platform_sys == "Linux":
        if subprocess.check_output("whoami", shell=True, encoding='utf-8').replace("\n", "") == "root":
            admin_check = "yes"
        else:
            admin_check = "no"

    else:
        admin_check = "yes"
    return admin_check

    # For test
    #return "yes"

@eel.expose
def checkinternet():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        internet_check = "yes"
    except socket.error:
        internet_check = "no"
    return internet_check

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
        """
        ##
        # Host Database
        #
        # localhost is used to configure the loopback interface
        # when the system is booting.  Do not change this entry.
        ##
        127.0.0.1	localhost
        255.255.255.255	broadcasthost
        ::1             localhost
        """
        if os.path.exists("/etc/hosts"):
            hostsfilepath = "/etc/hosts"
        else:
            hostsfilepath = "/private/etc/hosts"

    elif platform_sys == "Windows":
        hostsfilepath = "C:\Windows\System32\drivers\etc\hosts"
    
    else:
        exit()

    program_name = "AdCleaner"

    eel.start("index.html")