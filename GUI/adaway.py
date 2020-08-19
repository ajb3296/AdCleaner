# -*- coding: utf-8 -*-

import kivy
kivy.require('1.9.0')

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.config import Config

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import CoverBehavior
from kivy.uix.image import Image

from kivy.uix.label import Label
from kivy.lang import Builder

import os
from bs4 import BeautifulSoup
import socket
import requests
import webbrowser
import re
import asyncio
import urllib.request

# Error
class OtherError(FloatLayout):
    pass
class OtherErrorApp(App):
    def build(self):
        self.title = title_bar
        if img_exist:
            Builder.load_string(f"""

<OtherError>

    orientation:"vertical"

    CoverImage:
        source: '{background_img}'

    Label:
        text: '{error_txt}'
        font_size: '15sp'

    Button:
        text: "Exit"
        font_size: '20sp'
        background_normal: '{normal_button}'
        background_down: '{pushed_button}'
        size_hint: 1, .1
        on_release: exit(1)

<CoverImage@CoverBehavior+Image>:
    reference_size: self.texture_size
""")


        else:
            Builder.load_string(f"""
<OtherError>

    orientation:"vertical"

    Label:
        text: '{error_txt}'
        font_size: '15sp'

    Button:
        text: "Exit"
        font_size: '20sp'
        size_hint: 1, .1
        on_release: exit(1)
""")
        return OtherError()

# Version up
class Verup(FloatLayout):
    pass
class VerupApp(App):
    def build(self):
        self.title = "Update"
        Builder.load_string(f"""

<Verup>

    orientation:"vertical"

    CoverImage:
        source: 'image/update_background.png'

    Label:
        text: 'An update is required for your Adaway.'
        font_size: '20sp'

    Button:
        text: "Download the latest version"
        font_size: '20sp'
        background_normal: '{normal_button}'
        background_down: '{pushed_button}'
        size_hint: 1, .1
        on_release: app.OpenUpdateSite()

<CoverImage@CoverBehavior+Image>:
    reference_size: self.texture_size
""")
        return Verup()

    def OpenUpdateSite(self):
        webbrowser.open_new(afwdownload)
        exit(1)






async def download(url):
    # Make file name
    host_name = f"""{re.sub('[/\:*?<>"|.]', '', url).replace('\n', '')}.txt"""
    print(f"{host_download} : {url}")
    try:
        # Download hosts file
        await loop.run_in_executor(None, urllib.request.urlretrieve, url, f"hosts/{host_name}")
    except:
        print(f"{host_download_fail} : {url}")
        return "fail"
    else:
        print(f"{host_download_success} : {url}")
        return host_name

async def downloadhost():

    fts = [asyncio.ensure_future(download(u)) for u in urls]
    r = await asyncio.gather(*fts)

    try:
        file = open("hosts/hosts", "a", encoding = 'UTF-8')
    except:
        print(temp_host_error)

    for i in r:
        if i == "fail":
            pass
        else:
            host = open(f"hosts/{i}", "r", encoding = 'UTF-8')
            data = host.read()
            host.close()

            # Remove unnecessary file
            os.remove(f"hosts/{i}")

            file.write(f"{data}\n\n")
    file.close()












# Main app
class Main(BoxLayout):
    pass
class MainApp(App):

    def build(self):

        Builder.load_string(f"""
<Main>
    orientation:"vertical"
    Label:
        text: "{program_name} v{version}"
        size_hint: 1, .1

    FloatLayout:
        CoverImage:
            source: 'image/background.png'

        BoxLayout:
            orientation:"vertical"

            Button:
                text: "{check_update}"
                font_name: '{font_path}'
                background_normal: '{normal_button}'
                background_down: '{pushed_button}'
                on_release: 
            Button:
                text: "{adaway_latest_install}"
                font_name: '{font_path}'
                background_normal: '{normal_button}'
                background_down: '{pushed_button}'
                on_release: app.hosts_install()
            Button:
                text: "{adaway_disable}"
                font_name: '{font_path}'
                background_normal: '{normal_button}'
                background_down: '{pushed_button}'
                on_release: 
            Button:
                text: "{hosts_source}"
                font_name: '{font_path}'
                background_normal: '{normal_button}'
                background_down: '{pushed_button}'
                on_release: os.system('start {hostlist}')
            Button:
                text: "{afw_setting}"
                font_name: '{font_path}'
                background_normal: '{normal_button}'
                background_down: '{pushed_button}'
                on_release: exit(1)
            Button:
                text: "{afw_exit}"
                font_name: '{font_path}'
                background_normal: '{normal_button}'
                background_down: '{pushed_button}'
                on_release: exit(1)

<CoverImage@CoverBehavior+Image>:
    reference_size: self.texture_size
""")
        self.title = f'{program_name.replace(" ", "_")} V.{version}'
        return Main()

    #def chack_update():
    
    def hosts_install(self):

        asyncio.run(downloadhost())


if __name__ == '__main__':

    if not os.path.exists("system/Adaway_for_Windows"):
        title_bar = 'Unzip Error'
        error_txt = 'Please unzip the file properly and execute it. Press click exit button to exit the program.'
        img_exist = False
        OtherErrorApp().run()

    # Main program version
    version = "1.3"

    # Set program name
    program_name = "Adaway for Windows"

    # Host file list path setting
    hostlist = "hosts_list.txt"
    hostsfilepath = "C:\Windows\System32\drivers\etc\hosts"

    # Font path
    font_path = 'font/ko/NanumSquareRoundB.ttf'

    # Button path

    normal_button = "image/button.png"
    pushed_button = "image/pushed_button.png"

    # Chack setting file
    if not os.path.exists("setting.xml"):
        language = "en"
    else:
        file = open("setting.xml", "r", encoding = 'UTF-8')
        setting = file.read()
        file.close()
        soup = BeautifulSoup(setting, 'lxml')
        language = soup.find("language")
        language = language.get_text()

    if not os.path.exists(f"language/{language}.xml"):
        title_bar = 'Language Pack Error'
        error_txt = 'The language pack for the language you entered does not exist.'
        img_exist = True
        background_img = "image/error_background.png"
        OtherErrorApp().run()

    else:

        # Reading language pack
        file = open(f"language/{language}.xml", "r", encoding = 'UTF-8')
        languagecode = file.read()
        file.close()
        soup = BeautifulSoup(languagecode, 'lxml')
        afwver = soup.find("afwver")
        afwver = afwver.get_text()
        # Check compatibility of language packs and programs
        if not afwver == version:
            title_bar = "Language Error"
            error_txt = "This language pack is not available due to compatibility issues with the program."
            img_exist = True
            background_img = "image/error_background.png"
            OtherErrorApp().run()

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
        afw_setting = soup.find("afw_setting").get_text()
        afw_exit = soup.find("afw_exit").get_text()
        host_download_fail = soup.find("host_download_fail").get_text()
        host_download_success = soup.find("host_download_success").get_text()
        temp_host_error = soup.find("temp_host_error").get_text()



    #ipaddress = socket.gethostbyname(socket.gethostname())

    ipaddress = "127.0.0.0"

    if not ipaddress == "127.0.0.1":
        # https://github.com/NewPremium/version/blob/master/index.xml
        r = requests.get("https://newpremium.github.io/version/")
        soup = BeautifulSoup(r.text, "lxml")
        afw = soup.find("afw").get_text()
        afwdownload = soup.find("afwdownload").get_text()

        # Version chack
        #if not afw == version:
        #    VerupApp().run()
    
    else:
        title_bar = "No internet connection detected"
        error_txt = "Please run the program again after you have the internet connection."
        img_exist = True
        background_img = "image/error_background.png"
        OtherErrorApp().run()


    MainApp().run()