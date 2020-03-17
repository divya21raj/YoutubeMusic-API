from selenium import webdriver

from time import sleep
import os
import json

class Google:

    def __init__(self,login):
        
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        if(login): self.googleLogin()

    def googleLogin(self):
        username, password = self.load_creds()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('user-data-dir='+self.ROOT_DIR+'/config')
                
        self.driver=webdriver.Chrome(options=chrome_options)
        self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
        sleep(3)
        print(self.driver.title)
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
        self.driver.close()


    def getLibrary(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('user-data-dir='+self.ROOT_DIR+'/config')
        # chrome_options.add_argument('--headless')
        self.driver=webdriver.Chrome(options=chrome_options)
        self.driver.get('https://music.youtube.com')
        sleep(5)
        self.driver.save_screenshot("2.png")
        mylike.driver.find_element_by_xpath('//*[@id="layout"]/ytmusic-nav-bar/div[2]/ytmusic-pivot-bar-renderer/ytmusic-pivot-bar-item-renderer[3]').click()
        sleep(3)


    def load_creds(self): 
        with open('creds.json') as f:
            data = json.load(f)
            username = data['username']
            password = data['password']

        return username, password


mylike= Google(login=False)
mylike.getLibrary()
