from bs4 import BeautifulSoup as bs
import random
from selenium import webdriver
import constants

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

constants.__init__()

class games(object):
    def __init__(self):
        self.chromedriver_path = str(constants.DRIVER_PATH)
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--incognito")
        self.prox = Proxy()
        self.prox.proxy_type = ProxyType.MANUAL
        self.prox.socks5_proxy = constants.PROXY['https']
        self.capabilities = webdriver.DesiredCapabilities.CHROME
        self.prox.add_to_capabilities(self.capabilities)
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, options=self.chrome_options,
                                       desired_capabilities=self.capabilities)
        self.pst_links = []
    def get_link(self, link):
        self.driver.get(link)
        sleep(random.randint(3,5))
    def accept(self):
        button = self.driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
        self.driver.execute_script("arguments[0].click();", button)
        #WebDriverWait(self.driver, random.randint(3,5)).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'))).click()
    def get_soup(self):
        sleep(random.randint(3,5))
        content = self.driver.page_source
        soup = bs(content,features='lxml')
        return soup
    def table(self,link):
        soup = self.get_soup()
        element = soup.find('div', {'id': 'sub-sub-navigation', 'class': 'with-single-level'})
        l = element.findAll('a')['href']
        self.pst_links.append(l)
        dic = dict()
        table = soup.find('div',{'id':'live-match'})
        corners = table.findAll('li',{'class':'match-centre-stat','data-for':'cornersTotal'})
        dic['game_id'] = link
        dic['home_team'] = table.findAll('a',{'class':'team-name'})[0].text
        dic['away_team'] = table.findAll('a',{'class':'team-name'})[1].text
        dic['home_team_formation'] = table.findAll('div',{'class':'formation'})[0].text
        dic['away_team_formation'] = table.findAll('div',{'class':'formation'})[1].text
        dic['first_half_result'] = soup.findAll('dd')[1].text
        dic['full_time_result'] = table.find('div',{'class':'score'}).text
        dic['attendance'] = table.findAll('span',{'class':'value'})[1].text
        dic['home_team_corners'] = float(corners[0].findAll('span',{'class':'match-centre-stat-value'})[0].text)
        dic['away_team_corners'] = float(corners[0].findAll('span',{'class':'match-centre-stat-value'})[1].text)
        self.driver.quit()
        return dic