from selenium import webdriver

from time import sleep
import os
import sys

from utils.creds import load_creds

class YtMusic:

    def __init__(self):
        
        self.ROOT_DIR = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
        self.init_command_dict()


    def setup_driver(self, headless):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('user-data-dir='+self.ROOT_DIR+'/config')
        if(headless): chrome_options.add_argument('--headless')
        self.driver=webdriver.Chrome(options=chrome_options)

    
    def googleLogin(self):
        try:
            username, password = load_creds(self.ROOT_DIR)
            
            self.setup_driver(headless=False)

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
            self.setup_driver(headless=True)

            self.driver.get('https://music.youtube.com/library/playlists')
            sleep(3)
            self.driver.save_screenshot("1.png")
            
            element = self.driver.find_element_by_xpath('//*[@id="contents"]/ytmusic-item-section-renderer')
            items = element.find_element_by_xpath('.//*[@id="items"]')

            for item in items.find_elements_by_tag_name('a'):
                if("playlist" in item.get_attribute('href') and item.get_attribute('class') == 'yt-simple-endpoint style-scope yt-formatted-string'):
                    print(item.text)
        
        except Exception as e:
            print(e)
        
        finally:
            if (hasattr(self, 'driver')): self.driver.close()
            else: sys.exit(1)
    
    
    def cleanup_playlists(self):
        try:
            self.setup_driver(headless=False)
            self.driver.get('https://music.youtube.com/library/playlists')
            sleep(3)
            self.driver.save_screenshot("3.png")

            element = self.driver.find_element_by_xpath('//*[@id="contents"]/ytmusic-item-section-renderer')
            items = element.find_element_by_xpath('.//*[@id="items"]')

            self.playlistMap = {}
            for item in items.find_elements_by_tag_name('a')[6:]:
                if("playlist" in item.get_attribute('href') and item.get_attribute('class') == 'yt-simple-endpoint style-scope yt-formatted-string'):
                    self.playlistMap[item.text] = item.get_attribute('href')
                    # self.createPlaylist(title=item.text)
                    print(item.text)

            for title in self.playlistMap:
                self.driver.get(self.playlistMap[title])
                sleep(5)
                print('=========' + title + '==========')
                items = self.driver.find_elements_by_xpath('//*[@id="contents"]/ytmusic-responsive-list-item-renderer')
                for index, item in enumerate(items):
                    try:
                        print(item.find_element_by_xpath('//*[@id="contents"]/ytmusic-responsive-list-item-renderer['+str(index+1)+']/div[2]/div[1]/yt-formatted-string/a').text)
                    except:  # Can be a deleted song
                        pass

        except Exception as e:
            print(e)
        finally:
            pass

    def createPlaylist(self, title):
        sleep(1)
        self.driver.find_element_by_xpath('//*[@id="items"]/ytmusic-two-row-item-renderer[1]/div[1]/yt-formatted-string[1]/a').click()
        self.driver.find_element_by_xpath('//*[@id="input-2"]/input').send_keys(title)
        self.driver.find_element_by_xpath('//*[@id="general-pane"]/div[2]/paper-button[2]').click()
        sleep(2)

    def init_command_dict(self):
        self.command_dict ={'get-playlists' : self.getPlaylists,
                            'cleanup-playlists': self.cleanup_playlists,}

    