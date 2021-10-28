# for Windows : python setup.py py2exe
# for macOS   : python3 setup.py py2app

from setuptools import setup
import platform
import glob
import sys
import os
import shutil
import base64

# Path setting
mainPath = "AdCleaner.py"
hostlist = "hosts_list.txt"
buildFolder = "build"

# Make build folder
try:
    shutil.rmtree(buildFolder)
except FileNotFoundError:
    pass
os.mkdir(buildFolder)

file = open(mainPath, "r", encoding = 'UTF-8')
mainProgram = file.read()
file.close()

print("Code encoding...")
mainProgram = mainProgram.encode("utf-8")
mainProgramEncode = base64.b64encode(mainProgram)

file = open(f"{buildFolder}/{mainPath}", "w", encoding = 'UTF-8')
file.write(f"""import base64
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

code = base64.b64decode({mainProgramEncode})
exec(code.decode("utf-8"))""")
file.close()

print("Copy file...")
shutil.copy2("./hosts_list.txt", f"./{buildFolder}/hosts_list.txt")

print("Copy folder...")
shutil.copytree("./web", f"./{buildFolder}/web")

# For build
ProgramVersion = "2.0"

if platform.system() == "Darwin":
    setup(
        name    = 'AdCleaner',
        version = ProgramVersion,
        author  = 'An Jaebeom',
        app     = [f"{buildFolder}/{mainPath}"],

        data_files=[
            (f'{buildFolder}/web', glob.glob('web/*.*')),
            (f'{buildFolder}/web/css', glob.glob('web/css/*.*')),
            (f'{buildFolder}/web/img', glob.glob('web/img/*.*')),
            (f'{buildFolder}/web/js', glob.glob('web/js/*.*'))
        ],
        setup_requires=['py2app'],

        options={
            'py2app': {
                'iconfile':'icon.icns',
                'includes': ['base64',
                            'os',
                            're',
                            'sys',
                            'eel',
                            'ctypes',
                            'shutil',
                            'socket',
                            'asyncio',
                            'platform',
                            'subprocess',
                            'urllib.request']
            }
        },
    )

elif platform.system() == "Windows":
    
    import py2exe
    import py2exe.build_exe

    def isSystemDLL(pathname):
        dlls = ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll")
        if os.path.basename(pathname).lower() in dlls:
            return 0
        return py2exe.build_exe.isSystemDLL(pathname)
    py2exe.build_exe.isSystemDLL = isSystemDLL

    sys.argv.append('py2exe')
    
    setup(
        name    = 'AdCleaner',
        version = ProgramVersion,
        author  = 'An Jaebeom',
        setup_requires=["py2app"],
        options = {
            'py2exe': {
                'bundle_files': 1, # doesn't work on win64
                'compressed': True,
                'includes': ['base64',
                            'os',
                            're',
                            'sys',
                            'eel',
                            'ctypes',
                            'shutil',
                            'socket',
                            'asyncio',
                            'platform',
                            'subprocess',
                            'urllib.request']
            }
        },
        data_files = [
            (f'{buildFolder}/web', glob.glob('web/*.*')),
            (f'{buildFolder}/web/css', glob.glob('web/css/*.*')),
            (f'{buildFolder}/web/img', glob.glob('web/img/*.*')),
            (f'{buildFolder}/web/js', glob.glob('web/js/*.*'))
        ],

        windows = [{
            'script': f"{buildFolder}/{mainPath}",
            'icon_resources': [
                (1, 'logo.ico')
            ]
        }],

        zipfile=None,
    )

else:
    print("Build fail")

print("Finish!")