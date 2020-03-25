from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import os
import sys
from time import sleep

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
        self.driver.implicitly_wait(5)  # seconds


    def googleLogin(self):
        try:
            username, password = load_creds(self.ROOT_DIR)

            self.setup_driver(headless=False)

            self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
            print(self.driver.title)

            #Check if already logged in
            if(self.driver.title == 'Stack Overflow - Where Developers Learn, Share, & Build Careers'):
                print("Already logged in, nothing to do....")
                return

            self.driver.save_screenshot("1.png")
            self.driver.find_element(By.XPATH, '//*[@id="openid-buttons"]/button[1]').click()

            print(self.driver.title)
            self.driver.save_screenshot("1.png")
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//input[@type="email"]'))).send_keys(username)
            self.driver.find_element(By.XPATH, '//*[@id="identifierNext"]').click()

            print(self.driver.title)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//input[@type="password"]'))).send_keys(password)
            self.driver.find_element(By.XPATH, '//*[@id="passwordNext"]').click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     '/html/body/header')))  # Waiting for login to complete

            self.driver.get('https://music.youtube.com')
            self.driver.save_screenshot("1.png")
            print(self.driver.title)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//ytmusic-section-list-renderer/div[2]/ytmusic-carousel-shelf-renderer[2]'
                ))) # Waiting for page to load

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
            self.driver.save_screenshot("1.png")

            element = self.driver.find_element(By.XPATH, '//*[@id="contents"]/ytmusic-item-section-renderer')
            items = element.find_element(By.XPATH, './/*[@id="items"]')

            for item in items.find_elements(By.TAG_NAME, 'a'):
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
            self.driver.save_screenshot("3.png")

            element = self.driver.find_element(By.XPATH, '//*[@id="contents"]/ytmusic-item-section-renderer')
            items = element.find_element(By.XPATH, './/*[@id="items"]')

            self.playlistMap = {}   #{playlist_title : url}
            for item in items.find_elements_by_tag_name('a')[6:]:
                if("playlist" in item.get_attribute('href') and item.get_attribute('class') == 'yt-simple-endpoint style-scope yt-formatted-string'):
                    self.playlistMap[item.text] = item.get_attribute('href')
                    # self.createPlaylist(title=item.text)
                    # print(item.text)

            # for title in self.playlistMap:
            #     self.driver.get(self.playlistMap[title])
            #     print('=========' + title + '==========')
            #     items = self.driver.find_elements(By.XPATH, '//*[@id="contents"]/ytmusic-responsive-list-item-renderer')
            #     for index, item in enumerate(items):
            #         try:
            #             print(item.find_element(By.XPATH, '//*[@id="contents"]/ytmusic-responsive-list-item-renderer['+str(index+1)+']/div[2]/div[1]/yt-formatted-string/a').text)
            #         except:  # Can be a deleted song
            #             pass

            self.driver.get(self.playlistMap['Non Stop Pop'])
            items = self.driver.find_elements(By.XPATH, '//*[@id="contents"]/ytmusic-responsive-list-item-renderer')

            self.driver.implicitly_wait(0)
            for index, item in enumerate(items):
                try:
                    title = item.find_element(By.XPATH,
                        '//*[@id="contents"]/ytmusic-responsive-list-item-renderer['
                        + str(index + 1) +
                        ']/div[2]/div[1]/yt-formatted-string/a').text
                    artist = item.find_element(By.XPATH,
                        '//*[@id="contents"]/ytmusic-responsive-list-item-renderer['
                        + str(index + 1) +
                        ']/div[2]/div[3]/yt-formatted-string/a').text
                    print(title)

                    hover = ActionChains(self.driver).move_to_element(item)
                    hover.perform()

                    button = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@id='gridProduct10247118']//a[@class='primary-button']")))
                    hover = ActionChains(self.driver).move_to_element(button)
                    hover.perform()

                    button.click()

                except Exception as e:  # Can be a deleted song
                    print(e)

        except Exception as e:
            print(e)

        finally:
            self.driver.implicitly_wait(10)


    def get_artist(self, query):
        self.setup_driver(headless=True)

        self.driver.get('https://music.youtube.com/search?q='+query)
        try:
            # Top result
            self.driver.find_element(
                By.XPATH,
                '//*[@id="contents"]/ytmusic-shelf-renderer[1]/h2/yt-formatted-string'
            )

            artist_link = self.driver.find_element(By.XPATH,
                '//*[@id="contents"]/ytmusic-responsive-list-item-renderer/a'
            ).get_attribute('href')

            print(artist_link)
            self.driver.get(artist_link)

        except Exception as e:
            print(e)
            # No result
            try:
                self.driver.find_element(By.LINK_TEXT, "Did you mean")
                newQuery = self.driver.find_element(By.ID, 'corrected-link')
                print('Did you mean: ' + newQuery + ' ?')
            except:
                print('Artist not found...')


    def createPlaylist(self, title):
        self.driver.find_element(By.XPATH, '//*[@id="items"]/ytmusic-two-row-item-renderer[1]/div[1]/yt-formatted-string[1]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="input-2"]/input').send_keys(title)
        self.driver.find_element(By.XPATH, '//*[@id="general-pane"]/div[2]/paper-button[2]').click()

    
    def init_command_dict(self):
        self.command_dict ={'get-playlists' : self.getPlaylists,
                            'cleanup-playlists': self.cleanup_playlists,
                            'get-artist': self.get_artist}
