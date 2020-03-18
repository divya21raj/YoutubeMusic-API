from selenium import webdriver

from time import sleep
import os
import sys
import json

class YtMusic:

    def __init__(self):
        
        self.ROOT_DIR = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
        self.init_command_dict()

    def googleLogin(self):
        try:
            username, password = self.load_creds()

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('user-data-dir='+self.ROOT_DIR+'/config')
                    
            self.driver=webdriver.Chrome(options=chrome_options)
            self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
            sleep(3)
            print(self.driver.title)

            #Check if already logged in
            if(self.driver.title == 'Stack Overflow - Where Developers Learn, Share, & Build Careers'): 
                print("Already logged in, nothing to do....")
                return
            
            self.driver.save_screenshot("1.png")
            self.driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
            
            print(self.driver.title)
            self.driver.save_screenshot("1.png")
            sleep(5)
            self.driver.save_screenshot("1.png")
            self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
            self.driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
            sleep(3)
            
            print(self.driver.title)
            self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
            self.driver.save_screenshot("1.png")
            self.driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
            sleep(5)
            
            self.driver.get('https://music.youtube.com')
            sleep(5)
            self.driver.save_screenshot("1.png")
            print(self.driver.title)

        except Exception as e:
            print(e)
        
        finally:
            if(hasattr(self, 'driver')): 
                self.driver.close()
            else: sys.exit(1)


    def getPlaylists(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('user-data-dir='+self.ROOT_DIR+'/config')
            chrome_options.add_argument('--headless')
            self.driver=webdriver.Chrome(options=chrome_options)
            self.driver.get('https://music.youtube.com')
            sleep(5)
            self.driver.save_screenshot("2.png")
            self.driver.find_element_by_xpath('//*[@id="layout"]/ytmusic-nav-bar/div[2]/ytmusic-pivot-bar-renderer/ytmusic-pivot-bar-item-renderer[3]').click()
            sleep(5)

            element = self.driver.find_element_by_xpath('//*[@id="contents"]/ytmusic-item-section-renderer')
            items = element.find_element_by_xpath('.//*[@id="items"]')
            for item in items.find_elements_by_tag_name('a'):
                if("playlist" in item.get_attribute('href') and item.get_attribute('class') == 'yt-simple-endpoint style-scope yt-formatted-string'):
                    print(item.text)
        finally:
            if (hasattr(self, 'driver')): self.driver.close()
            else: sys.exit(1)
    
    def init_command_dict(self):
        self.command_dict ={'get-playlists' : self.getPlaylists,}

    def load_creds(self):
        try: 
            with open(self.ROOT_DIR + '/creds.json') as f:
                data = json.load(f)
                username = data['username']
                password = data['password']

            return username, password
            
        except: print("creds.json not found")